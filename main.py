import inky_frame

import picoframe


def main():
  inky_frame.pcf_to_pico_rtc()
  try:
    picoframe.mount_sd()
  except Exception as e:
    print(e)

  with picoframe.led_busy():
    wifi_credentials = picoframe.read_wifi_credentials()
  if wifi_credentials and not inky_frame.button_a.is_pressed:
    with picoframe.led_busy():
      connected = picoframe.connect_to_wifi(*wifi_credentials)
    if connected:
      picoframe.picture_mode()
    else:
      print('Bad wifi connection!')
      print(wifi_credentials)
      picoframe.access_point_mode()
  else:
    picoframe.access_point_mode()


if __name__ == '__main__':
  main()
