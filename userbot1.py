from pyrogram import Client
import asyncio

api_id = 'api_id'
api_hash = 'api_hash'



async def main():
    async with Client("my_account", api_id=api_id, api_hash=api_hash) as app:
        bot_username = "@kstatkz_bot"

        while True:
            # Отправляем сообщение боту
            message_text = 'привет'
            await app.send_message(bot_username, message_text)

            # Ждем ответа от бота
            async for message in app.get_chat_history(bot_username):
                if message.from_user.is_bot:
                    print("Ответ от бота:", message.text)
                    break  # Завершаем цикл после получения ответа


asyncio.run(main())