Documento PDF: [Documentación del servidor web.pdf](https://github.com/cpalacior/TelematicWebServer/files/11300256/Documentacion.del.servidor.web.pdf)

Telematics Web Server (TWS)


Integrantes del equipo:

- Camilo Palacio Restrepo
- Maria Paulina Lopez Salazar
- Víctor Manuel Botero Gómez


1. Introducción

Los servidores tienen como función principal ofrecer sus recursos o servicios para así responder de una manera oportuna y eficiente a las solicitudes de uno o varios clientes en la red. Su utilidad se fundamenta en el almacenamiento de archivos, datos o recursos que son transmitidos según la demanda del cliente, en este proyecto se ha desarrollado un servidor web en Python que considera los siguientes aspectos:

Implementación de métodos HTTP como GET, HEAD y POST. cada uno con su respectivo análisis en el numeral 2 (Desarrollo) y con su evidencia de casos de prueba en el hipertexto del servidor web.

Manejo robusto de errores y sus excepciones correspondientes enviadas al cliente, entre estos se soporta el caso 200 (serie 200 orientada al éxito de procesamiento de la petición y retorno de respuestas al cliente), y el error 400 y 404 (Serie 400 orientada al fallo de procesamiento de solicitudes del cliente).

Implementación del concepto logger con el fin de visualizar tanto las peticiones entrantes a nivel HTTP como respuestas del servidor hacia el cliente.

Manejo en la página web de imágenes, hipertextos y archivos de aproximadamente 1MB de tamaño para las peticiones del usuario, así mismo se garantiza mediante los hilos la disponibilidad para ejecutar tareas concurrentes en el tiempo.

En este informe documentado se hace énfasis en la composición del código del servidor y sus funcionalidades detallando a su vez como el HTML de la aplicación permite acceder a los diversos métodos (GET,HEAD, POST) para probar el intercambio de recursos tanto a manera individual como múltiple.





2. Desarrollo

Para el desarrollo del servidor se ha utilizado el lenguaje de programación Python, el detalle del desarrollo se presenta a continuación:

Este código es un servidor web que según la definición de la variable port, escucha en el puerto 80 de la dirección IP interna ‘172.31.93.217’ otorgada por el despliegue definida en la variable host. El servidor acepta conexiones entrantes y maneja solicitudes HTTP GET, HEAD y POST. 

El código comienza importando el módulo "socket" para la comunicación en red, "threading" para los multihilos (lo que garantiza la disponibilidad del servidor) y “os” para el acceso a los archivos, y al sistema operativo en sí.

import socket 
import threading
import os

Luego se define el host y el puerto en el que el servidor escuchará.

host = '172.31.93.217'
port =  80

A continuación, se crea un objeto de socket llamado "serversocket" con la función "socket.socket()" y se configura con las opciones "socket.SO_REUSEADDR" y "socket.AF_INET".
Se establece la opción "socket.SO_REUSEADDR" para permitir que se vuelva a utilizar la misma dirección local en caso de que se cierre el socket anteriormente. "socket.AF_INET" indica que se utilizará IPv4 para la comunicación.

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1)

Después de configurar el área del socket, este se enlaza a la dirección IP y el puerto que se ha definido previamente mediante la función "serversocket.bind()". 

serversocket.bind((host , port))

Se establece el número máximo de conexiones entrantes que el servidor aceptará mediante la función "serversocket.listen()".

serversocket.listen(1)
print('servidor en el puerto',port)

Además, se establece un tiempo de espera de 60 segundos, lo que indica que si no se recibe ninguna actividad en el servidor, la función de escucha se interrumpirá y enviará una excepción.
 
serversocket.settimeout(60.0) 

Luego, se entra en un bucle infinito que acepta conexiones entrantes con la función "serversocket.accept()".

while True:
    connection , address = serversocket.accept()

Cuando se recibe una solicitud de conexión, se decodifica la solicitud entrante en formato UTF-8 y se almacena en la variable "request". 

    request = connection.recv(1024).decode('utf-8')
    print(request)

