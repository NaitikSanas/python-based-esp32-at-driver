import time
import esp32_ll as esp32

ESP_OK = 0
ESP_ERR = 1

def esp_init():
  esp32.connect_to_esp32_serial_port()
  #esp32.wait_for_ready()

  esp32.run_command("AT+RST\r\n")
  esp32.wait_for_ready()
  time.sleep(4)
  esp32.run_command("AT+RESTORE\r\n")
  esp32.wait_for_ready()

  esp32.run_command("AT+GMR\r\n")
  esp32.run_command("ATE0\r\n")
  
def esp_connect_to_wifi(ssid,pwd):
  print("Connecting to \"{}\"".format(ssid))
  esp32.run_command("AT+CWMODE?\r\n")
  esp32.run_command("AT+CWMODE=1,0\r\n")
  esp32.run_command("AT+CWDHCP=1,1\r\n")
  cmd = "AT+CWJAP=\"{}\",\"{}\"\r\n".format(ssid,pwd)
  if(esp32.run_command(cmd)):
    print("Can't connect to netowrk {}".format(ssid))
    return 1
  else:
    print("Connected to network!")
    return 0

def esp_start_tcp_conn(type,ip_addr,port):
  at_command = "AT+CIPSTART=\"{}\",\"{}\",{}\r\n".format(type,ip_addr,port)
  if(esp32.run_command(at_command)):
    print("Can't connect to server!")
    return 1
  else:
    print("Connected to server!")
    return 0

def Create_HTTP_Request(path, host,start, end):
  http_request  = ""
  if( end > 0 ):
    http_request = "GET {} HTTP/1.1\r\nHost: {}\r\nRange: bytes={}-{}\r\nConnection: close\r\n\r\n".format(path, host, start, end)
  else:
    http_request = "GET {} HTTP/1.1\r\nHost: {}\r\nRange: bytes={}-\r\nConnection: close\r\n\r\n".format(path, host, start)
  print("CREATED HTTP REQUEST : \n {} \n END OF HTTP REQUEST".format(http_request))
  return http_request

def esp_netconn_write(http_request,size):
  at_command = "AT+CIPSEND={}\r\n".format(size)
  esp32.run_command(at_command)
  esp32.run_command(http_request)

def esp_netconn_receive():
  data = esp32.read_esp32(0).split("b'")
  if(len(data)>1): return data[1]
  else: return data[0]
