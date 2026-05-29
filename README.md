# DJI ROS 2 Aerial Mapping Pipeline

Offline-first pipeline for DJI aerial imagery, mission metadata, and ROS 2 mapping handoff. The repo is designed to connect real UAV data collection with the existing building-footprint and SLAM evaluation projects without mixing hardware-specific DJI concerns into those algorithm repos.

## What this demonstrates

- DJI mission manifest intake from image metadata exports.
- Sidecar geotag files for image processing pipelines.
- GeoJSON camera footprint export for quick GIS inspection.
- ROS 2 package structure for later online integration.
- Jenkins CI for Python tests and packaging checks.

## Workflow

```text
DJI flight export
  -> mission_manifest.csv
  -> sidecar JSON per image
  -> GeoJSON camera positions
  -> downstream footprint extraction or SLAM evaluation
```

## Quick start

```bash
python -m pip install -e .
python -m pytest -q
mission_manifest data/example/mission_manifest.csv
geojson_export data/example/mission_manifest.csv outputs/camera_positions.geojson
write_sidecars data/example/mission_manifest.csv outputs/sidecars
```

## Downstream links

- Send orthomosaic or image tiles to `uav-building-footprint-extraction`.
- Send trajectory estimates and synchronized imagery to `visual-slam-evaluation-kitti-euroc`.
- Deploy edge perception pieces through `robotics-edge-infra-lab`.

## DJI integration stance

This repo starts with offline exported data because that is easiest to test and publish. Live DJI SDK integration can be added behind a separate adapter once the target aircraft, controller, SDK, and operating mode are known.