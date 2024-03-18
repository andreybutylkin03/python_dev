import asyncio
import shlex

async def echo(reader, writer):
    while data := await reader.readline():
        a = shlex.split(data.decode(), False, False)

        if len(a) > 1 and a[0] == 'print':
            writer.write(shlex.join(a[1:]).encode() + b'\n')
        if len(a) > 1 and a[0] == 'info':
            address, port = writer.get_extra_info('peername')
            if a[1] == 'port':
                writer.write(str(port).encode() + b'\n')
            else:
                writer.write(str(address).encode() + b'\n')
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(echo, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
