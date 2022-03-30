

#import warnings
import numpy as np
#import pandas as pd
from scipy.special import binom
from scipy.special import factorial
#import matplotlib.pyplot as plt
#from itertools import zip_longest
#from itertools import chain
#from collections import Counter
from tools_io import is_iterable

import TargetApproximationModel

def target_filter(
	target_sequence: list,
	sample_rate: float = 44100 / 110,
	onset_state: float = None,
	sample_times: list = None,
	filter_order: int = 5,
	):
	if isinstance( target_sequence, TargetApproximationModel.Target_Sequence ):
		target_sequence = target_sequence.targets
	trajectory = []
	start = target_sequence[ 0 ].onset_time
	end   = target_sequence[ -1 ].offset_time()
	duration = end - start
	n_samples = duration * sample_rate
	if not is_iterable( sample_times ):
		sample_times = np.arange( start, end, duration / n_samples )
	#print( 'Len of sample times: {}'.format( len(sample_times) ) )
	#print( 'tam onset: {}'.format(onset_state) )
	if onset_state == None:
		onset_state = target_sequence[0].offset
	current_state = [ onset_state ]
	for _ in range( 1, filter_order ):
		current_state.append( 0.0 )
	b_begin = target_sequence[ 0 ].onset_time
	b_end = b_begin
	sample_index = 0
	for target in target_sequence:
		b_begin = b_end
		b_end = b_begin + target.duration
		c = _calculate_coefficients( target, current_state, filter_order )
		while( sample_times[ sample_index ] <= b_end +  0.000000000000001 ):
			#print( 'sample time: {}, b_end: {}'.format( sample_times[ sample_index ], b_end ) )
			constant = 0.0
			t = sample_times[ sample_index ] - b_begin
			for n in range( 0, filter_order ):
				constant += c[ n ] * ( t**n )
			time = sample_times[ sample_index ]
			value= constant * np.exp( - (1/target.time_constant) * t ) + target.slope * t + target.offset
			trajectory.append( [ time, value ] )
			sample_index += 1
			if sample_index >= len( sample_times ):
				return np.array( trajectory )
		current_state = _calculate_state( current_state, b_end, b_begin, target, filter_order );
	return np.array( trajectory )
#---------------------------------------------------------------------------------------------------------------------------------------------------#
def _calculate_coefficients(
	target,
	current_state,
	filter_order,
	):
	coefficients = [ 0 for _ in current_state ]
	assert len( coefficients ) == filter_order, 'Size conflict'
	coefficients[ 0 ] = current_state[ 0 ] - target.offset
	for n in range( 1, filter_order ):
		acc = 0
		for i in range( 0, n ):
			acc += ( coefficients[ i ] * ( (-1 / target.time_constant)**(n - i) ) * binom( n, i ) * factorial( i ) )
		if n == 1:
			acc += target.slope # adaption for linear targets; minus changes in following term!
		coefficients[ n ] = ( current_state[ n ] - acc ) / factorial( n )
	return coefficients
#---------------------------------------------------------------------------------------------------------------------------------------------------#
def _calculate_state(
	state,
	time,
	start_time,
	target,
	filter_order,
	):
	t = time - start_time
	state_update = [ 0 for _ in range( 0, filter_order ) ]
	c = _calculate_coefficients( target, state, filter_order)
	for n in range( 0, filter_order ):
		acc = 0
		for i in range( 0, filter_order ):
			q = 0
			for k in range( 0, np.min( [ filter_order - i, n + 1 ] ) ):
				q += ( ( (-1 / target.time_constant)**(n - k) ) * binom(n, k) * c[i + k] * factorial(k + i) / factorial(i) )
			acc += ( (t**i) * q );
		state_update[ n ] = acc * np.exp( -( 1 / target.time_constant) * t)
	# correction for linear targets
	if (filter_order > 1):
		state_update[ 0 ] += (target.offset + target.slope * t)
	if (filter_order > 2):
		state_update[ 1 ] += target.slope
	return state_update
