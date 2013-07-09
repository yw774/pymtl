#=========================================================================
# SignalValue.py
#=========================================================================
# Module containing the SignalValue class.

#-------------------------------------------------------------------------
# SignalValue
#-------------------------------------------------------------------------
# Base class for value types, provides hooks used by SimulationTool.
# Any value that can be passed as a parameter to a Signal object
# (InPort, OutPort, Wire), needs to subclass SignalValue.
class SignalValue( object ):

  constant    = False
  _callbacks  = []
  _slices     = []

  #-----------------------------------------------------------------------
  # Write v property
  #-----------------------------------------------------------------------
  @property
  def v( self ):
    return self
  @property
  def value( self ):
    return self

  @v.setter
  def v( self, value ):
    if value != self:
      self.write( value )
      self.notify_sim_comb_update()
      for func in self._slices: func()
  @value.setter
  def value( self, value ):
    if value != self:
      self.write( value )
      self.notify_sim_comb_update()
      for func in self._slices: func()

  #-----------------------------------------------------------------------
  # Write n property
  #-----------------------------------------------------------------------
  @property
  def n( self ):
    return self._shadow_value
  @property
  def next( self ):
    return self._shadow_value

  @n.setter
  def n( self, value ):
    # TODO: get raw int value or copy obj?
    # TODO: implement as shadow_write() instead and make part of ABC?
    self._shadow_value.write( value )
    self.notify_sim_seq_update()
  @next.setter
  def next( self, value ):
    # TODO: get raw int value or copy obj?
    # TODO: implement as shadow_write() instead and make part of ABC?
    self._shadow_value.write( value )
    self.notify_sim_seq_update()

  #-----------------------------------------------------------------------
  # __setitem__
  #-----------------------------------------------------------------------
  # We need this to make writing to slices notify the sim correctly.
  # The notify_sim_slice_update function differs depending on if this
  # is a shadow SignalValue (points to notify_sim_comb_update), or not
  # (points to notify_sim_seq_update).  It's up to the SimulationTool
  # to set this.
  # TODO: this seems pretty hacky, better way?
  def __setitem__( self, addr, value ):
    self.write_slice( addr, value )
    self.notify_sim_slice_update()
    for func in self._slices: func()

  #-----------------------------------------------------------------------
  # flop
  #-----------------------------------------------------------------------
  # Update the value to match the _shadow_value (flop the register).
  def flop( self ):
    self.v = self._shadow_value

  #-----------------------------------------------------------------------
  # write (Abstract)
  #-----------------------------------------------------------------------
  # Abstract method, must be implemented by subclasses!
  # TODO: use abc module to create abstract method?
  def write( self, value ):
    raise NotImplementedError( "Subclasses of SignalValue must "
                               "implement the write() method!" )

  #-----------------------------------------------------------------------
  # write_slice (Abstract)
  #-----------------------------------------------------------------------
  # Abstract method, must be implemented by subclasses?
  # TODO: use abc module to create abstract method?
  def write_slice( self, addr, value ):
    raise NotImplementedError( "Subclasses of SignalValue must "
                               "implement the write_slice() method!" )

  #-----------------------------------------------------------------------
  # uint (Abstract)
  #-----------------------------------------------------------------------
  # Abstract method, must be implemented by subclasses!
  # TODO: use abc module to create abstract method?
  def uint( self, value ):
    raise NotImplementedError( "Subclasses of SignalValue must "
                               "implement the uint() method!" )

  #-----------------------------------------------------------------------
  # int (Abstract)
  #-----------------------------------------------------------------------
  # Abstract method, must be implemented by subclasses!
  # TODO: use abc module to create abstract method?
  def int( self, value ):
    raise NotImplementedError( "Subclasses of SignalValue must "
                               "implement the int() method!" )

  #-----------------------------------------------------------------------
  # is_constant
  #-----------------------------------------------------------------------
  # Returns true if this SignalValue contains a constant value which
  # should never be written.
  def is_constant( self ):
    return self.constant

  #-----------------------------------------------------------------------
  # notify_sim_comb_update
  #-----------------------------------------------------------------------
  # Notify simulator of combinational update.
  # Another abstract method used as a hook by simulator tools.
  # Not meant to be implemented by subclasses.
  # NOTE: This approach uses closures, other methods can be found in:
  #       http://brg.csl.cornell.edu/wiki/lockhart-2013-03-18
  #       Is this the fastest approach?
  def notify_sim_comb_update( self ):
    pass

  #-----------------------------------------------------------------------
  # notify_sim_seq_update
  #-----------------------------------------------------------------------
  # Notify simulator of sequential update.
  # Another abstract method used as a hook by simulator tools.
  # Not meant to be implemented by subclasses.
  # NOTE: This approach uses closures, other methods can be found in:
  #       http://brg.csl.cornell.edu/wiki/lockhart-2013-03-18
  #       Is this the fastest approach?
  def notify_sim_seq_update( self ):
    pass

  #-----------------------------------------------------------------------
  # notify_sim_slice_update
  #-----------------------------------------------------------------------
  # Notify simulator of sequential update.
  # Another abstract method used as a hook by simulator tools.
  # Not meant to be implemented by subclasses.
  # NOTE: This approach uses closures, other methods can be found in:
  #       http://brg.csl.cornell.edu/wiki/lockhart-2013-03-18
  #       Is this the fastest approach?
  def notify_sim_slice_update( self ):
    pass

  #-----------------------------------------------------------------------
  # register_callback
  #-----------------------------------------------------------------------
  def register_callback( self, func_ptr ):
    if not self._callbacks:
      self._callbacks = []
    self._callbacks.append( func_ptr )

  #-----------------------------------------------------------------------
  # register_slice
  #-----------------------------------------------------------------------
  def register_slice( self, func_ptr ):
    if not self._slices:
      self._slices = []
    self._slices.append( func_ptr )
