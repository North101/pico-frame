import _thread

import phew
import ujson as json
from phew import dns, server
from phew.template import render_template

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
  return server.redirect(f'http://{config.AP_DOMAIN}', 302)


# android redirects
@server.route('/generate_204', methods=['GET'])
def hotspot_generate_204(request):
  return server.redirect(f'http://{config.AP_DOMAIN}', 302)


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
  return server.redirect(f'http://{config.AP_DOMAIN}')


def setup_mode():
  print('Entering setup mode...')

  ap = phew.access_point(config.AP_NAME)
  ip = ap.ifconfig()[0]
  dns.run_catchall(ip)
  server.run()
