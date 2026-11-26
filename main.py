"""Copy the built front page to the output file.

The entry image is rendered by build_image.py into entry.png next to
this file. This program copies those exact bytes to /output/entry.png
(or to the directory named by OUTPUT_DIR when testing locally). It
uses only the Python standard library, never touches the network, and
never uses randomness or the time or date, so repeated runs produce
byte-identical output.
"""

import hashlib
import os
import shutil
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    output_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    target = os.path.join(output_dir, "entry.png")
    shutil.copyfile(source, target)
    # Confirm the copy is complete before reporting success.
    source_size = os.path.getsize(source)
    target_size = os.path.getsize(target)
    if target_size != source_size:
        print(f"Copy failed: {target} is {target_size} bytes, "
              f"expected {source_size}", file=sys.stderr)
        return 1
    with open(target, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    size = os.path.getsize(target)
    print(f"Copied {size} bytes to {target} (sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
