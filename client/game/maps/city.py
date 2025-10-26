from engine.maps.map import Map
from game.arts.buildings import house, farm_house_map_version
from game.maps.map_transition import CityToDungeonTransition
from game.ui.interactiveuis.landlord_ui import LandlordUI

class City(Map):
  def __init__(self, dungeon_map=None):
    super().__init__(60, 30)
    self.buildings = []
    self.portalPosition = [self.windowHeight // 2, self.windowWidth - 1]
    self.dungeon_map = dungeon_map

  def calculateDoorPositions(self, art):
    doors = []
    for y in range(len(art)):
      for x in range(len(art[y])):
        if art[y][x] == 'H':
          doors.append((y, x))
    return doors if doors else [(0, 0)]

  def onEnterBuilding(self, buildingName, player, term):
    if buildingName == 'LandLordHouse':
      landLordUi = LandlordUI(player, term)
      landLordUi.open()
    elif buildingName == 'FarmHouse':
      from game.ui.interactiveuis.farmui import FarmUI
      farmUi = FarmUI(player, term)
      farmUi.open()

  def generateHouses(self):
    houseArt = self.convertArtToBoardItem(house)
    farmHouseArt = self.convertArtToBoardItem(farm_house_map_version)

    houseDoorPositions = self.calculateDoorPositions(houseArt)
    farmHouseDoorPositions = self.calculateDoorPositions(farmHouseArt)

    doorPositions = [(8 + door[0], 8 + door[1]) for door in houseDoorPositions]
    farmHousePositions = [(20 + door[0], 30 + door[1]) for door in farmHouseDoorPositions]

    self.buildings.append({ 'name': 'LandLordHouse', 'startY': 8, 'startX': 8, 'art': houseArt, 'onEnter': self.onEnterBuilding, 'doorPositions': doorPositions })
    self.buildings.append({ 'name': 'FarmHouse', 'startY': 20, 'startX': 30, 'art': farmHouseArt, 'onEnter': self.onEnterBuilding, 'doorPositions': farmHousePositions })

  def handleCollisions(self, player, draw, term):
    for building in self.buildings:
      for doorPosition in building['doorPositions']:
        if player.getPlayerPosition() == list(doorPosition):
          building['onEnter'](building['name'], player, term)
          break

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
  
  def drawPortal(self):
    """Always draw dungeon entrance portal"""
    self.lines[self.portalPosition[0]][self.portalPosition[1]] = 'D'
  
  def redrawBuildings(self):
    """Redraw all buildings (in case they were overwritten by player movement)"""
    for building in self.buildings:
      self.placeArt(building['startY'], building['startX'], building['art'])
  
  def init(self, players, term):
    if len(self.lines) == 0:
      self.createBoard()
    
    self.redrawBuildings()
    self.drawPortal()
    
    for player in players:
      player.drawPlayer()
    
    self.printPlayerInfo(players[0], term)
    self.printBoard(term)

  def getPortalPosition(self):
    return self.portalPosition
  
  def setDungeonMap(self, dungeon_map):
    self.dungeon_map = dungeon_map
  
  def checkPortalTransition(self, player):
    if self.portalPosition == player.getPlayerPosition() and self.dungeon_map:
      return CityToDungeonTransition(self.dungeon_map, [0, 0])
    return None
