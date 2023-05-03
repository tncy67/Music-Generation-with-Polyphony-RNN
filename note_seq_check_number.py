import tensorflow as tf

# input_file = './songs_MIDI_monophonic/notesequences.tfrecord'
input_file = './songs_MIDI_polyphonic/notesequences_polyphonic.tfrecord'

dataset = tf.data.TFRecordDataset(input_file)
total_count = 0

for record in dataset:
    total_count += 1

print("Total number of NoteSequences in the TFRecord file:", total_count)
