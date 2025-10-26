class StateManager:
  """Manages persistent game state and systems (Farm, Quests, etc.)"""
  
  def __init__(self):
    self.systems = {}
  
  def registerSystem(self, name, system):
    """Register a game system"""
    self.systems[name] = system
  
  def getSystem(self, name):
    """Get a registered system"""
    return self.systems.get(name)
  
  def update(self):
    """Update all systems that need per-frame updates"""
    for system in self.systems.values():
      if hasattr(system, 'update'):
        system.update()
