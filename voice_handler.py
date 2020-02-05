import os
import subprocess

import utils


async def process_voice(directory, aiogram_voice):
    path_pattern = 'voice_{new_number:03d}'

    download_dir = directory + '_ogg'
    utils.make_dir(download_dir)

    convert_dir = directory + '_wav'
    utils.make_dir(convert_dir)

    download_path = await utils.download_obj(aiogram_voice,
                                             directory=download_dir,
                                             path_ptn=path_pattern + '.ogg')

    convert_to_wav(convert_dir, download_path, path_pattern)


def convert_to_wav(convert_dir, download_path, path_pattern):
    new_number = len(os.listdir(convert_dir)) + 1
    output_path = f"{convert_dir}/{path_pattern.format(new_number=new_number)}.wav"

    subprocess.run(f'ffmpeg -i {download_path} -ar 16000 {output_path}')
