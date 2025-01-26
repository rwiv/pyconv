import os
import shutil
import time
import subprocess


GIGA_BYTE = 1024 * 1024 * 1024


def get_directory_size(directory: str) -> int:
    total_size = 0
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
    return total_size


def merge_one(target_path: str, out_path: str):
    ts_filenames = sorted(
        [f for f in os.listdir(target_path) if f.endswith(".ts")],
        key=lambda x: int(x.split(".")[0])
    )

    with open(out_path, "wb") as outfile:
        for ts_filename in ts_filenames:
            with open(os.path.join(target_path, ts_filename), "rb") as infile:
                outfile.write(infile.read())


def convert_one(target_path: str, out_path: str):
    command = ['ffmpeg', '-i', target_path, '-c', 'copy', out_path]
    subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def merge_channel(target_path: str, out_dirpath: str):
    for dirname in os.listdir(target_path):
        src_path = os.path.join(target_path, dirname)
        ts_path = os.path.join(out_dirpath, f"{dirname}.ts")
        mp4_path = os.path.join(out_dirpath, f"{dirname}.mp4")
        merge_one(src_path, ts_path)
        convert_one(ts_path, mp4_path)
        os.remove(ts_path)
        return mp4_path


def merge_all(target_path: str, out_dirpath: str, tmp_dirpath: str):
    os.makedirs(out_dirpath, exist_ok=True)
    os.makedirs(tmp_dirpath, exist_ok=True)
    for dirname in os.listdir(target_path):
        start_time = time.time()

        src_path = os.path.join(target_path, dirname)
        tmp_path = os.path.join(tmp_dirpath, dirname)

        dir_size = get_directory_size(src_path)
        if (dir_size / GIGA_BYTE) > 100:
            raise Exception("too big file")

        os.makedirs(tmp_path, exist_ok=True)
        tmp_mp4_path = merge_channel(src_path, tmp_path)

        os.makedirs(os.path.join(out_dirpath, dirname), exist_ok=True)
        out_mp4_path = os.path.join(out_dirpath, dirname, os.path.basename(tmp_mp4_path))
        shutil.move(tmp_mp4_path, out_mp4_path)

        if len(os.listdir(tmp_path)) == 0:
            os.rmdir(tmp_path)
        if len(os.listdir(tmp_dirpath)) == 0:
            os.rmdir(tmp_dirpath)

        end_time = time.time()
        print(f"{src_path}: {end_time - start_time} seconds")


target_path = "target"
out_dirpath = "out"
tmp_dirpath = "tmp"


if __name__ == "__main__":
    merge_all(target_path, out_dirpath, tmp_dirpath)
