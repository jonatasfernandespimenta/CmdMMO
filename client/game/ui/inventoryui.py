import time

class InventoryUi:
  def __init__(self, player, term):
    self.player = player
    self.term = term
  
  def draw(self):
    print(self.term.home + self.term.clear)
    print(self.term.bold_cyan('=== INVENTORY ===\n'))
    playerInventory = self.player.getInventory()

    itemId = 0

    if len(playerInventory) == 0:
      print(self.term.yellow("You have no items!"))

    for item in playerInventory:
      print(self.term.green(item['art']))
      print(self.term.bold('#' + str(itemId)))
      print(self.term.cyan(str(item['name'])))
      print(self.term.white('Quantity: ') + self.term.yellow(str(item['quantity'])))
      itemId += 1
      print('\n')

    print('\n\n')

    print(self.term.bold_white("What would you like to do?"))
    print(self.term.green("1. ") + "Equip Item")
    print(self.term.green("2. ") + "Drop Item")
    print(self.term.green("3. ") + "Close Inventory")

    playerChoice = ''
    while True:
      key = self.term.inkey(timeout=0.1)
      if key and key.isprintable():
        playerChoice = key
        break
    
    if playerChoice == "1":
      self.equipItem()

    elif playerChoice == "2":
      self.dropItem()

    elif playerChoice == "3":
      self.player.setIsInventoryOpen(False)
  
  def dropItem(self):
    print(self.term.yellow("\nWhich item would you like to drop?"))
    playerChoice = ''
    while True:
      key = self.term.inkey(timeout=0.1)
      if key and key.isprintable():
        playerChoice = key
        break
    
    try:
      itemIndex = int(playerChoice)
      itemDropped = self.player.getInventory()[itemIndex]
      self.player.dropItem(itemIndex)
      print(self.term.green("You dropped " + itemDropped['name']))
    except:
      print(self.term.red("Invalid item!"))
    
    time.sleep(1)

  def equipItem(self):
    print(self.term.yellow("\nWhich item would you like to equip/use?"))
    playerChoice = ''
    while True:
      key = self.term.inkey(timeout=0.1)
      if key and key.isprintable():
        playerChoice = key
        break
    
    inventory = self.player.getInventory()
    
    try:
      if int(playerChoice) >= len(inventory) or int(playerChoice) < 0:
        print(self.term.red("Invalid item selection!"))
        time.sleep(1)
        return
      
      itemIndex = int(playerChoice)
      itemName = inventory[itemIndex]['name']
      self.player.equipItem(itemIndex)
      print(self.term.green("You equipped " + itemName))
      self.player.dropItem(itemIndex)
    except:
      print(self.term.red("Invalid item!"))
    
    time.sleep(1)
