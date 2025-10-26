import uuid
from datetime import datetime, timedelta
from random import randint

class Crop:
  def __init__(self, name, growth_time):
    self.id = str(uuid.uuid4())
    self.name = name
    self.growth_time = growth_time
    self.planted_time = datetime.now()
    self.is_ready = False
  
  def check_ready(self):
    if self.is_ready:
      return True
    
    elapsed = (datetime.now() - self.planted_time).total_seconds()
    if elapsed >= self.growth_time:
      self.is_ready = True
      return True
    return False
  
  def time_remaining(self):
    if self.is_ready:
      return 0
    
    elapsed = (datetime.now() - self.planted_time).total_seconds()
    remaining = max(0, self.growth_time - elapsed)
    return remaining
  
  def get_growth_percentage(self):
    if self.is_ready:
      return 100
    
    elapsed = (datetime.now() - self.planted_time).total_seconds()
    percentage = min(100, (elapsed / self.growth_time) * 100)
    return percentage
  
  def harvest(self):
    if self.check_ready():
      return {
        'name': self.name,
        'harvested_at': datetime.now(),
        'quantity': randint(2, 4)
      }
    else:
      return None