Luego, se divide la solicitud en una lista de cadenas utilizando el espacio como un delimitador de separación, seguidamente se accede a los elementos de la lista para extraer el método y el nombre del archivo que está siendo solicitado.

    try:
        string_list = request.split(' ')
        method = string_list[0]
        requesting_file = string_list[1]
    except:
        string_list = request.split(' ')
        method = string_list[0]
        requesting_file = string_list[0]

El servidor admite solicitudes HTTP GET, HEAD y POST.

print('Client request',method ,requesting_file)

Si la solicitud es una solicitud POST y contiene la palabra "firstname", el servidor almacena el nombre y el apellido del usuario, previamente enviado por medio de un formulario, en un archivo de texto llamado "archivoDeNombres.txt" que se encuentra en la carpeta del proyecto.

    if method == "POST":
        if request.find("firstname") != -1:
            nombre_completo = request[request.find("firstname"):len(request)]
            nombre_completo = nombre_completo.split("&")
            datos = ""
            with open("archivoDeNombres.txt", "r") as file:
                datos = file.read()
                file.close()
            with open("archivoDeNombres.txt", "w") as file:
                file.write( datos + "\n"+ nombre_completo[0] + " " +nombre_completo[1])
                file.close()

Si la solicitud es una solicitud HEAD, se verifica si la petición se encuentra en el sistema de archivos, si esto es afirmativo se establece el encabezado de la respuesta como exitosa, si no se establece la respuesta como fallida, y se envía a una página de error.

   if method == "HEAD":
        if os.path.isfile(os.getcwd() + requesting_file):
            response = 'HTTP/1.1 200 OK\n'
        else:
            response = '<html><body>Error 404: File not found</body></html>'.encode('utf-8')

Si la solicitud es una solicitud GET, se verifica que el archivo solicitado esté presente en la solicitud, si se encuentra una cadena vacía se establece el ‘index.html’ como archivo a solicitar, luego, se lee el archivo, se determina el tipo de contenido y se obtiene una respuesta.

myfile = requesting_file.split('?')[0]
    myfile = myfile.lstrip('/')
    if(myfile == ''):
        myfile = 'index.html'

    try:
        file = open(myfile , 'rb')
        response = file.read()
        try:
            file_lenght = os.stat(myfile)
            file_lenght=file_lenght.st_size
            response += bytes(file_lenght)
        except Exception as error:
            print(error)
        file.close()

        header = 'HTTP/1.1 200 OK\n'

Además, se establece el encabezado de la respuesta según el tipo de archivo solicitado. Si el archivo es una imagen, se establece el tipo de contenido en "image/jpg". Si es un archivo CSS, el tipo de contenido se establece en "text/css". Si es un archivo PDF, el tipo de contenido se establece en "application/pdf". Si es un archivo de documento de Microsoft Word, el tipo de contenido se establece en "application/docx". Si es cualquier otro tipo de archivo, se establece el tipo de contenido en "text/html".

        if(myfile.endswith('.jpg')):
            mimetype = 'image/jpg'
        elif(myfile.endswith('.css')):
            mimetype = 'text/css'
        elif(myfile.endswith('.pdf')):
            mimetype = 'application/pdf'
        elif(myfile.endswith('.docx')):
            mimetype = 'application/docx'
        elif(myfile.endswith('.exe')):
            mimetype = 'application/exe'
        else:
            mimetype = 'text/html'

        header += 'Content-Type: '+str(mimetype)+'\n\n'

Si no se encuentra el archivo, se devuelve un mensaje de error HTTP 404.

    except Exception as e:
        print("-")
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html><body>Error 404: File not found</body></html>'.encode('utf-8')

Finalmente, el servidor crea la respuesta HTTP para enviarla al cliente a través de la conexión establecida y se cierra la conexión con el cliente para liberar los recursos.

   final_response = header.encode('utf-8')
    final_response += response
    connection.send(final_response)
    connection.close()
	