#---------------------------------------------------------------------------------------------------------------------------------------------------#


















'''
#####################################################################################################################################################
#---------------------------------------------------------------------------------------------------------------------------------------------------#
class Target_Approximation_Filter():
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	"""Target-Approximation-Model filter""" 
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def __init__( self, order = 5 ):
		self.FILTERORDER = order
		return
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def response(
		self,
		target_sequence: list,
		sample_rate: float = 44100 / 110,
		onset_state: float = None,
		sample_times = None ) -> np.array:
		trajectory = []
		start = target_sequence[ 0 ].onset_time
		end   = target_sequence[ -1 ].offset_time
		duration = end - start
		n_samples = duration * sample_rate
		if not is_iterable( sample_times ):
			sample_times = np.arange( start, end, duration / n_samples )
		
		#print( 'Len of sample times: {}'.format( len(sample_times) ) )
		#print( 'tam onset: {}'.format(onset_state) )
		if onset_state == None:
			onset_state = target_sequence[0].offset
		current_state = [ onset_state ]
		for _ in range( 1, self.FILTERORDER ):
			current_state.append( 0.0 )

		b_begin = target_sequence[ 0 ].onset_time
		b_end = b_begin

		sample_index = 0

		for target in target_sequence:
			b_begin = b_end
			b_end = b_begin + target.duration
			c = self.calculate_coefficients( target, current_state )

			while( sample_times[ sample_index ] <= b_end +  0.000000000000001 ):
				#print( 'sample time: {}, b_end: {}'.format( sample_times[ sample_index ], b_end ) )
				constant = 0.0
				t = sample_times[ sample_index ] - b_begin
				for n in range( 0, self.FILTERORDER ):
					constant += c[ n ] * ( t**n )
				time = sample_times[ sample_index ]
				value= constant * np.exp( - (1/target.time_constant) * t ) + target.slope * t + target.offset
				trajectory.append( [ time, value ] )
				sample_index += 1
				if sample_index >= len( sample_times ):
					return np.array( trajectory )
			current_state = self.calculate_state( current_state, b_end, b_begin, target );

		return np.array( trajectory )
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def calculate_coefficients( self, target, current_state ):
		coefficients = [ 0 for _ in current_state ]
		assert len( coefficients ) == self.FILTERORDER, 'Sometimes size does matter bro...'
		coefficients[ 0 ] = current_state[ 0 ] - target.offset
		for n in range( 1, self.FILTERORDER ):
			acc = 0
			for i in range( 0, n ):
				acc += ( coefficients[ i ] * ( (-1 / target.time_constant)**(n - i) ) * binom( n, i ) * factorial( i ) )
			if n == 1:
				acc += target.slope # adaption for linear targets; minus changes in following term!
			coefficients[ n ] = ( current_state[ n ] - acc ) / factorial( n )
		return coefficients
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def calculate_state( self, state, time, start_time, target ):
		t = time - start_time
		state_update = [ 0 for _ in range( 0, self.FILTERORDER ) ]
		c = self.calculate_coefficients( target, state)
		for n in range( 0, self.FILTERORDER ):
			acc = 0
			for i in range( 0, self.FILTERORDER ):
				q = 0
				for k in range( 0, np.min( [ self.FILTERORDER - i, n + 1 ] ) ):
					q += ( ( (-1 / target.time_constant)**(n - k) ) * binom(n, k) * c[i + k] * factorial(k + i) / factorial(i) )
				acc += ( (t**i) * q );
			state_update[ n ] = acc * np.exp( -( 1 / target.time_constant) * t)
		# correction for linear targets
		if (self.FILTERORDER > 1):
			state_update[ 0 ] += (target.offset + target.slope * t)
		if (self.FILTERORDER > 2):
			state_update[ 1 ] += target.slope
		return state_update
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#####################################################################################################################################################
'''