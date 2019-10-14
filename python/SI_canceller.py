#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2019 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr

class SI_canceller(gr.sync_block):
    """
    docstring for block SI_canceller
    """
    def __init__(self, No_points):
        self.No_points = No_points
        self.passed_index = 0
	self.flag = 1
	self.thres = 0.05
        self.padding = 5   # to synchronize between RX and TX packet
	self.queue = [0 for i in range(self.padding)]  # queue as list
        self.queue_fltr = []  # queue as list
        self.temp_mem = []
        self.initial = 1 # is this the first frame? 
        self.A_vec = numpy.array([0 for i in range(self.No_points)])
        self.N_cut = 10 # to ignore the first few samples of RX and SRC stream to remove the distortion at the transient phase 
	self.N_max_filter = 200 # to limit the number of samples used to calculate filter 
        gr.sync_block.__init__(self,
            name="SI_canceller",
            in_sig=[numpy.complex64,numpy.complex64],
            out_sig=[numpy.complex64,numpy.complex64])


    def work(self, input_items, output_items):
        in0 = input_items[0]
        in1 = input_items[1]
        out0 = output_items[0]
	out1 = output_items[1]
        # <+signal processing here+>
        N_output = len(output_items[0])
        N_points = self.No_points
        k = 0
        self.temp_mem[:] = in0   #np array to list
        self.queue.extend(self.temp_mem)  # list extention
        #self.queue = numpy.concatenate((self.queue,in0),axis=None)
        
        if (self.flag == 1 and self.initial == 0):
            out_temp = numpy.absolute(in1[:])
            while(k < N_output):
    	        if(out_temp[k] > self.thres):
        	    self.flag = 2
        	    self.delay = k + self.passed_index
                    break
    	        k += 1
	
        out1[:] = in1
        if self.flag == 1:
	    out0[:] = numpy.zeros(N_output,dtype=complex)
            #out1[:] = in1       
        elif self.flag == 2:
            ## matrix calculation
            print('N_ouptut:{}, k;{}, N_output-k:{}, delay:{}'.format(N_output,k,N_output-k,self.delay))
	    R_W = numpy.zeros([N_points,N_points],dtype=complex)
            R_SW = numpy.zeros(N_points,dtype=complex)
            if (N_output-k < self.N_max_filter):
	        for n in range(N_points):
	            for m in range(N_points):
            	        i = int(numpy.abs(n-m))
			if (n < m or (n == 0 and m ==0)):            	        
			    #R_W[n,m] = numpy.mean(numpy.multiply(in1[k:N_output-(N_points-1)],numpy.conj(in1[k+i:N_output-(N_points-1)+i])))
            	            R_W[n,m] = numpy.mean(numpy.multiply(self.queue[0:(N_output-k)-(N_points-1)],numpy.conj(self.queue[i:(N_output-k)-(N_points-1)+i])))
		        elif n == m:
                            R_W[n,m] = R_W[0,0]
                        else:
                            R_W[n,m] = R_W[m,n]
	        for n in range(N_points):
    	            #R_SW[n] = numpy.mean(numpy.multiply(in1[k:N_output-(N_points-1)],numpy.conj(self.queue[n:N_output-(N_points-1)-k+n])))
                    R_SW[n] = numpy.mean(numpy.multiply(self.queue[self.N_cut:(N_output-k)-(N_points-1)],numpy.conj(in1[self.N_cut+k+n:N_output-(N_points-1)+n])))
	    else:
                for n in range(N_points):
	            for m in range(N_points):
            	        i = int(numpy.abs(n-m))
                        if (n < m or (n == 0 and m ==0)):
			    R_W[n,m] = numpy.mean(numpy.multiply(self.queue[0:self.N_max_filter-(N_points-1)],numpy.conj(self.queue[i:self.N_max_filter-(N_points-1)+i])))
			elif n == m:
                            R_W[n,m] = R_W[0,0]
                        else:
                            R_W[n,m] = R_W[m,n] 
		for n in range(N_points):
                    R_SW[n] = numpy.mean(numpy.multiply(self.queue[self.N_cut:self.N_max_filter-(N_points-1)],numpy.conj(in1[self.N_cut+k+n:self.N_max_filter+k-(N_points-1)+n])))

	    #print(R_W)
	    #print(R_SW)
	    self.A_vec = numpy.matmul(numpy.linalg.inv(R_W),numpy.conj(R_SW))
	    #self.A_vec = numpy.zeros(N_points,dtype=complex)
            #self.A_vec[0] = 1
            #print(self.A_vec)
            # src signal if you want to bypass tx stream after synchronizing with rx stream 
	    #out0[:k] = numpy.zeros(k,dtype=complex)
            #out0[k:] = self.queue[:(N_output-k)] 
	    #del self.queue[:(N_output-k)]	    
	    
            # filter output with tx stream as input for the first time, rx_stream - filter_output_stream
            out0[:k] = numpy.zeros(k,dtype=complex)  # before the start of the rx stream	    
            temp_1 = numpy.convolve(self.A_vec,self.queue[:(N_output-k)])  # filtering
	    out0[k:] = temp_1[:(N_output-k)] 
	    del self.queue[:(N_output-k-(N_points-1))] # keep the N_points-1 previous samples

            # SI cancellation
            out1[:] = out1[:] - out0[:]  
	    
            # filter output with tx stream as input for the first time, filter_output_stream - source_stream 
	    #self.queue_fltr.extend(in1)
            #temp_1 = numpy.convolve(self.A_vec,self.queue_fltr)  # filter pass
            #out1[:] = temp_1[:N_output]  # take the first N_output symbols
            #del self.queue_fltr[:(N_output-(N_points-1))]  # remain the last N_points symbols to be used as filter input 
            
            self.flag = 3
        else: 
	    # src signal if you want to bypass tx stream after synchronizing with rx stream
            #out0[:] = self.queue[:N_output]
            #del self.queue[:N_output] 
	    #out0[:] = in0

	    # filter output with tx stream as input for the second time, rx_stream - filter_output_stream            #self.queue_fltr.extend(in1)
            temp_1 = numpy.convolve(self.A_vec,self.queue[:N_output+N_points-1])  # filter pass
       	    out0[:] = temp_1[N_points-1:N_output+N_points-1]
            del self.queue[:N_output]
            out1[:] = out1[:] - out0[:]

            # filter output with rx stream as input for the second time, filter_output_stream - source_stream 
            #self.queue_fltr.extend(in1)
            #temp_1 = numpy.convolve(self.A_vec,self.queue_fltr)  # filter pass
       	    #out1[:] = temp_1[]
            #del self.queue_fltr[:N_output]
            #out1[:] = out1[:] - out0[:]
        #print(self.passed_index) 
        self.passed_index += len(output_items[0])
        self.initial = 0  # denotes the first frame has passed. we need to avoid the first frame because the impulse at the first few symbols
        return len(output_items[0])


