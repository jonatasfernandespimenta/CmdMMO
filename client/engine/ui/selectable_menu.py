from typing import TYPE_CHECKING, List, Dict, Callable, Optional

if TYPE_CHECKING:
  from blessed import Terminal

class MenuItem:
  def __init__(self, name: str, callback: Optional[Callable] = None, data: Optional[Dict] = None):
    self.name = name
    self.callback = callback
    self.data = data or {}
    self.is_selectable = True
    self.is_visible = True

class SelectableMenu:
  def __init__(self, term: 'Terminal', title: str = '', show_numbers: bool = True):
    self.term = term
    self.title = title
    self.show_numbers = show_numbers
    self.items: List[MenuItem] = []
    self.selected_index = 0
    self.marker_selected = ' ▶ '
    self.marker_unselected = '   '
    self.color_selected = 'black_on_yellow'
    self.color_unselected = 'white'
  
  def add_item(self, name: str, callback: Optional[Callable] = None, data: Optional[Dict] = None) -> MenuItem:
    item = MenuItem(name, callback, data)
    self.items.append(item)
    return item
  
  def clear_items(self):
    self.items = []
    self.selected_index = 0
  
  def get_selected_item(self) -> Optional[MenuItem]:
    if 0 <= self.selected_index < len(self.items):
      return self.items[self.selected_index]
    return None
  
  def next_item(self):
    if len(self.items) == 0:
      return
    
    original_index = self.selected_index
    while True:
      self.selected_index = (self.selected_index + 1) % len(self.items)
      if self.items[self.selected_index].is_selectable or self.selected_index == original_index:
        break
  
  def previous_item(self):
    if len(self.items) == 0:
      return
    
    original_index = self.selected_index
    while True:
      self.selected_index = (self.selected_index - 1) % len(self.items)
      if self.items[self.selected_index].is_selectable or self.selected_index == original_index:
        break
  
  def select_by_number(self, number: int) -> bool:
    if 0 <= number < len(self.items) and self.items[number].is_selectable:
      self.selected_index = number
      return True
    return False
  
  def execute_selected(self) -> bool:
    item = self.get_selected_item()
    if item and item.callback:
      item.callback(item)
      return True
    return False
  
  def render(self, x: int = 0, y: int = 0, width: int = 30):
    current_y = y
    
    if self.title:
      border = '╔' + '═' * (width - 2) + '╗'
      print(self.term.move_xy(x, current_y) + self.term.bold_cyan(border))
      current_y += 1
      
      title_text = f' {self.title}'.ljust(width - 2)
      print(self.term.move_xy(x, current_y) + self.term.bold_cyan('║') + 
            self.term.bold_white(title_text) + self.term.bold_cyan('║'))
      current_y += 1
      
      separator = '╠' + '═' * (width - 2) + '╣'
      print(self.term.move_xy(x, current_y) + self.term.bold_cyan(separator))
      current_y += 1
    
    for i, item in enumerate(self.items):
      if not item.is_visible:
        continue
      
      if i == self.selected_index:
        marker = self.term.bold_yellow(self.marker_selected)
        color_func = getattr(self.term, self.color_selected)
      else:
        marker = self.term.white(self.marker_unselected)
        color_func = getattr(self.term, self.color_unselected)
      
      number_prefix = f'{i+1}. ' if self.show_numbers else ''
      item_text = f'{number_prefix}{item.name}'.ljust(width - 6)[:width - 6]
      
      if self.title:
        print(self.term.move_xy(x, current_y) + self.term.bold_cyan('║') + 
              marker + color_func(item_text) + self.term.bold_cyan('║'))
      else:
        print(self.term.move_xy(x, current_y) + marker + color_func(item_text))
      
      current_y += 1
    
    if self.title:
      bottom = '╚' + '═' * (width - 2) + '╝'
      print(self.term.move_xy(x, current_y) + self.term.bold_cyan(bottom))
  
  def handle_input(self, key) -> str:
    if key.name == 'KEY_UP' or key.lower() == 'w':
      self.previous_item()
      return 'navigate'
    elif key.name == 'KEY_DOWN' or key.lower() == 's':
      self.next_item()
      return 'navigate'
    elif key.name == 'KEY_ENTER' or key == ' ':
      if self.execute_selected():
        return 'execute'
      return 'none'
    elif key.isdigit() and self.show_numbers:
      index = int(key) - 1
      if self.select_by_number(index):
        if self.execute_selected():
          return 'execute'
    
    return 'none'
