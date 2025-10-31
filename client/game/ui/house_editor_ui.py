from typing import TYPE_CHECKING
from game.arts.buildings import house, mushroom_house, bank, rank_board
from engine.ui.grid_editor import GridEditor
from engine.ui.draggable import DraggableElement
from engine.ui.selectable_menu import SelectableMenu

if TYPE_CHECKING:
  from game.entities.player import Player

class HouseEditorUI:
  def __init__(self, player: 'Player', houseDimensions, term):
    self.player = player
    self.houseDimensions = houseDimensions
    self.term = term
    self.windowWidth = houseDimensions.get('width', 80)
    self.windowHeight = houseDimensions.get('height', 20)
    
    self.grid_editor = GridEditor(term, self.windowWidth, self.windowHeight)
    
    initial_furniture = DraggableElement(5, 3, house, 'furniture_0')
    self.grid_editor.add_element(initial_furniture)
    
    self.available_furnitures = [
      {'name': 'House', 'art': house},
      {'name': 'Mushroom House', 'art': mushroom_house},
      {'name': 'Bank', 'art': bank},
      {'name': 'Rank Board', 'art': rank_board}
    ]
    
    self.furniture_menu = SelectableMenu(term, 'FURNITURE MENU', show_numbers=False)
    for furniture in self.available_furnitures:
      self.furniture_menu.add_item(furniture['name'], data=furniture)
    
    self.placed_menu = SelectableMenu(term, 'PLACED FURNITURE', show_numbers=False)
    self.placed_menu.marker_selected = ' ► '
    self.placed_menu.color_selected = 'black_on_green'
    self.update_placed_menu()

  def update_placed_menu(self):
    self.placed_menu.clear_items()
    for element in self.grid_editor.elements:
      def select_furniture(item, elem=element):
        for i, e in enumerate(self.grid_editor.elements):
          if e.element_id == elem.element_id:
            self.grid_editor.selected_index = i
            break
      self.placed_menu.add_item(element.element_id, callback=select_furniture)
    
    self.placed_menu.selected_index = self.grid_editor.selected_index

  def draw_furniture_selector(self):
    self.furniture_menu.render(self.windowWidth + 5, 2, 21)
    
    menu_height = len(self.available_furnitures) + 4
    self.placed_menu.render(self.windowWidth + 5, menu_height + 2, 21)

  def render(self):
    is_open = True
    
    while is_open:
      print(self.term.home + self.term.clear)
      print(self.term.bold_cyan('=== HOUSE EDITOR ===\n'))
      
      self.grid_editor.render_grid()
      self.draw_furniture_selector()
      
      controls_y = self.windowHeight + 2
      print(self.term.move_xy(0, controls_y) + self.term.bold_cyan('╔═══════════════════════════════════════╗'))
      print(self.term.move_xy(0, controls_y + 1) + self.term.bold_cyan('║') + 
            self.term.bold_white('            CONTROLS                   ') + self.term.bold_cyan('║'))
      print(self.term.move_xy(0, controls_y + 2) + self.term.bold_cyan('╠═══════════════════════════════════════╣'))
      print(self.term.move_xy(0, controls_y + 3) + self.term.bold_cyan('║ ') + 
            self.term.black_on_green(' ↑↓←→ ') + self.term.white(' Move furniture              ') + self.term.bold_cyan('║'))
      print(self.term.move_xy(0, controls_y + 4) + self.term.bold_cyan('║ ') + 
            self.term.black_on_cyan(' SPACE ') + self.term.white(' Next placed furniture       ') + self.term.bold_cyan('║'))
      print(self.term.move_xy(0, controls_y + 5) + self.term.bold_cyan('║ ') + 
            self.term.black_on_magenta(' TAB   ') + self.term.white(' Next furniture type         ') + self.term.bold_cyan('║'))
      print(self.term.move_xy(0, controls_y + 6) + self.term.bold_cyan('║ ') + 
            self.term.black_on_yellow(' ENTER ') + self.term.white(' Add furniture to house      ') + self.term.bold_cyan('║'))
      print(self.term.move_xy(0, controls_y + 7) + self.term.bold_cyan('║ ') + 
            self.term.black_on_red(' Q     ') + self.term.white(' Exit editor                 ') + self.term.bold_cyan('║'))
      print(self.term.move_xy(0, controls_y + 8) + self.term.bold_cyan('╚═══════════════════════════════════════╝'))
      
      key = self.term.inkey()
      
      if key.lower() == 'q':
        is_open = False
      elif key == ' ':
        self.grid_editor.next_element()
        self.update_placed_menu()
      elif key.name == 'KEY_TAB':
        self.furniture_menu.next_item()
      elif key.name == 'KEY_ENTER':
        selected_item = self.furniture_menu.get_selected_item()
        if selected_item:
          furniture_count = len(self.grid_editor.elements)
          new_element = DraggableElement(
            5, 3,
            selected_item.data['art'],
            f"furniture_{furniture_count}"
          )
          self.grid_editor.add_element(new_element)
          self.update_placed_menu()
      else:
        self.grid_editor.handle_movement(key)

  def init(self):
    self.render()
