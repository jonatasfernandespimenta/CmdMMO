from game.arts.farm_elements import farm_merchant
from engine.ui.interaction_ui import InteractionUI
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from game.entities.player import Player
  from blessed import Terminal

def add_property_to_player(item, ui):
  """Action to add property to player"""
  ui.player.addProperty(item)

class LandlordUI:
  """UI for interacting with the landlord (property vendor)"""
  
  def __init__(self, player: 'Player', term: 'Terminal'):
    self.ui = InteractionUI(player, term, {
      'art': farm_merchant,
      'message': 'Welcome! Looking to buy some property?',
      'show_gold': True,
      'items': [
        {
          'id': 'farm_plot_1',
          'name': 'Farm Plot',
          'price': 2500,
          'description': 'Your own farmland to grow crops',
          'owned': False,
          'action': add_property_to_player
        },
      ]
    })
  
  def open(self):
    """Open the landlord UI"""
    self.ui.open()
