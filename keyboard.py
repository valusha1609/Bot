from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)

main_kb = [
    [KeyboardButton(text='Получить отчет')]
    ]

main = ReplyKeyboardMarkup(keyboard=main_kb,
                            resize_keyboard=True)