Además del desarrollo de este servidor, se ha realizado la respectiva interfaz de aplicación. Esta se puede encontrar en el archivo “index.html”.	 Este es un código HTML en el que se define la estructura y el contenido de la página web del servidor (este contenido obedece principalmente a las pruebas y requisitos solicitados en el entregable para validar el funcionamiento del servidor desarrollado). 

Algunos elementos que se pueden destacar son:

La sección header contiene información sobre la página, como el título, metadatos y enlaces a archivos CSS y JS.
El elemento body contiene el contenido visible de la página, incluyendo una barra de navegación (nav) y varias secciones que contienen listas de imágenes (ul) y formularios (form) para recopilar información del usuario.
Se utilizan clases y estilos para dar formato al contenido, por ejemplo, se define un estilo para establecer el borde de todos los elementos en la página y se usan clases como "waves-effect" y "waves-light" para añadir mejorar el aspecto visual de los botones.
También se tiene código de JavaScript en la página. Este se encarga de descargar un archivo al hacer clic en el botón "Installar documento word" (InstallButton) para cumplir con el requisito del Caso 3: Página web que contiene un solo archivo de aproximadamente un tamaño de 1MB.


3. Despliegue y pruebas del servidor

Después de haber creado y conectado la instancia en aws, se accede a la consola y se instala ‘git’ y ‘Python’, seguido de esto se ejecutan las siguientes instrucciones:

1. git clone https://github.com/cpalacior/TelematicWebServer.git

2. cd TelematicWebServer

3. sudo su

4. python3 servidorweb.py

