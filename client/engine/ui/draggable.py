from typing import Optional, Tuple

class DraggableElement:
  def __init__(self, x: int, y: int, art: str, element_id: str, bounds: Optional[Tuple[int, int, int, int]] = None):
    self.x = x
    self.y = y
    self.art = art
    self.element_id = element_id
    self.bounds = bounds
    self.is_selected = False
  
  def move(self, dx: int, dy: int) -> bool:
    new_x = self.x + dx
    new_y = self.y + dy
    
    if self.bounds:
      min_x, min_y, max_x, max_y = self.bounds
      if not (min_x <= new_x <= max_x and min_y <= new_y <= max_y):
        return False
    
    self.x = new_x
    self.y = new_y
    return True
  
  def set_position(self, x: int, y: int):
    self.x = x
    self.y = y
  
  def get_position(self) -> Tuple[int, int]:
    return (self.x, self.y)
  
  def get_art_lines(self):
    art_lines = self.art.split('\n')
    if art_lines and art_lines[0] == '':
      art_lines = art_lines[1:]
    if art_lines and art_lines[-1] == '':
      art_lines = art_lines[:-1]
    return art_lines
