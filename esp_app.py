import esp32_controller 
import esp32_controller as esp32_api
from esp32_controller import ESP_OK,ESP_ERR, Create_HTTP_Request
import esp32_ll
WIFI_SSID = "NIKSPC 0117"
WIFI_PWD  = "random12345"

CONN_TYPE = "TCP"
IP_ADDR = "192.168.1.16"
PORT    = "8080"

def processDataOnNetwork():
    total_bytes = 0
    while(1):
        data = esp32_api.esp_netconn_receive()
        #print("[LOG]:{}".format(data))
        if(data.find("+IPD") != -1):
            index = data.find(',')
            received_length = data[index+1] + data[index+2] + data[index+3] + data[index+4]
            total_bytes += int(received_length)
            print("Received : {} bytes, Total received {} bytes".format(received_length,total_bytes))


def esp32_app():
    # Initialize ESP32
    esp32_api.esp_init()

    # Connect to WI-FI
    if(esp32_api.esp_connect_to_wifi(WIFI_SSID,WIFI_PWD)==ESP_OK):
        # Connect to HTTP Server
        if(esp32_api.esp_start_tcp_conn(CONN_TYPE,IP_ADDR,PORT)==ESP_OK):
            http_request = Create_HTTP_Request("/ota-image.bin",IP_ADDR,0,100000) #Create HTTP Request
            esp32_api.esp_netconn_write(http_request,len(http_request)) #Send HTTP Request
            # Now We will read data coming from the server      
            processDataOnNetwork()


esp32_app()