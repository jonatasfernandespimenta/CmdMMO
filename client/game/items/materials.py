from game.arts.materials import *

materials = [
  {
    'name': 'Snake Skin',
    'category': 'material',
    'rarity': 'common',
    'art': snake_skin,
    'sell_price': 5,
    'origins': ['enemy_drop']
  },
  {
    'name': 'Mushroom',
    'category': 'material',
    'rarity': 'uncommon',
    'art': mushroom,
    'sell_price': 25,
    'origins': ['harvest', 'enemy_drop', 'chest', 'merchant', 'forage', 'quest']
  }
]

seeds = [
  {
    'name': 'Mushroom Seed',
    'category': 'seed',
    'rarity': 'uncommon',
    'growth_time': 60,
    'art': seed,
    'sell_price': 10,
    'origins': ['harvest', 'enemy_drop', 'chest', 'merchant', 'forage', 'quest']
  }
]
