from telethon import TelegramClient, events,Button
from telethon.tl.types import ChannelParticipantsAdmins
import os
import sqlite3
import asyncio

api_id = YOUR_API_ID
api_hash = 'YOUR_API_HASH'
bot_token = 'YOUR_BOT_TOKEN'

button3 = Button.url('➕ 𝐌𝐞𝐧𝐢 𝐐𝐫𝐮𝐩𝐚 𝐞𝐥𝐚𝐯𝐞 𝐞𝐭 ➕','https://t.me/Enotagbot?startgroup=true')
button2 = Button.url('𝐊𝐎𝐌𝐄𝐊 📡', 'https://t.me/Enobots/23')
button1 = Button.url('𝐒𝐀𝐇𝐈𝐁𝐈𝐌 👨🏻‍💻', 'http://t.me/ltfl_elvin')


client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

class FlagContainer:
    is_active = False
      
@client.on(events.NewMessage(pattern='/tag (.+)'))
async def etiketle(event):
    is_admin = False
    async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
        if admin.id == event.sender_id:
            is_admin = True
            break
    if not is_admin:
        await event.respond('🤓 Sən bir admin deyilsən!')
        return
    if len(event.pattern_match.group(1)) == 0:
        await event.respond('tag üçün bir mesaj yazın.')
        return
    FlagContainer.is_active = True
    chat = await event.get_input_chat()
    participants = await client.get_participants(chat)
    tag_message = event.pattern_match.group(1)
    for i in range(0, len(participants), 1):
        if not FlagContainer.is_active:
            break
        tags = [f"[{tag_message}](tg://user?id={user.id})" for user in participants[i:i+1]]
        await client.send_message(chat, " ".join(tags))
        await asyncio.sleep(1.3)

@client.on(events.NewMessage(pattern='/tagf (.+)'))
async def etiketle(event):
    is_admin = False
    async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
        if admin.id == event.sender_id:
            is_admin = True
            break
    if not is_admin:
        await event.respond('🤓 Sən admin deyilsən!')
        return
    if len(event.pattern_match.group(1)) == 0:
        await event.respond('Tag üçün bir mesaj yazın.')
        return
    FlagContainer.is_active = True
    chat = await event.get_input_chat()
    participants = await client.get_participants(chat)
    tag_message = event.pattern_match.group(1)
    for i in range(0, len(participants), 1):
        if not FlagContainer.is_active:
            break
        tags = [f"[{tag_message}](tg://user?id={user.id})" for user in participants[i:i+5]]
        await client.send_message(chat, " ".join(tags))
        await asyncio.sleep(1.3)
  


@client.on(events.NewMessage(pattern="/dayan"))
async def etikleme_islemi_durdur(event):
    is_admin = False
    async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
        if admin.id == event.sender_id:
            is_admin = True
            break
    if not is_admin:
        return
    FlagContainer.is_active = False
    await event.reply("**ㅤ\n🚫 tag prosesi dayandırıldı**\nㅤ",buttons = [button3])
      

database_file = 'chats.db'

if not os.path.exists(database_file):
    conn = sqlite3.connect(database_file)
    conn.execute('''CREATE TABLE chats (chat_id INTEGER PRIMARY KEY)''')
    conn.commit()
    conn.close()

@client.on(events.NewMessage(pattern='/reyting'))
async def get_active_chats(event):
    if event.sender.username == 'ltfl_elvin':
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()
        cursor.execute('''SELECT COUNT(*) FROM chats''')
        total_chats = cursor.fetchone()[0]
        cursor.execute('''SELECT COUNT(*) FROM chats WHERE chat_id < 0''')
        total_groups = cursor.fetchone()[0]
        total_private_chats = total_chats - total_groups
        message = f"👤 Özəl Söhbətlər: {total_private_chats}\n👥 Qrup Söhbətlər: {total_groups}"
        await event.respond(message)
        conn.close()

@client.on(events.NewMessage())
async def save_chat_id(event):
    chat_id = event.chat_id
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    cursor.execute('''INSERT OR IGNORE INTO chats (chat_id) VALUES (?)''', (chat_id,))
    conn.commit()
    conn.close()

@client.on(events.ChatAction)
async def remove_chat_id(event):
    chat_id = event.chat_id
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM chats WHERE chat_id = ?''', (chat_id,))
    conn.commit()
    conn.close()

@client.on(events.NewMessage(pattern='/reklam'))
async def send_message_to_all_chats(event):
    if event.sender.username == 'ltfl_elvin':
        if event.is_reply and event.message.reply_to_msg_id:
            reply_msg = await event.get_reply_message()
            if reply_msg.media:
                message = reply_msg.message or ''
                conn = sqlite3.connect('chats.db')
                cursor = conn.cursor()
                cursor.execute('SELECT chat_id FROM chats')
                chat_ids = [row[0] for row in cursor.fetchall()]
                for chat_id in chat_ids:
                    try:
                        await client.send_file(chat_id, reply_msg.media, caption=message)
                    except Exception as e:
                        print(f'Error sending message to chat_id {chat_id}: {str(e)}')
                conn.close()
            elif reply_msg.text:
                message = reply_msg.text.strip()
                conn = sqlite3.connect('chats.db')
                cursor = conn.cursor()
                cursor.execute('SELECT chat_id FROM chats')
                chat_ids = [row[0] for row in cursor.fetchall()]
                for chat_id in chat_ids:
                    try:
                        await client.send_message(chat_id, message)
                    except Exception as e:
                        print(f'Error sending message to chat_id {chat_id}: {str(e)}')
                conn.close()
            else:
                print('The message cannot be empty unless a file is provided.')
              
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('**Salamm. mən Tagger 🤖 \n\nQruplarda tək-tək və 5-5 tağ edə bilen botam 🛷\n\n⁉️ Necə istifadə edəcəyinizi öyrənmək üçün aşağıdakı kömək düyməsinə tıklayın**', buttons=[[button1, button2] , [button3]]) 


client.run_until_disconnected()
