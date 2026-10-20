#!/usr/bin/env python3
"""Offline crop geometry and exact decoded-sample auditing; no generation or retouching.

8-bit L/LA/RGB/RGBA lossless PNG/TIFF only. Exit 0: valid/pass; 1: preservation
violation; 2: invalid or unsupported input. No color conversion is performed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

from PIL import Image, ImageChops, PngImagePlugin

MAX_PIXELS = 64_000_000


def fingerprint(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def positive_pair(values):
    if len(values) != 2 or any(v <= 0 for v in values):
        raise ValueError('width and height must be positive integers')
    return tuple(values)


def crop_box(values):
    x, y, w, h = values
    positive_pair((w, h))
    if x < 0 or y < 0:
        raise ValueError('crop origin must be nonnegative')
    return x, y, x + w, y + h


def mapping(crop, generated):
    crop_box(crop)
    gw, gh = positive_pair(generated)
    x, y, w, h = crop
    if w * gh != h * gw:
        raise ValueError('aspect ratio differs; inspect padding/reframing instead of stretching')
    return {'matrix': [w / gw, 0, 0, h / gh, x, y],
            'native_size': [w, h], 'generated_size': [gw, gh],
            'condition': 'Same framing and alignment must be verified visually.'}


def expansion(size, margins):
    w, h = positive_pair(size)
    l, t, r, b = margins
    if min(margins) < 0:
        raise ValueError('expansion margins must be nonnegative')
    return {'canvas_size': [w + l + r, h + t + b],
            'original_box': [l, t, l + w, t + h], 'original_offset': [l, t]}


def load_lossless(path):
    with Image.open(path) as im:
        if im.format not in ('PNG', 'TIFF'):
            raise ValueError('Use lossless PNG/TIFF, not JPEG or a screenshot codec.')
        if im.width * im.height > MAX_PIXELS:
            raise ValueError('Image exceeds 64M-pixel helper limit; use a native-depth tiled auditor.')
        if im.mode not in ('L', 'LA', 'RGB', 'RGBA'):
            raise ValueError('Only 8-bit L/LA/RGB/RGBA supported; do not downconvert the original.')
        if 'transparency' in im.info:
            raise ValueError('Color-key transparency is unsupported; use explicit-alpha lossless comparison exports.')
        if getattr(im, 'n_frames', 1) != 1:
            raise ValueError('Use a single-frame lossless comparison export.')
        if im.getexif().get(274, 1) != 1:
            raise ValueError('Nontrivial EXIF orientation; export in document pixel coordinates.')
        if im.format == 'TIFF':
            if any(tag in im.tag_v2 for tag in (301, 318, 319, 532)):
                raise ValueError('TIFF transfer/white-point/primary metadata is unsupported; use a verified color-managed export/auditor.')
            bits = im.tag_v2.get(258, (8,))
            bits = (bits,) if isinstance(bits, int) else bits
            if any(bit != 8 for bit in bits) or im.tag_v2.get(259) in (6, 7):
                raise ValueError('16/32-bit or JPEG-compressed TIFF requires a native-depth auditor.')
        # Check PNG bit depth even if a decoder exposes multichannel 16-bit as RGB.
        if im.format == 'PNG':
            with open(path, 'rb') as f:
                header = f.read(25)
            if header[24] != 8:
                raise ValueError('Only 8-bit PNG comparison is supported.')
        im.load()
        result = im.copy()
        result.info = dict(im.info)
        return result


def color_signature(im):
    return (im.mode, im.info.get('icc_profile'), im.info.get('gamma'),
            im.info.get('srgb'), im.info.get('chromaticity'))


def comparable(a, b):
    if a.mode != b.mode:
        raise ValueError('Image modes differ; no implicit mode or alpha conversion.')
    if color_signature(a) != color_signature(b):
        raise ValueError('Color profile/transfer metadata differs; export comparable baselines.')


def changes(a, b):
    if a.size != b.size:
        raise ValueError('Image dimensions differ.')
    # getbbox() on an RGBA difference can overlook RGB changes when alpha stays zero.
    bands = ImageChops.difference(a, b).split()
    delta = bands[0]
    for band in bands[1:]:
        delta = ImageChops.lighter(delta, band)
    return delta.point(lambda v: 255 if v else 0)


def count(binary):
    return binary.histogram()[255]


def verify_local(before, after, mask):
    comparable(before, after)
    delta = changes(before, after)
    if mask.mode != 'L' or mask.size != before.size:
        raise ValueError('Allow-mask must be an 8-bit L image at full document size.')
    protected = mask.point(lambda v: 0 if v else 255)
    leak = ImageChops.multiply(delta, protected)
    return {'passed': not count(leak), 'size': list(before.size),
            'changed_pixels': count(delta), 'changed_bbox': delta.getbbox(),
            'allowed_pixels': count(ImageChops.invert(protected)),
            'protected_changed_pixels': count(leak),
            'protected_change_bbox': leak.getbbox(),
            'scope': 'decoded channel samples; not a visual-quality or file-byte equivalence test'}


def verify_outpaint(before, after, margins):
    comparable(before, after)
    geo = expansion(before.size, margins)
    if list(after.size) != geo['canvas_size']:
        raise ValueError('Output dimensions do not match source plus expansion margins.')
    delta = changes(before, after.crop(geo['original_box']))
    bbox = delta.getbbox()
    l, t = geo['original_offset']
    if bbox:
        bbox = [bbox[0] + l, bbox[1] + t, bbox[2] + l, bbox[3] + t]
    return {**geo, 'passed': not count(delta), 'protected_changed_pixels': count(delta),
            'protected_change_bbox': bbox,
            'scope': 'original rectangle only; new content still needs visual review'}


def extract_crop(source, box, output):
    image = load_lossless(source)
    rect = crop_box(box)
    if rect[2] > image.width or rect[3] > image.height:
        raise ValueError('Crop exceeds source bounds; choose an explicit in-bounds context crop.')
    if Path(output).suffix.lower() != '.png':
        raise ValueError('Crop output must be a new PNG path.')
    cropped = image.crop(rect)
    options = {}
    if image.info.get('icc_profile'):
        options['icc_profile'] = image.info['icc_profile']
    pnginfo = PngImagePlugin.PngInfo()
    if 'gamma' in image.info:
        pnginfo.add(b'gAMA', struct.pack('>I', round(image.info['gamma'] * 100000)))
    if 'srgb' in image.info:
        pnginfo.add(b'sRGB', bytes([image.info['srgb']]))
    if 'chromaticity' in image.info:
        pnginfo.add(b'cHRM', struct.pack('>8I', *(round(v * 100000) for v in image.info['chromaticity'])))
    # Exclusive creation refuses replacements, including symlinks to existing files.
    with open(output, 'xb') as f:
        cropped.save(f, format='PNG', pnginfo=pnginfo, **options)
    return {'source_sha256': fingerprint(source), 'source_size': list(image.size),
            'crop': list(box), 'output_size': list(cropped.size), 'output': str(output)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('map', help='Affine mapping for an unchanged-framing generated crop.')
    p.add_argument('--crop', nargs=4, type=int, required=True, metavar=('X', 'Y', 'W', 'H'))
    p.add_argument('--generated', nargs=2, type=int, required=True, metavar=('W', 'H'))
    p = sub.add_parser('expand', help='Compute target canvas and translated protected rectangle.')
    p.add_argument('--source-size', nargs=2, type=int, required=True)
    p.add_argument('--margins', nargs=4, type=int, required=True, metavar=('L', 'T', 'R', 'B'))
    p = sub.add_parser('crop', help='Extract a generator context crop without resizing.')
    p.add_argument('--source', required=True)
    p.add_argument('--box', nargs=4, type=int, required=True, metavar=('X', 'Y', 'W', 'H'))
    p.add_argument('--output', required=True)
    for name in ('local', 'outpaint'):
        p = sub.add_parser(name, help='Verify exact preservation of protected decoded pixels.')
        p.add_argument('--before', required=True)
        p.add_argument('--after', required=True)
        p.add_argument('--expected-source-sha256')
        if name == 'local':
            p.add_argument('--allow-mask', required=True)
        else:
            p.add_argument('--margins', nargs=4, type=int, required=True, metavar=('L', 'T', 'R', 'B'))
    args = parser.parse_args()
    try:
        if args.command == 'map':
            result = mapping(args.crop, args.generated)
        elif args.command == 'expand':
            result = expansion(args.source_size, args.margins)
        elif args.command == 'crop':
            result = extract_crop(args.source, args.box, args.output)
        else:
            digest = fingerprint(args.before)
            if args.expected_source_sha256 and digest != args.expected_source_sha256.lower():
                raise ValueError('Source SHA256 changed: the baseline is stale or incorrect.')
            before, after = load_lossless(args.before), load_lossless(args.after)
            if args.command == 'local':
                result = verify_local(before, after, load_lossless(args.allow_mask))
            else:
                result = verify_outpaint(before, after, args.margins)
            result.update(source_sha256=digest, output_sha256=fingerprint(args.after))
        print(json.dumps(result, ensure_ascii=False))
        return 0 if result.get('passed', True) else 1
    except (OSError, ValueError, Image.DecompressionBombError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False))
        return 2


if __name__ == '__main__':
    sys.exit(main())
