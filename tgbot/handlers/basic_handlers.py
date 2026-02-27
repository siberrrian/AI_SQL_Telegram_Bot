from aiogram import Router, types, F
from aiogram.filters.command import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Это бот для отбора в ТПШ-2026.  Умеет выдавать статистику по видео-креаторам публикующим контент в разных соц. сетях. База данных содержит информацию о видеороликах (id видео, id креатора, дата и время публикации видео, общее количество просмотров, лайков, комментариев и жалоб), а также информацию о почасовых снапшотах каждого видео (id снапшота, время снапшота, текущие значения на момент снапшота количества просмотров, лайков, комментариев и жалоб, приращения с момента прошлого снапшота количества просмотров, лайков, комментариев и жалоб). Задавайте вопросы, подразумевающие в качестве ответа одно число.")


@router.message(F.photo)
async def handle_photo(message: types.Message):
    await message.answer("Это фото. Данный бот работает только с текстом.")


@router.message(F.sticker)
async def handle_sticker(message: types.Message):
    await message.answer("Это стикер. Данный бот работает только с текстом.")


