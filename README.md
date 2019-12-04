# audio_streaming_using_pyaudio

Python programs for reading and writing multi-channel audio input stream. *Pyaudio* is used to read the audio input buffer and *wave* is used to write wav output file. The reading of audio input stream is done in non-blocking mode using callback function. 


## Prerequisites

You will need to install portaudio library and pyaudio

```
$ sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp
$ pip install pyaudio
```

## Running the tests

*audio_reader.py* contains the class for reading audio input stream. *wav_writer.py contains the class to write .wav file

### Test audio_reader.py

Use *audio_reader_unit_test.py* to test *audio_reader.py*. First, you need to set up the parameters according to the microphone/microphone array and the OS that you are using. Below is an example for UMA-8 microphone array and Ubuntu 16.04

```
host_api = 'ALSA'
n_chans = 8
```
After that, run *audio_reader_unit_test.py*

### Read audio signal from stream and write to .wav file in non-blocking mode

Explain what these tests test and why

Use *main_recorder.py*. First, you need to set up the parameters according to the microphone/microphone array and the OS that you are using. Below is an example for UMA-8 microphone array and Ubuntu 16.04

```
host_api = 'ALSA'
n_chans = 8
```

After that, run *main_recorder.py*

## Authors

* **Tho Nguyen** (https://github.com/thomeou)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Pyaudio documentations: http://people.csail.mit.edu/hubert/pyaudio/
