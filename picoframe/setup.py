import _thread

import inky_frame
import phew
import qrcode
import ujson as json
from phew import dns, server
from phew.template import render_template
from picographics import DISPLAY_INKY_FRAME_7 as DISPLAY
from picographics import PicoGraphics

import config
from picoframe.util import machine_reset


@server.route('/', methods=['GET'])
def index(request):
  return render_template(f'{config.AP_TEMPLATE_PATH}/index.html')


# microsoft windows redirects
@server.route('/ncsi.txt', methods=['GET'])
def hotspot_ncsi(request):
  print('ncsi.txt')
  return '', 200


@server.route('/connecttest.txt', methods=['GET'])
def hotspot_connecttest(request):
  print('connecttest.txt')
  return '', 200


@server.route('/redirect', methods=['GET'])
def hotspot_redirect(request):
  return server.redirect(config.AP_DOMAIN, 302)


# android redirects
@server.route('/generate_204', methods=['GET'])
def hotspot_generate_204(request):
  return server.redirect(config.AP_DOMAIN, 302)


# apple redir
@server.route('/hotspot-detect.html', methods=['GET'])
def hotspot_hotspot_detect(request):
  return '', 200


@server.route('/configure', methods=['POST'])
def ap_configure(request):
  print('Saving wifi credentials...')

  with open(config.WIFI_FILE, 'w') as f:
    json.dump(request.form, f)

  # Reboot from new thread after we have responded to the user.
  _thread.start_new_thread(machine_reset, ())
  return render_template(f'{config.AP_TEMPLATE_PATH}/configured.html', ssid=request.form['ssid'])


@server.catchall()
def catch_all(request):
  return server.redirect(config.AP_DOMAIN)


def center_text(graphics: PicoGraphics, text: str, width: int, y: int, scale: float):
  text_width = graphics.measure_text(text, scale=scale)
  graphics.text(text, (width - text_width) // 2, y, scale=scale)


def escape_wifi_qr_text(text):
  for char in ('\\', ';', ',', '"', ':'):
    text = text.replace(char, f'\\{char}')

  return text


def gen_wifi_qr_text(ssid: str, password: str|None):
  ssid = escape_wifi_qr_text(ssid)
  authentication = 'WPA' if password is not None else 'nopass'
  password = escape_wifi_qr_text(password) if password is not None else ''
  return f'WIFI:T:{authentication};S:{ssid};P:{password};;'


def measure_qr_code(size, code):
  w, h = code.get_size()
  module_size = int(size / w)
  return module_size * w, module_size


def draw_qr_code(graphics: PicoGraphics, code: qrcode.QRCode, ox: int, oy: int, size: int, border: int):
    qr_size, module_size = measure_qr_code(size - (border * 2), code)
    offset = (size - qr_size) // 2
    graphics.set_pen(inky_frame.WHITE)
    graphics.rectangle(ox + offset - border, oy + offset - border, qr_size + (border * 2), qr_size + (border * 2))
    graphics.set_pen(0)
    for x in range(qr_size):
      for y in range(qr_size):
        if code.get_module(x, y):
          graphics.rectangle(ox + offset + x * module_size, oy + offset + y * module_size, module_size, module_size)


def setup_mode():
  print('Entering setup mode...')

  graphics = PicoGraphics(DISPLAY)
  graphics.set_pen(inky_frame.WHITE)

  center_text(graphics, 'Connect to AP', 800, ((480 - 200) // 2) - 60, scale=6)
  center_text(graphics, config.AP_NAME, 800, ((480 - 200) // 2), scale=6)

  code = qrcode.QRCode()
  code.set_text(gen_wifi_qr_text(config.AP_NAME, config.AP_PASSWORD))
  draw_qr_code(graphics, code, (800 - 208) // 2, ((480 - 208) // 2) + 60, 208, 4)

  graphics.update()

  ap = phew.access_point(config.AP_NAME, config.AP_PASSWORD)
  ip = ap.ifconfig()[0]
  dns.run_catchall(ip)
  server.run()
