#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: OFDM Loopback Example
# Description: Transmit a pre-defined signal (a complex sine) as OFDM packets.
# Generated: Mon Oct 14 03:04:59 2019
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import fullduplex
import sip
import sys
import time


class ofdm_loopback_example(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "OFDM Loopback Example")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("OFDM Loopback Example")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "ofdm_loopback_example")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1000000
        self.packet_len = packet_len = 192
        self.noise_voltage = noise_voltage = 0.1
        self.len_tag_key = len_tag_key = "packet_len"
        self.freq_offset = freq_offset = 0
        self.freq = freq = 910e6
        self.fft_len = fft_len = 64

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0.set_gain(0, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(freq, 0)
        self.uhd_usrp_sink_0.set_gain(0, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.qtgui_freq_sink_x_0_0_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"FFT Plot", #name
        	3 #number of inputs
        )
        self.qtgui_freq_sink_x_0_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0_0_0.enable_grid(True)
        self.qtgui_freq_sink_x_0_0_0.set_fft_average(0.05)
        self.qtgui_freq_sink_x_0_0_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_0_0_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0_0_0.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(3):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_0_0_win)
        self._noise_voltage_range = Range(0, 1, .01, 0.1, 200)
        self._noise_voltage_win = RangeWidget(self._noise_voltage_range, self.set_noise_voltage, "Noise Amplitude", "counter_slider", float)
        self.top_layout.addWidget(self._noise_voltage_win)
        self.fullduplex_SI_canceller_0 = fullduplex.SI_canceller(10)
        self._freq_offset_range = Range(-3, 3, .01, 0, 200)
        self._freq_offset_win = RangeWidget(self._freq_offset_range, self.set_freq_offset, "Frequency Offset (Multiples of Sub-carrier spacing)", "counter_slider", float)
        self.top_layout.addWidget(self._freq_offset_win)
        self.digital_ofdm_tx_0 = digital.ofdm_tx(
        	  fft_len=fft_len, cp_len=fft_len/4,
        	  packet_length_tag_key=len_tag_key,
        	  bps_header=1,
        	  bps_payload=2,
        	  rolloff=0,
        	  debug_log=False,
        	  scramble_bits=False
        	 )
        self.digital_ofdm_rx_0 = digital.ofdm_rx(
        	  fft_len=fft_len, cp_len=fft_len/4,
        	  frame_length_tag_key='frame_'+"rx_len",
        	  packet_length_tag_key="rx_len",
        	  bps_header=1,
        	  bps_payload=2,
        	  debug_log=False,
        	  scramble_bits=False
        	 )
        self.blocks_tag_gate_0_0 = blocks.tag_gate(gr.sizeof_char * 1, False)
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_gr_complex * 1, False)
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, packet_len, len_tag_key)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((0.05, ))
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, "/home/k/index4.jpeg", True)
        self.blocks_file_sink_2_0_1_0_0_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, "/home/k/youngmin/files/log_Source", False)
        self.blocks_file_sink_2_0_1_0_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_char*1, "/home/k/test1", False)
        self.blocks_file_sink_0_0.set_unbuffered(True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_tag_gate_0, 0))    
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.digital_ofdm_tx_0, 0))    
        self.connect((self.blocks_tag_gate_0, 0), (self.fullduplex_SI_canceller_0, 0))    
        self.connect((self.blocks_tag_gate_0, 0), (self.qtgui_freq_sink_x_0_0_0, 0))    
        self.connect((self.blocks_tag_gate_0, 0), (self.uhd_usrp_sink_0, 0))    
        self.connect((self.blocks_tag_gate_0_0, 0), (self.blocks_file_sink_0_0, 0))    
        self.connect((self.digital_ofdm_rx_0, 0), (self.blocks_tag_gate_0_0, 0))    
        self.connect((self.digital_ofdm_tx_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.fullduplex_SI_canceller_0, 0), (self.blocks_file_sink_2_0_1_0_0_0_0, 0))    
        self.connect((self.fullduplex_SI_canceller_0, 1), (self.qtgui_freq_sink_x_0_0_0, 2))    
        self.connect((self.uhd_usrp_source_0, 0), (self.digital_ofdm_rx_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.fullduplex_SI_canceller_0, 1))    
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_freq_sink_x_0_0_0, 1))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ofdm_loopback_example")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0_0_0.set_frequency_range(0, self.samp_rate)

    def get_packet_len(self):
        return self.packet_len

    def set_packet_len(self, packet_len):
        self.packet_len = packet_len
        self.blocks_stream_to_tagged_stream_0.set_packet_len(self.packet_len)
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt(self.packet_len)

    def get_noise_voltage(self):
        return self.noise_voltage

    def set_noise_voltage(self, noise_voltage):
        self.noise_voltage = noise_voltage

    def get_len_tag_key(self):
        return self.len_tag_key

    def set_len_tag_key(self, len_tag_key):
        self.len_tag_key = len_tag_key

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_sink_0.set_center_freq(self.freq, 0)
        self.uhd_usrp_source_0.set_center_freq(self.freq, 0)

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len


def main(top_block_cls=ofdm_loopback_example, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
