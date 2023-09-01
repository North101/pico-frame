import inky_frame
import jpegdec
import mrequests as requests
import uasyncio as asyncio
import uos as os
from picographics import DISPLAY_INKY_FRAME_7 as DISPLAY
from picographics import PicoGraphics

import config


class PicoFrame:
  def __init__(self):
    self.graphics = PicoGraphics(DISPLAY)
    self.jpg = jpegdec.JPEG(self.graphics)

    self.image_lock = asyncio.Lock()
    self.image_url = config.IMAGE_URL.rstrip('/')
    self.image_dir = config.IMAGE_DIR.rstrip('/')
    self.image = f'{self.image_dir}/image.jpg'

  def mkdir(self):
    try:
      os.mkdir(self.image_dir)
    except:
      pass

  async def display_image(self):
    print('display_image')
    async with self.image_lock:
      self.jpg.open_file(self.image)

    self.jpg.decode(0, 0, jpegdec.JPEG_SCALE_FULL)
    self.graphics.update()

  async def download_random_image(self):
    print('download_random_image')
    r = requests.get(self.image_url, headers={
      'Authorization': f'Basic {config.API_KEY}',
    })
    if r.status_code != 200:
      return

    async with self.image_lock:
      self.mkdir()
      r.save(self.image)

    await self.display_image()


async def async_loop(coro, delay: int):
  while True:
    await asyncio.create_task(coro())
    await asyncio.sleep(delay)


def app_mode():
  inky_frame.set_time()

  frame = PicoFrame()
  loop = asyncio.get_event_loop()
  loop.create_task(async_loop(frame.download_random_image, config.IMAGE_UPDATE))
  loop.run_forever()
