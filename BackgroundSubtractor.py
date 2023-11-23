from video_tools import (
    Polarity, BackgroundSubtractor, BackgroundSubtractorWidget,
    BackroundImage, StaticBackground, DynamicBackground,
    DynamicBackgroundMP
)
import argparse

parser = argparse.ArgumentParser(description='Create background subtracted video')

# polarity
parser.add_argument(
    "polarity", 
    type = Polarity,
    choices = list(Polarity)
)

# background subtraction method
args = parser.parse_args()