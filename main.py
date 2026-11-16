#!/usr/bin/env python3
# First Spark: Copies entry.png to the output directory for the ai-excited-01 competition.
import os
import sys
def main():
    # Locate entry.png beside main.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(script_dir, 'entry.png')
    if not os.path.exists(source_path):
        print("Error: entry.png not found beside main.py", file=sys.stderr)
        sys.exit(1)
    # Read all bytes
    with open(source_path, 'rb') as f:
        data = f.read()
    # Validate image: PNG or JPEG
    if len(data) < 8:
        print("Error: file too small to be a valid image", file=sys.stderr)
        sys.exit(1)
    sig = data[:8]
    if sig == b'\x89PNG\r\n\x1a\n':
        # PNG: ends with IEND chunk (last 12 bytes: IEND + CRC + len=0)
        if not (data[-12:] == b'IEND\x00\x00\x00\x00\xAE\x42\x60\x82'):
            print("Error: invalid PNG (missing IEND chunk)", file=sys.stderr)
            sys.exit(1)
    elif sig[:2] == b'\xff\xd8':
        # JPEG: starts with FF D8, ends with FF D9
        if not data[-2:] == b'\xff\xd9':
            print("Error: invalid JPEG (missing EOI marker)", file=sys.stderr)
            sys.exit(1)
    else:
        print("Error: unsupported image format (only PNG or JPEG allowed)", file=sys.stderr)
        sys.exit(1)
    # Get output directory
    output_dir = os.getenv('MAKEFUN_OUTPUT_DIR', '/output')
    os.makedirs(output_dir, exist_ok=True)
    # Write bytes
    output_path = os.path.join(output_dir, 'entry.png')
    with open(output_path, 'wb') as f:
        written = f.write(data)
    if written != len(data):
        print("Error: partial write", file=sys.stderr)
        sys.exit(1)
    print(f"Successfully copied {len(data)} bytes to {output_path}")
if __name__ == "__main__":
    main()
