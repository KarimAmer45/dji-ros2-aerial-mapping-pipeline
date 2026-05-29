from __future__ import annotations

import argparse
import json
from pathlib import Path

from .mission_manifest import MissionImage, load_manifest


def feature_for_image(image: MissionImage) -> dict:
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [image.longitude, image.latitude, image.altitude_m],
        },
        "properties": {
            "image": image.image,
            "timestamp_utc": image.timestamp_utc,
            "yaw_deg": image.yaw_deg,
        },
    }


def to_feature_collection(images: list[MissionImage]) -> dict:
    return {
        "type": "FeatureCollection",
        "features": [feature_for_image(image) for image in images],
    }


def export_geojson(manifest_path: str | Path, output_path: str | Path) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    collection = to_feature_collection(load_manifest(manifest_path))
    output.write_text(json.dumps(collection, indent=2), encoding="utf-8")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Export DJI camera positions to GeoJSON.")
    parser.add_argument("manifest", help="Path to mission_manifest.csv")
    parser.add_argument("output", help="Output GeoJSON path")
    args = parser.parse_args()
    output = export_geojson(args.manifest, args.output)
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()