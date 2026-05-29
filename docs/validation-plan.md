# Validation Plan

## Metadata checks

- Required manifest columns are present.
- Latitude, longitude, altitude, and yaw values parse as numbers.
- GeoJSON output uses longitude, latitude, altitude order.

## Mapping checks

- Camera positions load in a GIS viewer.
- Sidecar files match image names exactly.
- Downstream footprint extraction can consume the image product.

## Future checks

- Compare DJI GNSS path with SLAM trajectory estimates.
- Add reprojection sanity checks once camera intrinsics are available.