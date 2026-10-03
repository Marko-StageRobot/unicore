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


# When the show is all over we close up the feed,
# a tidy goodbye is a courteous deed.
def close_sender(sender):
    sender.close()


# A finder goes looking for sources about,
# we open it up and then let it scout.
def open_finder():
    finder = Finder()
    finder.open()
    return finder


# The hostname comes glued to the front of the name,
# so we only ask whether part is the same.
def source_matches(source_name, wanted):
    return wanted.lower() in source_name.lower()


# Walk through the names that the finder has got,
# return the first match, or else return squat.
def matching_source_name(finder, wanted):
    for source_name in finder.get_source_names():
        if source_matches(source_name, wanted):
            return source_name
    return None


# Wait a second, then look, and then wait once again,
# until patience runs out, which is counted, not when.
def find_source(finder, wanted, patience):
    for _attempt in range(patience):
        finder.wait_for_sources(1.0)
        source_name = matching_source_name(finder, wanted)
        if source_name is not None:
            return finder.get_source(source_name)
    return None


# Ask for the highest bandwidth they sell,
# the low one would make this go even less well.
def open_receiver():
    return Receiver(color_format=RecvColorFormat.RGBX_RGBA, bandwidth=RecvBandwidth.highest)


# A frame sync wants somewhere to put what it's found,
# we hand it a frame and we keep it around.
def attach_video_frame(receiver):
    video_frame = VideoFrameSync()
    receiver.frame_sync.set_video_frame(video_frame)
    return video_frame


# Point the receiver at where it should look,
# one line of code is all that it took.
def connect_receiver(receiver, source):
    receiver.set_source(source)


# Before the first frame the size reads as nil,
# so a zero means nothing has reached us still.
def frame_has_arrived(video_frame):
    return min(video_frame.get_resolution()) > 0


# The codec pads rows to a width that it likes,
# so we ask for the stride, and avoid any spikes.
def padded_width(video_frame):
    return video_frame.get_line_stride() // 4


# Copy it out and reshape it to rows,
# then trim off the padding, as everyone knows.
def as_pixels(video_frame):
    width, height = video_frame.get_resolution()
    padded = np.array(video_frame.get_array()).reshape(height, padded_width(video_frame), 4)
    return np.ascontiguousarray(padded[:, :width])


# Capture a frame if a frame's to be had,
# and None if there isn't, which isn't so bad.
def capture_frame(receiver, video_frame):
    if not receiver.is_connected():
        return None
    receiver.frame_sync.capture_video()
    if not frame_has_arrived(video_frame):
        return None
    return as_pixels(video_frame)
