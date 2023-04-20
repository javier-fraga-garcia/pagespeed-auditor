## PageSpeed Auditor

Este script permite automatizar la realización de auditorías de **WebVitals** en un gran número de páginas.

#### Requisitos previos

1. Es necesario disponer de una clave que permita hacer peticiones a la API de PageSpeed. Para obtener dicha clave se recomienda seguir las instrucciones de la documentación de Google. Se pueden consultar en este [enlace](https://developers.google.com/speed/docs/insights/v5/get-started#APIKey). Una vez que se ha obtenido la clave, se recomienda añadirla en un archivo *.txt* para su uso durante la ejecución del script. En la carpeta `examples` se aporta un ejemplo para comprobar la estructura que debe tener el archivo.

2. Tener una lista de URLs que se quieren auditar. Se aporta en la carpeta `examples` un ejemplo con la estructura que debe tener este archivo. Como el archivo de las URLs puede haberse obtenido mediante *web scraping* u otros medios y puede contener URLs de sitios que no interese obtener o URLs con una estructura no adecuada, el código del script realiza ciertas validaciones:
    * Elimina los espacios en blanco
    * Elimina las URLs duplicadas
    * Se necesita enviar el argumento `domain` para asegurarse de que solamente se auditan las URLs del sitio objetivo

3. Tener instalado **Python** y haber instalado las dependencias necesarias para la ejecución del script. Este último paso puede hacerse mediante la ejecución del comando `pip install -r requirements.txt`.

#### Ejecución y argumentos del script

Para ejecutar el script es necesario utilizar el comando `py main.py` seguido de los argumentos necesarios para el correcto funcionamiento del programa. Estos argumentos son:

* `-u`, `--url`: *(obligatorio)* la ruta al archivo que contiene las URLs que se desea auditar. Ejemplo: `C:\Users\user\Desktop\urls-to-audit.txt`
* `-k`, `--key`: *(obligatorio)* la ruta al archivo que contiene la clave API de PageSpeed. Ejemplo: `C:\Users\user\Desktop\api-key.txt`.
* `-s`, `--strategy`: *(obligatorio)* el dispositivo en el que se desea realizar la auditoría. Opciones posibles &rarr; (desktop, mobile).
* `-r`, `--result`: *(obligatorio)* el nombre del archivo en el que se almacenarán los resultados. El nombre debe ir sin extensión. Ejemplo: `audit-res-mobile`, también se puede indicar una ruta en caso de que se quiera que el script almacene el archivo en una carpeta determinada `C:\Users\user\desktop\data\audit-res-mobile`
* `-p`, `--parallel`: *(opcional)* si se desea que las auditorías se realicen en varios hilos. Se recomienda en casos en que haya muchas URLs para auditar y el proceso se alargue demasiado. Por defecto está en `False`.
* `-h`, `--help`: da acceso a un menú de ayuda con toda esta información.

Comandos de ejemplo:

`py main.py -u C:\Users\user\Desktop\urls-to-audit.txt -k C:\Users\user\Desktop\api-key.txt -s mobile -d https://www.example.com -r C:\Users\user\desktop\data\audit-res-mobile`

En caso de querer una ejecución multihilo para el caso anterior simplemente se añadiría el parámetro `-c`

`py main.py -u C:\Users\user\Desktop\urls-to-audit.txt -k C:\Users\user\Desktop\api-key.txt -s mobile -d https://www.example.com -r C:\Users\user\desktop\data\audit-res-mobile -c`

#### Reporte de resultados

Conforme se vayan realizando las auditorías se irá generando una traza de como va el proceso. Una vez finalizado se generará un archivo *.csv* con los resultados. Las información sobre qué significa cada métrica y cómo interpretar los resultados se puede consultar en las siguientes páginas.

* [Documentación de PageSpeed Insights](https://developers.google.com/speed/docs/insights/v5/about)
* [Get Started PageSpeed API](https://developers.google.com/speed/docs/insights/v5/get-started?hl=es-419)
* [Referencia de métricas de PageSpeed API](https://developers.google.com/speed/docs/insights/v5/reference/pagespeedapi/runpagespeed?hl=es-419)
* [Documentación de Lighthouse](https://developer.chrome.com/docs/lighthouse/)

#### Versión con interfaz de usuario

Se ha creado una versión de este script en [Google Colab](https://colab.research.google.com/) para que funcione a modo de interfaz de usuario. El cuaderno es público y accesible desde este [enlace](https://colab.research.google.com/github/javier-fraga-garcia/pagespeed-auditor/blob/main/notebooks/PageSpeed_Auditor.ipynb).