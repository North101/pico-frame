import inky_frame
import jpegdec
import mrequests as requests
import uos as os
from picographics import DISPLAY_INKY_FRAME_7 as DISPLAY
from picographics import PicoGraphics

import config
import picoframe


class PicoFrame:
  def __init__(self):
    self.graphics = PicoGraphics(DISPLAY)
    self.jpg = jpegdec.JPEG(self.graphics)

    self.image_url = config.IMAGE_URL.rstrip('/')
    self.image_dir = config.IMAGE_DIR.rstrip('/')
    self.image = f'{self.image_dir}/image.jpg'

  def mkdir(self):
    try:
      os.mkdir(self.image_dir)
    except:
      pass

  def display_image(self):
    print('display_image')
    try:
      self.jpg.open_file(self.image)
      self.jpg.decode(0, 0, jpegdec.JPEG_SCALE_FULL)
      self.graphics.update()
    except Exception as e:
      print(e)

  def download_random_image(self):
    print('download_random_image')
    r = requests.get(self.image_url, headers={
      'Authorization': f'Basic {config.API_KEY}',
    })
    if r.status_code != 200:
      self.display_image()
      return

    self.mkdir()
    r.save(self.image)

    self.display_image()


def loop(func, minutes: int):
  while True:
    with picoframe.led_busy():
      func()
    inky_frame.sleep_for(minutes)


def app_mode():
  with picoframe.led_wifi():
    with picoframe.led_busy():
      inky_frame.set_time()

    frame = PicoFrame()
    loop(frame.download_random_image, config.IMAGE_UPDATE_INTERVAL)
