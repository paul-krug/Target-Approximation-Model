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

import pandas as pd
from itertools import zip_longest

import target
from target_estimation import fit
from target_approximation_filter import Target_Approximation_Filter

from harry_plotter import finalize_plot
from harry_plotter import get_plot
from harry_plotter import get_plot_limits



#####################################################################################################################################################
#---------------------------------------------------------------------------------------------------------------------------------------------------#
class Target_Sequence():
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	"""Sequence of articulatory targets""" 
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def __init__(
		self,
		onset_time: float = 0.0,
		durations: list = [],
		slopes: list = [],
		offsets: list = [],
		time_constants: list = [],
		onset_state: float = None,
		targets: list = None,
		name: str = '',
		):
		if targets != None:
			self.targets = targets
		else:
			self.targets = []
			function_argument_names = [ 'duration', 'slope', 'offset', 'time_constant' ]
			for idx_target, args in enumerate( zip_longest( durations, slopes, offsets, time_constants ) ):
				kwargs = {}
				kwargs[ 'onset_time' ] = onset_time
				for idx_member, arg in enumerate( args ):
					if arg != None:
						kwargs[ function_argument_names[ idx_member ] ] = arg
				self.targets.append( Target( **kwargs ) )
				onset_time += self.targets[ -1 ].duration
		self.onset_time = self.targets[ 0 ].onset_time
		if onset_state != None:
			self.onset_state = onset_state
		else:
			self.onset_state = self.targets[ 0 ].onset_state
		self.name = name
		return
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	#@classmethod
	#def from_audio_file( cls, audio_file_path, **kwargs ):
	#	data = get_f0( audio_file_path )
	#	fit_result = fit( data[ 'time' ].to_numpy(), data[ 'f0' ].to_numpy(), **kwargs )
	#	return cls( targets = fit_result.out_targets, name = 'F0' )
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	@classmethod
	def from_data( cls, data, name, **kwargs ):
		fit_result = fit( data[ :, 0 ], data[ :, 1 ], **kwargs )
		return cls( targets = fit_result.out_targets, name = name )
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def __str__( self, ):
		columns = [ 'onset_time', 'duration', 'slope', 'offset', 'time_constant' ]
		return str( pd.DataFrame( [ [ tar.onset_time, tar.duration, tar.m, tar.b, tar.tau ] for tar in self.targets ], columns = columns ) )
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def get_boundaries( self, ):
		#print( 'in get bound 1: {}'.format( self.onset_time ) )
		boundaries = [ self.onset_time ]
		for target in self.targets:
			boundaries.append( boundaries[ -1 ] + target.duration )
		#print( 'in get bound 2: {}'.format( self.onset_time ) )
		return boundaries
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def get_contour( self, sr: float = None, sample_times = None ):
		if sr == None:
			constants = vtl.get_constants()
			sr = constants[ 'samplerate_internal' ]
		tam = Target_Approximation_Filter()
		#print( 'get contour: {}'.format(self.onset_state) )
		contour = tam.response( target_sequence = self.targets,
			                    discretization_rate = sr,
			                    onset_state = self.onset_state,
			                    sample_times = sample_times,
			                    )
		return contour
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def plot(
		self,
		plot_contour = True,
		plot_targets = True,
		ax = None,
		plot_kwargs = PT.state_plot_kwargs,
		**kwargs,
		): #, time = 'seconds'
		figure, ax = get_plot( n_rows = 1, axs = ax )
		if plot_contour:
			#tam = Target_Approximation_Model()
			#contour = tam.response( self.targets )
			contour = self.get_contour()
			contour_kwargs = plot_kwargs.get( self.name )
			if contour_kwargs == None:
				warnings.warn( 'The parameter: {} does not exist in the plot_kwargs dict, doing a standard plot now.'.format( self.name ) )
				contour_kwargs = dict( color = 'navy' )
			x = contour[ :, 0 ]
			#if time == 'samples':
			#	constants = vtl.get_constants()
			#	x *= constants[ 'samplerate_internal' ]
			ax[ 0 ].plot( x, contour[ :, 1 ], **contour_kwargs )
			ax[ 0 ].set( ylim = get_plot_limits( contour[ :, 1 ], 0.3 ) )
		if plot_targets:
			ax[ 0 ].axvline( self.targets[0].onset_time, color = 'black' )
			y_data = []
			for tar in self.targets:
				#x = tar.offset_time
				#if time == 'samples':
				#	constants = vtl.get_constants()
				#	x *= constants[ 'samplerate_internal' ]
				ax[ 0 ].axvline( tar.offset_time, color = 'black' )
				x = [ tar.onset_time, tar.offset_time ]
				y = [ tar.slope * (tar.onset_time-tar.onset_time) + tar.offset, tar.slope * (tar.offset_time-tar.onset_time) + tar.offset ]
				ax[ 0 ].plot( x, y, color = 'black', linestyle='--' )
				y_data.append( y )
			if not plot_contour:
				ax[ 0 ].set( ylim = get_plot_limits( y_data, 0.3 ) )
		ax[ 0 ].set( xlabel = 'Time [s]', ylabel = self.name )
		#ax[ 0 ].label_outer()
		finalize_plot( figure, ax, **kwargs )
		return ax
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#####################################################################################################################################################