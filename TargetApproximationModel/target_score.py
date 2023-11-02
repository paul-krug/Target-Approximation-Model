#!/usr/bin/env python        
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

from .harry_plotter import finalize_plot
from .harry_plotter import get_plot
from .harry_plotter import get_plot_limits
from .harry_plotter import get_valid_tiers
from .target_sequence import TargetSequence

from typing import List, Optional, Dict, Any, Union, Tuple, Iterable


def read_tract_seq_GLP( index ):
	if (index > 7) and (index % 2 == 0):
		return False
	else:
		return True

def read_tract_seq_VTP( index ):
	if (index > 7) and ((index-1) % 2 == 0):
		return False
	else:
		return True


class MotorSeries( TargetSeries ):
    
    def __init__(
            self,
            series: np.ndarray,
            sr: float,
            ):
        tiers = [
            'VX',
            'VO',
            'TRX',
        ]
        super().__init__( series, sr, tiers )
        return
    
    @classmethod
    def from_motor_file(
            cls,
            path: str,
            sr = None,
            ):
        if sr is None:
            sr = 44100/110 #Dont use hardcode here but vtl_constants
        df = pd.read_csv(
            path,
            delim_whitespace = True,
            skiprows= lambda x: _read_tract_seq_VTP(x),
            header = None,
            )
        df_GLP = pd.read_csv( tract_file_path, delim_whitespace = True, skiprows= lambda x: read_tract_seq_GLP(x) , header = None )
		df_VTP = pd.read_csv( tract_file_path, delim_whitespace = True, skiprows= lambda x: read_tract_seq_VTP(x) , header = None )
		return cls( Supra_Glottal_Sequence( df_VTP.to_numpy() ), Sub_Glottal_Sequence( df_GLP.to_numpy() ), tract_file_path )
        return cls( df.to_numpy(), sr = sr )
    
    





class TargetSeries():

    def __init__(
            self,
            series: np.ndarray,
            sr: float,
            tiers: List[ str ],
            ):
        print( f'len tiers: { len( tiers ) }' )
        print( f'series shape: { series.shape }' )
        if len( tiers ) != series.shape[ 0 ]:
            raise ValueError( 'tiers and series must have the same length' )
        self.series = pd.DataFrame( series.T, columns = tiers )
        self.sr = sr
        self.tiers = tiers
        print( 'tiers: ', self.tiers )
        if len( set( self.tiers ) ) != len( self.tiers ):
            raise ValueError( 'tiers must be unique' )
        return
    
    def __str__(self) -> str:
        return self.series.__str__()
    
    def to_target_score(
            self,
            durations: List[ float ],
            onset_time: float = 0.0,
            ):
        return TargetScore.from_series(
            series = self,
            durations = durations,
            onset_time = onset_time,
            )
    


def pad_sequences( sequences, maxlen=None ):
    #print( sequences )
    #print( sequences.shape )
    max_length = max( len( x ) for x in sequences )
    padded = np.zeros( ( len( sequences ), max_length ) )
    for index, sequence in enumerate( sequences ):
        padded[ index, :len( sequence ) ] = sequence
    print( padded.shape )
    #stop
    return padded



class TargetScore():

    def __init__(
        self,
        target_sequences: List[ TargetSequence ],
        ):
        if not isinstance( target_sequences, Iterable ):
            target_sequences = [ target_sequences ]
        self.target_sequences = target_sequences
        # if there are non unique names, raise error
        print( 'tiers: ', self.tiers() )
        if len( set( self.tiers() ) ) != len( self.tiers() ):
            raise ValueError( 'target sequence names must be unique' )
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
    
    @classmethod
    def from_series(
            self,
            series: TargetSeries,
            durations: List[ float ],
            onset_time: float = 0.0,
            ):
        target_sequences = []
        for tier in series.tiers:
            if series.sr is not None:
                target_sequences.append(
                    TargetSequence.from_fit(
                        data = np.array( series.series[ tier ].values )[0],
                        name = tier,
                        sr = series.sr,
                        )
                    )
            else:
                target_sequences.append(
                    TargetSequence.from_params(
                        durations = durations,
                        offsets = series.series.loc[ :, tier ].values.tolist(),
                        name = tier,
                        onset_time = onset_time,
                        )
                    )
        return TargetScore( target_sequences )
        
    def tiers( self ):
        return [ target_sequence.name for target_sequence in self.target_sequences ]
    
    def contour(
            self,
            sr: float = 500,
            sample_times = None,
            ):
        contours = [
            target_sequence.contour(
                sr = sr,
                sample_times = sample_times,
                )[ :, 1]
            for target_sequence in self.target_sequences
            ]
        target_time_series = pad_sequences( contours )
        return target_time_series

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
    
    def to_time_series( self, sr, sample_times = None ):
        contour = self.contour( sr = sr, sample_times = sample_times )
        return TargetSeries( contour, sr, self.tiers() )






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