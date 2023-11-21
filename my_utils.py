import ffmpeg
import numpy as np

# import praatio
# import praatio.praat_scripts
import os
import sys

import random

import csv

platform_stft_mapping = {
    "linux": "stftpitchshift",
    "darwin": "stftpitchshift",
    "win32": "stftpitchshift.exe",
}

stft = platform_stft_mapping.get(sys.platform)
# praatEXE = join('.',os.path.abspath(os.getcwd()) + r"\Praat.exe")


def CSVutil(file, rw, type, *args):
    if type == "formanting":
        if rw == "r":
            with open(file) as fileCSVread:
                csv_reader = list(csv.reader(fileCSVread))
                return (
                    (csv_reader[0][0], csv_reader[0][1], csv_reader[0][2])
                    if csv_reader is not None
                    else (lambda: exec('raise ValueError("No data")'))()
                )
        else:
            if args:
                doformnt = args[0]
            else:
                doformnt = False
            qfr = args[1] if len(args) > 1 else 1.0
            tmb = args[2] if len(args) > 2 else 1.0
            with open(file, rw, newline="") as fileCSVwrite:
                csv_writer = csv.writer(fileCSVwrite, delimiter=",")
                csv_writer.writerow([doformnt, qfr, tmb])
    elif type == "stop":
        stop = args[0] if args else False
        with open(file, rw, newline="") as fileCSVwrite:
            csv_writer = csv.writer(fileCSVwrite, delimiter=",")
            csv_writer.writerow([stop])


def load_audio(file, sr):
    try:
        # https://github.com/openai/whisper/blob/main/whisper/audio.py#L26
        # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
        # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
        file = (
            file.strip(" ").strip('"').strip("\n").strip('"').strip(" ")
        )  # 防止小白拷路径头尾带了空格和"和回车
        out, _ = (
            ffmpeg.input(file, threads=0)
            .output("-", format="f32le", acodec="pcm_f32le", ac=1, ar=sr)
            .run(cmd=["ffmpeg", "-nostdin"], capture_stdout=True, capture_stderr=True)
        )
    except Exception as e:
        raise RuntimeError(f"Failed to load audio: {e}")

    return np.frombuffer(out, np.float32).flatten()
