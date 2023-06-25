
from src.controller.abstractController import AbstractController
from src.presenter.AbstractPresenter import AbstractPresenter
#Importing Libraries
import numpy as np
from music21 import *
from midi2audio import FluidSynth
import uuid
import os
from music21 import converter
from sklearn.model_selection import train_test_split
import tensorflow

np.random.seed(42)

from keras.models import load_model

model = load_model('model.h5')
length = 40
#Loading the list of chopin's midi files as stream
filepath = "content/"
#Getting midi files
all_midis= []
for i in os.listdir(filepath):
    if i.endswith(".mid"):
        tr = filepath+i
        print(tr)
        midi = converter.parse(tr)
        all_midis.append(midi)

#Helping function
def extract_notes(file):
    notes = []
    pick = None
    for j in file:
        songs = instrument.partitionByInstrument(j)
        for part in songs.parts:
            pick = part.recurse()
            for element in pick:
                if isinstance(element, note.Note):
                    notes.append(str(element.pitch))
                elif isinstance(element, chord.Chord):
                    notes.append(".".join(str(n) for n in element.normalOrder))

    return notes


#Getting the list of notes as Corpus
Corpus= extract_notes(all_midis)
print("Total notes in all the Chopin midis in the dataset:", len(Corpus))
# Storing all the unique characters present in my corpus to bult a mapping dic.
symb = sorted(list(set(Corpus)))

L_corpus = len(Corpus) #length of corpus
L_symb = len(symb) #length of total unique characters

#Building dictionary to access the vocabulary from indices and vice versa
mapping = dict((c, i) for i, c in enumerate(symb))
reverse_mapping = dict((i, c) for i, c in enumerate(symb))

print("Total number of characters:", L_corpus)
print("Number of unique characters:", L_symb)


features = []
targets = []
for i in range(0, L_corpus - length, 1):
    feature = Corpus[i:i + length]
    target = Corpus[i + length]
    features.append([mapping[j] for j in feature])
    targets.append(mapping[target])


L_datapoints = len(targets)
print("Total number of sequences in the Corpus:", L_datapoints)

# reshape X and normalize
X = (np.reshape(features, (L_datapoints, length, 1)))/ float(L_symb)
# one hot encode the output variable
y = tensorflow.keras.utils.to_categorical(targets)

X_train, X_seed, y_train, y_seed = train_test_split(X, y, test_size=0.2, random_state=42)

class MusicController(AbstractController):
    def __init__(self, presenter: AbstractPresenter) -> None:
        super().__init__(presenter)

    def chords_n_notes(self, Snippet):
        Melody = []
        offset = 0 #Incremental
        for i in Snippet:
            #If it is chord
            if ("." in i or i.isdigit()):
                chord_notes = i.split(".") #Seperating the notes in chord
                notes = []
                for j in chord_notes:
                    inst_note=int(j)
                    note_snip = note.Note(inst_note)
                    notes.append(note_snip)
                    chord_snip = chord.Chord(notes)
                    chord_snip.offset = offset
                    Melody.append(chord_snip)
            # pattern is a note
            else:
                note_snip = note.Note(i)
                note_snip.offset = offset
                Melody.append(note_snip)
            # increase offset each iteration so that notes do not stack
            offset += 1
        Melody_midi = stream.Stream(Melody)
        return Melody_midi

    def Malody_Generator(self, Note_Count):
        seed = X_seed[np.random.randint(0,len(X_seed)-1)]
        Music = ""
        Notes_Generated=[]
        for i in range(Note_Count):
            seed = seed.reshape(1, length ,1)
            prediction = model.predict(seed, verbose=0)[0]
            prediction = np.log(prediction) / 1.0 #diversity
            exp_preds = np.exp(prediction)
            prediction = exp_preds / np.sum(exp_preds)
            index = np.argmax(prediction)
            index_N = index/ float(L_symb)
            Notes_Generated.append(index)
            Music = [reverse_mapping[char] for char in Notes_Generated]
            seed = np.insert(seed[0],len(seed[0]),index_N)
            seed = seed[1:]
        #Now, we have music in form or a list of chords and notes and we want to be a midi file.
        Melody = self.chords_n_notes(Music)
        Melody_midi = stream.Stream(Melody)
        return Melody_midi

    def handle(self, controllerInput: dict) -> any:
        Melody = self.Malody_Generator(150)
        unique_string = str(uuid.uuid4())
        Melody.write('midi',f'static/music/{unique_string}.mid')
        FluidSynth().midi_to_audio(f'static/music/{unique_string}.mid', f"static/music/{unique_string}.wav")
        return unique_string