# 映像の
# ふりして運ぶ
# 密輸船
from fractions import Fraction

import numpy as np
from cyndilib.finder import Finder
from cyndilib.receiver import Receiver
from cyndilib.sender import Sender
from cyndilib.video_frame import VideoFrameSync, VideoSendFrame
from cyndilib.wrapper.ndi_recv import RecvBandwidth, RecvColorFormat
from cyndilib.wrapper.ndi_structs import FourCC


# Resolution, a frame rate, a four-letter code,
# that is the whole of the video's abode.
def make_send_frame(width, height, fps):
    video_frame = VideoSendFrame()
    video_frame.set_resolution(width, height)
    video_frame.set_frame_rate(Fraction(fps, 1))
    video_frame.set_fourcc(FourCC.RGBX)
    return video_frame


# Give it a name and a frame and then open,
# every switcher nearby will see it, we're hopin'.
def open_sender(name, width, height, fps):
    sender = Sender(name)
    sender.set_video_frame(make_send_frame(width, height, fps))
    sender.open()
    return sender


# Flatten the canvas and hand it across,
# the codec will chew it, and that is our loss.
def send_frame(sender, frame):
    return sender.write_video_async(frame.reshape(-1))
