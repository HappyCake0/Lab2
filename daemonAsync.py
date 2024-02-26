import asyncio, socket
import json

with open("daemonConfig.json", "r") as j:
    cfg = json.loads(j.read())
async def handle_client(client, address):
    loop = asyncio.get_event_loop()
    response = 'OK'
    try:
        request = (await loop.sock_recv(client, cfg['buffer_size'])).decode('utf8')
        with open(f'{cfg["path"]}/{address}.txt', 'w') as f:
            f.write(request)
    except IOError:
        response = 'Не удается записать отправленне Вами данные. Ошибка файловой системы.'
    except BaseException:
        response = f'Слишком длинное сообщение. Буфер составляет {cfg["buffer_size"]}'

    await loop.sock_sendall(client, response.encode('utf8'))
    client.close()

async def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((cfg['address'], cfg["port"]))
    server.listen(cfg['max_connections'])
    server.setblocking(False)

    loop = asyncio.get_event_loop()

    while True:
        client, address = await loop.sock_accept(server)
        loop.create_task(handle_client(client, address))

asyncio.run(run_server())