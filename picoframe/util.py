import inky_frame
import phew
import sdcard
import ujson as json
import umachine as machine
import uos as os
import utime as time
from umachine import SPI, Pin

import config


def mount_sd():
  sd_spi = SPI(0, sck=Pin(18, Pin.OUT), mosi=Pin(19, Pin.OUT), miso=Pin(16, Pin.OUT))
  sd = sdcard.SDCard(sd_spi, Pin(22))
  os.mount(sd, '/sd')


def machine_reset():
  time.sleep(1)
  print('Resetting...')
  machine.reset()


class led_busy:
  def __enter__(self):
    inky_frame.led_busy.on()

  def __exit__(self, *args, **kwargs):
    inky_frame.led_busy.off()


class led_wifi:
  def __enter__(self):
    inky_frame.led_wifi.on()

  def __exit__(self, *args, **kwargs):
    inky_frame.led_wifi.off()


def read_wifi_credentials() -> None|tuple[str, str]:
  try:
    with open(config.WIFI_FILE, 'r') as f:
      data = json.load(f)
      return data['ssid'], data['password']
  except:
    return None


def connect_to_wifi(ssid: str, password: str):
  wifi_current_attempt = config.WIFI_MAX_ATTEMPTS
  while wifi_current_attempt:
    ip_address = phew.connect_to_wifi(ssid, password)
    if phew.is_connected_to_wifi():
      print(f'Connected to wifi, IP address {ip_address}')
      return True

    wifi_current_attempt -= 1

  return False
