# Workflow

1. Export images and flight metadata from the DJI capture workflow.
2. Normalize metadata into `mission_manifest.csv`.
3. Generate sidecar JSON files for image-level geotags.
4. Export camera positions to GeoJSON for quick map inspection.
5. Feed imagery products into `uav-building-footprint-extraction`.
6. Feed trajectories or synchronized image sequences into `visual-slam-evaluation-kitti-euroc`.