import socket 
import threading
import os

host = '127.0.0.1'
port =  8000

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1)
serversocket.bind((host , port))
serversocket.listen(1)
print('servidor en el puerto',port)

while True:
    print("-----------------------------------")
    connection , address = serversocket.accept()
    request = connection.recv(1024).decode('utf-8')
    print(request)
    try:
        string_list = request.split(' ')
        method = string_list[0]
        requesting_file = string_list[1]
    except:
        string_list = request.split(' ')
        method = string_list[0]
        requesting_file = string_list[0]

    print('Client request',method ,requesting_file)
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

    except Exception as e:
        print("-")
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html><body>Error 404: File not found</body></html>'.encode('utf-8')
    

    final_response = header.encode('utf-8')
    final_response += response
    connection.send(final_response)
    connection.close()