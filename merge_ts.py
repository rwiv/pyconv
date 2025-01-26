import os
import time
import subprocess


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
        start_time = time.time()

        src_path = os.path.join(target_path, dirname)
        ts_path = os.path.join(out_dirpath, f"{dirname}.ts")
        mp4_path = os.path.join(out_dirpath, f"{dirname}.mp4")
        merge_one(src_path, ts_path)
        convert_one(ts_path, mp4_path)
        os.remove(ts_path)

        end_time = time.time()
        print(f"{src_path}: {end_time - start_time} seconds")


def merge_all(target_path: str, out_dirpath: str):
    os.makedirs(out_dirpath, exist_ok=True)
    for dirname in os.listdir(target_path):
        src_path = os.path.join(target_path, dirname)
        out_path = os.path.join(out_dirpath, dirname)
        os.makedirs(out_path, exist_ok=True)
        merge_channel(src_path, out_path)


target_path = "target"
out_dirpath = "out"

if __name__ == "__main__":
    merge_all(target_path, out_dirpath)
