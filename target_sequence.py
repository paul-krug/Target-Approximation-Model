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
        )
    
    tgs_2 = TargetSequence.from_params(
        durations = [ 0.1, 0.2, 0.3 ],
        offsets = [ 1, 2, 3 ],
        slopes = [ 0.1, 0.2, 0.3 ],
        time_constants = [ 0.01, 0.02, 0.03 ],
        )
    
    sum_tgs = tgs_1 + tgs_2

    tga = TargetScore( [ tgs_1, tgs_2, sum_tgs ] )

    print( tga )
    tga.plot()