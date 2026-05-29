from __future__ import annotations

import argparse
import json
from pathlib import Path

from .mission_manifest import MissionImage, load_manifest


def sidecar_payload(image: MissionImage) -> dict:
    return {
        "image": image.image,
        "timestamp_utc": image.timestamp_utc,
        "position": {
            "latitude": image.latitude,
            "longitude": image.longitude,
            "altitude_m": image.altitude_m,
        },
        "attitude": {
            "yaw_deg": image.yaw_deg,
        },
    }


def write_sidecars(manifest_path: str | Path, output_dir: str | Path) -> list[Path]:
    output_root = Path(output_dir)
    output_root.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for image in load_manifest(manifest_path):
        image_name = Path(image.image).name
        sidecar_path = output_root / f"{image_name}.json"
        sidecar_path.write_text(json.dumps(sidecar_payload(image), indent=2), encoding="utf-8")
        written.append(sidecar_path)
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description="Write JSON sidecars for DJI image geotags.")
    parser.add_argument("manifest", help="Path to mission_manifest.csv")
    parser.add_argument("output_dir", help="Directory for sidecar JSON files")
    args = parser.parse_args()
    written = write_sidecars(args.manifest, args.output_dir)
    print(f"Wrote {len(written)} sidecar files")


if __name__ == "__main__":
    main()