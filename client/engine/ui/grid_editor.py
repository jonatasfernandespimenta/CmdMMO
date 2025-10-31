from typing import TYPE_CHECKING, List, Optional
from engine.ui.draggable import DraggableElement

if TYPE_CHECKING:
  from blessed import Terminal

class GridEditor:
  def __init__(self, term: 'Terminal', width: int, height: int):
    self.term = term
    self.width = width
    self.height = height
    self.elements: List[DraggableElement] = []
    self.selected_index = 0
    self.grid_lines = []
  
  def add_element(self, element: DraggableElement):
    element.bounds = (1, 1, self.width - 2, self.height - 2)
    self.elements.append(element)
  
  def remove_element(self, element_id: str):
    self.elements = [e for e in self.elements if e.element_id != element_id]
    if self.selected_index >= len(self.elements):
      self.selected_index = max(0, len(self.elements) - 1)
  
  def get_selected_element(self) -> Optional[DraggableElement]:
    if 0 <= self.selected_index < len(self.elements):
      return self.elements[self.selected_index]
    return None
  
  def next_element(self):
    if len(self.elements) > 0:
      self.selected_index = (self.selected_index + 1) % len(self.elements)
  
  def previous_element(self):
    if len(self.elements) > 0:
      self.selected_index = (self.selected_index - 1) % len(self.elements)
  
  def create_grid(self, floor_char: str = '.', wall_char_h: str = '═', wall_char_v: str = '║'):
    self.grid_lines = []
    for i in range(self.height):
      self.grid_lines.append([])
      for j in range(self.width):
        if i == 0 or i == self.height - 1:
          self.grid_lines[i].append(wall_char_h)
        elif j == 0 or j == self.width - 1:
          self.grid_lines[i].append(wall_char_v)
        else:
          self.grid_lines[i].append(floor_char)
    
    if self.grid_lines:
      self.grid_lines[0][0] = '╔'
      self.grid_lines[0][self.width - 1] = '╗'
      self.grid_lines[self.height - 1][0] = '╚'
      self.grid_lines[self.height - 1][self.width - 1] = '╝'
  
  def place_element_on_grid(self, element: DraggableElement):
    art_lines = element.get_art_lines()
    
    for y in range(len(art_lines)):
      for x in range(len(art_lines[y])):
        grid_y = element.y + y
        grid_x = element.x + x
        
        if 0 <= grid_y < self.height and 0 <= grid_x < self.width:
          if art_lines[y][x] != ' ':
            self.grid_lines[grid_y][grid_x] = art_lines[y][x]
  
  def render_elements(self):
    for element in self.elements:
      self.place_element_on_grid(element)
  
  def render_grid(self):
    self.create_grid()
    self.render_elements()
    
    for line in self.grid_lines:
      print(self.term.white(''.join(line)))
  
  def handle_movement(self, key) -> bool:
    selected = self.get_selected_element()
    if not selected:
      return False
    
    moved = False
    if key.name == 'KEY_UP' or key.lower() == 'w':
      moved = selected.move(0, -1)
    elif key.name == 'KEY_DOWN' or key.lower() == 's':
      moved = selected.move(0, 1)
    elif key.name == 'KEY_LEFT' or key.lower() == 'a':
      moved = selected.move(-1, 0)
    elif key.name == 'KEY_RIGHT' or key.lower() == 'd':
      moved = selected.move(1, 0)
    
    return moved
