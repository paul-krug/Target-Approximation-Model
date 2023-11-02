#!/usr/bin/env python
# -*- coding: utf-8 -*-


from TargetApproximationModel.target import Target
from TargetApproximationModel.target_sequence import TargetSequence
from TargetApproximationModel.target_score import TargetScore

    
if __name__ == '__main__':
    tgs_1 = TargetSequence.from_params(
        durations = [ 0.1, 0.2, 0.3 ],
        offsets = [ 1, 2, 3 ],
        slopes = [ 0.1, 0.2, 0.3 ],
        time_constants = [ 0.01, 0.02, 0.03 ],
        name = 'tg1',
        )
    
    tgs_2 = TargetSequence.from_params(
        durations = [ 0.1, 0.2, 0.3 ],
        offsets = [ 1, 2, 3 ],
        slopes = [ 0.1, 0.2, 0.3 ],
        time_constants = [ 0.01, 0.02, 0.03 ],
        name = 'tg2',
        )
    
    sum_tgs = tgs_1 + tgs_2
    sum_tgs.name = 'sum_tgs'
    print( 'sum tgs name: ', sum_tgs.name )

    tga = TargetScore( [ tgs_1, tgs_2, sum_tgs ] )
    series = tga.to_time_series( sr = 5, sample_times = None )
    series.sr = None
    tga_from_series = TargetScore.from_series( series, durations = [ 0.1, 0.2, 0.3, 0.1, 0.2, 0.4,0.1 ] )
    print( series )
    stop

    import matplotlib.pyplot as plt
    fig, axs = plt.subplots( series.shape[ 1 ], 1 )
    for index, ax in enumerate( axs ):
        ax.plot( series[ :, index ] )

    plt.show()

    print( tga )
    #tga.plot()