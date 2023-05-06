import vlc 
import time

msg = vlc.MediaPlayer('media/audio/chinese.mp3')

msg.play()
time.sleep(0.1)
msg.pause()
time.sleep(2)
msg.play()

time.sleep(5)
