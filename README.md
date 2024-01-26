# mpii-to-yolopose
mpii format to yolopose format for using mpii data 
- desired format: class-index x y width height px1 py1 px2 py2 ... pxn pyn
- current format: not that ^ 
- Yolopose format: https://docs.ultralytics.com/datasets/pose/#ultralytics-yolo-format
- for custom training yolov8-pose models

# Set up
directory structure
- test
    - images + json
- test_output

- then run converter2.py script 
