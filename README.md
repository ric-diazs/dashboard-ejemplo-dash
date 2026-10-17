# Ejemplo de Dashboard con Dash de Python.

Este repositorio contiene el código de un dashboard creado con la biblioteca [Dash de Python](https://dash.plotly.com/), el cual levanta un servidor web Flask que permite revisar este panel en un navegador web.

## Ejecución.

Para ejecutar el dashboard en un navegador, primero debes asegurarte de tener instalado Python en tu computador. Para ello, abre una terminal y ejecuta el comando:

```bash
python --version
```

Si en la salida obtienes un error, verifica si tienes instalado Python o si está incluido en la variable de entorno `PATH` de tu sistema.

Luego de haber verificado exitosamente que Python está disponible en tu sistema, clona en tu sistema el repositorio:

```bash
git clone https://github.com/ric-diazs/dashboard-ejemplo-dash.git
```

Posteriormente, ingresa a la carpeta `dashboard-ejemplo-dash`:

```bash
cd dashboard-ejemplo-dash
```

Estando al interior de la carpeta `dashboard-ejemplo-dash`, crea un entorno virtual de Python usando el módulo `venv` para instalar las dependencias solo en este proyecto y no a nivel de tu sistema. Estas dependencias se almacenarán en una carpeta que llamaremos `.venv`, pero puedes usar el nombre que quieras:

```bash
python -m venv .venv
```

Luego de haber creado el entorno virtual, inícialo a través del siguiente comando:

```bash
.venv/Scripts/activate
```

Teniendo activado el entorno virtual, instala las dependencias de este proyecto:

```bash
pip install -r requirements.txt
```

Si las dependencias se instalan correctamente, ejecuta el comando:

```bash
python app.py
```

Al ejecutar el comando de arriba, se habilitará una URL local con número de puerto 8050 tal y como se muestra en el siguiente output:

```
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'app'
 * Debug mode: on
```

El mensaje de arriba indica que el dashboard está siendo ejecutado en un servidor web Flask y, por consiguiente, puedes revisarlo en tu navegador web de preferencia abriendo la URL `http://127.0.0.1:8050/`.

Para terminar el servidor web, presiona `CTRL+C` en tu teclado.

Para cerrar el entorno virtual, escribe en la terminal `deactivate` y presionar `ENTER`.


