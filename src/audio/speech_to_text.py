
import os
import time
import warnings
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel

warnings.filterwarnings("ignore")

# CONFIG 
SAMPLE_RATE = 16000
AUDIO_PATH = os.path.join(os.getcwd(), "input.wav")

SILENCE_THRESHOLD = 500
SILENCE_DURATION = 0.5     # faster stop
MAX_RECORD_SECONDS = 10

# model initialization - (use medium or large for better accuracy if you have the GPU memory)
model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)



def record_until_silence():
    print("Speak now...")
    audio_chunks = []
    silence_start = None

    def callback(indata, frames, time_info, status):
        nonlocal silence_start

        volume = np.linalg.norm(indata) * 10
        audio_chunks.append(indata.copy())

        if volume < SILENCE_THRESHOLD:
            if silence_start is None:
                silence_start = time.time()
            elif time.time() - silence_start > SILENCE_DURATION:
                raise sd.CallbackStop
        else:
            silence_start = None

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
        callback=callback
    ):
        sd.sleep(int(MAX_RECORD_SECONDS * 1000))

    audio = np.concatenate(audio_chunks, axis=0)
    write(AUDIO_PATH, SAMPLE_RATE, audio)


def audio_to_text():
    record_until_silence()

    segments, info = model.transcribe(
        AUDIO_PATH,
        language="en"
    )

    text = " ".join(segment.text for segment in segments)
    return text.strip()


