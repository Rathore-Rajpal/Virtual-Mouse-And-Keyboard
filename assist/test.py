import struct
import time
import pvporcupine
import pyaudio
import pyautogui as autogui

def hotword():
    porcupine = None
    pa = None
    audio_stream = None

    try:
        access_key = "nm2uZzRWhxQ1MxyzsIGhOOkROeGh2WTdGQmdkOBtlaq4b9trt0YENQ=="
        keyword_path = "C:\\VirtualMouseProject\\hey-buddy_en_windows_v3_0_0\\hey-buddy_en_windows_v3_0_0.ppn"

        porcupine = pvporcupine.create(
            access_key=access_key,
            keyword_paths=[keyword_path],
            sensitivities=[0.5]
        )

        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        print("Listening for 'buddy'...")

        while True:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            result = porcupine.process(pcm)
            
            if result >= 0:
                print("Hotword detected!")
                autogui.hotkey('alt', 'j')  # Simplified key combination
                time.sleep(1)

    except Exception as e:
        print("Error:", e)
    finally:
        if porcupine:
            porcupine.delete()
        if audio_stream:
            audio_stream.close()
        if pa:
            pa.terminate()

hotword()