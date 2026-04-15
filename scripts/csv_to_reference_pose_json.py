#!/usr/bin/env python3
"""
Convert a pose CSV (MediaPipe 33 landmarks) to ReferencePoseSequence JSON for defendu-mobile.

Usage:
  python csv_to_reference_pose_json.py ../defensive_moves/SlipandDuck_MiksAboyme_pose_data.csv \\
    module_0vFVfQfnHdeH57m9Fki70C0aZFv2_1774890300372 ../../defendu-mobile/reference/slip_duck_ref.json
"""

import csv
import json
import sys
from pathlib import Path

MP_COUNT = 33


def row_to_frame(row: dict) -> list[dict]:
    frame: list[dict] = []
    for i in range(MP_COUNT):
        x = float(row[f"lm_{i}_x"])
        y = float(row[f"lm_{i}_y"])
        z = float(row[f"lm_{i}_z"])
        v = float(row[f"lm_{i}_v"])
        frame.append({"x": x, "y": y, "z": z, "visibility": v})
    return frame


def main() -> None:
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)
    csv_path = Path(sys.argv[1])
    module_id = sys.argv[2]
    out_path = Path(sys.argv[3])
    rows: list[dict] = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append(row)
    sequence = [row_to_frame(row) for row in rows]
    payload = {
        "moduleId": module_id,
        "frameCount": len(sequence),
        "landmarksPerFrame": MP_COUNT,
        "sequence": sequence,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {len(sequence)} frames to {out_path}")


if __name__ == "__main__":
    main()
