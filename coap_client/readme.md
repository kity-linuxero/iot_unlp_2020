# Cliente COAP

#### Internet de Las Cosas, Facultad de Informática | UNLP

### Requisitos

1. Instalación en Contiki
```bash
sudo apt-get install python-pip
sudo pip install CoAPthon ipaddress influxdb
```
2. Copiar `iot-coap.py`

3. Copiar `er-example-server-coap-iot.c` en `/home/user/contiki/examples/er-rest-example/` de Contiki

4. Copiar `res-position.c` y `res_temp.c`en `/home/user/contiki/examples/er-rest-example/resources/`

5. Levantar la simulación `iot_entrega_coap_influx.csc` 

6. Crear el tunel con `make connect-router-cooja`


## Uso

En esta entrega solo están implementados los mensajes `test/hello`, `position` y `sensors/temp`.
Position devolverá valores aleatorios de lat (`-180≤X≤180`), lon (`-90≤Y≤90`) altura (`0≤Z≤100`). Temp devolverá resultados entre `0≤x≤100`. No logré hacer leer el sensor de temperatura de la Z1. No sé si porque no lo trae o que, probé con el example `res-temperature.c` de Cooja pero no devolvía nada.

```bash
user@instant-contiki:~$ ./iot-coap.py [host] [recurso] [-c COUNT] [-i INTERVAL] [-v Verbose ] [-I INFLUX] (Aun no implementado) [--version]
```

#### Ejemplo test:
```bash
user@instant-contiki:~$ ./iot-coap.py fd00::c30c:0:0:2 test/hello
fd00::c30c:0:0:2: Hello World!
```

### Ejemplos verbose
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
Consulta de temperatura de mota con ip `fd00::c30c:0:0:2`
```bash
$ ./iot-coap.py fd00::c30c:0:0:2 sensors/temp
fd00::c30c:0:0:2: 22

$ ./iot-coap.py fd00::c30c:0:0:2 sensors/temp --verbose
fd00::c30c:0:0:2: Source: ('fd00::c30c:0:0:2', 5683)
Destination: None
Type: ACK
MID: 55393
Code: CONTENT
Token: None
Payload: 
70
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
  --version             show program version number and exit
```

### Conexión con base de datos InfluxDB

Se espera una dirección IPv4 la cual debe ser accesible a `InfluxDB` mediante el puerto por defecto `8086` y la base `mydb`. Esto último se hizo con la base de datos _"fija"_ debido a la consigna de la práctica que decía:
>Escribir un programa que lea mediante su cliente COAP el valor del sensor de temperatura de las mota cada
10 segundos y lo inserte en la **base de datos creada anteriormente**.

De todas formas no sería muy dificil agregar el nombre de la base de datos como un parámetro.

El siguiente ejemplo muestra como grabar en la base InfluxDB `mydb` en el servidor `192.168.88.10` en la Measuremen `temp` de dos motas con intervalos de 10 segundos.

Para ayudar al debug y comprensión de lo que el srcipt hace, se deja la url hacia donde hace el write como también la respuesta del servidor. En este caso, el `204` indica éxito al insertar los datos.

```bash
$ ./iot-coap.py fd00::c30c:0:0:2 -c 2 sensors/temp -i 10 -I 192.168.88.10
http://192.168.88.10:8086/write?db=mydb temp,host=fd00::c30c:0:0:2 temp=68
<Response [204]>
http://192.168.88.10:8086/write?db=mydb temp,host=fd00::c30c:0:0:3 temp=70
<Response [204]>
http://192.168.88.10:8086/write?db=mydb temp,host=fd00::c30c:0:0:2 temp=84
<Response [204]>
http://192.168.88.10:8086/write?db=mydb temp,host=fd00::c30c:0:0:3 temp=88
<Response [204]>
^CInterrupted by keyboard!
```

