"""
Offline DJI mapping launch stub.

This pipeline has no ROS 2 nodes — all processing is done via CLI entry points:
  mission_manifest <manifest.csv>
  geojson_export   <manifest.csv> <output.geojson>
  write_sidecars   <manifest.csv> <output_dir>

This launch file exists only to satisfy the ament_python package layout and
logs a reminder message when invoked via `ros2 launch`.
"""

from launch import LaunchDescription
from launch.actions import LogInfo


def generate_launch_description():
    return LaunchDescription(
        [
            LogInfo(
                msg=(
                    "Offline DJI mapping pipeline: run mission_manifest, "
                    "geojson_export, and write_sidecars from the CLI."
                )
            )
        ]
    )