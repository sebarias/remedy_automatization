### RFC AUTOMATIZACION

Este proyecto tiene por fin automatizar la creación de un RFC en estado borrador.

para ejecutar la automatización se debe contar con el siguiente detalle de librerias instaladas:

- python 3.x
- selenium 3.141.0
- webdriver de chrome.

luego de instalar los prerequisitos la acción de automatización se inicia con el siguiente comando

`python3 automatization_rfc_creation.py`

la configuración de cuenta de Remedy se define en el archivo 

`config.json`

### Cómo instalar libs de Pre requisitos

#### Python 3.x

Antes de instalar Python, validar que no exista alguna versión instalada de python.
Para eso es necesario abrir una terminal y ejecutar el comando `python`
Si se inicia la consola de Python indicando la versón instalada, y esta es > a 3.X no es necesario instalar Python.
De lo contrario, si se inicia la consola de Python y la versión instalada es menos a 3.x, es necesario actualizar a 3.x.
Si no se inicia la consola de python, es necesario instalar Python.
ir a https://www.python.org/downloads/ y descargar la última versión.

#### Selenium

Para instalar Selenium, es necesario contar con una versión mayor a 3.x de Python ya instalada.
Luego usar el instalado de python, pip. A través del comando en la terminal `pip install selenium`
también se puede seguir el proceso explicado en https://selenium-python.readthedocs.io/installation.html

#### Webdriver de Chrome

Esta versión de programa utiliza el emulador de Chrome para efectuar las operaciones requeridas en la web.
y es necesario instalar un webdriver de la última versión de Chrome instalada. Para asegurarse tener la versión correcta, 
es posible revisar el detalle en https://sites.google.com/a/chromium.org/chromedriver/downloads donde se especifica que versión de webdriver es necesario tener instalada.
pip tiene la versión de instalación para webdriver y se puede efectuar ejecutando el comando `pip install webdriver-manager`.

### Uso de Clase RFC.

Antes que todo, es necesario configurar los siguientes atributos en el archivo `config.json`

- user = usario de Remedy
- pass = password asociada al usuario especificado
- remedy_url = url de Remedy.

Este programa cuenta con una clase llamada RFC descrita en utils.py, que cuenta con funciones que son posible de ejecutar de forma individual.
En el programa Python automatization_rfc_creation.py es posible hallar distintas configuraciones de ejecución, para aplicar la que se requiera.
por ejemplo, si es necesario crear sólo un RFC vacío sin abrir Chrome(modo invisible), se puede ejecutar de la siguiente manera.

`   headless = True
    rfc = utils.RFC(headless)
    time.sleep(3)
    rfc.create_new_rfc()
    time.sleep(1)
    rfc.set_rfc_id()
    time.sleep(2)
    rfc.setting_data_mobile()
    time.sleep(2)
    #rfc.save_rfc()
    #time.sleep(4)
    rfc.cerrar_sesion()
    time.sleep(2)
    rfc.close_page()`

o ejecutar la función main().

Así también si se quiere buscar un RFC, se puede ejecutar la función main_search(), donde se solicitará vía terminal el id del RFC y se configurará en modo visible, si se requiere utilizar el modo invisible, sólo se debe cambiar el atributo `headless` a `True` y volver a ejecutar.