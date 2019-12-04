#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 15:42:16 2019

@author: tho_nguyen

Unit test for audio_reader module: read audio input from buffer 

Tested for UMA-8 microphone array and ubuntu 16.04
"""
import time
import multiprocessing
import numpy as np
import audio_reader

# change these parameters accordingly to the microphones and OS
host_api = 'ALSA'
n_chans = 8
fs = 44100
chunk_size = 1024*8

QMAXSIZE = 20
audio_input_queue = multiprocessing.Queue(QMAXSIZE)
stream_reader = audio_reader.Reader(audio_input_queue, n_chans, fs, host_api,
                                    chunk_size)
stream_reader.start_streaming()

start_time = time.time()
count = 0
max_count = 10
while (count < max_count):
    if not audio_input_queue.empty():
        achunk = audio_input_queue.get()[0]
        #######################################################################
        # do some audio processing here
        # convert string to int16 to numpy float32
        input_signal = np.reshape(np.frombuffer(achunk, dtype='int16')/32768.0,
                                 (chunk_size, n_chans))
        print(input_signal.shape)
        #######################################################################
        count += 1       
print('elapsed time: {:.4f} s'.format(time.time() - start_time))
print('data duration: {:.4f} s'.format(chunk_size * max_count/fs))
stream_reader.stop_streaming()
# read all the audio buffer before closing to preven broken pipe error
while not audio_input_queue.empty():
    achunk = audio_input_queue.get()
audio_input_queue.close()
audio_input_queue.join_thread()
print("End of program")
