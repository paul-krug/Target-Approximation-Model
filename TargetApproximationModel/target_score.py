#!/usr/bin/env python        
# -*- coding: utf-8 -*-



from .harry_plotter import finalize_plot
from .harry_plotter import get_plot
from .harry_plotter import get_plot_limits
from .harry_plotter import get_valid_tiers
from .target_sequence import TargetSequence

from typing import List, Optional, Dict, Any, Union, Tuple, Iterable





class TargetScore():

    def __init__(
        self,
        target_sequences: List[ TargetSequence ],
        ):
        if not isinstance( target_sequences, Iterable ):
            target_sequences = [ target_sequences ]
        self.target_sequences = target_sequences
        return
    
    def __getitem__( self, index ):
        return self.target_sequences[ index ]
    
    def __len__( self, ):
        return len( self.target_sequences )
    
    def __iter__( self, ):
        return iter( self.target_sequences )

    @classmethod
    def from_params():
        return

    def names( self ):
        return [ target_sequence.name for target_sequence in self.target_sequences ]

    def plot(
            self,
            plot_tiers: Optional[ List[ str ] ] = None,
            plot_contour = True,
            plot_targets = True,
            axs = None,
            **kwargs,
            ):
        #if plot_tiers is
        figure, axs = get_plot( n_rows = len( self ), axs = axs )
        index = 0
        for target_sequence in self.target_sequences:
                target_sequence.plot(
                    plot_contour = plot_contour,
                    plot_targets= plot_targets,
                    ax = axs[ index ],
                    show=False
                    )
                index += 1
        finalize_plot( figure, axs, **kwargs )
        return






class Synchronous_Target_Score( TargetScore ):
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