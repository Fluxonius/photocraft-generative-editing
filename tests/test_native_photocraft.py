"""Optional real-engine integration test. Set PHOTOCRAFT_CLI to an installed CLI.

Only a temporary, headless synthetic session is used. No GUI or user document.
"""
import importlib.util
import json
import os
from pathlib import Path
import select
import subprocess
import tempfile
import unittest

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('pixel_guard', ROOT / 'skills/photocraft-generative-editing/scripts/pixel_guard.py')
guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guard)


@unittest.skipUnless(os.environ.get('PHOTOCRAFT_CLI'), 'Set PHOTOCRAFT_CLI for the optional native-engine check.')
class NativePhotoCraftTests(unittest.TestCase):
    def test_masked_patch_expansion_and_native_roundtrip(self):
        with tempfile.TemporaryDirectory(prefix='photocraft-skill-') as tmp:
            root = Path(tmp)
            src = Image.new('RGBA', (128, 96))
            for y in range(96):
                for x in range(128):
                    src.putpixel((x, y), (x * 2, y * 2, (x + y) % 256, 128 if (x, y) == (0, 0) else 255))
            src.save(root / 'source.png')
            Image.new('RGB', (32, 24), (220, 70, 20)).save(root / 'patch.png')
            allow = Image.new('L', (128, 96)); allow.paste(255, (48, 36, 80, 60))
            p = subprocess.Popen([os.environ['PHOTOCRAFT_CLI'], 'serve', '--automation-read-root', tmp,
                                  '--automation-write-root', tmp], stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
            request_id = 0

            def rpc(method, params):
                nonlocal request_id
                request_id += 1
                p.stdin.write(json.dumps({'id': request_id, 'method': method, 'params': params}) + '\n')
                p.stdin.flush()
                self.assertTrue(select.select([p.stdout], [], [], 30)[0], 'Native RPC timed out; never replay automatically.')
                reply = json.loads(p.stdout.readline())
                self.assertEqual(reply['id'], request_id)
                self.assertTrue(reply.get('ok'), reply)
                return reply['result']

            try:
                rpc('doc.open', {'path': 'source.png'})
                rpc('doc.save', {'path': 'baseline.png'})
                rpc('doc.place', {'path': 'patch.png', 'fit': False, 'scale': 100, 'center': [64, 48]})
                rpc('engine.execute', {'command': 'select.rect', 'params': {'x': 48, 'y': 36, 'width': 32, 'height': 24}})
                rpc('engine.execute', {'command': 'layer.layerMask.revealSelection', 'params': {}})
                rpc('doc.save', {'path': 'filled.png'})
                rpc('doc.save', {'path': 'filled.pcraft'})
                rpc('doc.open', {'path': 'filled.pcraft'})
                state = rpc('doc.inspect', {})
                self.assertEqual((state['width'], state['height']), (128, 96))
                self.assertEqual(len(state['layers']), 2)
                self.assertTrue(state['layers'][0]['hasMask'])
                rpc('doc.save', {'path': 'reopened-filled.png'})
                original_export = guard.load_lossless(root / 'filled.png')
                reopened_export = guard.load_lossless(root / 'reopened-filled.png')
                guard.comparable(original_export, reopened_export)
                self.assertEqual(guard.count(guard.changes(original_export, reopened_export)), 0)
                before = guard.load_lossless(root / 'baseline.png')
                result = guard.verify_local(before, guard.load_lossless(root / 'filled.png'), allow)
                self.assertTrue(result['passed'])
                self.assertEqual(result['changed_pixels'], 768)
                rpc('doc.open', {'path': 'source.png'})
                rpc('engine.execute', {'command': 'image.canvasSize', 'params': {'width': 144, 'height': 104,
                                               'anchor': 'center', 'extensionColor': 'transparent'}})
                rpc('doc.save', {'path': 'expanded.png'})
                rpc('doc.save', {'path': 'expanded.pcraft'})
                rpc('doc.open', {'path': 'expanded.pcraft'})
                state = rpc('doc.inspect', {})
                self.assertEqual((state['width'], state['height']), (144, 104))
                rpc('doc.save', {'path': 'reopened-expanded.png'})
                original_export = guard.load_lossless(root / 'expanded.png')
                reopened_export = guard.load_lossless(root / 'reopened-expanded.png')
                guard.comparable(original_export, reopened_export)
                self.assertEqual(guard.count(guard.changes(original_export, reopened_export)), 0)
                result = guard.verify_outpaint(before, guard.load_lossless(root / 'expanded.png'), (8, 4, 8, 4))
                self.assertTrue(result['passed'])
                self.assertEqual(result['protected_changed_pixels'], 0)
            finally:
                p.terminate()
                try:
                    p.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    p.kill(); p.wait(timeout=5)
                p.stdin.close(); p.stdout.close()


if __name__ == '__main__':
    unittest.main()
