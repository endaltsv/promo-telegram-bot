from sqlalchemy import delete
from sqlalchemy.future import select

from bot.database.models.Category import Category
from bot.database.models.Setting import Setting
from bot.database.database_config import async_session


async def insert_initial_data():
    try:
        async with async_session() as session:
            async with session.begin():
                init_settings = Setting(id=1, start_message='This start, u can change me')
                session.add(init_settings)

        await session.commit()
    except Exception as e:
        print(e)


async def add_category(category_name: str, text: str):
    """
    Adds a new category to the database.

    :param category_name: The name of the category.
    :param text: The text associated with the category.
    :return: "Category already exists" if the category already exists, otherwise "Category added".
    """
    async with async_session() as session:
        stmt = select(Category).filter_by(category=category_name)
        result = await session.execute(stmt)
        category = result.scalars().first()

        if category:
            return "Category already exists"

        new_category = Category(category=category_name, text=text)
        session.add(new_category)
        await session.commit()
        return "Category added"


async def get_category_by_id(category_id: int):
    """
    Retrieves a category by its ID from the database.

    :param category_id: The ID of the category to retrieve.
    :return: The category object if found, otherwise None.
    """
    async with async_session() as session:
        stmt = select(Category).filter_by(id=category_id)
        result = await session.execute(stmt)
        category = result.scalars().first()

        if category:
            return category


async def get_all_categories():
    """
    Retrieves all categories from the database.

    :return: A list of all categories.
    """
    async with async_session() as session:
        stmt = select(Category).where()
        result = await session.execute(stmt)
        categories = result.scalars().all()
        return categories


async def delete_category_by_id(category_id: int):
    """
    Deletes a category by its ID from the database.

    :param category_id: The ID of the category to delete.
    :return: None
    """
    async with async_session() as session:
        async with session.begin():
            stmt = delete(Category).filter_by(id=category_id)
            await session.execute(stmt)
            await session.commit()
