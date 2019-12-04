# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 15:08:31 2015

@author: tho.nguyen
"""
import os
import time
import math
import wave


class Writer(object):
    def __init__(self, n_chans, fs, chunk_size, sampwidth, wav_length_second=1,
                 output_dir='data', prefix='audio'):
        self.n_chans = n_chans
        self.fs = fs
        self.chunk_size = chunk_size
        self.sampwidth = sampwidth
        self.wav_length_second = wav_length_second
        self.max_frame_count = int(math.floor(self.wav_length_second * self.fs/
                                              self.chunk_size))
        self.output_dir = output_dir
        self.prefix = prefix
        self.count_frame = 0
        self.io_flag = False
        
    def open_file(self):
        filename = os.path.join(self.output_dir, self.prefix + '_' + 
                                time.strftime("%Y_%m_%d_%H_%M_%S") + ".wav")
        try: 
            self.wf = wave.open(filename, 'wb')
            self.wf.setnchannels(self.n_chans)
            self.wf.setsampwidth(self.sampwidth)
            self.wf.setframerate(self.fs)
            self.io_flag = True
        except IOError as ie:
            self.io_flag = False
        
        return self.io_flag

    def write_wav(self, input_stream):
        if self.count_frame == 0:
            self.open_file()
        if self.count_frame == self.max_frame_count:
            # close the current file
            self.wf.close()
            self.open_file()
            self.count_frame = 0
        # write to current file
        if self.io_flag: 
            self.wf.writeframes(b''.join(input_stream))
            self.count_frame += 1
        
        return None
    
    def close_file(self):
        self.wf.close()
