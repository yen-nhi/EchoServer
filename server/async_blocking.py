import asyncio
import socket
from settings import SERVER_HOST, SERVER_PORT


async def read_data(reader, writer):
    while True:
        data = await reader.read(255)
        if not data:
            break
        addr = writer.get_extra_info('peername')
        print(f'Received {data.decode()} from {addr}')
        writer.write(data)
        await writer.drain()

async def run_socket():
   server = await asyncio.start_server(read_data, SERVER_HOST, SERVER_PORT)
   async with server:
       await server.serve_forever()



if __name__ == '__main__':
    asyncio.run(run_socket())
