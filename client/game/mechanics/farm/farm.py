from game.entities.player import Player

class Farm:
  def __init__(self, player: 'Player'):
    self.player = player
    self.crops = []

  def plantCrop(self, crop):
    playerInventory = self.player.getInventory()
