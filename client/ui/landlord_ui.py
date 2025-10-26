from arts.farm_elements import farm_merchant
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from player import Player
  from blessed import Terminal

class LandlordUI:
  """UI for interacting with the landlord (property vendor)"""
  
  def __init__(self, player: 'Player', term: 'Terminal'):
    self.player: Player = player
    self.term: Terminal = term
    self.isOpen = False
    self.properties = [
      {
        'id': 'farm_plot_1',
        'name': 'Farm Plot',
        'price': 2500,
        'description': 'Your own farmland to grow crops',
        'owned': False
      },
    ]
  
  def draw(self):
    """Draw the landlord UI"""
    print(self.term.home + self.term.clear)
    
    # Draw merchant art
    merchantLines = farm_merchant.split('\n')
    for line in merchantLines:
      print(self.term.yellow(line))
    
    print()
    print(self.term.yellow('  Welcome! Looking to buy some property?'))
    print(self.term.white('  Your Gold: ') + self.term.bold_yellow(str(self.player.getGold())))
    print()
    
    for i, prop in enumerate(self.properties):
      status = self.term.green('[OWNED]') if prop['owned'] else self.term.yellow(f"[{prop['price']} Gold]")
      print(self.term.white(f"  {i+1}. ") + self.term.bold(prop['name']) + ' ' + status)
      print(self.term.white(f"     {prop['description']}"))
      print()
    
    print(self.term.bold_cyan('=' * 60))
    print(self.term.white('  [1-3] Buy property | [Q] Exit'))
    print(self.term.bold_cyan('=' * 60))

  def handleExit(self, key):
    if key.lower() == 'q':
      currentPosition = self.player.getPlayerPosition()
      self.player.setPlayerPosition([currentPosition[0] + 1, currentPosition[1]])
      self.isOpen = False

  def open(self):
    """Open the landlord UI and handle interactions"""
    self.isOpen = True
    
    while self.isOpen:
      self.draw()
      
      key = self.term.inkey(timeout=None)
      
      self.handleExit(key)

      if key in ['1', '2', '3']:
        propIndex = int(key) - 1
        self.buyProperty(propIndex)
  
  def buyProperty(self, index):
    """Attempt to buy a property"""
    if index < 0 or index >= len(self.properties):
      return
    
    prop = self.properties[index]
    
    if prop['owned']:
      print(self.term.move_y(self.term.height - 2) + self.term.center(self.term.red('You already own this property!')).rstrip())
      self.term.inkey(timeout=2)
      return
    
    if self.player.getGold() < prop['price']:
      print(self.term.move_y(self.term.height - 2) + self.term.center(self.term.red('Not enough gold!')).rstrip())
      self.term.inkey(timeout=2)
      return
    
    # Purchase successful
    self.player.addGold(-prop['price'])
    prop['owned'] = True
    self.player.addProperty(prop)
    print(self.term.move_y(self.term.height - 2) + self.term.center(self.term.bold_green(f'Purchased {prop["name"]}!')).rstrip())
    self.term.inkey(timeout=2)
