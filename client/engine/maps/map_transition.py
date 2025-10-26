import time

class MapTransition:
  """Represents a transition between maps via portals"""
  
  def __init__(self, destination_map, player_spawn_position=[0, 0]):
    self.destination_map = destination_map
    self.player_spawn_position = player_spawn_position
  
  def execute(self, player, term):
    """Execute the transition (show message, change map, reposition player)"""
    raise NotImplementedError("Subclasses must implement execute()")
  
  def getDestinationMap(self):
    return self.destination_map
