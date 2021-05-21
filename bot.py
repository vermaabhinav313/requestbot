from telethon.tl.types import ChannelParticipantsAdmins
from telethon.utils import get_display_name
from telethon import *
import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

IN_GRP = -1001395532797

REQ_GO = -1001264185629

api_id = 908950
api_hash = 'b3d97d5998f10a88c87650b28e96d92f'
bot_token = "1895968093:AAGCLiKFlh8aJp-tBLsJ2tN2aboQ6C4qYH8"

asst = TelegramClient('anon', api_id, api_hash).start(bot_token=bot_token)
bot = asst

auth = [1613301947, 1270604313, 1132363465, 1380685014, 1779623655]

@asst.on(events.NewMessage(chats=IN_GRP))
async def filter_requests(event):
    if event.fwd_from:
        return
    if "#request" in event.text:
        if (event.reply_to_msg_id):
            msg = (await event.get_reply_message()).message
        else:
            msg = event.text
        try:
            sender = event.sender
            if sender.bot:
                return
            if not sender.username:
                user = f"[{get_display_name(sender)}](tg://user?id={event.sender_id})"
            else:
                user = "@" + str(sender.username)
        except BaseException:
            user = f"[User](tg://user?id={event.sender_id})"
        chat_id = (str(event.chat_id)).replace("-100", "")
        username = ((await bot.get_entity(REQ_GO)).username)
        x = await asst.send_message(REQ_GO,
                                f"**Request By {user}**\n\n{msg}",
                                buttons=[
                                    [Button.url("Go to Message", url=f"https://t.me/c/{chat_id}/{event.message.id}"),
                                    Button.inline("Unavailable", data="reqdelete")
                                ],[Button.inline("Done", data="isdone")]])
        await event.reply("Your request has been submitted!", buttons=[Button.url("View", url=f"https://t.me/{username}/{x.id}")])
        if not auth:
            async for x in bot.iter_participants("@anime_chat_ocean", filter=ChannelParticipantsAdmins):
                auth.append(x.id)
    

@asst.on(events.callbackquery.CallbackQuery(data="reqdelete"))
async def delete_message(event):
    if not auth:
        async for x in bot.iter_participants("@anime_chat_ocean", filter=ChannelParticipantsAdmins):
             auth.append(x.id)
    if event.sender_id in auth:
        x = await bot.get_messages(event.chat_id, ids=event.message_id)
        xx = x.raw_text
        await event.edit(f"~~{xx}~~", buttons=[Button.inline("❌ Request Unavailable ❌", data="ndone")])
    else:
        await event.answer("This is for admins/mainainers only.", alert=True, cache_time=0)
        
        
@asst.on(events.callbackquery.CallbackQuery(data="isdone"))
async def isdone(e):
    if not auth:
        async for x in bot.iter_participants("@WeebGalaxy", filter=ChannelParticipantsAdmins):
             auth.append(x.id)
    if e.sender_id in auth:
        x = await bot.get_messages(e.chat_id, ids=e.message_id)
        xx = x.raw_text
        await e.edit(f"~~{xx}~~", buttons=[Button.inline("✅Request Completed✅", data="donne")])
    else:
        await e.answer("This is for admins/mainainers only. You are not one. Go Back!!!", alert=True, cache_time=0)
        
    
@asst.on(events.callbackquery.CallbackQuery(data="donne"))
async def ans(e):
    await e.answer("This Request is completed check out channels 😁😁", alert=True, cache_time=0)
        
        
@asst.on(events.callbackquery.CallbackQuery(data="ndone"))
async def ans(e):
    await e.answer("Sorry, This Requested Anime Is Not Available.", alert=True, cache_time=0)
        
asst.start()
print("Bot Started")
asst.run_until_disconnected()
