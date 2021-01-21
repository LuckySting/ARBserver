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
        image = await FileModel.create(path='/static/rests/bob/asdf1f13.jpg')
        img2 = await FileModel.create(path='/static/rest/bob/dishes/sa1fsdf.png')
        img3 = await FileModel.create(path='/static/rest/bob/dishes/fkapsdkfpbn1fsdf.png')
        img4 = await FileModel.create(path='/static/rest/bob/dishes/bf1fsdf.bmp')
        img5 = await FileModel.create(path='/static/rest/bob/tables/b3233f.jpeg')
        img6 = await FileModel.create(path='/static/rest/bob/gallery/assd.jpeg')
        img7 = await FileModel.create(path='/static/rest/bob/gallery/ssss.jpeg')
        rest = await RestaurantModel.create(name='Закусочная у Боба', image=image,
                                            description='Лучшая закусочная рядом с тобой')
        await DishModel.create(name='Оливье', price=180, restaurant=rest, image=img2)
        await DishModel.create(name='Шаурма', price=220, restaurant=rest, image=img3)
        await DishModel.create(name='Двойная шаурма', price=280, restaurant=rest, image=img4, sale=True,
                               sale_price=240)

        place = await PlaceModel.create(address='Коломяжский пр., 28 корпус 3, Санкт-Петербург',
                                        longitude=60.0092013,
                                        latitude=30.2939209,
                                        work_time='10:00 - 23:00',
                                        restaurant=rest
                                        )
        await PlaceGalleryModel.create(place=place, file=img6)
        await PlaceGalleryModel.create(place=place, file=img7)
        await TableModel.create(name='Столик у окна', capacity=6, place=place, image=img5)
    finally:
        await db.close_connections()


if __name__ == '__main__':
    asyncio.run(fill_mock_data())
