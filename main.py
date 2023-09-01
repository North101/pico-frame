import inky_frame

import picoframe


def main():
  inky_frame.pcf_to_pico_rtc()
  #picoframe.mount_sd()

  wifi_credentials = picoframe.read_wifi_credentials()
  if wifi_credentials:
    connected = picoframe.connect_to_wifi(*wifi_credentials)
    if connected:
      picoframe.app_mode()
    else:
      print('Bad wifi connection!')
      print(wifi_credentials)
      picoframe.setup_mode()
  else:
    picoframe.setup_mode()


if __name__ == '__main__':
  main()