from game.arts.merchant import merchant
from engine.ui.interaction_ui import InteractionUI
from game.items.potions import potions
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from game.entities.player import Player
  from blessed import Terminal

class AlchemistUI:
  def __init__(self, player: 'Player', term: 'Terminal'):
    self.player = player
    self.term = term
    
    self.ui = InteractionUI(player, term, {
      'art': merchant,
      'message': 'Welcome to the Alchemist! I can trade mushrooms for potions.',
      'show_gold': True,
      'options': [
        {
          'key': '1',
          'label': 'Trade 2 Mushrooms → Small Health Potion',
          'action': self.trade_small_potion
        },
        {
          'key': '2',
          'label': 'Trade 4 Mushrooms → Medium Health Potion',
          'action': self.trade_medium_potion
        },
        {
          'key': '3',
          'label': 'Buy Small Health Potion (100 gold)',
          'action': self.buy_small_potion
        },
        {
          'key': '4',
          'label': 'Buy Medium Health Potion (200 gold)',
          'action': self.buy_medium_potion
        }
      ]
    })
  
  def count_mushrooms(self):
    count = 0
    for item in self.player.inventory:
      if item.get('name') == 'Mushroom' and item.get('category') == 'material':
        count += 1
    return count
  
  def remove_mushrooms(self, amount):
    removed = 0
    for _ in range(amount):
      for item in self.player.inventory:
        if item.get('name') == 'Mushroom' and item.get('category') == 'material':
          self.player.inventory.remove(item)
          removed += 1
          break
    return removed
  
  def trade_small_potion(self):
    mushroom_count = self.count_mushrooms()
    if mushroom_count < 2:
      print(f"Not enough mushrooms! You have {mushroom_count}, need 2.")
      self.term.inkey(timeout=2)
      return
    
    self.remove_mushrooms(2)
    small_potion = next(p for p in potions if p['name'] == 'Small Healing Potion')
    self.player.addToInventory(small_potion)
    print("Traded 2 Mushrooms for Small Health Potion!")
    self.term.inkey(timeout=2)
  
  def trade_medium_potion(self):
    mushroom_count = self.count_mushrooms()
    if mushroom_count < 4:
      print(f"Not enough mushrooms! You have {mushroom_count}, need 4.")
      self.term.inkey(timeout=2)
      return
    
    self.remove_mushrooms(4)
    medium_potion = next(p for p in potions if p['name'] == 'Medium Healing Potion')
    self.player.addToInventory(medium_potion)
    print("Traded 4 Mushrooms for Medium Health Potion!")
    self.term.inkey(timeout=2)
  
  def buy_small_potion(self):
    if self.player.getGold() < 100:
      print(f"Not enough gold! You have {self.player.getGold()}, need 100.")
      self.term.inkey(timeout=2)
      return

    self.player.removeGold(100)
    small_potion = next(p for p in potions if p['name'] == 'Small Healing Potion')
    self.player.addToInventory(small_potion)
    print("Purchased Small Health Potion for 100 gold!")
    self.term.inkey(timeout=2)
  
  def buy_medium_potion(self):
    if self.player.getGold() < 200:
      print(f"Not enough gold! You have {self.player.getGold()}, need 200.")
      self.term.inkey(timeout=2)
      return
    
    self.player.removeGold(200)
    medium_potion = next(p for p in potions if p['name'] == 'Medium Healing Potion')
    self.player.addToInventory(medium_potion)
    print("Purchased Medium Health Potion for 200 gold!")
    self.term.inkey(timeout=2)
  
  def open(self):
    self.ui.open()
