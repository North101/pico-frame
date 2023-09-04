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
