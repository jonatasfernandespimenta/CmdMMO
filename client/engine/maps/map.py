class Map:
  """Base class for all maps in the game (Dungeon, City, Farm, etc.)"""
  
  def __init__(self, width, height):
    self.windowWidth = width
    self.windowHeight = height
    self.lines = []
  
  def createBoard(self):
    """Creates the initial board/map layout"""
    raise NotImplementedError("Subclasses must implement createBoard()")
  
  def printBoard(self, term):
    """Renders the map to the terminal"""
    raise NotImplementedError("Subclasses must implement printBoard()")
  
  def getLines(self):
    return self.lines
  
  def getWindowWidth(self):
    return self.windowWidth
  
  def getWindowHeight(self):
    return self.windowHeight
  
  def init(self, players, term):
    """Initialize and draw the map"""
    raise NotImplementedError("Subclasses must implement init()")
  
  def handleCollisions(self, player, draw, term):
    """Handle collision logic specific to this map (enemies, NPCs, etc.)"""
    pass
  
  def checkPortalTransition(self, player):
    """Check if player is on a portal and return the transition object"""
    return None
  
  def placeArt(self, startY: int, startX: int, art):
    for y in range(len(art)):
      for x in range(len(art[y])):
        if startY + y < self.windowHeight and startX + x < self.windowWidth:
          self.lines[startY + y][startX + x] = art[y][x]

  def convertArtToBoardItem(self, art: str):
    return [list(line) for line in art.split('\n')]
