"""Real-image contracts for coordinate errors, leakage and silent conversions."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from PIL import Image

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/photocraft-generative-editing/scripts/pixel_guard.py'


class PixelGuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def save(self, name, image, **kw):
        p = self.root / name
        image.save(p, **kw)
        return p

    def cli(self, *args, code=0):
        p = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)
        self.assertEqual(p.returncode, code, p.stderr + p.stdout)
        return json.loads(p.stdout)

    def test_maps_offset_crop_at_correct_scale(self):
        r = self.cli('map', '--crop', 1900, 950, 1000, 1000, '--generated', 1250, 1250)
        self.assertEqual(r['matrix'], [0.8, 0, 0, 0.8, 1900, 950])

    def test_rejects_generator_reframing(self):
        r = self.cli('map', '--crop', 1, 2, 1000, 1000, '--generated', 1536, 1024, code=2)
        self.assertIn('aspect', r['error'].lower())

    def test_asymmetric_expand_geometry(self):
        r = self.cli('expand', '--source-size', 6000, 4000, '--margins', 555, 0, 556, 0)
        self.assertEqual(r['canvas_size'], [7111, 4000])
        self.assertEqual(r['original_box'], [555, 0, 6555, 4000])

    def test_negative_margin_rejected(self):
        self.cli('expand', '--source-size', 10, 10, '--margins', -1, 0, 3, 0, code=2)

    def test_irregular_mask_catches_leak_inside_bbox(self):
        a = Image.new('RGB', (5, 5), (60, 90, 120))
        b = a.copy(); b.putpixel((1, 1), (100, 100, 100)); b.putpixel((2, 2), (1, 2, 3))
        m = Image.new('L', a.size); m.putpixel((1, 1), 255); m.putpixel((3, 3), 1)
        r = self.cli('local', '--before', self.save('a.png', a), '--after', self.save('b.png', b), '--allow-mask', self.save('m.png', m), code=1)
        self.assertFalse(r['passed'])
        self.assertEqual(r['protected_changed_pixels'], 1)
        self.assertEqual(r['protected_change_bbox'], [2, 2, 3, 3])

    def test_nonzero_feather_allowed(self):
        a = Image.new('RGB', (4, 4), (40, 50, 60)); b = a.copy(); b.putpixel((1, 2), (41, 50, 60))
        m = Image.new('L', a.size); m.putpixel((1, 2), 1)
        r = self.cli('local', '--before', self.save('a.png', a), '--after', self.save('b.png', b), '--allow-mask', self.save('m.png', m))
        self.assertTrue(r['passed'])
        self.assertEqual(r['changed_pixels'], 1)

    def test_hidden_rgb_with_zero_alpha_detected(self):
        a = Image.new('RGBA', (3, 3), (0, 0, 0, 0)); b = a.copy(); b.putpixel((0, 0), (99, 0, 0, 0))
        r = self.cli('local', '--before', self.save('a.png', a), '--after', self.save('b.png', b), '--allow-mask', self.save('m.png', Image.new('L', a.size)), code=1)
        self.assertEqual(r['protected_changed_pixels'], 1)

    def test_icc_mismatch_refused(self):
        a = Image.new('RGB', (3, 3))
        r = self.cli('local', '--before', self.save('a.png', a, icc_profile=b'profile-one'), '--after', self.save('b.png', a, icc_profile=b'profile-two'), '--allow-mask', self.save('m.png', Image.new('L', a.size)), code=2)
        self.assertIn('profile', r['error'].lower())

    def test_16_bit_refused_without_conversion(self):
        a = Image.new('I;16', (3, 3), 1000)
        self.cli('local', '--before', self.save('a.png', a), '--after', self.save('b.png', a), '--allow-mask', self.save('m.png', Image.new('L', a.size)), code=2)

    def test_jpeg_refused(self):
        a = Image.new('RGB', (3, 3))
        self.cli('local', '--before', self.save('a.jpg', a), '--after', self.save('b.png', a), '--allow-mask', self.save('m.png', Image.new('L', a.size)), code=2)

    def test_mode_and_size_mismatch_refused(self):
        src = self.save('a.png', Image.new('RGB', (3, 3)))
        mask = self.save('m.png', Image.new('L', (3, 3)))
        self.cli('local', '--before', src, '--after', self.save('b.png', Image.new('RGB', (4, 3))), '--allow-mask', mask, code=2)
        self.cli('local', '--before', src, '--after', self.save('c.png', Image.new('RGBA', (3, 3))), '--allow-mask', mask, code=2)

    def test_expand_checks_translated_original(self):
        a = Image.new('RGB', (3, 2)); a.putpixel((0, 0), (10, 20, 30)); a.putpixel((2, 1), (100, 110, 120))
        b = Image.new('RGB', (6, 4), (200, 100, 50)); b.paste(a, (1, 1))
        src = self.save('a.png', a)
        r = self.cli('outpaint', '--before', src, '--after', self.save('b.png', b), '--margins', 1, 1, 2, 1)
        self.assertTrue(r['passed'])
        b.putpixel((3, 2), (101, 110, 120))
        r = self.cli('outpaint', '--before', src, '--after', self.save('c.png', b), '--margins', 1, 1, 2, 1, code=1)
        self.assertEqual(r['protected_change_bbox'], [3, 2, 4, 3])

    def test_crop_preserves_samples_and_profile(self):
        a = Image.new('RGB', (5, 4)); a.putpixel((2, 1), (40, 80, 120))
        src = self.save('a.png', a, icc_profile=b'same-profile')
        out = self.root / 'crop.png'
        r = self.cli('crop', '--source', src, '--box', 1, 1, 3, 2, '--output', out)
        with Image.open(out) as c:
            self.assertEqual(c.size, (3, 2))
            self.assertEqual(c.getpixel((1, 0)), (40, 80, 120))
            self.assertEqual(c.info['icc_profile'], b'same-profile')
        self.assertEqual(len(r['source_sha256']), 64)
        self.cli('crop', '--source', src, '--box', 1, 1, 3, 2, '--output', out, code=2)
        self.cli('crop', '--source', src, '--box', 4, 1, 3, 2, '--output', self.root / 'bad.png', code=2)

    def test_stale_baseline_hash_refused(self):
        a = Image.new('RGB', (2, 2)); src = self.save('a.png', a)
        self.cli('local', '--before', src, '--after', src, '--allow-mask', self.save('m.png', Image.new('L', a.size)), '--expected-source-sha256', '0' * 64, code=2)

    def test_png_color_key_transparency_cannot_pass_as_opaque(self):
        a = Image.new('RGB', (3, 3), (0, 0, 0))
        src = self.save('a.png', a, transparency=(0, 0, 0))
        self.cli('local', '--before', src, '--after', self.save('b.png', a), '--allow-mask', self.save('m.png', Image.new('L', a.size)), code=2)
        self.cli('crop', '--source', src, '--box', 0, 0, 2, 2, '--output', self.root / 'crop.png', code=2)

    def test_tiff_transfer_metadata_cannot_be_ignored_or_dropped(self):
        a = Image.new('L', (3, 3), 90)
        src = self.save('a.tif', a, tiffinfo={301: tuple(i * 257 for i in range(256))})
        after = self.save('b.tif', a, tiffinfo={301: (65535,) * 256})
        self.cli('local', '--before', src, '--after', after, '--allow-mask', self.save('m.png', Image.new('L', a.size)), code=2)
        self.cli('crop', '--source', src, '--box', 0, 0, 2, 2, '--output', self.root / 'crop.png', code=2)


if __name__ == '__main__':
    unittest.main()
