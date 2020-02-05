import os

from aiogram import Bot, Dispatcher, executor, types

import photos_handler as ph
import voice_handler as vh
import utils

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(content_types=types.message.ContentType.PHOTO)
async def photo(message: types.Message):
    await message.answer('Сейчас посмотрим...')

    photo_thumbnail = message.photo[0]  # миниатюра для быстрого поиска
    async with ph.AiogramTmpFile(photo_thumbnail, 'tmp_photo.png') as file_path:
        if ph.face_detect(file_path):
            await message.answer('Похоже на лицо, поэтому сохраню.')

            await utils.download_obj(message.photo[1],
                                     directory=f'{message.from_user.id}_faces',
                                     path_ptn='photo_{new_number:03d}.png')  # сохранение полного размера
        else:
            await message.answer('Не очень похоже на лицо.')


@dp.message_handler(content_types=types.message.ContentType.VOICE)
async def voice(message: types.Message):
    await message.answer('Пожалуй сохраню это в wav.')

    await vh.process_voice(f'{message.from_user.id}_voices', message.voice)
    await message.answer('Сделано!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
