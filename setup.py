from glob import glob

from setuptools import setup


package_name = "dji_ros2_aerial_mapping_pipeline"


setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    package_dir={"": "src"},
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        (f"share/{package_name}/config", glob("config/*.yaml")),
        (f"share/{package_name}/launch", glob("launch/*.py")),
    ],
    install_requires=[],
    zip_safe=True,
    maintainer="Karim",
    maintainer_email="karim@example.com",
    description="Offline DJI aerial mapping intake and ROS 2 handoff pipeline.",
    license="MIT",
    entry_points={
        "console_scripts": [
            "mission_manifest = dji_ros2_aerial_mapping_pipeline.mission_manifest:main",
            "geojson_export = dji_ros2_aerial_mapping_pipeline.geojson_export:main",
            "write_sidecars = dji_ros2_aerial_mapping_pipeline.geotag_images:main",
        ],
    },
)