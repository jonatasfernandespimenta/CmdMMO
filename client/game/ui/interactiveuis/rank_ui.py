from game.arts.rank import draw_rank_board
from typing import TYPE_CHECKING
import requests

if TYPE_CHECKING:
  from game.entities.player import Player
  from blessed import Terminal

class RankUI:
  """UI for viewing player rankings"""
  
  def __init__(self, player: 'Player', term: 'Terminal', server_url: str = 'http://172.23.209.86:3001'):
    self.player = player
    self.term = term
    self.server_url = server_url
    self.isOpen = False
    
    self.current_rank_type = 'gold'
    self.scroll_position = 0
    self.rank_data = []
    
  def fetch_rank_data(self, rank_type: str):
    """Fetch ranking data from server API"""
    try:
      response = requests.get(f'{self.server_url}/api/rankings/{rank_type}', timeout=5)
      if response.status_code == 200:
        return response.json()
      else:
        return []
    except Exception as e:
      print(f"Error fetching rank data: {e}")
      return []
  
  def load_rank_type(self, rank_type: str):
    """Load a specific rank type"""
    self.current_rank_type = rank_type
    self.scroll_position = 0
    self.rank_data = self.fetch_rank_data(rank_type)
  
  def draw(self):
    """Draw the rank board UI"""
    print(self.term.home + self.term.clear)
    
    # Draw rank board
    board_art = draw_rank_board(self.scroll_position, self.current_rank_type, self.rank_data)
    print(self.term.yellow(board_art))
    print()
    
    # Draw options
    print(self.term.bold_cyan('=' * 60))
    print(self.term.white('  [1] View Gold Rankings'))
    print(self.term.white('  [2] View Level Rankings'))
    print(self.term.white('  [3] View Dungeon Level Rankings'))
    print(self.term.white('  [↑/↓] Scroll (if more than 10 entries)'))
    print(self.term.white('  [Q] Exit'))
    print(self.term.bold_cyan('=' * 60))
  
  def handle_input(self, key):
    """Handle user input"""
    if key.lower() == 'q':
      # Exit and move player forward
      currentPosition = self.player.getPlayerPosition()
      self.player.setPlayerPosition([currentPosition[0] + 1, currentPosition[1]])
      self.isOpen = False
      return
    
    # Change rank type
    if key == '1':
      self.load_rank_type('gold')
    elif key == '2':
      self.load_rank_type('level')
    elif key == '3':
      self.load_rank_type('dungeon')
    
    # Scroll controls
    elif key.name == 'KEY_UP':
      if self.scroll_position > 0:
        self.scroll_position -= 1
    elif key.name == 'KEY_DOWN':
      max_scroll = max(0, len(self.rank_data) - 10)
      if self.scroll_position < max_scroll:
        self.scroll_position += 1
  
  def open(self):
    """Open the rank UI"""
    self.isOpen = True
    self.load_rank_type('gold')  # Start with gold rankings
    
    while self.isOpen:
      self.draw()
      key = self.term.inkey(timeout=None)
      self.handle_input(key)
