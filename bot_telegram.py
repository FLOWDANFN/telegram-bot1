from telethon import TelegramClient, events
import asyncio

api_id = 23198863  
api_hash = 'a77bc2693b80c383c25a2c0132e861ee'
phone = '+34684279659' 

source = -1003134180851 
target = -1003254874208 
topic_id = 2

import re

def adaptar_mensaje(mensaje):
    tipo = "Long" if "LONG" in mensaje.upper() else "Short"
    simbolo = re.search(r'(BTC|ETH|XRP|BNB|SOL)', mensaje.upper())
    simbolo = simbolo.group(0) if simbolo else 'BTC'
    entradas = re.findall(r'Entrada\d?:\s?(\d+)', mensaje)
    tps = re.findall(r'TP\d?:\s?(\d+)', mensaje)
    sl = re.findall(r'SL:\s?(\d+)', mensaje)

    if entradas:
        entrada_min = min([int(e) for e in entradas])
        entrada_max = max([int(e) for e in entradas])
        rango_entrada = f"{entrada_max} - {entrada_min}"
    else:
        rango_entrada = "N/A"

    texto = (
        f"#{simbolo}/USDT\n"
        f"Exchanges: Bitget Futures\n"
        f"Signal Type: Regular ({tipo})\n"
        f"Leverage: Isolated (20X)\n"
        f"Entry Zone:\n"
        f"{rango_entrada}\n"
        f"Take-Profit Targets:\n"
    )
    for i, tp in enumerate(tps, start=1):
        texto += f"{i}) {tp}\n"
    texto += "Stop Targets:\n"
    for i, s in enumerate(sl, start=1):
        texto += f"{i}) {s}\n"

    return texto


async def main():
    client = TelegramClient('session', api_id, api_hash)
    await client.start(phone=phone)

    @client.on(events.NewMessage(chats=source))
    async def handler(event):
        mensaje = event.message.message  # Extrae el texto original
        señal_adaptada = adaptar_mensaje(mensaje)  # Adapta el texto
        await client.send_message(target, señal_adaptada)  # Lo envía adaptado


    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
