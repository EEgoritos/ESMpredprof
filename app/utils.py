from midiutil import MIDIFile
import fluidsynth

def recognize_notes(image_path):
    # Заглушка для распознавания нот
    return [60, 62, 64, 65, 67]  # MIDI ноты для C4, D4, E4, F4, G4

def create_midi(notes, output_path):
    midi = MIDIFile(1)
    track = 0
    time = 0
    midi.addTrackName(track, time, "Track")
    midi.addTempo(track, time, 120)
    channel = 0
    volume = 100
    for i, note in enumerate(notes):
        midi.addNote(track, channel, note, time + i, 1, volume)
    with open(output_path, "wb") as output_file:
        midi.writeFile(output_file)

def convert_to_audio(midi_path, audio_path):
    fs = fluidsynth.Synth()
    sfid = fs.sfload("soundfont.sf2")  # Убедитесь, что у вас есть файл soundfont
    fs.program_select(0, sfid, 0, 0)
    fs.start()
    fs.midi_to_audio(midi_path, audio_path)
    fs.delete()