#!/usr/bin/env python
# -*- coding: utf-8 -*-


import warnings
import pandas as pd
from itertools import zip_longest

#import target
#from target_estimation import fit

from .target_approximation_filter import target_filter
from .harry_plotter import state_plot_kwargs
from .harry_plotter import finalize_plot
from .harry_plotter import get_plot
from .harry_plotter import get_plot_limits

from .target import Target

from typing import List, Optional, Dict, Any, Union, Tuple, Iterable


class TargetSequence():

    def __init__(
            self,
            targets: List[ Target ],
            name: Optional[ str ] = None,
            ):
        if not isinstance( targets, Iterable ):
            targets = [ targets ]
        self.targets = targets
        for index, target in enumerate( self.targets[ 1: ] ):
            target.onset_time = self.targets[ index ].offset_time()

        self.onset_time = self.targets[ 0 ].onset_time
        self.onset_state = self.targets[ 0 ].onset_state
        self.name = name
        return
    
    def __getitem__( self, index ):
        return self.targets[ index ]
    
    def __len__( self, ):
        return len( self.targets )
    
    def __iter__( self, ):
        return iter( self.targets )
    
    def __add__( self, other ):
        return TargetSequence( self.targets + other.targets )
    
    def __radd__( self, other ):
        return TargetSequence( other.targets + self.targets )
    
    #def __mul__( self, other ):
    #    return TargetSequence( self.targets * other )
    
    #def __rmul__( self, other ):
    #    return TargetSequence( self.targets * other )
    
    #def __repr__( self, ):
    #    return str( self.targets )
    
    def __str__( self, ):
        columns = [ 'onset_time', 'duration', 'slope', 'offset', 'time_constant' ]
        tgs_df = pd.DataFrame(
            [
                [
                    tg.onset_time,
                    tg.duration,
                    tg.m(),
                    tg.b(),
                    tg.tau(),
                    ]
                for tg in self.targets
            ],
            columns = columns,
            )
        return str( tgs_df )
    
    @classmethod
    def from_params(
            cls,
            durations: Union[ List[ float ], float ],
            offsets: Union[ List[ float ], float ],
            slopes: Union[ List[ float ], float ] = 0.0,
            time_constants: Union[ List[ float ], float ] =  0.015,
            onset_time: float = 0.0,
            onset_state: float = None,
            ):
        
        targets = []
        # check if some inputs are lists, then they should have the same length

        # Ensure that all input lists have the same length or convert constants to lists
        if not isinstance(durations, list):
            durations = [durations]
        if not isinstance(offsets, list):
            offsets = [offsets]
        if not isinstance(slopes, list):
            slopes = [slopes]
        if not isinstance(time_constants, list):
            time_constants = [time_constants]

        lengths = [ len(x) for x in [durations, offsets, slopes, time_constants] if x != 1 ]
        # check if all lengths are equal
        if len(set(lengths)) > 1:
            raise ValueError("All input lists must have the same length or be a single value.")

        # Create a list of Target objects
        targets = []
        for args in zip_longest( durations, slopes, offsets, time_constants ):
            duration, offset, slope, time_constant = args

            target = Target(
                onset_time=onset_time,
                duration=duration,
                slope=slope,
                offset=offset,
                time_constant=time_constant,
                onset_state=onset_state,
            )
            targets.append(target)

        return cls(targets)


    #@classmethod
    #def from_audio_file( cls, audio_file_path, **kwargs ):
    #    data = get_f0( audio_file_path )
    #    fit_result = fit( data[ 'time' ].to_numpy(), data[ 'f0' ].to_numpy(), **kwargs )
    #    return cls( targets = fit_result.out_targets, name = 'F0' )

    @classmethod
    def from_data( cls, data, name, **kwargs ):
        fit_result = fit( data[ :, 0 ], data[ :, 1 ], **kwargs )
        return cls( targets = fit_result.out_targets, name = name )

    def get_boundaries( self, ):
        #print( 'in get bound 1: {}'.format( self.onset_time ) )
        boundaries = [ self.onset_time ]
        for target in self.targets:
            boundaries.append( boundaries[ -1 ] + target.duration )
        #print( 'in get bound 2: {}'.format( self.onset_time ) )
        return boundaries

    def contour( self, sr: float = 500, sample_times = None ):
        contour = target_filter(
            target_sequence = self.targets,
            sample_rate = sr,
            onset_state = self.onset_state,
            sample_times = sample_times,
            )
        return contour

    def plot(
        self,
        plot_contour = True,
        plot_targets = True,
        ax = None,
        plot_kwargs = state_plot_kwargs,
        **kwargs,
        ): #, time = 'seconds'
        figure, ax = get_plot( n_rows = 1, axs = ax )
        if plot_contour:
            #tam = Target_Approximation_Model()
            #contour = tam.response( self.targets )
            contour = self.contour()
            contour_kwargs = plot_kwargs.get( self.name )
            if contour_kwargs == None:
                warnings.warn( 'The parameter: {} does not exist in the plot_kwargs dict, doing a standard plot now.'.format( self.name ) )
                contour_kwargs = dict( color = 'navy' )
            x = contour[ :, 0 ]
            #if time == 'samples':
            #    constants = vtl.get_constants()
            #    x *= constants[ 'samplerate_internal' ]
            ax[ 0 ].plot( x, contour[ :, 1 ], **contour_kwargs )
            ax[ 0 ].set( ylim = get_plot_limits( contour[ :, 1 ], 0.3 ) )
        if plot_targets:
            ax[ 0 ].axvline( self.targets[0].onset_time, color = 'black' )
            y_data = []
            for tar in self.targets:
                #x = tar.offset_time
                #if time == 'samples':
                #    constants = vtl.get_constants()
                #    x *= constants[ 'samplerate_internal' ]
                ax[ 0 ].axvline( tar.offset_time(), color = 'black' )
                x = [ tar.onset_time, tar.offset_time() ]
                y = [ tar.slope * (tar.onset_time-tar.onset_time) + tar.offset, tar.slope * (tar.offset_time()-tar.onset_time) + tar.offset ]
                ax[ 0 ].plot( x, y, color = 'black', linestyle='--' )
                y_data.append( y )
            if not plot_contour:
                ax[ 0 ].set( ylim = get_plot_limits( y_data, 0.3 ) )
        ax[ 0 ].set( xlabel = 'Time [s]', ylabel = self.name )
        #ax[ 0 ].label_outer()
        finalize_plot( figure, ax, **kwargs )
        return ax