import time
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
  from blessed import Terminal

class Player:
  """Base Player class with common functionality for top-down terminal games"""
  
  def __init__(self, lines: List[List[str]], windowWidth: int, windowHeight: int, 
               playerPosition: List[int], name: str, term: 'Terminal', 
               blockers: List[str] = None):
    """
    Initialize base player
    
    Args:
      lines: Game board (2D array)
      windowWidth: Width of the game window
      windowHeight: Height of the game window
      playerPosition: Starting position [y, x]
      name: Player name
      term: Blessed Terminal instance
      blockers: List of characters that block movement (default: ['#'])
    """
    self.lines = lines
    self.windowWidth = windowWidth
    self.windowHeight = windowHeight
    self.playerPosition = playerPosition
    self.name = name
    self.term = term
    self.blockers = blockers if blockers else ['#']
    
    # Stats
    self.hp = 100
    self.maxHp = 100
    self.attack = 10
    self.defense = 5
    
    # Level system
    self.xp = 0
    self.level = 1
    self.xpToNextLevel = 100
    
    # Inventory system
    self.inventory = []
    self.isInventoryOpen = False
    self.gold = 0
    
    # Notifications
    self.notificationMessage = ''
    self.notificationTime = 0
    
    # Player character on map
    self.playerChar = 'X'
  
  # ==================== Movement ====================
  
  def movePlayer(self, network_callback=None):
    """
    Handle player movement with WASD or arrow keys
    
    Args:
      network_callback: Optional callback(new_position) for multiplayer sync
    """
    newPlayerPosition = self.playerPosition.copy()
    key = self.term.inkey(timeout=0.05)
    
    if key.name == 'KEY_UP' or key == 'w':
      self.lines[self.playerPosition[0]][self.playerPosition[1]] = '.'
      if not self.pathIsBlocked([self.playerPosition[0]-1, self.playerPosition[1]]):
        newPlayerPosition[0] -= 1
    
    elif key.name == 'KEY_DOWN' or key == 's':
      self.lines[self.playerPosition[0]][self.playerPosition[1]] = '.'
      if not self.pathIsBlocked([self.playerPosition[0]+1, self.playerPosition[1]]):
        newPlayerPosition[0] += 1
    
    elif key.name == 'KEY_LEFT' or key == 'a':
      self.lines[self.playerPosition[0]][self.playerPosition[1]] = '.'
      if not self.pathIsBlocked([self.playerPosition[0], self.playerPosition[1]-1]):
        newPlayerPosition[1] -= 1
    
    elif key.name == 'KEY_RIGHT' or key == 'd':
      self.lines[self.playerPosition[0]][self.playerPosition[1]] = '.'
      if not self.pathIsBlocked([self.playerPosition[0], self.playerPosition[1]+1]):
        newPlayerPosition[1] += 1
    
    elif key == 'i':
      self.isInventoryOpen = not self.isInventoryOpen
    
    if newPlayerPosition != self.playerPosition:
      if network_callback:
        network_callback(newPlayerPosition)
      self.playerPosition = newPlayerPosition
  
  def pathIsBlocked(self, position: List[int]) -> bool:
    """Check if a position is blocked"""
    if position[0] < 0 or position[0] > self.windowHeight-1:
      return True
    if position[1] < 0 or position[1] > self.windowWidth-1:
      return True
    if self.lines[position[0]][position[1]] in self.blockers:
      return True
    return False
  
  def drawPlayer(self):
    """Draw player on the board"""
    self.lines[self.playerPosition[0]][self.playerPosition[1]] = self.playerChar
  
  def removePlayer(self):
    """Remove player from current position"""
    self.lines[self.playerPosition[0]][self.playerPosition[1]] = '.'
  
  # ==================== Position ====================
  
  def getPlayerPosition(self) -> List[int]:
    return self.playerPosition
  
  def setPlayerPosition(self, position: List[int]):
    self.playerPosition = position
  
  def setBoard(self, lines: List[List[str]], windowWidth: int, windowHeight: int):
    """Update the board reference (e.g., when changing maps)"""
    self.lines = lines
    self.windowWidth = windowWidth
    self.windowHeight = windowHeight
  
  # ==================== Stats ====================
  
  def getName(self) -> str:
    return self.name
  
  def getHp(self) -> int:
    return self.hp
  
  def getMaxHp(self) -> int:
    return self.maxHp
  
  def setHp(self, hp: int):
    self.hp = min(hp, self.maxHp)  # Cap at max HP
  
  def getAttack(self) -> int:
    return self.attack
  
  def setAttack(self, attack: int):
    self.attack = attack
  
  def getDefense(self) -> int:
    return self.defense
  
  def setDefense(self, defense: int):
    self.defense = defense
  
  # ==================== Level System ====================
  
  def getLevel(self) -> int:
    return self.level
  
  def getXp(self) -> int:
    return self.xp
  
  def getXpToNextLevel(self) -> int:
    return self.xpToNextLevel
  
  def addXp(self, amount: int):
    """Add XP and auto-level up if threshold reached"""
    self.xp += amount
    while self.xp >= self.xpToNextLevel:
      self.levelUp()
  
  def levelUp(self):
    """Level up and increase stats"""
    self.xp -= self.xpToNextLevel
    self.level += 1
    self.xpToNextLevel = int(self.xpToNextLevel * 1.5)
    
    # Stat increases (can be overridden in subclasses)
    self.maxHp += 10
    self.hp = self.maxHp
    self.attack += 2
    self.defense += 1
    
    self.showNotification(f"LEVEL UP! You are now level {self.level}!")
  
  # ==================== Inventory ====================
  
  def getInventory(self) -> List[dict]:
    """Get inventory with item quantities"""
    inventory = self.inventory.copy()
    
    for item in inventory:
      item['quantity'] = self.inventory.count(item)
    
    # Remove duplicates
    inventory = list({v['name']:v for v in inventory}.values())
    
    return inventory
  
  def addToInventory(self, item: dict):
    """Add item to inventory"""
    self.inventory.append(item)
    self.showNotification(f"Collected: {item['name']}!")
  
  def dropItem(self, itemIndex: int):
    """Remove item from inventory"""
    self.inventory.remove(self.inventory[itemIndex])
  
  def equipItem(self, itemIndex: int):
    """Equip an item (apply its effects)"""
    item = self.inventory[itemIndex]
    
    if 'hp' in item:
      self.hp = min(self.hp + item['hp'], self.maxHp)
    if 'attack' in item:
      self.attack += item['attack']
    if 'defense' in item:
      self.defense += item['defense']
  
  def getIsInventoryOpen(self) -> bool:
    return self.isInventoryOpen
  
  def setIsInventoryOpen(self, isOpen: bool):
    self.isInventoryOpen = isOpen
  
  # ==================== Gold ====================
  
  def getGold(self) -> int:
    return self.gold
  
  def addGold(self, amount: int):
    self.gold += amount
  
  # ==================== Notifications ====================
  
  def showNotification(self, message: str, duration: float = 3.0):
    """Show a temporary notification"""
    self.notificationMessage = message
    self.notificationTime = time.time()
  
  def getNotification(self) -> str:
    """Get current notification if still active"""
    if self.notificationTime > 0 and time.time() - self.notificationTime < 3:
      return self.notificationMessage
    return ''
  
  # ==================== Update ====================
  
  def update(self, network_callback=None):
    """Called every frame - override in subclasses for custom behavior"""
    self.movePlayer(network_callback)
