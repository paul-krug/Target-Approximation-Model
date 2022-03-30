#!/usr/bin/env python
# -*- coding: utf-8 -*-



from .harry_plotter import finalize_plot
from .harry_plotter import get_plot
from .harry_plotter import get_plot_limits
from .harry_plotter import get_valid_tiers


#####################################################################################################################################################
#---------------------------------------------------------------------------------------------------------------------------------------------------#
class Target_Score():
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	"""Score of articulatory targets""" 
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def __init__(
		self,
		target_sequences: list, # target sequence objects
		):
		self.target_sequences = check_if_list_is_valid( target_sequences, Target_Sequence )
		return
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	@classmethod
	def from_targets( cls ):
		return cls( target_sequences )
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def names( self ):
		return [ target_sequence.name for target_sequence in self.target_sequences ]
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def plot( self, parameters = None, plot_contour = True, plot_targets = True, axs = None, **kwargs ):
		parameters = get_valid_tiers( parameters, self.names )
		figure, axs = get_plot( n_rows = len( parameters ), axs = axs )
		index = 0
		for target_sequence in self.target_sequences:
			if target_sequence.name in parameters:
				target_sequence.plot(
					plot_contour = plot_contour,
					plot_targets= plot_targets,
					ax = axs[ index ],
					show=False
					)
				index += 1
		finalize_plot( figure, axs, **kwargs )
		return
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#####################################################################################################################################################





#####################################################################################################################################################
#---------------------------------------------------------------------------------------------------------------------------------------------------#
class Synchronous_Target_Score( Target_Score ):
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	"""Synchronous score of articulatory targets""" 
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def __init__(
		self,
		durations: list,
		names: list,
		onset_time: float = 0.0,
		slope_score: list = [],
		offset_score: list = [],
		time_constant_score: list = [],
		):
		onset_time = onset_time
		self.target_sequences = []
		for args in zip_longest( names, slope_score, offset_score, time_constant_score ):
			#print( 'args: {}'.format(args) )
			args_corrected = []
			for x in args:
				try:
					if x == None:
						args_corrected.append( [] )
					else:
						args_corrected.append( x )
				except Exception:
					args_corrected.append( x )
			args = args_corrected
			#print( args )
			#args = [ [] if (not isinstance( x, list) ) and (x == None) else x for x in args]
			name, slopes, offsets, time_constants = args
			#print( 'na,e:{}, slopes:{}, off:{}, tico:{}'.format( name, slopes, offsets, time_constants) )
			self.target_sequences.append( Target_Sequence( onset_time, durations, slopes, offsets, time_constants, name = name ) )
		self.names = [ target_sequence.name for target_sequence in self.target_sequences ]
		return
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#####################################################################################################################################################