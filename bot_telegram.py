from telethon import TelegramClient, events
import asyncio

api_id = 23198863  
api_hash = 'a77bc2693b80c383c25a2c0132e861ee'
phone = '+34684279659' 

source = -1002272368383 
target = -1003254874208 
topic_id = 1

async def main():
    client = TelegramClient('session', api_id, api_hash)
    await client.start(phone=phone)

    @client.on(events.NewMessage(chats=source))
    async def handler(event):
        # Envía el mensaje nuevo al canal/grupo de destino
        await client.send_message(target, event.message)

    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())

async def handler(event):
    print("Mensaje recibido:", event.message.text)
   



