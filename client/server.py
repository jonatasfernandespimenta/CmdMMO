import socketio
import json
from player import Player

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
      if player['playerId'] not in self.players:
        self.players.append(Player(self.boardInfo[0], self.boardInfo[1], self.boardInfo[2], player['playerPosition'], player['playerId']))

  def on_player_move(self, data):
    for player in data:
      for i in range(len(self.players)):
        if self.players[i].getName() == player['playerId']:
          self.players[i].removePlayer()
          self.players[i].setPlayerPosition(player['playerPosition'])
          
