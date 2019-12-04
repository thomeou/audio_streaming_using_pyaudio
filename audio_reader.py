# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 12:47:03 2015

@author: tho.nguyen - ADSC - NTU

audio_record module record audio from audio stream 
log:
    updated: 02 12 2019

"""

import pyaudio
import numpy as np

class Reader(object):
    '''Recorder class: initialize, open, record and close port audio stream
    '''

    def __init__(self, audio_input_queue, n_chans, fs, host_api = 'ALSA',
                 chunk_size=8192):
        self.audio_input_queue = audio_input_queue  # queue to buffer audio input
        self.n_chans = n_chans  # number of channels of audio input device
        self.fs = fs  # sampling rate
        self.host_api = host_api  # eg.: 'ALSA' for linux, 'ASIO' for window
        self.CHUNK = chunk_size  
        self.FORMAT = pyaudio.paInt16
        # initilize pyaudio object
        self.p = pyaudio.PyAudio()
        self.SAMPWIDTH = self.p.get_sample_size(self.FORMAT)
        # get device index
        self.get_dev_idx()
        # open audio steam
        self.open_stream()
       
    def get_dev_idx(self):
        ''' get device index from OS
        '''
        self.input_dev_idx = 0
        host_api_found_flag = False
        # get hostApi index
        for ihostapi in range(self.p.get_host_api_count()):
            api_info = self.p.get_host_api_info_by_index(ihostapi)
            if api_info['name'] == self.host_api:
                host_api_idx = api_info['index']
                host_api_found_flag = True
                break

        # get device index
        n_devices = self.p.get_device_count()
        input_dev_found_flag = False
        if host_api_found_flag:
            for idev in range(n_devices):
                dev_info = self.p.get_device_info_by_index(idev)                
                if (dev_info['hostApi'] == host_api_idx) and \
                (dev_info['maxInputChannels'] == self.n_chans):
                    self.input_dev_idx = idev
                    input_dev_found_flag = True
                    break

        self.dev_found_flag = host_api_found_flag and input_dev_found_flag

        return None

    def callback(self, in_data, frame_count, time_info, status):
        '''
        callback to store audio data in non-blocking mode to buffer
        audio stream is converted from string to numpy array before writing to buffer
        '''
        # convert string to int16 to numpy float32
        # aframe = np.reshape(np.fromstring(in_data, dtype='int16')/32768.0,
        #                    (self.CHUNK, self.n_chans))
        try:
            if not self.audio_input_queue.full():
                # self.audio_input_queue.put([aframe[:,:]]) 
                self.audio_input_queue.put([in_data])
            return(None, pyaudio.paContinue)        
        except RuntimeError as re:            
            return(None, pyaudio.paContinue)

    def open_stream(self):
        ''' open pyaudio audio stream
        '''
        if self.dev_found_flag: 
            self.audio_stream = self.p.open(format=self.FORMAT,
                                        channels=self.n_chans,
                                        rate=self.fs,
                                        input=True,
                                        input_device_index=self.input_dev_idx,
                                        frames_per_buffer=self.CHUNK,
                                        stream_callback= self.callback)
        else:
            print('The required audio device is not found!')
        
        return None

    def start_streaming(self):
        if self.dev_found_flag:
            self.audio_stream.start_stream() 
        else:
            print('Can not start stream! Device is not found.')
        return None


    def stop_streaming(self):
        ''' terminate port audio binding
        '''
        if self.dev_found_flag:
            # close stream
            self.audio_stream.stop_stream()
            self.audio_stream.close()
            # terminate pyaudio object
            self.p.terminate()
        
        return None
