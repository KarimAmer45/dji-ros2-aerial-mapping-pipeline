import json
from pathlib import Path

import pytest
from dji_ros2_aerial_mapping_pipeline.geojson_export import export_geojson, to_feature_collection
from dji_ros2_aerial_mapping_pipeline.geotag_images import sidecar_payload, write_sidecars
from dji_ros2_aerial_mapping_pipeline.mission_manifest import load_manifest, mission_bounds, summarize_manifest


FIXTURE = Path(__file__).resolve().parents[1] / "data" / "example" / "mission_manifest.csv"


def test_load_manifest_reads_rows():
    images = load_manifest(FIXTURE)
    assert len(images) == 3
    assert images[0].image == "DJI_0001.JPG"
    assert images[0].altitude_m == 118.2


def test_bounds_cover_manifest():
    bounds = mission_bounds(load_manifest(FIXTURE))
    assert bounds["min_latitude"] < bounds["max_latitude"]
    assert bounds["min_longitude"] < bounds["max_longitude"]


def test_geojson_uses_lon_lat_alt_order():
    images = load_manifest(FIXTURE)
    collection = to_feature_collection(images)
    coordinates = collection["features"][0]["geometry"]["coordinates"]
    assert coordinates == [13.404954, 52.520008, 118.2]


def test_sidecar_payload_contains_position_and_attitude():
    image = load_manifest(FIXTURE)[0]
    payload = sidecar_payload(image)
    assert payload["position"]["latitude"] == image.latitude
    assert payload["attitude"]["yaw_deg"] == image.yaw_deg


def test_summarize_manifest_contains_image_count():
    result = summarize_manifest(FIXTURE)
    assert "3 images" in result


def test_export_geojson_writes_valid_file(tmp_path):
    out = tmp_path / "out.geojson"
    export_geojson(FIXTURE, out)
    assert out.exists()
    data = json.loads(out.read_text())
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) == 3


def test_write_sidecars_creates_one_file_per_image(tmp_path):
    written = write_sidecars(FIXTURE, tmp_path)
    assert len(written) == 3
    for path in written:
        assert Path(path).exists()


def test_load_manifest_raises_on_missing_column(tmp_path):
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("image,timestamp_utc\nDJI_0001.JPG,2026-05-01T10:00:00Z\n")
    with pytest.raises(ValueError, match="missing required columns"):
        load_manifest(bad_csv)


def test_load_manifest_empty_data_returns_empty_list(tmp_path):
    empty_csv = tmp_path / "empty.csv"
    empty_csv.write_text("image,timestamp_utc,latitude,longitude,altitude_m,yaw_deg\n")
    assert load_manifest(empty_csv) == []