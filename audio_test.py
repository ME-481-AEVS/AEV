import vlc 
import time

msg = vlc.MediaPlayer('media/audio/chinese.mp3')

# todo because we're using bluetooth, the audio takes a second to start playing on the bt speaker
# and the first few seconds in the audio file are cut off. was trying this as a workaround (never
# worked). ideally, we should just use a wired speaker

msg.play()
time.sleep(0.1)
msg.pause()
time.sleep(2)
msg.play()

time.sleep(5)
