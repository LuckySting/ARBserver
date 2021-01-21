import asyncio
from app.models import DishModel, FileModel, RestaurantModel, PlaceModel, PlaceGalleryModel, TableModel
from app.settings import current_settings

from tortoise import Tortoise


async def fill_mock_data():
    db = Tortoise()
    try:
        await db.init(config=current_settings.get_tortoise_orm_config())
        await asyncio.gather(RestaurantModel.all().delete(), DishModel.all().delete(), FileModel.all().delete(),
                             PlaceModel.all().delete(), TableModel.all().delete(), PlaceGalleryModel.all().delete())
        rest_img = await FileModel.create(path='/static/rests/bob/rest.jpg')
        dish_img = await FileModel.create(path='/static/rest/bob/dish.jpg')
        table_img = await FileModel.create(path='/static/rest/bob/table.jpg')
        gallery_img = await FileModel.create(path='/static/rest/bob/gallery.jpg')
        rest = await RestaurantModel.create(name='Закусочная у Боба', image=rest_img,
                                            description='Лучшая закусочная рядом с тобой')
        await DishModel.create(name='Шаурма', price=220, restaurant=rest, image=dish_img)
        await DishModel.create(name='Двойная шаурма', price=280, restaurant=rest, image=dish_img, sale=True,
                               sale_price=240)

        place = await PlaceModel.create(address='Коломяжский пр., 28 корпус 3, Санкт-Петербург',
                                        longitude=60.0092013,
                                        latitude=30.2939209,
                                        work_time='10:00 - 23:00',
                                        restaurant=rest
                                        )
        await PlaceGalleryModel.create(place=place, file=rest_img)
        await PlaceGalleryModel.create(place=place, file=gallery_img)
        await PlaceGalleryModel.create(place=place, file=gallery_img)
        await TableModel.create(name='Столик у окна', capacity=6, place=place, image=table_img)
    finally:
        await db.close_connections()


if __name__ == '__main__':
    asyncio.run(fill_mock_data())
