import time
from engine.maps.map_transition import MapTransition

class CityToDungeonTransition(MapTransition):
  """Transition from City to Dungeon"""
  
  def execute(self, player, term):
    print(term.home + term.clear)
    print(term.move_y(term.height // 2 - 1) + term.center(term.bold_cyan('=== ENTERING DUNGEON ===')).rstrip())
    print(term.move_y(term.height // 2 + 1) + term.center(term.bold_magenta('Prepare for battle...')).rstrip())
    time.sleep(2)
    
    # Reset dungeon to level 1 when entering from city
    dungeon = self.destination_map
    dungeon.currentLevel = 1
    dungeon.enemies.clear()
    dungeon.chests.clear()
    dungeon.portalActive = False
    dungeon.portalPosition = None
    
    # Regenerate the board first
    dungeon.createBoard()
    
    # Setup dungeon with new enemies and chests (they'll use the new board)
    dungeon.createRandomEnemies(5)
    dungeon.createRandomChests(5)
    dungeonInfo = [dungeon.getLines(), dungeon.getWindowWidth(), dungeon.getWindowHeight()]
    player.setBoard(dungeonInfo[0], dungeonInfo[1], dungeonInfo[2])
    player.setPlayerPosition(self.player_spawn_position)

class DungeonNextLevelTransition(MapTransition):
  """Transition to next dungeon level"""
  
  def execute(self, player, term):
    print(term.home + term.clear)
    print(term.move_y(term.height // 2 - 1) + term.center(term.bold_green('=== STAGE ' + str(self.destination_map.getCurrentLevel()) + ' COMPLETE! ===')).rstrip())
    print(term.move_y(term.height // 2 + 1) + term.center(term.bold_magenta('Entering portal...')).rstrip())
    
    nextStage = self.destination_map.getCurrentLevel() + 1

    player.maxDungeonLevel = max(player.maxDungeonLevel, nextStage)

    if nextStage % 5 == 0:
      print(term.move_y(term.height // 2 + 3) + term.center(term.bold_red('!!! WARNING: BOSS ROOM AHEAD !!!')).rstrip())
    
    print(term.move_y(term.height // 2 + 4) + term.center(term.yellow('Advancing to Stage ' + str(nextStage) + '...')).rstrip())
    time.sleep(3)
    
    self.destination_map.nextLevel()
    player.setPlayerPosition(self.player_spawn_position)

class DungeonToCityTransition(MapTransition):
  """Transition from Dungeon back to City"""
  
  def execute(self, player, term):
    print(term.home + term.clear)
    print(term.move_y(term.height // 2 - 1) + term.center(term.bold_cyan('=== LEAVING DUNGEON ===')).rstrip())
    print(term.move_y(term.height // 2 + 1) + term.center(term.bold_green('Returning to city...')).rstrip())
    time.sleep(2)
    
    # Setup city
    cityInfo = [self.destination_map.getLines(), self.destination_map.getWindowWidth(), self.destination_map.getWindowHeight()]
    player.setBoard(cityInfo[0], cityInfo[1], cityInfo[2])
    player.setPlayerPosition(self.player_spawn_position)
