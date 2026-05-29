from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REQUIRED_COLUMNS = {
    "image",
    "timestamp_utc",
    "latitude",
    "longitude",
    "altitude_m",
    "yaw_deg",
}


@dataclass(frozen=True)
class MissionImage:
    image: str
    timestamp_utc: str
    latitude: float
    longitude: float
    altitude_m: float
    yaw_deg: float


def load_manifest(path: str | Path) -> list[MissionImage]:
    manifest_path = Path(path)
    with manifest_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_COLUMNS.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Manifest missing required columns: {sorted(missing)}")

        rows: list[MissionImage] = []
        for row_number, row in enumerate(reader, start=2):
            try:
                rows.append(
                    MissionImage(
                        image=row["image"],
                        timestamp_utc=row["timestamp_utc"],
                        latitude=float(row["latitude"]),
                        longitude=float(row["longitude"]),
                        altitude_m=float(row["altitude_m"]),
                        yaw_deg=float(row["yaw_deg"]),
                    )
                )
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Invalid numeric value on manifest row {row_number}") from exc

    return rows


def mission_bounds(images: Iterable[MissionImage]) -> dict[str, float]:
    image_list = list(images)
    if not image_list:
        raise ValueError("Cannot calculate bounds for an empty mission")

    return {
        "min_latitude": min(item.latitude for item in image_list),
        "max_latitude": max(item.latitude for item in image_list),
        "min_longitude": min(item.longitude for item in image_list),
        "max_longitude": max(item.longitude for item in image_list),
        "min_altitude_m": min(item.altitude_m for item in image_list),
        "max_altitude_m": max(item.altitude_m for item in image_list),
    }


def summarize_manifest(path: str | Path) -> str:
    images = load_manifest(path)
    bounds = mission_bounds(images)
    return (
        f"{len(images)} images, "
        f"lat {bounds['min_latitude']:.6f}..{bounds['max_latitude']:.6f}, "
        f"lon {bounds['min_longitude']:.6f}..{bounds['max_longitude']:.6f}, "
        f"alt {bounds['min_altitude_m']:.1f}..{bounds['max_altitude_m']:.1f} m"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize a DJI mission manifest CSV.")
    parser.add_argument("manifest", help="Path to mission_manifest.csv")
    args = parser.parse_args()
    print(summarize_manifest(args.manifest))


if __name__ == "__main__":
    main()