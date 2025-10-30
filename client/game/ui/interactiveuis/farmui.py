from game.arts.farm_elements import farm_house
from engine.ui.interaction_ui import InteractionUI
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from game.entities.player import Player
  from blessed import Terminal

class FarmUI:
  """UI for interacting with the farm"""
  def __init__(self, player: 'Player', term: 'Terminal'):
    self.id = 'farm_plot_1'
    self.player = player
    self.farm = player.farm
    self.term = term
    
    # Build options based on ownership
    options = []
    if self.checkIfPlayerOwnsFarm():
      options = [
        {
          'key': '1',
          'label': 'View Silo',
          'action': self.viewSilo
        },
        {
          'key': '2',
          'label': 'Plant Crops',
          'action': self.plantCrop
        },
        {
          'key': '3',
          'label': 'Check Crops Status',
          'action': self.checkCrops
        },
        {
          'key': '4',
          'label': 'Store seeds from Inventory',
          'action': self.storeSeeds
        }
      ]
    
    self.ui = InteractionUI(player, term, {
      'art': farm_house,
      'message': 'Welcome to your farm!' if self.checkIfPlayerOwnsFarm() else 'You need to buy this farm first!',
      'show_gold': False,
      'options': options
    })

  def viewSilo(self):
    silo = self.farm.getSilo()
    if not silo:
      print("The silo is empty.")
      self.ui.term.inkey(timeout=2)
      return
    
    print("Seeds in silo:")
    for seed in silo:
      print(f"- {seed['name']}")
    self.ui.term.inkey(timeout=2)
  
  def storeSeeds(self):
    self.farm.storePlayerSeeds()
    print("Seeds have been stored in the silo.")
    self.ui.term.inkey(timeout=2)

  def checkCrops(self):
    allCrops = self.farm.crops
    if not allCrops:
      print("You have no crops planted.")
      self.ui.term.inkey(timeout=2)
      return

    readyCrops = []
    growingCrops = []
    
    for crop in allCrops:
      if crop.check_ready():
        readyCrops.append(crop)
      else:
        growingCrops.append(crop)

    if growingCrops:
      print("Crops currently growing:")
      for crop in growingCrops:
        time_remaining = crop.time_remaining()
        hours = int(time_remaining // 3600)
        minutes = int((time_remaining % 3600) // 60)
        seconds = int(time_remaining % 60)
        
        if hours > 0:
          time_str = f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
          time_str = f"{minutes}m {seconds}s"
        else:
          time_str = f"{seconds}s"
        
        growth_percentage = crop.get_growth_percentage()
        print(f"- {crop.name}: {growth_percentage:.1f}% grown, {time_str} remaining")
      print()

    if readyCrops:
      print("Crops ready for harvest:")
      for crop in readyCrops:
        print(f"#{readyCrops.index(crop)+1} - {crop.name} (READY)")
      print("\nPress number to harvest (or Q to cancel)")

      key = self.ui.term.inkey(timeout=None)
      
      if key.lower() == 'q':
        return
      
      if key.isdigit():
        cropIndex = int(key) - 1
        if 0 <= cropIndex < len(readyCrops):
          selectedCrop = readyCrops[cropIndex]
          harvestInfo = selectedCrop.harvest()
          if harvestInfo:
            from game.items.materials import materials
            material = next((m for m in materials if m['name'] == harvestInfo['name']), None)
            
            if material:
              for _ in range(harvestInfo['quantity']):
                self.player.addToInventory(material)
            else:
              for _ in range(harvestInfo['quantity']):
                self.player.inventory.append({
                  'name': harvestInfo['name'],
                  'category': 'material'
                })
            
            print(f"You have harvested {harvestInfo['quantity']} of {harvestInfo['name']}.")
            self.farm.crops.remove(selectedCrop)
            self.ui.term.inkey(timeout=2)
          else:
            print("This crop is not ready for harvest.")
            self.ui.term.inkey(timeout=2)
        else:
          print("Invalid selection.")
          self.ui.term.inkey(timeout=2)
    else:
      print("No crops are ready for harvest yet.")
      self.ui.term.inkey(timeout=2)

  def plantCrop(self):
    playerInventory = self.player.getInventory()
    availableSeeds = []

    for seed in self.farm.getSilo():
      availableSeeds.append({ 'origin': 'silo', 'seed': seed })

    for item in playerInventory:
      if item['category'] == 'seed' and item not in availableSeeds:
        availableSeeds.append({ 'origin': 'inventory', 'seed': item })
    if not availableSeeds:
      print("You have no seeds to plant.")
      self.ui.term.inkey(timeout=2)
      return
    
    print("Available seeds to plant:")
    for seed in availableSeeds:
      print(f"#{availableSeeds.index(seed)+1} - {seed['seed']['name']}")
    print("\nPress number to plant (or Q to cancel)")

    key = self.ui.term.inkey(timeout=None)
    
    if key.lower() == 'q':
      return
    
    if key.isdigit():
      seedIndex = int(key) - 1
      if 0 <= seedIndex < len(availableSeeds):
        selectedSeed = availableSeeds[seedIndex]
        self.farm.plantCrop(selectedSeed['seed'])
        if selectedSeed['origin'] == 'inventory':
          for i, item in enumerate(self.player.inventory):
            if item['name'] == selectedSeed['seed']['name']:
              self.player.inventory.pop(i)
              break
        elif selectedSeed['origin'] == 'silo':
          self.farm.removeFromSilo(self.farm.silo.index(selectedSeed['seed']))
        print(f"You have planted: {selectedSeed['seed']['name']}")
        self.ui.term.inkey(timeout=2)
      else:
        print("Invalid selection.")
        self.ui.term.inkey(timeout=2)
  
  def checkIfPlayerOwnsFarm(self):
    """Check if player owns this farm"""
    for properties in self.player.getProperties():
      if properties['id'] == self.id and properties['owned']:
        return True
    return False
  
  def open(self):
    """Open the farm UI"""
    self.ui.open()
