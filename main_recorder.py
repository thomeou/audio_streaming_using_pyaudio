#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 15:42:16 2019

@author: tho_nguyen
"""
import os
import time
import multiprocessing
import audio_reader
import wav_writer

# parameters to read audio input
QMAXSIZE = 20
audio_input_queue = multiprocessing.Queue(QMAXSIZE)

host_api = 'ALSA'
n_chans = 8
fs = 44100
chunk_size = 1024*8
stream_reader = audio_reader.Reader(audio_input_queue, n_chans, fs, host_api,
                                    chunk_size)

# parameters to write wav file 
output_dir = os.path.join('data', 'test')
os.makedirs(os.path.dirname(output_dir), exist_ok=True)
filename_prefix = 'uma8'
wav_length_second = 10 # 60 second
file_writer = wav_writer.Writer(n_chans, fs, chunk_size, stream_reader.SAMPWIDTH, 
                                wav_length_second, output_dir, filename_prefix)
 
# duration of recording
record_length = 60
max_count = int(record_length * fs//chunk_size)
count = 0

stream_reader.start_streaming()
start_time = time.time()
while (count < max_count):
    if not audio_input_queue.empty():
        achunk = audio_input_queue.get()
        file_writer.write_wav(achunk)
        count += 1        
print('elapsed time: {:.4f} s'.format(time.time() - start_time))
print('data duration: {:.4f} s'.format(chunk_size * max_count/fs))
stream_reader.stop_streaming()
file_writer.close_file()
# read all the audio buffer before closing to preven broken pipe error
while not audio_input_queue.empty():
    achunk = audio_input_queue.get()
audio_input_queue.close()
audio_input_queue.join_thread()
print("End of program")

