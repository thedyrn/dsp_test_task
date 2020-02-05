import os
from aiogram.types.mixins import Downloadable


def make_dir(dir_name):
    if dir_name not in os.listdir('.'):
        os.mkdir(dir_name)


async def download_obj(aiogram_obj: Downloadable, directory: str, path_ptn: str):
    make_dir(directory)
    new_number = len(os.listdir(directory)) + 1
    path = f'{directory}/{path_ptn.format(new_number=new_number)}'
    await aiogram_obj.download(path)
    return path
