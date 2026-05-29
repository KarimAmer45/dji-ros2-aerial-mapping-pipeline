# DJI Integration Notes

Start offline and version the manifest format before adding live SDK code. That keeps the project testable without a drone connected.

Potential live adapters:

- Flight log exporter adapter.
- Media card ingest adapter.
- ROS 2 image publisher adapter.
- Mission status bridge.

Choose the adapter after the target aircraft, controller, SDK, and operating mode are known.