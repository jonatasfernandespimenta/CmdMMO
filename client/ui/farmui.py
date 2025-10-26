from arts.farm_elements import farm_house
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from player import Player
  from blessed import Terminal

class FarmUI:
  def __init__(self, player: 'Player', term: 'Terminal'):
    self.id = 'farm_plot_1'
    self.player: Player = player
    self.term: Terminal = term
    self.isOpen = False
  
  def checkIfPlayerOwnsFarm(self):
    for properties in self.player.getProperties():
      if properties['id'] == self.id and properties['owned']:
        return True
    return False

  def draw(self):
    print(self.term.home + self.term.clear)

    lines = farm_house.split('\n')
    for line in lines:
      print(self.term.yellow(line))

    if(self.checkIfPlayerOwnsFarm()):
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
    else:
      print()
      print(self.term.red('  You do not own this property. Please contact the landlord to purchase a farm plot.'))
      print()
      print(self.term.bold_cyan('=' * 60))
      print(self.term.white('  [Q] Exit'))
      print(self.term.bold_cyan('=' * 60))

  def handleExit(self, key):
    if key.lower() == 'q':
      currentPosition = self.player.getPlayerPosition()
      self.player.setPlayerPosition([currentPosition[0] + 1, currentPosition[1]])
      self.isOpen = False

  def open(self):
    self.isOpen = True
    
    while self.isOpen:
      self.draw()
      
      key = self.term.inkey(timeout=None)
      
      self.handleExit(key)
