from note_seq.protobuf import music_pb2
import note_seq
import tensorflow as tf

input_file = './songs_MIDI_monophonic/notesequences.tfrecord'

# Read NoteSequences from the input TFRecord file
record_iterator = tf.io.tf_record_iterator(input_file)

# Print NoteSequences
for record in record_iterator:
    ns = music_pb2.NoteSequence()
    ns.ParseFromString(record)
    print(note_seq.sequence_proto_to_pretty_midi(ns))
