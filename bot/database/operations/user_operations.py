from sqlalchemy.future import select

from bot.admin.admin_notifications import new_user_logging
from bot.database.models.User import User
from bot.database.database_config import async_session


async def add_or_update_user(user_id: int, username: str, first_name: str, last_message: int = None):
    """
    Adds a new user or updates an existing one if they already exist in the database.

    :param first_name:
    :param user_id: The ID of the user.
    :param username: The new username of the user.
    :param last_message: The last message sent by the user.
    :return: None
    """
    async with async_session() as session:

        stmt = select(User).filter_by(user_id=user_id)
        result = await session.execute(stmt)
        user = result.scalars().first()

        if user:
            if user.username != username or user.last_message != last_message:
                user.username = username
                user.last_message = last_message
                await session.commit()
                return
        else:
            await new_user_logging(user_id=user_id, username=username, first_name=first_name)
            new_user = User(user_id=user_id, username=username, last_message=last_message)
            session.add(new_user)
            await session.commit()
            return


async def get_all_users():
    """
    Retrieves all users from the database.

    :return: A list of all users.
    """
    async with async_session() as session:
        stmt = select(User)
        result = await session.execute(stmt)
        users = result.scalars().all()
        return users


async def get_user_by_id(user_id: int):
    """
    Retrieves a user by their ID from the database.

    :param user_id: The ID of the user to retrieve.
    :return: The user object if found, otherwise None.
    """
    async with async_session() as session:
        stmt = select(User).filter_by(user_id=user_id)
        result = await session.execute(stmt)
        user = result.scalars().first()

        if user:
            return user


async def get_last_message_by_user_id(user_id: int):
    """
    Retrieves the last message sent by a user from the database.

    :param user_id: The ID of the user.
    :return: The last message sent by the user if found, otherwise None.
    """
    async with async_session() as session:
        stmt = select(User).filter_by(user_id=user_id)
        result = await session.execute(stmt)
        user = result.scalars().first()

        if user:
            return user.last_message


async def get_language_by_user_id(user_id: int):
    """
    Retrieves the language preference of a user from the database.

    :param user_id: The ID of the user.
    :return: The language preference of the user if found, otherwise None.
    """
    async with async_session() as session:
        stmt = select(User).filter_by(user_id=user_id)
        result = await session.execute(stmt)
        user = result.scalars().first()

        if user:
            return user.language


async def update_language_by_user_id(user_id: int):
    """
    Updates the language preference of a user in the database.

    :param user_id: The ID of the user.
    :return: None
    """
    async with async_session() as session:

        stmt = select(User).filter_by(user_id=user_id)
        result = await session.execute(stmt)
        user = result.scalars().first()

        if user:
            if user.language == 'ru':
                user.language = 'en'

            elif user.language == 'en':
                user.language = 'ru'
            await session.commit()
            return
