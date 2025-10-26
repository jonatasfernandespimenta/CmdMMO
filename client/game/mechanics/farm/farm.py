from typing import TYPE_CHECKING, TypedDict
from game.mechanics.farm.crop import Crop

if TYPE_CHECKING:
  from game.entities.player import Player

class FarmCrop(TypedDict):
  name: str
  growth_time: int
class Farm:
  def __init__(self, player: 'Player'):
    self.player = player
    self.crops = []
    self.silo = []

  def plantCrop(self, crop: FarmCrop):
    cropName = crop['name'].split(' Seed')[0]

    cropInstance = Crop(cropName, crop.get('growth_time', 60))
    self.crops.append(cropInstance)
    
  def getSilo(self):
    return self.silo

  def removeFromSilo(self, seedIndex):
    for seed in self.silo:
      if self.silo.index(seed) == seedIndex:
        self.silo.remove(seed)
        return seed

  def checkCrops(self):
    readyCrops = []
    for crop in self.crops:
      if crop.check_ready():
        readyCrops.append(crop)
    return readyCrops

  def harvestCrop(self, cropIndex):
    for crop in self.crops:
      if self.crops.index(crop) == cropIndex:
        harvestInfo = crop.harvest()
        if harvestInfo:
          self.player.inventory.append({
            'name': harvestInfo['name'],
            'category': 'material',
            'quantity': harvestInfo['quantity']
          })
          self.crops.remove(crop)
          return harvestInfo
    return None

  def storePlayerSeeds(self):
    playerInventory = self.player.getInventory()
    for item in playerInventory:
      if item['category'] == 'seed':
        self.silo.append(item)
        self.player.inventory.remove(item)
  
  def update_crops(self):
    for crop in self.crops:
      crop.check_ready()
  
  def harvest_crop(self, crop_id):
    for crop in self.crops:
      if crop.id == crop_id:
        if crop.check_ready():
          result = crop.harvest()
          self.crops.remove(crop)
          return result
        else:
          return {'error': 'Crop not ready', 'time_remaining': crop.time_remaining()}
    return {'error': 'Crop not found'}
  
  def get_all_crops_status(self):
    status = []
    for crop in self.crops:
      status.append({
        'id': crop.id,
        'name': crop.name,
        'is_ready': crop.check_ready(),
        'time_remaining': crop.time_remaining(),
        'growth_percentage': crop.get_growth_percentage()
      })
    return status
