import os
import io
import asyncio
import logging
import sys
import pandas as pd
import keyboard as kb
'''from dotenv import load_dotenv'''
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart

'''load_dotenv()'''
data = not()
TOKEN = os.getenv("TOKEN")
bot = Bot(token='6508449400:AAH_l_KdJjLZgda9kI8iUs-1ZRhLYKsWymw')

dp = Dispatcher()

form_router = Router()

class Form(StatesGroup):
   name = State()

@form_router.message(CommandStart())
async def command_start(message: Message):
   await message.answer("Привет! Загрузи файл для составления отчет по нужной группе и потом нажми кнопку Получить отчет")

# try - if, соблюдение полей
# except - если трай не работает, то выдает это
@dp.message(F.document)
async def report(message: Message):
   global data
   try:
      await message.answer('Подождите, загрузка файла может занять некоторое время')
      file_id  = message.document.file_id
      file = await bot.get_file(file_id)
      file_path = file.file_path
      my_object = io.BytesIO()
      MyBinaryIO = await bot.download_file(file_path, my_object)
      data = pd.read_excel(MyBinaryIO)
      await message.answer('Файл успешно загружен!', reply_markup=kb.main )
   except Exception as e:
      await message.answer(f"Произошла ошибка при загрузке файла. {e}")
   return


@form_router.message(F.text == "Получить отчет")
async def process_name(message: Message, state: FSMContext) -> None:
   try:
      name_group= data['Группа'].unique()
      names = ', '.join(map(str, name_group))
      await message.answer(f"Файл загружен. В данном файле представлены данные по следующим группам: {names}")
      await message.answer("Напишите номер необходимой группы")
      await state.set_state(Form.name)
      await message.answer(
         "Введите номер группы: ",
         reply_markup=ReplyKeyboardRemove())
   except:
      await message.answer(f"Загрузите другой файл, данный файл не подлежит обрабоке.")

@form_router.message(Form.name)
async def process_name(message: Message, state: FSMContext) -> None:
   await state.update_data(name = message.text)
   group = await state.get_data()
   await message.answer(f"Номер вашей группы:  {group['name']}")
   skore = data['Группа'].str.contains(str(group['name'])).sum()
   if skore == 0:
      await message.answer('Такой группы не существует', reply_markup=kb.main)
      return
   else:
      try:
         kol_vo=data.shape[0]
         kol_group = data['Группа'].str.contains(group['name']).sum()
         kol_stud = len(data[data['Группа'] == group['name']]['Личный номер студента'].unique())
         number_stud= data.loc[data['Группа']== group['name'] , 'Личный номер студента'].unique()
         number_stud2 = ', '.join(map(str, number_stud))
         control = data['Уровень контроля'].unique()
         control2 = ', '.join(map(str, control))
         god = data['Год'].unique()
         god2= ', '.join(map(str, god))
         await message.answer(f'В исходном дататесте содержалось {kol_vo}, оценок из них них, {kol_group}, относящихся к группе {group["name"]}. В датасете находятся оценки  {kol_stud} студентов со следующими личными номерами: {number_stud2}. Используемые формы контроля: {control2}. Данные представлены по следующим годам: {god2}.')
      except:
         await message.answer(f"Загрузите другой файл, данный файл не подлежит обрабоке.")


async def main():
   dp.include_router(form_router)
   await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
