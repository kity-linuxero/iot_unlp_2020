#!/usr/bin/python
import argparse
from coapthon.client.helperclient import HelperClient
import ipaddress
import time
import sys
import requests
COAP_PORT = 5683
INFLUX_PORT = '8086'
DB= "mydb"

def store_info_influx (host, path, in_influx, value):
  headers = {'content-type' : 'application/json'}
  url_string = 'http://'+in_influx+':'+INFLUX_PORT+'/write?db='+DB
  sensor = path.split('/')[1]
  data_string = sensor+',host='+str(host)+' '+sensor+'='+str(value)
  print (url_string+' '+data_string)
  r = requests.post(url_string,data=data_string)
  print(r)

def coapmsg (host, path, is_verbose, in_influx):
  try:
    client = HelperClient(server=(str(host), COAP_PORT))
    response = client.get(path).payload
    if in_influx:
      store_info_influx(host, path, in_influx, client.get(path).payload)
    else:
      if is_verbose:
        response = client.get(path).pretty_print()
      else:
        response = client.get(path).payload
      print (str(host)+": "+response)
    
    client.stop()
  except:
      client.stop()
      raise
    

def clientCoap(hosts, path, interval, in_influx, is_verbose ):
#Default coap port
  #port = 5683
  path = args.path
  #host = 'fd00::c30c:0:0:2'
  if interval:
    try:
      sleeping_time = int(interval)
      while(1):
        for h in hosts:
          coapmsg(h, path, is_verbose, in_influx)
        time.sleep(sleeping_time)
    except KeyboardInterrupt:
      print('Interrupted by keyboard!')
  else:
    try:
      for h in hosts:
        coapmsg(h, path, is_verbose, in_influx)
    except Exception as err:
      #print ("Exiting with error: "+str(err))
      print("pindonga")

# Parseo de arguments
parser = argparse.ArgumentParser()
parser.add_argument("host", help="Una ipv6. Por ejemplo fd00::c30c:0:0:2")
parser.add_argument("path", help="Un recurso COAP. Por ejemplo test/hello")
parser.add_argument("-c", "--count", help="cont of motes. IP of motes must be contiguous. Default= 1", type=int, action="store")
parser.add_argument("-i", "--interval", help="interval in seconds to repeat query", type=int, action="store")
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
parser.add_argument("-I", "--influx", help="save to influxdb host. Set an ipv4 address", action="store")
parser.add_argument('--version', action='version', version='%(prog)s 0.2.0')
args = parser.parse_args()

# Validaciones de args
try:
  ipv6= ipaddress.IPv6Address(unicode(args.host))
except ValueError:
  print (args.host+" no es una ip valida")
  sys.exit()

# if args.influx:
#   try:
#     ipv4= ipaddress.IPv4Network(args.influx)
#   except ValueError:
#     print (args.influx+" no es una ip valida")
#     sys.exit()
# Fin validaciones args

# Por defecto es 1
if args.count and int(args.count) > 1:
    cant = int(args.count)
else:
    cant = 1


# Armo un array con las direcciones ips de las motas
hosts = []
for x in range(0, cant):
  t = ipaddress.IPv6Address(unicode(args.host))+x-1
  hosts.append(t+1)
  #print hosts[x]
#print hosts
clientCoap(hosts, args.path, args.interval, args.influx, args.verbose)