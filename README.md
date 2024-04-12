# RoboPoseGen

RoboPoseGen utilizes Unreal Engine 5.3.2 to generate synthetic pose data for research in robotic pose estimation. The tool simulates realistic robot motions which are essential for developing and testing AI algorithms.

## Prerequisites

Ensure Unreal Engine version 5.3.2 is installed and configured as follows:

1. Navigate to `Edit > Plugins`.
2. Enable `Json Blueprint Utilities` from the plugins list to process JSON data, which is essential for pose generation.

## Generating Pose Data

RoboPoseGen outputs pose data in JPEG and JSON file formats, which include the imagery and pose metadata respectively:

1. Execute RoboPoseGen within Unreal Engine to simulate robot motions.
2. Upon completion, files are generated in the output directory:
   - **JPEG files**: Images depicting the robot in various poses.
   - **JSON files**: Metadata files that contain 2D coordinates, projecting the 3D joint positions onto the images.

## Annotating Pose Data

To annotate JPEG images with joint positions:

1. Move to the `ResultAnnotation` folder.
2. Execute `robot_pose_gen_annotation.py`, which uses the JSON files to overlay joint positions on the corresponding JPEG images.

RoboPoseGen is designed to streamline the creation and annotation of pose data, facilitating advancements in robotic pose estimation algorithms.
