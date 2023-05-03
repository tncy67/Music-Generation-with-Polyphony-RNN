#worked
import os
import sys
import numpy as np
from glob import glob

import librosa
import pretty_midi
import fluidsynth

def audio_to_midi_fluidsynth(audio_file, midi_file, sample_rate=44100):
    y, sr = librosa.load(audio_file, sr=sample_rate, mono=True)
    cqt = librosa.core.amplitude_to_db(librosa.cqt(y, sr=sample_rate), ref=np.max)

    midi_data = pretty_midi.PrettyMIDI()
    piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
    piano = pretty_midi.Instrument(program=piano_program)

    threshold = -24
    min_duration = 0.1

    for frame_idx in range(cqt.shape[1]):
        for bin_idx in range(cqt.shape[0]):
            if cqt[bin_idx, frame_idx] > threshold:
                pitch = bin_idx + librosa.note_to_midi('C1')
                start = librosa.frames_to_time(frame_idx, sr=sample_rate)
                end = start + min_duration

                new_note = pretty_midi.Note(velocity=100, pitch=pitch, start=start, end=end)
                piano.notes.append(new_note)

    midi_data.instruments.append(piano)
    midi_data.write(midi_file)

input_directory = "./songs"
output_directory = "./songs_MIDI"

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for root, dirs, files in os.walk(input_directory):
    for file in files:
        if file.lower().endswith((".mp3", ".wav")):
            input_file = os.path.join(root, file)
            output_subdir = root.replace(input_directory, output_directory)
            if not os.path.exists(output_subdir):
                os.makedirs(output_subdir)
            output_file = os.path.join(output_subdir, os.path.splitext(file)[0] + ".midi")

            print(f"Converting {input_file} to {output_file}")

            audio_to_midi_fluidsynth(input_file, output_file)
