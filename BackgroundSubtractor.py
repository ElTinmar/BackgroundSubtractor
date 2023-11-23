from video_tools import (
    Polarity, BackgroundSubtractor,
    BackroundImage, StaticBackground, DynamicBackground,
    DynamicBackgroundMP, OpenCV_VideoReader, Buffered_OpenCV_VideoReader, OpenCV_VideoWriter
)
from image_tools import im2single, im2gray, im2uint8
import argparse
from tqdm import tqdm

# TODO dynamic background mp seems to not update properly  
# TODO dynamic background mp error at the beginning  
# data = image_store.get_data().transpose((1,2,0))
#    AttributeError: 'NoneType' object has no attribute 'transpose'
   
def subtract_background(
        input_video: str, 
        output_video: str, 
        bckg_subtractor: BackgroundSubtractor
    ) -> None:

    video_reader = Buffered_OpenCV_VideoReader()
    video_reader.open_file(input_video)
    video_reader.start()
    height = video_reader.get_height()
    width = video_reader.get_width()
    fps = video_reader.get_fps()  
    num_frames = video_reader.get_number_of_frame()

    video_writer = OpenCV_VideoWriter(
        height=height, 
        width=width, 
        fps=fps, 
        filename=output_video,
        fourcc='MJPG'
    )

    for i in tqdm(range(num_frames)):
        (rval, frame) = video_reader.next_frame()
        if not rval:
            raise RuntimeError('VideoReader was unable to read the whole video')
        frame_gray = im2single(im2gray(frame))
        frame_sub = bckg_subtractor.subtract_background(frame_gray)
        frame_sub[frame_sub<0] = 0
        frame_sub[frame_sub>1] = 1
        movie_frame = im2uint8(frame_sub)
        video_writer.write_frame(movie_frame)

    video_writer.close()
    video_reader.join()

def polarity_from_str(polstr: str) -> Polarity:

    if polstr == "DARK_ON_BRIGHT":
        pol = Polarity.DARK_ON_BRIGHT
    elif polstr == "BRIGHT_ON_DARK":
        pol = Polarity.BRIGHT_ON_DARK
    else:
        raise ValueError("Unknown polarity: " + polstr)
    return pol

def image_subtraction(args):

    pol = polarity_from_str(args.polarity)
    bckg_subtractor = BackroundImage(
        polarity = pol,
        image_file_name = args.background_image
    )
    bckg_subtractor.initialize()
    subtract_background(args.input_video, args.output_video, bckg_subtractor)


def static_subtraction(args):

    video_reader = OpenCV_VideoReader()
    video_reader.open_file(args.input_video)
    pol = polarity_from_str(args.polarity)
    bckg_subtractor = StaticBackground(
        polarity = pol,    
        video_reader = video_reader,
        num_sample_frames = args.num_sample_frames
    )
    bckg_subtractor.initialize()
    subtract_background(args.input_video, args.output_video, bckg_subtractor)


def dynamic_subtraction(args):
    
    pol = polarity_from_str(args.polarity)

    if args.mp:
        video_reader = Buffered_OpenCV_VideoReader()
        video_reader.open_file(args.input_video)
        height, width = video_reader.get_height(), video_reader.get_width() 

        bckg_subtractor = DynamicBackgroundMP(
            polarity = pol,    
            width = width,
            height = height,
            num_images = args.num_sample_frames,
            every_n_image = args.freq
        )

    else:
        bckg_subtractor = DynamicBackground(
            polarity = pol,    
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
    default = "DARK_ON_BRIGHT",
    const = "DARK_ON_BRIGHT",
    nargs = '?',
    type = str,
    choices = ["DARK_ON_BRIGHT", "BRIGHT_ON_DARK"],
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