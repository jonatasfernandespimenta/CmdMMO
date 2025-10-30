from game.arts.shitpost import yago_ui
from engine.ui.interaction_ui import InteractionUI
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from game.entities.player import Player
  from blessed import Terminal

class YagoUI:
  """UI para interagir com o Yago"""
  
  def __init__(self, player: 'Player', term: 'Terminal'):
    self.ui = InteractionUI(player, term, {
      'art': yago_ui,
      'message': 'oh os cara ai meu',
      'show_gold': False,
      'items': []
    })
  
  def open(self):
    """Abrir a UI do Yago"""
    self.ui.open()
