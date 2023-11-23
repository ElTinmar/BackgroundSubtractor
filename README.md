# BackgroundSubtractor

Remove background from video

# Installation

```
git clone git@github.com:ElTinmar/BackgroundSubtractor.git
cd BackgroundSubtractor
conda env create -f BackgroundSubtractor.yml
```

# Usage

```
usage: BackgroundSubtractor.py [-h] [-p [{DARK_ON_BRIGHT,BRIGHT_ON_DARK}]] {image,static,dynamic} ... input_video output_video

Create background subtracted video

positional arguments:
  {image,static,dynamic}
                        background subtraction methods
    image               subtract a fixed image to all frames
    static              compute a static background image from video
    dynamic             dynamically compute background from video
  input_video           path to input video file
  output_video          path to output, background subtracted video file

optional arguments:
  -h, --help            show this help message and exit
  -p [{DARK_ON_BRIGHT,BRIGHT_ON_DARK}], --polarity [{DARK_ON_BRIGHT,BRIGHT_ON_DARK}]
                        fish to background polarity, default: DARK_ON_BRIGHT
```

```
usage: BackgroundSubtractor.py image [-h] background_image

positional arguments:
  background_image  path to background image

optional arguments:
  -h, --help        show this help message and exit
```


```
usage: BackgroundSubtractor.py static [-h] -n NUM_SAMPLE_FRAMES

optional arguments:
  -h, --help            show this help message and exit
  -n NUM_SAMPLE_FRAMES, --num_sample_frames NUM_SAMPLE_FRAMES
                        number of frames to sample to create background
```

```
usage: BackgroundSubtractor.py dynamic [-h] -n NUM_SAMPLE_FRAMES -f FREQ [--mp]

optional arguments:
  -h, --help            show this help message and exit
  -n NUM_SAMPLE_FRAMES, --num_sample_frames NUM_SAMPLE_FRAMES
                        number of frames to sample to create background
  -f FREQ, --freq FREQ  sample every X frames
  --mp                  use multiprocessing
```