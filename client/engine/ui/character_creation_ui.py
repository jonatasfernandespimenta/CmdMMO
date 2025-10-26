from typing import TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
  from blessed import Terminal

class CharacterCreationUI:
  """Reusable UI for character creation (name and class selection)"""
  
  def __init__(self, term: 'Terminal'):
    self.term = term
    self.player_name = ''
    self.player_class = ''
  
  def getName(self, title: str = '=== CMD MMO ===', prompt: str = 'Enter your name: ', max_length: int = 20) -> str:
    """
    Get player name with visual input
    
    Args:
      title: Title to display
      prompt: Prompt text
      max_length: Maximum name length
    
    Returns:
      The player name
    """
    print(self.term.home + self.term.clear)
    print(self.term.move_y(self.term.height // 2 - 1) + self.term.center(self.term.bold_cyan(title)).rstrip())
    print(self.term.move_y(self.term.height // 2) + self.term.center(prompt).rstrip(), end='', flush=True)
    
    player_name = ''
    with self.term.location():
      print(self.term.move_y(self.term.height // 2 + 1) + self.term.center(' ' * 30).rstrip())
      name_x = (self.term.width - 20) // 2
      print(self.term.move_xy(name_x, self.term.height // 2 + 1), end='', flush=True)
      
      while True:
        key = self.term.inkey(timeout=0.1)
        if key.name == 'KEY_ENTER':
          if player_name:
            break
        elif key.name == 'KEY_BACKSPACE':
          if player_name:
            player_name = player_name[:-1]
            print(self.term.move_xy(name_x, self.term.height // 2 + 1) + self.term.cyan(player_name) + ' ' + self.term.move_left, end='', flush=True)
        elif key and key.isprintable():
          if len(player_name) < max_length:
            player_name += key
            print(self.term.cyan(key), end='', flush=True)
    
    self.player_name = player_name
    return player_name
  
  def selectClass(self, title: str = '=== SELECT YOUR CLASS ===', classes: List[Dict] = None) -> str:
    """
    Class selection UI
    
    Args:
      title: Title to display
      classes: List of class definitions, e.g.:
        [
          {
            'key': '1',
            'name': 'Rogue',
            'description': 'High attack & luck, low defense',
            'stats': 'HP: 80 | Attack: 15 | Defense: 4 | Luck: 8',
            'color': 'bold_green',
            'id': 'rogue'
          },
          ...
        ]
    
    Returns:
      The class ID selected
    """
    print(self.term.home + self.term.clear)
    
    # Title
    y_offset = self.term.height // 2 - 5
    print(self.term.move_y(y_offset) + self.term.center(self.term.bold_cyan(title)).rstrip())
    print()
    
    y_offset += 2
    
    # Display each class
    for i, cls in enumerate(classes):
      color_func = getattr(self.term, cls.get('color', 'white'))
      
      # Class name and description
      print(self.term.move_y(y_offset) + self.term.center(
        color_func(f"{cls['key']}. {cls['name']}") + self.term.white(f" - {cls['description']}")
      ).rstrip())
      y_offset += 1
      
      # Stats
      print(self.term.move_y(y_offset) + self.term.center(
        self.term.yellow(f"   {cls['stats']}")
      ).rstrip())
      y_offset += 1
      
      # Spacing between classes
      if i < len(classes) - 1:
        print()
        y_offset += 1
    
    # Prompt
    print()
    y_offset += 1
    print(self.term.move_y(y_offset) + self.term.center(
      self.term.white(f"Choose (1-{len(classes)}): ")
    ).rstrip(), end='', flush=True)
    
    # Build key to class ID mapping
    class_map = {cls['key']: cls['id'] for cls in classes}
    
    # Wait for input
    while True:
      key = self.term.inkey(timeout=0.1)
      if key in class_map:
        player_class = class_map[key]
        print(self.term.bold_cyan(player_class.capitalize()))
        self.player_class = player_class
        return player_class
    
  def create(self, 
             game_title: str = '=== CMD MMO ===',
             name_prompt: str = 'Enter your name: ',
             class_title: str = '=== SELECT YOUR CLASS ===',
             classes: List[Dict] = None,
             max_name_length: int = 20) -> Dict[str, str]:
    """
    Complete character creation flow
    
    Returns:
      Dictionary with 'name' and 'class' keys
    """
    name = self.getName(game_title, name_prompt, max_name_length)
    player_class = self.selectClass(class_title, classes)
    
    return {
      'name': name,
      'class': player_class
    }