![MicrosoftTeams-image (5)](https://user-images.githubusercontent.com/83301681/233762094-ea790f8c-e06b-4709-a484-aed7fe138b38.png)

Lo primero que se debe realizar es clonar el repositorio git https://github.com/cpalacior/TelematicWebServer.git seguido a esto, se ingresa a la carpeta creada a partir de la clonacion anterior copiando el comando sudo su  con el fin de ingresar como super usuarios para adquirir todos los permisos, finalmente se corre el codigo de python y en el browser se digita la ip publica del servidor en cuestion.

En la siguiente imagen se puede apreciar una respuesta exitosa del servidor:

![MicrosoftTeams-image (6)](https://user-images.githubusercontent.com/83301681/233762143-b09bd738-c513-48c8-a9a5-df6af1d99e72.png)

Al acceder al servidor mediante la IP correspondiente es posible visualizar la interfaz para el cliente, en esta se puede evidenciar el método GET  descargando documentos de más de 1MB de tamaño, abriendo imágenes de manera simultánea con extensiones .png y/o .jpg.
Caso 4: Página web que contiene múltiples archivos y que aproximadamente tiene un tamaño de 1MB.

![MicrosoftTeams-image (7)](https://user-images.githubusercontent.com/83301681/233762159-16bd625b-5728-4f5e-b2fd-fd4342407a0b.png)

En la aplicación wireshark.org se evidencia el intercambio de archivos bajo el protocolo GET.

![MicrosoftTeams-image (9)](https://user-images.githubusercontent.com/83301681/233762398-dd146f1e-b30d-411e-9b8d-e4d8b537739f.png)

También, se ha creado un formulario con el fin de recolectar datos como el nombre y apellido de una persona para enviarlos en la petición al servidor que se ha desarrollado, de esta manera se puede evidenciar el uso del método POST que envía la información.

![MicrosoftTeams-image (10)](https://user-images.githubusercontent.com/83301681/233762412-05b56c8e-e099-4bdf-9cc1-e0e97260fce6.png)

Para comprobar el funcionamiento correcto de la interfaz del servidor se realiza un envío de una petición en Postman bajo el método HEAD que sirve para  comprobar la existencia o para obtener información sobre la ip de nuestro servidor desplegado.

![MicrosoftTeams-image (11)](https://user-images.githubusercontent.com/83301681/233762427-7915b107-490e-4b12-a3e4-9639393ca062.png)


4. Conclusiones

Los métodos HTTP son herramientas efectivas para la comunicación eficiente y óptima entre el cliente y el servidor, facilitan el intercambio de datos e información a través de la web.Dichos métodos son utilizados para indicar la acción que debe realizarse en un recurso identificado por una URL. Cada método tiene una finalidad específica, destacando en este proyecto los más comunes que son: 

GET: Este método nos sirve para obtener información de un recurso o dato en particular. Cuando se realiza una petición GET, el servidor devuelve una respuesta que contiene la información solicitada.

HEAD: Este método es similar al método GET, con la diferencia de que, el servidor devuelve únicamente la información descriptiva del recurso, dato u objeto. como el tamaño o el tipo de archivo. Este método es útil para comprobar la existencia o para obtener información sobre un archivo sin tener que descargarlo.

POST: Este método se utiliza para enviar información a un servidor. Los datos enviados en una petición POST se incluyen en el cuerpo de la petición, en nuestro caso este método es probado en el formulario de la aplicación del usuario.

Los hilos son importantes en el desarrollo y funcionamiento de un servidor ya que permiten que este maneje de una manera más óptima diversas solicitudes al mismo tiempo, que aproveche al máximo los recursos del sistema, como el procesador y la memoria, al permitir que varias solicitudes se procesan en paralelo, mejore la capacidad de respuesta del servidor y realice múltiples tareas. Esto significa que los clientes pueden recibir respuestas más rápidas a sus solicitudes. Finalmente, los hilos también permiten que un servidor maneje múltiples solicitudes de manera simultánea, lo que mejora el rendimiento general del servidor. En lugar de tener que esperar a que una solicitud se complete antes de procesar la siguiente, el servidor puede manejar varias solicitudes al mismo tiempo.

Un servidor es un equipo informático y tecnológico que ofrece servicios y recursos a otros dispositivos (clientes) a través de una red o de Internet. 

Dicho dispositivo o programa posee grandes ventajas como accesibilidad para que cualquier persona pueda utilizar los servicios que se ofrecen, escalabilidad para manejar una mayor cantidad de tráfico y usuarios, flexibilidad para permitir la  personalización y configuración de las diversas características y herramientas del servidor para adaptarse y encajar con las necesidades específicas del contexto para el que se requiere y finalmente puede garantizar la seguridad, los servidores pueden ser configurados para ofrecer un buen nivel de seguridad y protección contra ataques malintencionados. Esto incluye la implementación de medidas de seguridad como el cifrado de datos y la detección de intrusiones en los que se pueden utilizar diversos protocolos seguros.

Es importante que un servidor mantenga disponibilidad constante, siempre sus servicios deben estar activos y preparados para recibir las solicitudes de los usuarios, procesarlas y entregar resultados sin excepción alguna; incluso si no se llega a encontrar dicha consulta o petición, el servidor debe actuar enviando los códigos de error como lo pueden ser la serie 400 (que significa que no existen los recursos solicitados en su petición). El cliente siempre debe tener una respuesta o retroalimentación a su petición para tomar decisiones.


5. Referencias

https://developer.mozilla.org/es/docs/Web/HTTP/Methods
https://www.fing.edu.uy/tecnoinf/maldonado/cursos/so/material/teo/so05-hilos.pdf
https://realpython.com/python-sockets/#:~:text=Sockets%20and%20the%20socket%20API,own%20connections%20to%20other%20networks.
https://docs.python.org/es/3.8/library/threading.html
https://blog.hubspot.es/website/que-es-servidor-web#:~:text=Los%20servidores%20tienen%20como%20objetivo,a%20la%20informaci%C3%B3n%20que%20resguarda.
https://www.wireshark.org/
https://datatracker.ietf.org/doc/rfc2616/
https://github.com/ST0255/st0255-20231/tree/main/LabSocketsMultiThread
https://docs.aws.amazon.com/es_es/AmazonRDS/latest/UserGuide/CHAP_Tutorials.WebServerDB.CreateWebServer.html



