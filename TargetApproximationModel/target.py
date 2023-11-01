


class Target():
    """
    Implementation of an articulatory target

    Parameters
    ----------
    onset_time : float
        The target starting point (in senconds)

    duration : float
        The target duration (in seconds)

    slope : float
        The linear slope parameter of the target

    offset : float
        The linear offset parameter of the target

    time_constant : float
        The time constant of the target (in seconds).
        Describes the rate at which the target is approached.

    onset_state : float
        Describes the target contour onset. This values should be set only if the contour should
        start from a different value than the respective target value. The contour will then
        approach the target instead of following it exactly.


    Attributes
    ----------
    onset_time : float
        Stores the target onset time

    duration : float
        Stores the target duration

    slope : float
        Stores the slope parameter

    offset : float
        Stores the offset parameter

    time_constant : float
        Stores the time constant parameter

    onset_state : float
        Stores the target onset state


    """ 
    def __init__(
        self,
        onset_time: float = 0.0, 
        duration: float = 1.0, 
        slope: float = 0.0, 
        offset: float = 1.0, 
        time_constant: float = 0.015,
        onset_state: float = None,
        ):
        self.onset_time = onset_time
        self.duration = duration
        self.slope = slope
        self.offset = offset
        self.time_constant = time_constant
        self.onset_state = onset_state
        return

    def m( self ):
        '''
        A convenience function to acces the target slope (often referred to as m)

        Parameters
        ----------


        Returns
        -------
        m : float
            The target slope parameter

        '''
        return self.slope

    def b( self ):
        '''
        A convenience function to acces the target offset (often referred to as b)

        Parameters
        ----------


        Returns
        -------
        b : float
            The target offset parameter
            
        '''
        return self.offset

    def tau( self ):
        '''
        A convenience function to acces the target time constant (often referred to as tau)

        Parameters
        ----------


        Returns
        -------
        tau : float
            The target time_constant parameter
            
        '''
        return self.time_constant

    def offset_time( self ):
        '''
        A function to acces the final target time instance (in seconds)

        Parameters
        ----------


        Returns
        -------
        offset_time : float
            The target onset time + the target duration
            
        '''
        return self.onset_time + self.duration