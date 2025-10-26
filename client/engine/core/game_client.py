from blessed import Terminal
from engine.core.state_manager import StateManager

class GameClient:
  """Main game client that manages the game loop and state"""
  
  def __init__(self):
    self.term = Terminal()
    self.state_manager = StateManager()
    self.players = []
    self.current_map = None
    self.player = None
    self.running = False
  
  def registerSystem(self, name, system):
    """Register a game system with the state manager"""
    self.state_manager.registerSystem(name, system)
  
  def getSystem(self, name):
    """Get a registered system"""
    return self.state_manager.getSystem(name)
  
  def setCurrentMap(self, map_obj):
    """Set the current active map"""
    self.current_map = map_obj
  
  def setPlayer(self, player):
    """Set the main player"""
    self.player = player
    if player not in self.players:
      self.players.append(player)
  
  def draw(self):
    """Draw the current game state"""
    print(self.term.home + self.term.clear)
    if self.current_map:
      self.current_map.init(self.players, self.term)
  
  def update(self):
    """Update game state (called every frame)"""
    # Update all registered systems
    self.state_manager.update()
    
    # Check for portal transitions
    if self.current_map and self.player:
      transition = self.current_map.checkPortalTransition(self.player)
      if transition:
        transition.execute(self.player, self.term)
        self.current_map = transition.getDestinationMap()
      
      # Handle collisions
      self.current_map.handleCollisions(self.player, self.draw, self.term)
  
  def gameLoop(self):
    """Main game loop"""
    self.running = True
    
    with self.term.fullscreen(), self.term.cbreak(), self.term.hidden_cursor():
      while self.running:
        if self.player and self.player.getHp() <= 0:
          self.showGameOver()
          break
        
        # Check if inventory is open
        if self.player and hasattr(self.player, 'getIsInventoryOpen') and self.player.getIsInventoryOpen():
          # Inventory UI will be handled by the game-specific code
          pass
        else:
          self.draw()
        
        # Handle player input
        if self.player:
          self.player.init(getattr(self, 'sio', None))
        
        self.update()
  
  def showGameOver(self):
    """Display game over screen"""
    print(self.term.home + self.term.clear)
    print(self.term.move_y(self.term.height // 2 - 3) + self.term.center(self.term.bold_red('=== GAME OVER ===')).rstrip())
    print(self.term.move_y(self.term.height // 2 - 1) + self.term.center(self.term.yellow('You have been defeated...')).rstrip())
    print()
    print(self.term.move_y(self.term.height // 2 + 6) + self.term.center(self.term.white('Press any key to exit...')).rstrip())
    self.term.inkey()
    self.running = False
  
  def stop(self):
    """Stop the game loop"""
    self.running = False
