async def new_user_logging(user_id, username, first_name):
    from bot.config import bot, ADMIN_ID # todo: move imports
    message_text = f"❗️<b>New user: </b><a href='tg://user?id={user_id}'>{first_name}</a> @{username}"
    await bot.send_message(chat_id=ADMIN_ID, text=message_text)
