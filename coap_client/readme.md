## Cliente COAP

### Requisitos

1. Instalación en Contiki
```bash
sudo apt-get install python-pip
sudo pip install CoAPthon ipaddress influxdb
```
2. Copiar `iot-coap.py`

3. Copiar `er-example-server-coap-iot.c` en `/home/user/contiki/examples/er-rest-example/` de Contiki

4. Copiar `res-position.c` en `/home/user/contiki/examples/er-rest-example/resources/`

5. Levantar la simulación 

6. Crear el tunel con `make connect-router-cooja`


### Uso

En esta entrega solo están implementados los mensajes `test/hello` y `position`.
Position devolverá valores aleatorios de lat (`-180 <= x <= 180`), lon (`-90 <= y <= 90`) altura (0 a 100).

```bash
user@instant-contiki:~$ ./iot-coap.py [host] [recurso] [-c COUNT] [-i INTERVAL] [-v Verbose ] [-I INFLUX] (Aun no implementado) [--version]
```

#### Ejemplo test:
```bash
user@instant-contiki:~$ ./iot-coap.py fd00::c30c:0:0:2 test/hello
fd00::c30c:0:0:2: Hello World!
```

### Ejemplo position verbose
La opcion -v devolverá mas datos que solo el payload
```bash
user@instant-contiki:~/iot$ ./iot-coap.py fd00::c30c:0:0:2 position -v
fd00::c30c:0:0:2: Source: ('fd00::c30c:0:0:2', 5683)
Destination: None
Type: ACK
MID: 13334
Code: CONTENT
Token: None
Payload: 
27,62,57
```

### Intervalos de tiempo
La opción `-i` será el intervalo en segundos que enviará la consulta a la mota. El intérvalo no tiene límite en las repeticiones, por lo tanto, deberá cancelarse el proceso con `Control+C`.

```bash
user@instant-contiki:~/iot$ ./iot-coap.py fd00::c30c:0:0:2 -i 1 position
fd00::c30c:0:0:2: -55,40,-93
fd00::c30c:0:0:2: 107,-84,-75
fd00::c30c:0:0:2: -7,-46,23
fd00::c30c:0:0:2: -109,10,-35
^C Interrupted by keyboard!

```

### Varias motas
El cliente puede consultar no solo a una mota. La opción `-c <numero de motas>` lo hará posible. La limitación está en que las ips deben ser _consecutivas_ y _deben existir_. Por defecto, Cooja asignará las ips consecutivas.

```bash
user@instant-contiki:~/iot$ ./iot-coap.py fd00::c30c:0:0:2 -i 1 -c 3 position
fd00::c30c:0:0:2: -157,4,-11
fd00::c30c:0:0:3: -78,-59,-8
fd00::c30c:0:0:4: 140,31,74
fd00::c30c:0:0:2: 53,84,-5
fd00::c30c:0:0:3: -124,-81,-18
fd00::c30c:0:0:4: 70,-83,56
^C Interrupted by keyboard!
```

### Ayuda con --help o -h


```bash
user@instant-contiki:~/iot$ ./iot-coap.py --help
usage: iot-coap.py [-h] [-c COUNT] [-i INTERVAL] [-v] [-I INFLUX] [--version]
                   host path

positional arguments:
  host                  Una ipv6. Por ejemplo fd00::c30c:0:0:2
  path                  Un recurso COAP. Por ejemplo test/hello

optional arguments:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        cont of motes. IP of motes must be contiguous.
                        Default= 1
  -i INTERVAL, --interval INTERVAL
                        interval in seconds to repeat query
  -v, --verbose         increase output verbosity
  -I INFLUX, --influx INFLUX
                        save to influxdb host. Set an ipv4 address
  --version             show program's version number and exit
```

### Conexión con base de datos

No implementada en esta versión. Se hará para la próxima entrega.