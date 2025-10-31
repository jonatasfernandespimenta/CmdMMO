from engine.maps.map import Map
from game.arts.buildings import *
from game.ui.interactiveuis.landlord_ui import LandlordUI
from game.ui.interactiveuis.yago_ui import YagoUI
from game.ui.interactiveuis.rank_ui import RankUI
from game.maps.map_transition import CityToDungeonTransition

class City(Map):
  def __init__(self, dungeon_map=None):
    super().__init__(60, 30)
    self.buildings = []
    self.portalPosition = [self.windowHeight // 2, self.windowWidth - 1]
    self.yagoPosition = [0, self.windowWidth - 1]
    self.dungeon_map = dungeon_map

  def calculateDoorPositions(self, art):
    doors = []
    for y in range(len(art)):
      for x in range(len(art[y])):
        if art[y][x] == 'H':
          doors.append((y, x))
    return doors if doors else [(0, 0)]

  def onEnterBuilding(self, buildingName, player, term):
    # Map building names to their UI classes
    ui_map = {
      'LandLordHouse': LandlordUI,
      'FarmHouse': lambda p, t: __import__('game.ui.interactiveuis.farmui', fromlist=['FarmUI']).FarmUI(p, t),
      'AlchemistHouse': lambda p, t: __import__('game.ui.interactiveuis.alchemist_ui', fromlist=['AlchemistUI']).AlchemistUI(p, t),
      'Yago': YagoUI,
      'RankBoard': RankUI,
      'Bank': lambda p, t: __import__('game.ui.interactiveuis.bank_ui', fromlist=['BankUI']).BankUI(p, t)
    }
    
    ui_class = ui_map.get(buildingName)
    if ui_class:
      if callable(ui_class) and not isinstance(ui_class, type):
        # It's a lambda (for lazy imports)
        ui = ui_class(player, term)
      else:
        # It's a class
        ui = ui_class(player, term)
      ui.open()

  def generateHouses(self):
    building_configs = [
      ('LandLordHouse', house, 8, 5, None),
      ('AlchemistHouse', mushroom_house, 18, 5, None),
      
      ('RankBoard', rank_board, 15, 27, (14, 28)), 
      
      ('FarmHouse', farm_house_map_version, 8, 45, None),
      ('Bank', bank, 18, 45, None)
    ]
    
    for name, art, start_y, start_x, custom_door in building_configs:
      building_art = self.convertArtToBoardItem(art)
      
      if custom_door:
        door_positions = [custom_door]
      else:
        doors = self.calculateDoorPositions(building_art)
        door_positions = [(start_y + door[0], start_x + door[1]) for door in doors]
      
      self.buildings.append({
        'name': name,
        'startY': start_y,
        'startX': start_x,
        'art': building_art,
        'onEnter': self.onEnterBuilding,
        'doorPositions': door_positions
      })

  def handleCollisions(self, player, draw, term):
    # Check Yago collision
    if player.getPlayerPosition() == self.yagoPosition:
      self.onEnterBuilding('Yago', player, term)
      return
    
    # Check building collisions
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
    self.lines[self.yagoPosition[0]][self.yagoPosition[1]] = 'Y'

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
        elif char == 'P':  # Remote player
          line += term.bold_yellow(char)
        elif char == 'D':
          line += term.bold_blue_reverse(char)
        elif char == 'Y':
          line += term.bold_magenta(char)
        else:
          line += term.green(char)
      print(line)


  def printPlayerInfo(self, player, term):
    print(term.bold_white('=' * self.windowWidth))
    hp_color = term.green if player.getHp() > player.getMaxHp() * 0.5 else term.yellow if player.getHp() > player.getMaxHp() * 0.2 else term.red
    mp_color = term.cyan if player.getMP() > player.maxMp * 0.5 else term.yellow if player.getMP() > player.maxMp * 0.2 else term.red
    
    print(term.cyan('Name: ') + term.bold(player.getName()) + term.cyan(' [') + term.magenta(player.getPlayerClass()) + term.cyan('] Lvl: ') + term.bold_green(str(player.getLevel())))
    print(term.cyan('HP: ') + hp_color(str(player.getHp()) + '/' + str(player.getMaxHp())) + term.cyan(' | MP: ') + mp_color(str(player.getMP()) + '/' + str(player.maxMp)) + term.cyan(' | XP: ') + term.green(str(player.getXp()) + '/' + str(player.getXpToNextLevel())))
    print(term.cyan('ATK: ') + term.yellow(str(player.getAttack())) + term.cyan(' | DEF: ') + term.blue(str(player.getDefense())) + term.cyan(' | LCK: ') + term.magenta(str(player.getLuck())) + term.cyan(' | Gold: ') + term.yellow(str(player.getGold())))
    notification = player.getNotification()
    if notification:
      print(term.bold_green(notification))
    print(term.bold_white('=' * self.windowWidth))
  
  def drawPortal(self):
    """Always draw dungeon entrance portal"""
    self.lines[self.portalPosition[0]][self.portalPosition[1]] = 'D'
  
  def drawYago(self):
    """Always draw Yago"""
    self.lines[self.yagoPosition[0]][self.yagoPosition[1]] = 'Y'
  
  def redrawBuildings(self):
    """Redraw all buildings (in case they were overwritten by player movement)"""
    for building in self.buildings:
      self.placeArt(building['startY'], building['startX'], building['art'])
  
  def init(self, players, term):
    if len(self.lines) == 0:
      self.createBoard()
    
    self.redrawBuildings()
    self.drawPortal()
    self.drawYago()
    
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
