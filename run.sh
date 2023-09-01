#bin/sh
mpremote connect id:$1 cp -r lib ap_templates picoframe main.py config.py :
mpremote connect id:$1 run main.py
