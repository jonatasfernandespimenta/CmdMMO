var express = require('express'),
    app = express(), 
    server = require('http').createServer(app)

server.listen(3001);

const io = require('socket.io')(server, {
  cors: {
    origin: '*',
  }
});

const players = [];

io.on("connection", (socket) => {
  socket.on('join', (args) => {
    args = JSON.parse(args);
    
    if(!players.find(player => player.playerId === args.playerId)) {
      players.push({
        playerId: args.playerId,
        playerPosition: args.playerPosition,
      });

      io.emit('joined', players);  
    }
  });

  socket.on("move", (args) => {
    args = JSON.parse(args);

    const playerIndex = players.findIndex(p => p.playerId === args.playerId);

    if (playerIndex !== -1) {
      players[playerIndex].playerPosition = args.playerPosition;
    }

    io.emit('moved', players);
  });
});
