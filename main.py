import os.path
from subprocess import run
import json

from sklearn.model_selection import ParameterGrid
from glob import glob
from multiprocessing import Pool

files = list(glob("examples/*.jpg"))
SIZES = [550, 500, 450, 400, 350, 300, 250, 200, 150, 100]
# QUALITIES = [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
QUALITIES = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

params = {
    "file": files,
    "size": SIZES,
    "quality": QUALITIES
}

tasks = list(ParameterGrid(params))


def do_task(param):
    output_name = f"output/{os.path.basename(param['file'])}_{param['size']}_{param['quality']}.webp"
    data_name = f"data/{os.path.basename(param['file'])}_{param['size']}_{param['quality']}.json"
    if os.path.exists(output_name):
        os.remove(output_name)

    args = [
        "ffmpeg", "-i", param["file"],
        "-vf", f"scale={param['size']}:-1",
        "-sws_flags", "lanczos",
        "-q:v", f"{param['quality']}",
        "-compression_level", "6",
        "-hide_banner", "-loglevel", "error",
        output_name,
    ]

    run(args)

    output_file_size = os.stat(output_name).st_size

    data_dict = {
        "args": args,
        **param,
        "output_size": output_file_size
    }

    with open(data_name, "w") as f:
        json.dump(data_dict, f, indent=2)


with Pool(processes=31) as pool:
    pool.map(do_task, tasks)
