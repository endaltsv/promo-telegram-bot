from sqlalchemy import select, update

from bot.database.models.Setting import Setting
from bot.database.database_config import async_session


async def get_settings():
    """
    Retrieves the settings from the database.

    :return: The settings object if found, otherwise None.
    """
    async with async_session() as session:
        stmt = select(Setting).where(Setting.id == 1)
        result = await session.execute(stmt)
        settings = result.scalars().first()
        if settings:
            return settings


async def update_welcome_text(new_text):
    """
    Updates the welcome text in the settings.

    :param new_text: The new welcome text to set.
    :return: None
    """
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(Setting).
                where(Setting.id == 1).
                values(start_message=new_text)
            )
        await session.commit()


async def update_support_id(new_support_id):
    """
    Updates the support ID in the settings.

    :param new_support_id: The new support ID to set.
    :return: None
    """
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(Setting).
                where(Setting.id == 1).
                values(support_id=new_support_id)
            )
        await session.commit()
