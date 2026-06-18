#!/usr/bin/env python3
import sys
from pathlib import Path

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print(f"Usage: {sys.argv[0]} <input-file> [output-file]")
    print("If output file is omitted, writes to <input-stem>_paragraphed<suffix>")
    sys.exit(1)

input_file = sys.argv[1]
if len(sys.argv) == 3:
    output_file = sys.argv[2]
else:
    p = Path(input_file)
    output_file = str(p.with_name(f"{p.stem}_paragraphed{p.suffix}"))

with open(input_file, "r", encoding="utf-8") as fin, \
     open(output_file, "w", encoding="utf-8") as fout:
    for line in fin:
        line = line.rstrip("\n")
        if line == "":
            fout.write("<br>\n")
        else:
            fout.write(f"<p>{line}</p>\n")

output_path = Path(output_file).resolve()
print(f"Done. Output written to: {output_path}")
