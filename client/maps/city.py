from .map import Map
from arts.buildings import house

class City(Map):
  def __init__(self):
    super().__init__(60, 30)
    self.buildings = []
    self.portalPosition = [self.windowHeight // 2, self.windowWidth - 1]

  def calculateDoorPosition(self, art):
    for y in range(len(art)):
      for x in range(len(art[y])):
        if art[y][x] == '  ':
          return (y, x)
    return (0, 0)

  def generateHouses(self):
    houseArt = self.convertArtToBoardItem(house)
    houseDoorPosition = self.calculateDoorPosition(houseArt)

    self.buildings.append({ 'name': 'LandLordHouse', 'startY': 8, 'startX': 8, 'art': houseArt, 'onEnter': None, 'doorPosition': (8 + houseDoorPosition[0], 8 + houseDoorPosition[1]) })

  def initBuildings(self):
    self.generateHouses()

    for building in self.buildings:
      self.placeArt(building['startY'], building['startX'], building['art'])

  def createBoard(self):
    self.lines = []
    for i in range(self.windowHeight):
      self.lines.append([])
      for j in range(self.windowWidth):
        self.lines[i].append('.')

    self.initBuildings()

    self.lines[self.portalPosition[0]][self.portalPosition[1]] = 'D'

    return self.lines

  def printBoard(self, term):
    for i in range(self.windowHeight):
      line = ''
      for j in range(self.windowWidth):
        char = self.lines[i][j]
        if char == '#':
          line += term.bold_white(char)
        elif char == 'X':
          line += term.bold_cyan(char)
        elif char == 'D':
          line += term.bold_blue_reverse(char)
        else:
          line += term.green(char)
      print(line)


  def printPlayerInfo(self, player, term):
    print(term.bold_white('=' * self.windowWidth))
    hp_color = term.green if player.getHp() > player.getMaxHp() * 0.5 else term.yellow if player.getHp() > player.getMaxHp() * 0.2 else term.red
    print(term.cyan('Name: ') + term.bold(player.getName()) + term.cyan(' [') + term.magenta(player.getPlayerClass()) + term.cyan('] Lvl: ') + term.bold_green(str(player.getLevel())))
    print(term.cyan('HP: ') + hp_color(str(player.getHp()) + '/' + str(player.getMaxHp())) + term.cyan(' | XP: ') + term.green(str(player.getXp()) + '/' + str(player.getXpToNextLevel())))
    print(term.cyan('ATK: ') + term.yellow(str(player.getAttack())) + term.cyan(' | DEF: ') + term.blue(str(player.getDefense())) + term.cyan(' | Gold: ') + term.yellow(str(player.getGold())))
    notification = player.getNotification()
    if notification:
      print(term.bold_green(notification))
    print(term.bold_white('=' * self.windowWidth))
  
  def init(self, players, term):
    if len(self.lines) == 0:
      self.createBoard()
    
    for player in players:
      player.drawPlayer()
    
    self.printPlayerInfo(players[0], term)
    self.printBoard(term)

  def getPortalPosition(self):
    return self.portalPosition
