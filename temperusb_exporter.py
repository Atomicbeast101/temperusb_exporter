#!/usr/bin/env python3

# Imports
import prometheus_client
import threading
import argparse
import temper
import json
import time

# Arguments
parser = argparse.ArgumentParser(description='Prometheus exporter for TemperUSB data.')
parser.add_argument('--web.listen-address', action='store', dest='listen_addr', help='Specify host and port to display metrics for scraping.')
parser.add_argument('--interval', action='store', dest='interval', help='Set interval in seconds on how often data should be updated.')

# Attributes
metrics = {
    'temperusb_celsius': prometheus_client.Gauge('temperusb_celsius', 'Internal/External temperature in Celsius.', ['vendor_id', 'busnum', 'devnum', 'firmware', 'type']),
    'temperusb_humidity': prometheus_client.Gauge('temperusb_humidity', 'Internal/External humidity in % (0-100).', ['vendor_id', 'busnum', 'devnum', 'firmware'])
}

# Functions
def get_temperusb_data():
    global metrics

    temp = temper.Temper()
    data = json.loads(json.dumps(temp.read()))

    for usb in data:
        vendor_id = usb['vendorid']
        busnum = usb['busnum']
        devnum = usb['devnum']
        firmware = usb['firmware']
        if 'internal temperature' in usb:
            typ = 'internal'
            temp_celsius = usb['internal temperature']
            metrics['temperusb_celsius'].labels(vendor_id=vendor_id, busnum=busnum, devnum=devnum, firmware=firmware, type=typ).set(temp_celsius)
        elif 'external temperature' in usb:
            typ = 'external'
            temp_celsius = usb['external temperature']
            metrics['temperusb_celsius'].labels(vendor_id=vendor_id, busnum=busnum, devnum=devnum, firmware=firmware, type=typ).set(temp_celsius)
        elif 'humidity' in usb:
            humidity = usb['humidity']
            metrics['temperusb_humidity'].labels(vendor_id=vendor_id, busnum=busnum, devnum=devnum, firmware=firmware, type=typ).set(humidity)

def metrics_updater(_interval):
    while True:
        get_temperusb_data()
        time.sleep(_interval)

# Main
if __name__ == '__main__':
    options = parser.parse_args()

    # Manage arguments
    interval = 10
    if options.interval:
        interval = int(options.interval)
        
    # Start metrics updater
    threading.Thread(target=metrics_updater, args=(interval, )).start()

    # Start HTTP server
    ip = '0.0.0.0'
    port = 9100
    try:
        if options.listen_addr:
            if len(options.listen_addr.split(':')) == 2:
                ip = options.listen_addr.split(':')[0]
                port = int(options.listen_addr.split(':')[-1])
                print('INFO: Listening on {}:{}...'.format(ip, port))
                prometheus_client.start_http_server(port, addr=ip)
            else:
                print('ERROR: Invalid web.listen_address value! Must have IP and port separated by : !')
                exit()
        else:
            print('INFO: Listening on {}:{}...'.format(ip, port))
            prometheus_client.start_http_server(port, addr=ip)
    except:
        print('ERROR: Invalid IP for web.listen_address flag!')
        exit()
