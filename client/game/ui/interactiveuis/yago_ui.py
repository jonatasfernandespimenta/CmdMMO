from game.arts.shitpost import yago_ui_frame_0, yago_ui_frame_1, yago_ui_frame_2
from engine.ui.interaction_ui import InteractionUI
from typing import TYPE_CHECKING
import time

if TYPE_CHECKING:
  from game.entities.player import Player
  from blessed import Terminal

class YagoUI:
  """UI para interagir com o Yago"""
  
  def __init__(self, player: 'Player', term: 'Terminal'):
    self.frames = [yago_ui_frame_0, yago_ui_frame_1, yago_ui_frame_1, yago_ui_frame_2]
    self.current_frame = 0
    self.last_frame_time = time.time()
    self.frame_duration = 0.3  # seconds per frame
    self.animation_complete = False
    
    self.ui = InteractionUI(player, term, {
      'art': self.frames[0],
      'message': 'oh os cara ai meu',
      'show_gold': False,
      'items': []
    })
  
  def update_frame(self):
    """Update to next frame if enough time has passed"""
    if self.animation_complete:
      return
    
    current_time = time.time()
    if current_time - self.last_frame_time >= self.frame_duration:
      self.current_frame += 1
      
      if self.current_frame >= len(self.frames):
        # Freeze on last frame
        self.current_frame = len(self.frames) - 1
        self.animation_complete = True
      
      self.ui.art = self.frames[self.current_frame]
      self.last_frame_time = current_time
  
  def open(self):
    """Abrir a UI do Yago with animation"""
    self.ui.isOpen = True
    
    # Show first frame and wait 1 second
    self.ui.draw()
    key = self.ui.term.inkey(timeout=1)
    if key:
      self.ui.handleInput(key)
      if not self.ui.isOpen:
        return
    
    self.last_frame_time = time.time()
    
    while self.ui.isOpen:
      self.update_frame()
      self.ui.draw()
      
      # Use timeout to allow animation to continue
      timeout = self.frame_duration if not self.animation_complete else None
      key = self.ui.term.inkey(timeout=timeout)
      
      if key:
        self.ui.handleInput(key)
