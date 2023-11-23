from video_tools import (
    Polarity, BackgroundSubtractor,
    BackroundImage, StaticBackground, DynamicBackground,
    DynamicBackgroundMP, Buffered_OpenCV_VideoReader, OpenCV_VideoWriter
)
import argparse
from tqdm import tqdm

def subtract_background(
        input_video: str, 
        output_video: str, 
        bckg_subtractor: BackgroundSubtractor
    ) -> None:

    video_reader = Buffered_OpenCV_VideoReader()
    video_reader.open_file(input_video)
    height = video_reader.get_height()
    width = video_reader.get_width()
    fps = video_reader.get_fps()  
    num_frames = video_reader.get_number_of_frame()

    video_writer = OpenCV_VideoWriter(
        height=height, 
        width=width, 
        fps=fps, 
        filename=output_video
    )

    for i in tqdm(range(num_frames)):
        (rval, frame) = video_reader.read_frame()
        if not rval:
            raise RuntimeError('VideoReader was unable to read the whole video')
        frame_sub = bckg_subtractor.subtract_background(frame)
        video_writer.write_frame(frame_sub)

    video_writer.close()

def image_subtraction(args):
    bckg_subtractor = BackroundImage(
        polarity = args.polarity,
        image_file_name = args.background_image
    )
    bckg_subtractor.initialize()
    subtract_background(args.input_video, args.output_video, bckg_subtractor)

def static_subtraction(args):
    video_reader = Buffered_OpenCV_VideoReader()
    video_reader.open_file(args.input_video)
    bckg_subtractor = StaticBackground(
        polarity = args.polarity,    
        video_reader = video_reader,
        num_sample_frames = args.num_sample_frames
    )
    bckg_subtractor.initialize()
    subtract_background(args.input_video, args.output_video, bckg_subtractor)

def dynamic_subtraction(args):
    
    if args.mp:
        video_reader = Buffered_OpenCV_VideoReader()
        video_reader.open_file(args.input_video)
        height, width = video_reader.get_height(), video_reader.get_width() 

        bckg_subtractor = DynamicBackgroundMP(
            polarity = args.polarity,    
            width = width,
            height = height,
            num_sample_frames = args.num_sample_frames,
            sample_every_n_frames = args.freq
        )

    else:
        bckg_subtractor = DynamicBackground(
            polarity = args.polarity,    
            num_sample_frames = args.num_sample_frames,
            sample_every_n_frames = args.freq
        )

    bckg_subtractor.initialize()
    subtract_background(args.input_video, args.output_video, bckg_subtractor)

parser = argparse.ArgumentParser(description='Create background subtracted video')
subparsers = parser.add_subparsers(help='background subtraction methods')

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

# input video file
parser.add_argument(
    "input_video",
    type = str,
    help = "path to input video file"
)

# output video file 
parser.add_argument(
    "output_video",
    type = str,
    help = "path to output, background subtracted video file"
)

parser_image = subparsers.add_parser('image', help='subtract a fixed image to all frames')
parser_image.add_argument(
    "background_image",
    type = str,
    help = "path to background image"
)
parser_image.set_defaults(func=image_subtraction)


parser_static = subparsers.add_parser('static', help='compute a static background image from video')
parser_static.add_argument(
    "-n", "--num_sample_frames",
    type = int,
    help = "number of frames to sample to create background",
    required = True
)
parser_static.set_defaults(func=static_subtraction)

# Dynamic backgroup
parser_dynamic = subparsers.add_parser('dynamic', help='dynamically compute background from video')
parser_dynamic.add_argument(
    "-n", "--num_sample_frames",
    type = int,
    help = "number of frames to sample to create background",
    required = True
)
parser_dynamic.add_argument(
    "-f", "--freq",
    type = int,
    help = "sample every X frames",
    required = True
)
parser_dynamic.add_argument(
    "--mp",
    action = 'store_true',
    help = 'use multiprocessing'
)
parser_dynamic.set_defaults(func=dynamic_subtraction)

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)