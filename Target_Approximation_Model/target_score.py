#####################################################################################################################################################
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#	- This file is a part of the VocalTractLab Python module PyVTL, see https://github.com/paul-krug/VocalTractLab
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#
#	- Copyright (C) 2021, Paul Konstantin Krug, Dresden, Germany
#	- https://github.com/paul-krug/VocalTractLab
#	- Author: Paul Konstantin Krug, TU Dresden
#
#	- License info:
#
#		This program is free software: you can redistribute it and/or modify
#		it under the terms of the GNU General Public License as published by
#		the Free Software Foundation, either version 3 of the License, or
#		(at your option) any later version.
#		
#		This program is distributed in the hope that it will be useful,
#		but WITHOUT ANY WARRANTY; without even the implied warranty of
#		MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#		GNU General Public License for more details.
#		
#		You should have received a copy of the GNU General Public License
#		along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#####################################################################################################################################################
#---------------------------------------------------------------------------------------------------------------------------------------------------#

#---------------------------------------------------------------------------------------------------------------------------------------------------#
#####################################################################################################################################################
#---------------------------------------------------------------------------------------------------------------------------------------------------#
# Load essential packages:

#import warnings
#import numpy as np
#import pandas as pd
#from scipy.special import binom
#from scipy.special import factorial
#import matplotlib.pyplot as plt
#from itertools import zip_longest
#from itertools import chain
#from collections import Counter
#from VocalTractLab import plotting_tools as PT
from VocalTractLab.plotting_tools import finalize_plot
from VocalTractLab.plotting_tools import get_plot
#from VocalTractLab.plotting_tools import get_plot_limits
from VocalTractLab.plotting_tools import get_valid_tiers
#from VocalTractLab import function_tools as FT
#from VocalTractLab.function_tools import is_iterable
#from VocalTractLab import tract_sequence as TS
#from VocalTractLab.tract_sequence import Sub_Glottal_Sequence, Supra_Glottal_Sequence, Motor_Sequence
#from VocalTractLab.audio_tools import get_f0
#import VocalTractLab.VocalTractLabApi as vtl
#from VocalTractLab.target_estimation import fit




#####################################################################################################################################################
#---------------------------------------------------------------------------------------------------------------------------------------------------#
class Target_Score():
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	"""Score of articulatory targets""" 
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def __init__(
		self,
		target_sequences: list, #TODO target sequence objects
		):
		# #TODO target sequence objects
		self.target_sequences = target_sequences
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