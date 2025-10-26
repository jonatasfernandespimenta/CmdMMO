import random
from game.entities.enemy import Enemy
from game.items.materials import materials

class Snake(Enemy):
  def __init__(self, position, lines, level=1):
    self.base_hp = 10
    self.base_attack = 5
    self.base_defense = 2
    self.name = "Snake"
    
    super().__init__(position, lines, level)
    
    self.goldDrop = random.randint(level * 3, level * 8)
    self.xpDrop = random.randint(level * 8, level * 15)
    
    snake_skin = next(m for m in materials if m['name'] == 'Snake Skin')
    self.item_drops = [
      {'item': snake_skin, 'chance': 0.3}
    ]
