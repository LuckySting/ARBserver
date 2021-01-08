import asyncio
from app.models import DishModel, FileModel, RestaurantModel, PlaceModel, PlaceGallery
from app.settings import current_settings

from tortoise import Tortoise


async def fill_mock_data():
    db = Tortoise()
    try:
        await db.init(config=current_settings.get_tortoise_orm_config())
        rest_count = await RestaurantModel.all().count()
        if rest_count == 0:
            image = await FileModel.create(path='/static/rests/bob/asdf1f13.jpg')
            img2 = await FileModel.create(path='static/rest/bob/dishes/sa1fsdf.png')
            img3 = await FileModel.create(path='static/rest/bob/dishes/fkapsdkfpbn1fsdf.png')
            img4 = await FileModel.create(path='static/rest/bob/dishes/bf1fsdf.png')
            rest = await RestaurantModel.create(name='Закусочная у Боба', image=image,
                                                description='Лучшая закусочная рядом с тобой')
            await DishModel(name='Оливье', price=180, restaurant=rest, image=img2)
            await DishModel(name='Шаурма', price=220, restaurant=rest, image=img3)
            await DishModel(name='Двойная шаурма', price=280, restaurant=rest, image=img4, sale=True, sale_price=240)
    finally:
        await db.close_connections()


if __name__ == '__main__':
    asyncio.run(fill_mock_data())
