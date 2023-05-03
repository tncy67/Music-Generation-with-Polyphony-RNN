# AI-Generated Lyrics and Music

This repository contains the necessary files and instructions to generate AI-generated lyrics and music using LSTM and Magenta library, respectively.

## Prerequisites

1. Install the required Python libraries:
    - BeautifulSoup4
    - Requests
    - TensorFlow
    - Magenta

### Scraping Lyrics

1. Create a Python script to scrape song lyrics from a lyrics website.
2. Use BeautifulSoup and Requests to extract the lyrics from the HTML content.
3. Save the extracted lyrics to a text file.

### Preprocessing Lyrics

1. Create a Python script to preprocess the scraped lyrics.
2. Read the lyrics from the text file and apply necessary preprocessing steps, such as lowercasing and tokenization.
3. Save the preprocessed lyrics to a new text file.


#### Merging MIDI Files (Optional)

If you have multiple MIDI files and want to merge them into a single file for training, run the following command:



# MIDI Music Generation with Polyphony RNN

This repository contains the necessary files and instructions to train a polyphonic music generation model using Google's [Magenta](https://github.com/magenta/magenta) library, specifically the [Polyphony RNN](https://github.com/magenta/magenta/tree/main/magenta/models/polyphony_rnn) model.

## Prerequisites

1. Install [Magenta](https://github.com/magenta/magenta) library by following the installation instructions [here](https://github.com/magenta/magenta/blob/main/README.md).
2. Make sure you have a collection of MIDI files to use for training.

## Training the Model

Follow these steps to train the Polyphony RNN model:

1. Convert your MIDI files into a format suitable for training by running the following command:

polyphony_rnn_create_dataset
--input=./path_to_your_MIDI_files/*.mid
--output_dir=./polyphony_rnn_training_data
--eval_ratio=0.10



This will generate a `.tfrecord` file in the `./polyphony_rnn_training_data` directory.

2. Create a directory to store the model checkpoints:


mkdir songs_MIDI_polyphonic_checkpoints



3. Train the Polyphony RNN model by running the following command:


polyphony_rnn_train
--config=polyphony
--run_dir=./songs_MIDI_polyphonic_checkpoints
--sequence_example_file=./polyphony_rnn_training_data/training_poly_tracks.tfrecord
--hparams="batch_size=8,rnn_layer_sizes=[128,128,128]"
--num_training_steps=20000



You can stop the training process at any time using `Ctrl+C`. To resume training from the latest checkpoint, simply run the same command again. You can also adjust the `num_training_steps` argument as needed.

## Generating New Music

After training the model, you can use it to generate new music. Detailed instructions on how to do this will be added soon.

## License

This project is released under the [MIT License](https://opensource.org/licenses/MIT).



