var express = require('express'),
    app = express(), 
    server = require('http').createServer(app)

const { createPlayer, updatePlayer, getPlayerById, getPlayerByName, getAllPlayers, getTop3ByGold, getTop3ByLevel, getTop3ByDungeonLevel, getAllByGold, getAllByLevel, getAllByDungeonLevel } = require('./database');

app.use(express.json());

server.listen(3001);

const io = require('socket.io')(server, {
  cors: {
    origin: '*',
  }
});

const players = [];

// POST - Criar novo player
app.post('/api/player', (req, res) => {
  try {
    const { name, class: playerClass, maxDungeonLevel = 0, maxGold = 0, maxLevelReached = 1 } = req.body;
    
    if (!name || !playerClass) {
      return res.status(400).json({ error: 'Name and class are required' });
    }
    
    const result = createPlayer.run({
      name,
      class: playerClass,
      maxDungeonLevel,
      maxGold,
      maxLevelReached
    });
    
    const newPlayer = getPlayerById.get(result.lastInsertRowid);
    res.status(201).json(newPlayer);
  } catch (error) {
    if (error.code === 'SQLITE_CONSTRAINT_UNIQUE') {
      return res.status(409).json({ error: 'Player name already exists' });
    }
    res.status(500).json({ error: error.message });
  }
});

// PATCH - Atualizar player
app.patch('/api/player/:id', (req, res) => {
  try {
    const playerId = parseInt(req.params.id);
    const { class: playerClass, maxDungeonLevel, maxGold, maxLevelReached } = req.body;
    
    const existingPlayer = getPlayerById.get(playerId);
    if (!existingPlayer) {
      return res.status(404).json({ error: 'Player not found' });
    }
    
    updatePlayer.run({
      id: playerId,
      class: playerClass || null,
      maxDungeonLevel: maxDungeonLevel !== undefined ? maxDungeonLevel : null,
      maxGold: maxGold !== undefined ? maxGold : null,
      maxLevelReached: maxLevelReached !== undefined ? maxLevelReached : null
    });
    
    const updatedPlayer = getPlayerById.get(playerId);
    res.json(updatedPlayer);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// GET - Listar todos os players (útil para debug)
app.get('/api/players', (req, res) => {
  try {
    const allPlayers = getAllPlayers.all();
    res.json(allPlayers);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// GET - Buscar player por ID
app.get('/api/player/:id', (req, res) => {
  try {
    const player = getPlayerById.get(parseInt(req.params.id));
    if (!player) {
      return res.status(404).json({ error: 'Player not found' });
    }
    res.json(player);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// GET - Top 3 players por gold
app.get('/api/leaderboard/gold', (req, res) => {
  try {
    const top3 = getTop3ByGold.all();
    res.json(top3);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// GET - Top 3 players por level
app.get('/api/leaderboard/level', (req, res) => {
  try {
    const top3 = getTop3ByLevel.all();
    res.json(top3);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// GET - Top 3 players por dungeon level
app.get('/api/leaderboard/dungeon', (req, res) => {
  try {
    const top3 = getTop3ByDungeonLevel.all();
    res.json(top3);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// GET - Full rankings for rank board
app.get('/api/rankings/gold', (req, res) => {
  try {
    const rankings = getAllByGold.all();
    res.json(rankings);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/rankings/level', (req, res) => {
  try {
    const rankings = getAllByLevel.all();
    res.json(rankings);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/rankings/dungeon', (req, res) => {
  try {
    const rankings = getAllByDungeonLevel.all();
    res.json(rankings);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

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
