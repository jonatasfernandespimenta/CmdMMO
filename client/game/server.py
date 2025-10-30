import socketio
import json
from engine.core.player import Player as BasePlayer

class RemotePlayer:
  """Lightweight player representation for remote players (just for rendering)"""
  def __init__(self, lines, windowWidth, windowHeight, playerPosition, name):
    self.lines = lines
    self.windowWidth = windowWidth
    self.windowHeight = windowHeight
    self.playerPosition = playerPosition
    self.name = name
  
  def getName(self):
    return self.name
  
  def getPlayerPosition(self):
    return self.playerPosition
  
  def setPlayerPosition(self, position):
    self.playerPosition = position
  
  def drawPlayer(self):
    """Draw remote player on the map"""
    if (0 <= self.playerPosition[0] < len(self.lines) and 
        0 <= self.playerPosition[1] < len(self.lines[0])):
      self.lines[self.playerPosition[0]][self.playerPosition[1]] = 'P'
  
  def removePlayer(self):
    """Remove remote player from the map"""
    if (0 <= self.playerPosition[0] < len(self.lines) and 
        0 <= self.playerPosition[1] < len(self.lines[0])):
      self.lines[self.playerPosition[0]][self.playerPosition[1]] = '.'

class Server:
  def __init__(self, sio, host, port, players, boardInfo):
    self.host = host
    self.port = port
    self.players = players
    self.boardInfo = boardInfo
    self.sio = sio

  def start(self):
    self.sio.connect('http://' + self.host + ':' + str(self.port))
    self.sio.on('joined', self.on_player_join)
    self.sio.on('moved', self.on_player_move)

  def join(self, playerId, playerPosition):
    self.sio.emit('join', json.dumps({"playerId": playerId, "playerPosition": playerPosition}))

  def on_player_join(self, data):
    for player in data:
      # Check if player already exists
      player_exists = any(p.getName() == player['playerId'] for p in self.players)
      if not player_exists:
        # Create lightweight remote player
        remote_player = RemotePlayer(
          self.boardInfo[0], 
          self.boardInfo[1], 
          self.boardInfo[2], 
          player['playerPosition'], 
          player['playerId']
        )
        self.players.append(remote_player)

  def on_player_move(self, data):
    for player in data:
      for i in range(len(self.players)):
        if self.players[i].getName() == player['playerId']:
          self.players[i].removePlayer()
          self.players[i].setPlayerPosition(player['playerPosition'])
          
