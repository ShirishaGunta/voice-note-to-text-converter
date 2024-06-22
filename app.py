from flask import Flask, render_template, request, jsonify
import pyaudio
import wave
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import detect_silence
import os

app = Flask(__name__)

def record_audio(filename, duration=10, rate=44100, chunk=1024):
    audio_format = pyaudio.paInt16
    channels = 1

    p = pyaudio.PyAudio()
    stream = p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    print("Recording started")
    frames = []
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("recording ended")

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(audio_format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

def reduce_noise(audio_file, output_file):
    audio = AudioSegment.from_wav(audio_file)
    silence = detect_silence(audio, min_silence_len=1000, silence_thresh=-40)
    audio = audio.normalize()
    audio.export(output_file, format="wav")

def audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record', methods=['POST'])
def record():
    raw_audio_filename = "raw_recorded_audio.wav"
    cleaned_audio_filename = "cleaned_recorded_audio.wav"

    record_audio(raw_audio_filename)
    reduce_noise(raw_audio_filename, cleaned_audio_filename)
    transcription = audio_to_text(cleaned_audio_filename)


   

    return jsonify({'transcription': transcription})

if __name__ == '__main__':
    app.run(debug=True)
