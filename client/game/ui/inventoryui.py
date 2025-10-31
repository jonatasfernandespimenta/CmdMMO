import time
from engine.ui.selectable_menu import SelectableMenu

class InventoryUi:
  def __init__(self, player, term):
    self.player = player
    self.term = term
    self.main_menu = None
    self.inventory_menu = None
  
  def draw(self):
    should_close = [False]
    should_equip = [False]
    should_drop = [False]
    
    def close_action(item):
      should_close[0] = True
    
    def equip_action(item):
      should_equip[0] = True
    
    def drop_action(item):
      should_drop[0] = True
    
    self.main_menu = SelectableMenu(self.term, "What would you like to do?", show_numbers=True)
    self.main_menu.add_item("Equip Item", callback=equip_action)
    self.main_menu.add_item("Drop Item", callback=drop_action)
    self.main_menu.add_item("Close Inventory", callback=close_action)
    
    while True:
      print(self.term.home + self.term.clear)
      print(self.term.bold_cyan('=== INVENTORY ===\n'))
      playerInventory = self.player.getInventory()

      if len(playerInventory) == 0:
        print(self.term.yellow("You have no items!"))
      else:
        for i, item in enumerate(playerInventory):
          print(self.term.green(item['art']))
          print(self.term.bold('#' + str(i)))
          print(self.term.cyan(str(item['name'])))
          print(self.term.white('Quantity: ') + self.term.yellow(str(item['quantity'])))
          print('\n')

      print('\n')
      
      self.main_menu.render(0, self.term.get_location()[0], 40)
      
      key = self.term.inkey()
      
      if key.lower() == 'q':
        self.player.setIsInventoryOpen(False)
        break
      
      result = self.main_menu.handle_input(key)
      
      if result == 'execute':
        if should_close[0]:
          self.player.setIsInventoryOpen(False)
          break
        elif should_equip[0]:
          should_equip[0] = False
          self.equipItem()
        elif should_drop[0]:
          should_drop[0] = False
          self.dropItem()
  
  def dropItem(self):
    playerInventory = self.player.getInventory()
    
    if len(playerInventory) == 0:
      print(self.term.red("No items to drop!"))
      time.sleep(1)
      return
    
    print(self.term.home + self.term.clear)
    print(self.term.bold_cyan('=== DROP ITEM ===\n'))
    print(self.term.yellow("Which item would you like to drop?\n"))
    
    self.inventory_menu = SelectableMenu(self.term, "", show_numbers=True)
    
    for i, item in enumerate(playerInventory):
      def drop_action(menu_item, idx=i):
        itemDropped = self.player.getInventory()[idx]
        self.player.dropItem(idx)
        print(self.term.green(f"You dropped {itemDropped['name']}"))
        time.sleep(1)
      
      self.inventory_menu.add_item(f"{item['name']} (x{item['quantity']})", callback=drop_action)
    
    self.inventory_menu.render(0, 4, 40)
    
    key = self.term.inkey()
    self.inventory_menu.handle_input(key)

  def equipItem(self):
    playerInventory = self.player.getInventory()
    
    if len(playerInventory) == 0:
      print(self.term.red("No items to equip!"))
      time.sleep(1)
      return
    
    print(self.term.home + self.term.clear)
    print(self.term.bold_cyan('=== EQUIP ITEM ===\n'))
    print(self.term.yellow("Which item would you like to equip/use?\n"))
    
    self.inventory_menu = SelectableMenu(self.term, "", show_numbers=True)
    
    for i, item in enumerate(playerInventory):
      def equip_action(menu_item, idx=i):
        itemName = self.player.getInventory()[idx]['name']
        self.player.equipItem(idx)
        print(self.term.green(f"You equipped {itemName}"))
        self.player.dropItem(idx)
        time.sleep(1)
      
      self.inventory_menu.add_item(f"{item['name']} (x{item['quantity']})", callback=equip_action)
    
    self.inventory_menu.render(0, 4, 40)
    
    key = self.term.inkey()
    self.inventory_menu.handle_input(key)
