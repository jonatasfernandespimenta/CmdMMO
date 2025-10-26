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
