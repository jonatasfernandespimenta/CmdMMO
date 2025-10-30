import random
from game.entities.enemy import Enemy
from game.items.materials import materials
from game.skills.fighting_abilities import fighting_abilities

class Snake(Enemy):
  def __init__(self, position, lines, level=1, term=None):
    self.base_hp = 25
    self.base_attack = 10
    self.base_defense = 5
    self.name = "Snake"
    
    super().__init__(position, lines, level, term=term)
    
    self.goldDrop = random.randint(level * 3, level * 8)
    self.xpDrop = random.randint(level * 8, level * 15)
    
    # Snake skills - poison focused
    self.skills = ["poison_bite", "venomous_strike"]
    
    snake_skin = next(m for m in materials if m['name'] == 'Snake Skin')
    self.item_drops = [
      {'item': snake_skin, 'chance': 0.3}
    ]
