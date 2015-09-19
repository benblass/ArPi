#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Sat Sep 19 12:24:55 2015
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
import fcdproplus
import stbpilot
import threading
import time

class top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 192000
        self.pulse_width = pulse_width = 0.07
        self.pseudo_frequency = pseudo_frequency = 1
        self.fft_size = fft_size = 1024
        self.blocksize = blocksize = int(samp_rate / fft_size * pseudo_frequency *1.0 / (1.0 / pulse_width))  / 2
        self.timeout_blocks = timeout_blocks = int(samp_rate/fft_size * 1.0/blocksize)
        self.target_freq = target_freq = 457000
        self.measure = measure = 0
        self.firdes_tap = firdes_tap = firdes.low_pass(1, samp_rate, 500, 1000, firdes.WIN_HAMMING, 6.76)
        self.base_freq = base_freq = 450000
        self.burst_trigger = burst_trigger = 0.75

        ##################################################
        # Blocks
        ##################################################
        self.probe = blocks.probe_signal_f()
        self.stbpilot_signal_level_0 = stbpilot.signal_level(6, timeout_blocks)
        def _measure_probe():
            while True:
                val = self.probe.level()
                try:
                    self.set_measure(val)
                    print "Signal : " + str(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (1))
        _measure_thread = threading.Thread(target=_measure_probe)
        _measure_thread.daemon = True
        _measure_thread.start()
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, (firdes_tap), -(base_freq - target_freq), samp_rate)
        self.fft_vxx_0 = fft.fft_vcc(fft_size, True, (), True, 1)
        self.fcdproplus_fcdproplus_0 = fcdproplus.fcdproplus("",1)
        self.fcdproplus_fcdproplus_0.set_lna(1)
        self.fcdproplus_fcdproplus_0.set_mixer_gain(1)
        self.fcdproplus_fcdproplus_0.set_if_gain(0)
        self.fcdproplus_fcdproplus_0.set_freq_corr(0)
        self.fcdproplus_fcdproplus_0.set_freq(base_freq)
          
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, fft_size)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(burst_trigger, burst_trigger, 0)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_size)
        self.blocks_skiphead_0 = blocks.skiphead(gr.sizeof_float*1, (int(target_freq*1.0*fft_size/samp_rate)+1)*0+513)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_keep_one_in_n_1 = blocks.keep_one_in_n(gr.sizeof_float*1, fft_size)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.fft_vxx_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.fcdproplus_fcdproplus_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_keep_one_in_n_1, 0), (self.blocks_threshold_ff_0, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_keep_one_in_n_1, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_skiphead_0, 0))
        self.connect((self.blocks_skiphead_0, 0), (self.blocks_keep_one_in_n_1, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.stbpilot_signal_level_0, 0))
        self.connect((self.stbpilot_signal_level_0, 0), (self.probe, 0))



    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_firdes_tap(firdes.low_pass(1, self.samp_rate, 500, 1000, firdes.WIN_HAMMING, 6.76))
        self.set_timeout_blocks(int(self.samp_rate/self.fft_size * 1.0/self.blocksize))
        self.set_blocksize(int(self.samp_rate / self.fft_size * self.pseudo_frequency *1.0 / (1.0 / self.pulse_width))  / 2)

    def get_pulse_width(self):
        return self.pulse_width

    def set_pulse_width(self, pulse_width):
        self.pulse_width = pulse_width
        self.set_blocksize(int(self.samp_rate / self.fft_size * self.pseudo_frequency *1.0 / (1.0 / self.pulse_width))  / 2)

    def get_pseudo_frequency(self):
        return self.pseudo_frequency

    def set_pseudo_frequency(self, pseudo_frequency):
        self.pseudo_frequency = pseudo_frequency
        self.set_blocksize(int(self.samp_rate / self.fft_size * self.pseudo_frequency *1.0 / (1.0 / self.pulse_width))  / 2)

    def get_fft_size(self):
        return self.fft_size

    def set_fft_size(self, fft_size):
        self.fft_size = fft_size
        self.set_timeout_blocks(int(self.samp_rate/self.fft_size * 1.0/self.blocksize))
        self.set_blocksize(int(self.samp_rate / self.fft_size * self.pseudo_frequency *1.0 / (1.0 / self.pulse_width))  / 2)
        self.blocks_keep_one_in_n_1.set_n(self.fft_size)

    def get_blocksize(self):
        return self.blocksize

    def set_blocksize(self, blocksize):
        self.blocksize = blocksize
        self.set_timeout_blocks(int(self.samp_rate/self.fft_size * 1.0/self.blocksize))

    def get_timeout_blocks(self):
        return self.timeout_blocks

    def set_timeout_blocks(self, timeout_blocks):
        self.timeout_blocks = timeout_blocks

    def get_target_freq(self):
        return self.target_freq

    def set_target_freq(self, target_freq):
        self.target_freq = target_freq
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(-(self.base_freq - self.target_freq))

    def get_measure(self):
        return self.measure

    def set_measure(self, measure):
        self.measure = measure

    def get_firdes_tap(self):
        return self.firdes_tap

    def set_firdes_tap(self, firdes_tap):
        self.firdes_tap = firdes_tap
        self.freq_xlating_fir_filter_xxx_0.set_taps((self.firdes_tap))

    def get_base_freq(self):
        return self.base_freq

    def set_base_freq(self, base_freq):
        self.base_freq = base_freq
        self.fcdproplus_fcdproplus_0.set_freq(self.base_freq)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(-(self.base_freq - self.target_freq))

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = top_block()
    tb.start()
    tb.wait()
