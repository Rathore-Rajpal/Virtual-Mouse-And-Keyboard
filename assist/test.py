import struct
import time
import pvporcupine
import pyaudio
import pyautogui as autogui

def list_microphones(p):
    """List available microphone devices."""
    print("Available input devices:")
    for i in range(p.get_device_count()):
        dev_info = p.get_device_info_by_index(i)
        if dev_info.get('maxInputChannels') > 0:
            print(f"Index {i}: {dev_info.get('name')} (Sample Rate: {dev_info.get('defaultSampleRate')} Hz)")

def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    
    try:
        # Initialize Porcupine without access_key (as it's not needed in this version)
        porcupine = pvporcupine.create(
            keywords=["jarvis", "alexa"],  # List of keywords to detect
            sensitivities=[0.4, 0.4]  # Sensitivity for better detection accuracy
        )

        paud = pyaudio.PyAudio()
        
        
        # Use default input device or specify index manually
        input_device_index = None  # Set to None for default, or specify an index from list_microphones
        
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            input_device_index=input_device_index,  # Set microphone input device
            frames_per_buffer=porcupine.frame_length
        )

        print("Listening for hotwords...")

        # Hotword detection loop
        while True:
            try:
                pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
                
                # Detect keyword
                keyword_index = porcupine.process(pcm)
                
                if keyword_index >= 0:
                    detected_word = ["jarvis", "alexa"][keyword_index]
                    print(f"Hotword detected: {detected_word}")
                    
                    # Simulate keypress (Win+J)
                    autogui.keyDown("win")
                    autogui.press("j")
                    time.sleep(0.1)
                    autogui.keyUp("win")
                    time.sleep(1)  # Cooldown to prevent multiple detections

            except IOError as e:
                print("Audio read error:", e)
                continue

    except Exception as e:
        print("Error:", e)
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

# Run the hotword detection
hotword()
