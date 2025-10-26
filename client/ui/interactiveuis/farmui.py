from arts.farm_elements import farm_house
from ui.interaction_ui import InteractionUI
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from player import Player
  from blessed import Terminal

class FarmUI:
  """UI for interacting with the farm"""
  
  def __init__(self, player: 'Player', term: 'Terminal'):
    self.id = 'farm_plot_1'
    self.player = player
    
    self.ui = InteractionUI(player, term, {
      'art': farm_house,
      'message': 'Welcome to your farm!',
      'show_gold': False,
      'options': [
        # Add farm-specific options here later
      ]
    })
  
  def checkIfPlayerOwnsFarm(self):
    """Check if player owns this farm"""
    for properties in self.player.getProperties():
      if properties['id'] == self.id and properties['owned']:
        return True
    return False
  
  def open(self):
    """Open the farm UI"""
    if not self.checkIfPlayerOwnsFarm():
      # Player doesn't own the farm, show different message
      self.ui.message = 'You need to buy this farm first!'
    else:
      self.ui.message = 'Welcome to your farm!'
    
    self.ui.open()
