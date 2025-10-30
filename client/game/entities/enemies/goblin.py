import random
from game.entities.enemy import Enemy
from game.items.materials import seeds

class Goblin(Enemy):
  def __init__(self, position, lines, level=1, term=None):
    self.base_hp = 15
    self.base_attack = 7
    self.base_defense = 3
    self.name = "Goblin"
    
    super().__init__(position, lines, level, term=term)
    
    self.goldDrop = random.randint(level * 10, level * 20)
    self.xpDrop = random.randint(level * 15, level * 30)
    
    mushroom_seed = next(s for s in seeds if s['name'] == 'Mushroom Seed')
    self.item_drops = [
      {'item': mushroom_seed, 'chance': 0.05}
    ]
