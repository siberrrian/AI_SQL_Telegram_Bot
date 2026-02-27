import os
from dotenv import load_dotenv

import psycopg2
import pandas as pd
from sqlalchemy import create_engine

from gigachat import GigaChat

from aiogram import Router, types, F
from aiogram.filters.command import Command

load_dotenv()

connect_string = os.getenv("DB_DIALECT") + "://" + \
                 os.getenv("DB_USER") + ":" + \
                 os.getenv("DB_PASSWORD") + "@" + \
                 os.getenv("DB_HOST") + ":" + \
                 os.getenv("DB_CONTAINER_PORT") + "/" + \
                 os.getenv("DB_NAME")

router = Router()
engine = create_engine(connect_string)
conn = engine.connect()

async def ask_ai(prompt):
    giga = GigaChat(
        credentials=os.getenv("gigachat_token"),
        verify_ssl_certs=False,
        model="GigaChat-2-Max",
        scope="GIGACHAT_API_PERS"
    )

    aianswer = giga.chat(prompt)

    return aianswer.choices[0].message.content


@router.message(F.text)
async def handle_text(message: types.Message):
    prompt ="""
Ты SQL-программист, который составляет SQL-запросы к таблицам в базе данных postgreSQL на основе вопроса сформулированного русским языком (естесственным языком).

В базе данных есть две таблицы - videos и video_snapshots.
Первая таблица videos хранит итоговую статистику по каждому видео и состоит из следующих полей:
id (идентификатор видео), 
creator_id (идентификатор креатора), 
video_created_at (дата и время публикации видео), 
views_count (финальное количество просмотров), 
likes_count (финальное количество лайков), 
comments_count (финальное количество комментариев), 
reports_count (финальное количество жалоб), 
created_at (служебное поле со временем создания записи), 
updated_at (служебное поле со временем обновления информации в записи). 

Вторая таблица video_snapshots хранит почасовую статистику по каждому видео (чтобы отслеживать динамику) и состоит из следующих полей: 
id (идентификатор снапшота), 
video_id (идентификатор видео соответствующий полю id из таблицы videos),
views_count (текущее значение количества просмотров на момент замера), 
likes_count (текущее значение количества лайков на момент замера), 
comments_count (текущее значение количества комментариев на момент замера), 
reports_count (текущее значение количества жалоб на момент замера), 
delta_views_count (приращение количества просмотров - насколько изменилось значение с прошлого замера), 
delta_likes_count (приращение количества лайков - насколько изменилось значение с прошлого замера), 
delta_comments_count (приращение количества комментариев - насколько изменилось значение с прошлого замера), 
delta_reports_count (приращение количества жалоб - насколько изменилось значение с прошлого замера), 
created_at (время замера - раз в час), 
updated_at (служебное поле - время обновления записи).

Твой ответ на вопрос должен представлять собой SQL-запрос к таблицам в базе данных postgreSQL, выполнение которого в базе данных будет возвращать одно число (счётчик, сумму или прирост в зависимости от запроса). 

Отвечай одной строкой формата SQL без лишних пояснений и комментариев. Ответ не нужно выделять никакими тегами. Выведи просто текст ответа.

При составлении запроса строго соблюдай следующие правила:
- Для вычисления метрик за определенный период после публикации всегда используй JOIN таблицы video_snapshots с таблицей videos по полю video_id.
- Не используй функции MIN или MAX ко всей таблице снапшотов для определения точки отсчета, так как у каждого видео своя дата публикации.
- Всегда используй алиасы таблиц для всех полей в блоке WHERE и SELECT, чтобы избежать ошибки неоднозначности.
- При расчете за период 'N часов после публикации' используй нестрогое сравнение <=, чтобы учесть последний замер, сделанный ровно в момент истечения часа.

Если заданный вопрос не касается выборки данных из таблиц videos и video_snapshots или в вопросе недостаточно данных, то отвечай одним словом: NOT_UNDERSTAND

Ответь на следующий вопрос: 

"""
    ans_ai = await ask_ai(prompt + message.text)
    query = ans_ai
    query = query.replace("\n", " ")
    query = query.replace("```sql", "")
    query = query.replace("```", "")
    if (query != "NOT_UNDERSTAND"):
        answer = str(pd.read_sql(query, conn).iloc[0, 0])
    else:
        answer = "Уточните свой вопрос."
    await message.answer(answer)
