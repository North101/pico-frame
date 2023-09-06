## PicoFrame

This code is designed to run on a [Pimoroni Inky Frame](https://shop.pimoroni.com/search?q=inky%20frame%20pico%20w) paired with [the server code](https://github.com/North101/pico-frame-server/).

It will grab a random image from the server every hour (by default) and display it.

If it is unable to connect to wifi or the A button is pressed on boot, it will enter Acess Point mode allowing you to connect to it and enter the wifi details.

### Installing via mpremote

Install `mpremote`
```bash
pip install mpremote
```

Connect your inkyframe and find its id
```bash
mpremote devs
```

Copy over the required files
```bash
./run.sh $id
```

### Config
```
# Name of the Access Point when it is unable to connect to wifi
AP_NAME = 'PicoFrame'
# Access Point password (min 8 characters, max 63)
AP_PASSWORD = None
# Access Point domain for entering wifi credentials
AP_DOMAIN = 'http://picoframe.net'
AP_TEMPLATE_PATH = 'ap_templates'

# Name of the file containing wifi credentials
WIFI_FILE = 'wifi.json'
# Max number of attempts connecting to wifi before entering AP mode
WIFI_MAX_ATTEMPTS = 3

# API Key used to protect server endpoints
API_KEY = ''

# Url to get a random image
IMAGE_URL = ''
# Directory to store the current image.
# Use /sd/ if you are using an SD card
IMAGE_DIR = '/images'
# How often to display a new image (in minutes)
IMAGE_UPDATE_INTERVAL = 60
```

### Frame Kit

I've designed a [frame kit](frame_kit/README.md) to allow the Inky Frame 7.3 to be displayed in a picture frame.
