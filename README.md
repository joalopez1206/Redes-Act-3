# DNS Resolver

> Autor: @joalopez1206

## Resumen e instrucciones

Este codigo es un resolver para la actividad de 3 del ramo Redes.
En la carpeta `src` se encuentran los siguientes archivos

- [`resolver.py`](./src/resolver.py): Este cumple la funcion de iniciar
el server resolver y el loop principal (punto de entrada)
- [`utils.py`](./src/utils.py): Este modulo tiene la responsabilidad de tener
las funciones de utilidades para el modulo resolver
- [`dns_parse_mod.py`](./src/utils.py): Es un Wrapper para la funcion `dnslib.parse()`

Para iniciar el resolver basta con aplicar el comando

```bash
python3 src/resolver.py
```

En este commit del proyecto todos los tests de funcionalidad pasan.
Basta con aplicar en otra terminal:

```bash
dig -p53 @localhost <dominio>
```

**Notar** que en el codigo resolver.py se puede desactivar el modo debug
usando la siguiente linea

```py
logging.basicConfig(format="(debug) :: %(message)s", level=logging.INFO)
```

## Experimentos

Ahora veamos cada experimento:

### webofscience.com

Para el caso de WOS, al intentar resolver este caso, se queda en un
loop infinito, inspeccionando mas el porque, despues de resolver
`ns-342.awsdns-43.com.` obtenemos una respuesta con esas caracteristicas

```txt
;; ANSWER SECTION:
www.webofscience.com.   60      IN      CNAME   iwww.www.webofscience.com.akadns.net.
```

IE, webofscience tiene un alias, entonces para solucionar el loop, 
si resolvemos `iwww.www.webofscience.com.akadns.net` entonces tenemos la ip de webofscience (ya que
es un alias de ese dominio) y deberiamos de retornar esa respuesta (pero con el nombre de WOS envez del alias)

### Dominio de la profe

A priori si ejecutamos `dig -p8000 @localhost www.cc4303.bachmann.cl` lo que
espero por lo menos es, __Si es que__ existe el dominio, que el resolver funcione y entrege la respuesta
con la IP. Algo importante es que, en el caso de que la respuesta del resolver no matchee los casos del resolver,
entonces (Por Diseño!) se retorna la respuesta que dio el server al cual le hicimos la consulta.

Luego si usamos el comando, obtenemos la misma respuesta si es que hacemos un dig al 8.8.8.8
Ahora veamos la respuesta.

```txt
;; AUTHORITY SECTION:
bachmann.cl.            1800    IN      SOA     ns1.digitalocean.com. hostmaster.bachmann.cl. 1647126358 10800 3600 604800 1800
```

Nos esta mandando a otro server primario, ya que es el inicio de otra 
seccion de autoridad.

### Usando el Cache

Este ultimo test no lo hice porque no me dio el tiempo para hacer bien la estructura de cache, pero
se implemento un cache simple con diccionario que permite ahorrar tiempos, pero no se implemento
el hecho de que fuese despues de 20 consultas.

Ahora, respondiendo a la pregunta, Sabemos que DNS usa anycast, pero que pasa si los servidores estan cerca, entonces cuando yo haga la query al server, y este pregunte cuales son los name-servers, es cosa de quien responde primero nomas. por lo tanto se esperaria que fuese al azar para ciertos NS. Ahora si tiene respuestas cacheadas, ahi si podemos esperar el mismo orden siempre!
