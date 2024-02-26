import socket


file_name = input("Введите имя файла: ")
try:
    with open(file_name, 'r') as f:
        data = f.read()
except BaseException:
    print("Файл отсутствует или имеет некорректное содержание.")
    exit(1)

server_address = input("Введите адресс сервера в формате <ip:port> : ").split(":")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = server_address[0]
if len(server_address) < 2:
    port = 8686
else:
    port = server_address[1]
try:
    client.connect((ip, int(port)))
except BaseException:
    print(f"Не удается подключиться по {ip}:{port}")
    exit(1)

client.send(bytes(data, encoding='UTF-8'))
server_response = client.recv(1024)
print(str(server_response, encoding="utf-8"))
