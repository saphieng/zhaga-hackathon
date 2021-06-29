# DepthAI API Demo Program

This repo contains demo application, which can load different networks, create pipelines, record video, etc.

__Documentation is available at [https://docs.luxonis.com/](https://docs.luxonis.com/).__

## Python modules (Dependencies)

DepthAI Demo requires [numpy](https://numpy.org/), [opencv-python](https://pypi.org/project/opencv-python/) and [depthai](https://github.com/luxonis/depthai-python). 
To get the versions of these packages you need for the program, use pip: (Make sure pip is upgraded: ` python3 -m pip install -U pip`)
```
python3 install_requirements.py
```

## Examples

`python3 depthai_demo.py` - RGB & CNN inference example
`python3 depthai_demo.py -vid <path_to_video_or_yt_link>` - CNN inference on video example
`python3 depthai_demo.py -cnn person-detection-retail-0013` - Run `person-detection-retail-0013` model from `resources/nn` directory
`python3 depthai_demo.py -cnn tiny-yolo-v3 -sh 8` - Run `tiny-yolo-v3` model from `resources/nn` directory and compile for 8 shaves

## Usage

```
$ depthai_demo.py --help

usage: depthai_demo.py [-h] [-nd] [-cam {left,right,color}]
                       [-vid VIDEO] [-hq] [-dd] [-cnnp CNN_PATH]
                       [-cnn CNN_MODEL] [-sh SHAVES]
                       [-cnn-size CNN_INPUT_SIZE] [-rgbr {1080,2160,3040}]
                       [-rgbf RGB_FPS] [-dct DISPARITY_CONFIDENCE_THRESHOLD]
                       [-med {0,3,5,7}] [-lrc] [-scale SCALE] [-sbb]
                       [-sbb-sf SBB_SCALE_FACTOR] [-sync]
                       [-monor {400,720,800}] [-monof MONO_FPS]

optional arguments:
  -h, --help            show this help message and exit
  -nd, --no-debug       Prevent debug output
  -cam {left,right,color}, --camera {left,right,color}
                        Use one of DepthAI cameras for inference (conflicts
                        with -vid)
  -vid VIDEO, --video VIDEO
                        Path to video file to be used for inference (conflicts
                        with -cam)
  -hq, --high_quality   Low quality visualization - uses resized frames
  -dd, --disable_depth  Disable depth information
  -cnnp CNN_PATH, --cnn_path CNN_PATH
                        Path to cnn model directory to be run
  -cnn CNN_MODEL, --cnn_model CNN_MODEL
                        Cnn model to run on DepthAI
  -sh SHAVES, --shaves SHAVES
                        Name of the nn to be run from default depthai
                        repository
  -cnn-size CNN_INPUT_SIZE, --cnn_input_size CNN_INPUT_SIZE
                        Neural network input dimensions, in "WxH" format, e.g.
                        "544x320"
  -rgbr {1080,2160,3040}, --rgb_resolution {1080,2160,3040}
                        RGB cam res height: (1920x)1080, (3840x)2160 or
                        (4056x)3040. Default: 1080
  -rgbf RGB_FPS, --rgb_fps RGB_FPS
                        RGB cam fps: max 118.0 for H:1080, max 42.0 for
                        H:2160. Default: 30.0
  -dct DISPARITY_CONFIDENCE_THRESHOLD, --disparity_confidence_threshold DISPARITY_CONFIDENCE_THRESHOLD
                        Disparity confidence threshold, used for depth
                        measurement. Default: 200
  -med {0,3,5,7}, --stereo_median_size {0,3,5,7}
                        Disparity / depth median filter kernel size (N x N) .
                        0 = filtering disabled. Default: 7
  -lrc, --stereo_lr_check
                        Enable stereo 'Left-Right check' feature.
  -scale SCALE, --scale SCALE
                        Scale factor for the output window. Default: 1.0
  -sbb, --spatial_bounding_box
                        Display spatial bounding box (ROI) when displaying
                        spatial information. The Z coordinate get's calculated
                        from the ROI (average)
  -sbb-sf SBB_SCALE_FACTOR, --sbb_scale_factor SBB_SCALE_FACTOR
                        Spatial bounding box scale factor. Sometimes lower
                        scale factor can give better depth (Z) result.
                        Default: 0.3
  -sync, --sync         Enable NN/camera synchronization. If enabled, camera
                        source will be from the NN's passthrough attribute
  -monor {400,720,800}, --mono_resolution {400,720,800}
                        Mono cam res height: (1280x)720, (1280x)800 or
                        (640x)400. Default: 400
  -monof MONO_FPS, --mono_fps MONO_FPS
                        Mono cam fps: max 60.0 for H:720 or H:800, max 120.0
                        for H:400. Default: 30.0

```


## Conversion of existing trained models into Intel Movidius binary format

OpenVINO toolkit contains components which allow conversion of existing supported trained `Caffe` and `Tensorflow` models into Intel Movidius binary format through the Intermediate Representation (IR) format.

Example of the conversion:
1. First the `model_optimizer` tool will convert the model to IR format:  

       cd <path-to-openvino-folder>/deployment_tools/model_optimizer
       python3 mo.py --model_name ResNet50 --output_dir ResNet50_IR_FP16 --framework tf --data_type FP16 --input_model inference_graph.pb

    - The command will produce the following files in the `ResNet50_IR_FP16` directory:
        - `ResNet50.bin` - weights file;
        - `ResNet50.xml` - execution graph for the network;
        - `ResNet50.mapping` - mapping between layers in original public/custom model and layers within IR.
2. The weights (`.bin`) and graph (`.xml`) files produced above (or from the Intel Model Zoo) will be required for building a blob file,
with the help of the `myriad_compile` tool. When producing blobs, the following constraints must be applied:

       CMX-SLICES = 4 
       SHAVES = 4 
       INPUT-FORMATS = 8 
       OUTPUT-FORMATS = FP16/FP32 (host code for meta frame display should be updated accordingly)

    Example of command execution:

       <path-to-openvino-folder>/deployment_tools/inference_engine/lib/intel64/myriad_compile -m ./ResNet50.xml -o ResNet50.blob -ip U8 -VPU_NUMBER_OF_SHAVES 4 -VPU_NUMBER_OF_CMX_SLICES 4

## Reporting issues

We are actively developing the DepthAI framework, and it's crucial for us to know what kind of problems you are facing.  
If you run into a problem, please follow the steps below and email support@luxonis.com: 

1. Run `log_system_information.sh` and share the output from (`log_system_information.txt`).
2. Take a photo of a device you are using (or provide us a device model)
3. Describe the expected results; 
4. Describe the actual running results (what you see after started your script with DepthAI)
5. How you are using the DepthAI python API (code snippet, for example)
6. Console output
