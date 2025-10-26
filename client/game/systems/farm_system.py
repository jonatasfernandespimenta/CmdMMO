import uuid

class Crop:
  def __init__(self, name, growth_time):
    self.id = str(uuid.uuid4())
    self.name = name
    self.growth_time = growth_time
    self.planted_time = None

class Farm:
  def __init__(self, player):
    self.player = player
    self.crops = []
