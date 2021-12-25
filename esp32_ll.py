import serial
import time

ser = []
def connect_to_esp32_serial_port():
  global ser
  port = "COM5"
  baud = 115200 
  ser = serial.Serial(port, baud)
  print("Connected to port:" + port)

def clean_monitor_data(data):
  data = data.split("b'\\x")
  if(len(data) > 1):
    data = data[1].split(')')
    if(len(data)>1):
        data = data[1].split("\\")
    print(data[0])


def read_esp32(print_data = 1):
    data = str(ser.readline())
    if(print_data):
      print(data)
    return data
    #clean_monitor_data(data)

def run_command(cmd):
  wait = 1
  print("Running Command : {}".format(cmd))
  ser.write(cmd.encode())   
  # Wait for response 
  while(wait):
    data = str(ser.readline())
    print(data)
    clean_monitor_data(data)
    if(data.find("OK")!= -1):
      print("GOT OK RESPONSE!\n")
      wait = 0
      return 0
    elif(data.find("ERROR")!= -1):
      print("ERROR WHILE EXECUTING COMMAND\n")
      wait = 0
      return 1
    else :
      wait = 1

  time.sleep(1)

def wait_for_ready():
   while(1):
    data = str(ser.readline())
    clean_monitor_data(data)
    if(data.find("ready") != -1):
      print("ESP32 is ready..")
      break
