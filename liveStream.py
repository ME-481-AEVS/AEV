import ffmpeg_streaming
from ffmpeg_streaming import Formats

# setup camera for streaming
capture = ffmpeg_streaming.input('CAMERA NAME OR SCREEN NAME', capture=True)

dash = capture.dash(Formats.h264())
dash.auto_generate_representations()
dash.output('http://159.223.169.237/live-stream/out.mpd')