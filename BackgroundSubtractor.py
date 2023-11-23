from video_tools import (
    Polarity, BackgroundSubtractor, BackgroundSubtractorWidget,
    BackroundImage, StaticBackground, DynamicBackground,
    DynamicBackgroundMP
)
import argparse

METHODS = {
    'image': BackroundImage,
    'static': StaticBackground,
    'dynamic': DynamicBackground,
    'dynamic_mp': DynamicBackgroundMP
}

parser = argparse.ArgumentParser(description='Create background subtracted video')

# polarity
parser.add_argument(
    "-p", "--polarity", 
    default = Polarity.BRIGHT_ON_DARK,
    const = Polarity.BRIGHT_ON_DARK,
    nargs = '?',
    type = Polarity,
    choices = list(Polarity),
    help = "fish to background polarity, default: %(default)s"
)

# background subtraction method
parser.add_argument(
    "-m", "--method",
    default = 'static',
    const = 'static',
    nargs = '?',
    type = str,
    choices = METHODS.keys(),
    help = "background subtraction method, default: %(default)s"
)

# input video file
parser.add_argument(
    "input_video",
    type = str,
    help = "input video file"
)

# output video file 
parser.add_argument(
    "output_video",
    type = str,
    help = "output, background subtracted video file"
)

args = parser.parse_args()