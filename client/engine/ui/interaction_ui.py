from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from player import Player
  from blessed import Terminal

class InteractionUI:
  """Base UI for NPC and location interactions"""
  
  def __init__(self, player: 'Player', term: 'Terminal', config: dict):
    self.player: Player = player
    self.term: Terminal = term
    self.isOpen = False
    
    self.art = config.get('art', '')
    self.message = config.get('message', '')
    self.options = config.get('options', [])  # [{'key': '1', 'label': 'Text', 'action': callable}]
    self.show_gold = config.get('show_gold', True)
    self.items = config.get('items', [])  # [{'name': 'Item', 'price': 100, 'owned': False, 'action': callable}]
  
  def draw(self):
    """Draw the interaction UI"""
    print(self.term.home + self.term.clear)
    
    # Draw art
    if self.art:
      art_lines = self.art.split('\n')
      for line in art_lines:
        print(self.term.yellow(line))
      print()
    
    # Draw message
    if self.message:
      print(self.term.yellow(f'  {self.message}'))
    
    # Show player gold
    if self.show_gold:
      print(self.term.white('  Your Gold: ') + self.term.bold_yellow(str(self.player.getGold())))
      print()
    
    # Draw items (for shop-like interfaces)
    if self.items:
      for i, item in enumerate(self.items):
        status = self.term.green('[OWNED]') if item.get('owned', False) else self.term.yellow(f"[{item['price']} Gold]")
        print(self.term.white(f"  {i+1}. ") + self.term.bold(item['name']) + ' ' + status)
        if 'description' in item:
          print(self.term.white(f"     {item['description']}"))
        print()
    
    # Draw options footer
    print(self.term.bold_cyan('=' * 60))
    if self.options:
      option_text = ' | '.join([f"[{opt['key'].upper()}] {opt['label']}" for opt in self.options])
      option_text += ' | [Q] Exit'
    else:
      option_text = '[Q] Exit'
    print(self.term.white(f'  {option_text}'))
    print(self.term.bold_cyan('=' * 60))
  
  def handleExit(self, key):
    """Default exit behavior: move player forward and close UI"""
    if key.lower() == 'q':
      currentPosition = self.player.getPlayerPosition()
      self.player.setPlayerPosition([currentPosition[0] + 1, currentPosition[1]])
      self.isOpen = False
  
  def handleInput(self, key):
    """Handle user input based on configured options"""
    self.handleExit(key)
    
    # Check configured options
    for option in self.options:
      if key.lower() == option['key'].lower():
        action = option.get('action')
        if action and callable(action):
          action()
        return
    
    # Check number keys for items (1-9)
    if key.isdigit() and self.items:
      index = int(key) - 1
      if 0 <= index < len(self.items):
        self.handleItemSelection(index)
  
  def handleItemSelection(self, index):
    """Handle item selection - verifies gold and delegates to custom action"""
    if index < 0 or index >= len(self.items):
      return
    
    item = self.items[index]
    
    # Check if already owned
    if item.get('owned', False):
      self.showMessage('You already own this!', 'red')
      return
    
    # Check if player has enough gold
    if self.player.getGold() < item['price']:
      self.showMessage('Not enough gold!', 'red')
      return
    
    # Deduct gold
    self.player.addGold(-item['price'])
    
    # Mark as owned
    item['owned'] = True
    
    # Call custom action if provided
    action = item.get('action')
    if action and callable(action):
      action(item, self)
    
    self.showMessage(f"Purchased {item['name']}!", 'green')
  
  def showMessage(self, message, color='white'):
    """Show a temporary message at the bottom of the screen"""
    color_func = getattr(self.term, color, self.term.white)
    if color == 'green':
      color_func = self.term.bold_green
    elif color == 'red':
      color_func = self.term.red
    
    print(self.term.move_y(self.term.height - 2) + self.term.center(color_func(message)).rstrip())
    self.term.inkey(timeout=2)
  
  def open(self):
    """Open the interaction UI and handle user input"""
    self.isOpen = True
    
    while self.isOpen:
      self.draw()
      
      key = self.term.inkey(timeout=None)
      
      self.handleInput(key)
