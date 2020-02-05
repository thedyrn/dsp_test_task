import os
import dlib

from aiogram.types.mixins import Downloadable
import utils


def face_detect(file_path: str) -> bool:
    """Возвращает True, если найдено лицо, иначе False."""
    image = dlib.load_rgb_image(file_path)
    detector = dlib.get_frontal_face_detector()
    if len(detector(image)) > 0:
        return True
    else:
        return False


class AiogramTmpFile:
    """
    Временный файл для упрощения работы с dlib.
    Пример:
    async with AiogramTmpFile(photo_obj, 'tmp_photo.png') as file_path:
        do_smth_with_img(file_path)
    """
    def __init__(self, aiogram_obj: Downloadable, filename: str, tmp_dir: str = 'tmp'):
        self.filename = filename
        self.aiogram_object = aiogram_obj
        self.tmp_dir = tmp_dir

        self.path_with_tmp_dir = f'{self.tmp_dir}/{self.filename}'
        utils.make_dir(self.tmp_dir)

    @staticmethod
    def abs_path_to(path):
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), path)

    async def __aenter__(self):
        await self.aiogram_object.download(self.path_with_tmp_dir)
        return self.path_with_tmp_dir

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        os.remove(self.abs_path_to(self.path_with_tmp_dir))

        if len(os.listdir(self.abs_path_to(self.tmp_dir))) == 0:
            os.rmdir(self.abs_path_to(self.tmp_dir))
