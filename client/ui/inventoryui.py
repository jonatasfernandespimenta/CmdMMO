import time
import os
class InventoryUi:
  def __init__(self, player):
    self.player = player
  
  def draw(self):
    os.system('clear')
    playerInventory = self.player.getInventory()

    itemId = 0

    if len(playerInventory) == 0:
      print("You have no items!")

    for item in playerInventory:
      print(item['art'])
      print('#' + str(itemId))
      print(str(item['name']))
      print('Quantity: ' + str(item['quantity']))
      itemId += 1
      print('\n')

    print('\n\n\n\n')

    print("What would you like to do?")
    print("1. Equip Item")
    #print("2. Use Item")
    print("2. Drop Item")
    print("3. Close Inventory")

    playerChoice = input(">> ")
    
    if playerChoice == "1":
      self.equipItem()

    elif playerChoice == "2":
      self.dropItem()

    elif playerChoice == "3":
      self.player.setIsInventoryOpen(False)
  
  def dropItem(self):
    print("Which item would you like to drop?")
    playerChoice = input(">> ")
    itemDropped = self.player.getInventory()[int(playerChoice)]
    self.player.dropItem(playerChoice)
    
    print("You dropped " + str(itemDropped))
    time.sleep(1)

  def equipItem(self):
    print("Which item would you like to equip/use?")
    playerChoice = input(">> ")
    inventory = self.player.getInventory()
    
    if int(playerChoice) >= len(inventory) or int(playerChoice) < 0:
      print("Invalid item selection!")
      time.sleep(1)
      return
    
    itemName = inventory[int(playerChoice)]['name']
    self.player.equipItem(playerChoice)
    print("You equipped " + itemName)
    self.player.dropItem(playerChoice)
    time.sleep(1)
