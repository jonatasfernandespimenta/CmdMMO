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
const parties = new Map(); // partyId -> { leader, members: [], invites: [] }
const playerToParty = new Map(); // playerId -> partyId
const playerToSocket = new Map(); // playerId -> socketId
const partyDungeons = new Map(); // partyId -> { seed, level, enemies: [], chests: [], portalActive: bool }
let partyIdCounter = 0;

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

      playerToSocket.set(args.playerId, socket.id);
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

  // Party System Events
  socket.on('party_invite', (args) => {
    const { fromPlayer, toPlayer } = JSON.parse(args);
    
    // Check if fromPlayer already has a party
    let partyId = playerToParty.get(fromPlayer);
    
    if (!partyId) {
      // Create new party
      partyId = `party_${partyIdCounter++}`;
      parties.set(partyId, {
        id: partyId,
        leader: fromPlayer,
        members: [fromPlayer],
        invites: []
      });
      playerToParty.set(fromPlayer, partyId);
    }
    
    const party = parties.get(partyId);
    
    // Check if invite already exists or player is already in party
    if (party.invites.includes(toPlayer) || party.members.includes(toPlayer)) {
      return;
    }
    
    // Add invite
    party.invites.push(toPlayer);
    
    // Notify target player
    const targetSocketId = playerToSocket.get(toPlayer);
    if (targetSocketId) {
      io.to(targetSocketId).emit('party_invite_received', JSON.stringify({
        partyId,
        fromPlayer,
        leader: party.leader
      }));
    }
  });

  socket.on('party_accept', (args) => {
    const { playerId, partyId } = JSON.parse(args);
    
    const party = parties.get(partyId);
    if (!party) return;
    
    // Remove from invites and add to members
    party.invites = party.invites.filter(p => p !== playerId);
    
    if (!party.members.includes(playerId)) {
      party.members.push(playerId);
      playerToParty.set(playerId, partyId);
    }
    
    // Notify all party members
    party.members.forEach(memberId => {
      const socketId = playerToSocket.get(memberId);
      if (socketId) {
        io.to(socketId).emit('party_updated', JSON.stringify(party));
      }
    });
  });

  socket.on('party_decline', (args) => {
    const { playerId, partyId } = JSON.parse(args);
    
    const party = parties.get(partyId);
    if (!party) return;
    
    // Remove from invites
    party.invites = party.invites.filter(p => p !== playerId);
  });

  socket.on('party_leave', (args) => {
    const { playerId } = JSON.parse(args);
    
    const partyId = playerToParty.get(playerId);
    if (!partyId) return;
    
    const party = parties.get(partyId);
    if (!party) return;
    
    // Remove player from party
    party.members = party.members.filter(p => p !== playerId);
    playerToParty.delete(playerId);
    
    // If party is empty, delete it
    if (party.members.length === 0) {
      parties.delete(partyId);
    } else {
      // If leader left, assign new leader
      if (party.leader === playerId) {
        party.leader = party.members[0];
      }
      
      // Notify remaining members
      party.members.forEach(memberId => {
        const socketId = playerToSocket.get(memberId);
        if (socketId) {
          io.to(socketId).emit('party_updated', JSON.stringify(party));
        }
      });
    }
    
    // Notify the player who left
    const socketId = playerToSocket.get(playerId);
    if (socketId) {
      io.to(socketId).emit('party_left', JSON.stringify({ success: true }));
    }
  });

  socket.on('get_online_players', (args) => {
    const { requesterId } = JSON.parse(args);
    const socketId = playerToSocket.get(requesterId);
    
    if (socketId) {
      // Return list of online players (excluding requester)
      const onlinePlayers = players
        .filter(p => p.playerId !== requesterId)
        .map(p => ({ playerId: p.playerId }));
      
      io.to(socketId).emit('online_players_list', JSON.stringify(onlinePlayers));
    }
  });

  socket.on('get_pending_invites', (args) => {
    const { playerId } = JSON.parse(args);
    const socketId = playerToSocket.get(playerId);
    
    if (socketId) {
      // Find all parties where player has pending invite
      const pendingInvites = [];
      parties.forEach((party, partyId) => {
        if (party.invites.includes(playerId)) {
          pendingInvites.push({
            partyId,
            leader: party.leader,
            memberCount: party.members.length
          });
        }
      });
      
      io.to(socketId).emit('pending_invites_list', JSON.stringify(pendingInvites));
    }
  });

  socket.on('get_current_party', (args) => {
    const { playerId } = JSON.parse(args);
    const partyId = playerToParty.get(playerId);
    const socketId = playerToSocket.get(playerId);
    
    if (socketId) {
      if (partyId) {
        const party = parties.get(partyId);
        io.to(socketId).emit('current_party_info', JSON.stringify(party));
      } else {
        io.to(socketId).emit('current_party_info', JSON.stringify(null));
      }
    }
  });

  // ==================== Dungeon Sync Events ====================
  
  socket.on('dungeon_generate', (args) => {
    const { playerId, seed, level } = JSON.parse(args);
    const partyId = playerToParty.get(playerId);
    
    if (partyId) {
      // Initialize or update party dungeon
      if (!partyDungeons.has(partyId)) {
        partyDungeons.set(partyId, {
          seed,
          level,
          enemies: [],
          chests: [],
          portalActive: false
        });
      }
      
      const dungeon = partyDungeons.get(partyId);
      
      // Broadcast dungeon seed to all party members
      const party = parties.get(partyId);
      if (party) {
        party.members.forEach(memberId => {
          const socketId = playerToSocket.get(memberId);
          if (socketId) {
            io.to(socketId).emit('dungeon_seed', JSON.stringify({
              seed: dungeon.seed,
              level: dungeon.level
            }));
          }
        });
      }
    }
  });

  socket.on('enemy_spawn', (args) => {
    const { playerId, enemyId, position, level, isBoss, name } = JSON.parse(args);
    const partyId = playerToParty.get(playerId);
    
    if (partyId) {
      const dungeon = partyDungeons.get(partyId);
      if (dungeon) {
        // Add enemy to dungeon state
        dungeon.enemies.push({ enemyId, position, level, isBoss, name, hp: null });
        
        // Broadcast to all party members
        const party = parties.get(partyId);
        if (party) {
          party.members.forEach(memberId => {
            if (memberId !== playerId) {
              const socketId = playerToSocket.get(memberId);
              if (socketId) {
                io.to(socketId).emit('enemy_spawned', JSON.stringify({ enemyId, position, level, isBoss, name }));
              }
            }
          });
        }
      }
    }
  });

  socket.on('enemy_died', (args) => {
    const { playerId, enemyId } = JSON.parse(args);
    const partyId = playerToParty.get(playerId);
    
    if (partyId) {
      const dungeon = partyDungeons.get(partyId);
      if (dungeon) {
        // Remove enemy from dungeon state
        dungeon.enemies = dungeon.enemies.filter(e => e.enemyId !== enemyId);
        
        // Broadcast to all party members
        const party = parties.get(partyId);
        if (party) {
          party.members.forEach(memberId => {
            if (memberId !== playerId) {
              const socketId = playerToSocket.get(memberId);
              if (socketId) {
                io.to(socketId).emit('enemy_removed', JSON.stringify({ enemyId }));
              }
            }
          });
        }
      }
    }
  });

  socket.on('chest_opened', (args) => {
    const { playerId, chestId, position } = JSON.parse(args);
    const partyId = playerToParty.get(playerId);
    
    if (partyId) {
      // Broadcast to all party members
      const party = parties.get(partyId);
      if (party) {
        party.members.forEach(memberId => {
          if (memberId !== playerId) {
            const socketId = playerToSocket.get(memberId);
            if (socketId) {
              io.to(socketId).emit('chest_opened_sync', JSON.stringify({ chestId, position }));
            }
          }
        });
      }
    }
  });

  socket.on('portal_spawned', (args) => {
    const { playerId, position } = JSON.parse(args);
    const partyId = playerToParty.get(playerId);
    
    if (partyId) {
      const dungeon = partyDungeons.get(partyId);
      if (dungeon) {
        dungeon.portalActive = true;
        
        // Broadcast to all party members
        const party = parties.get(partyId);
        if (party) {
          party.members.forEach(memberId => {
            if (memberId !== playerId) {
              const socketId = playerToSocket.get(memberId);
              if (socketId) {
                io.to(socketId).emit('portal_spawned_sync', JSON.stringify({ position }));
              }
            }
          });
        }
      }
    }
  });

  socket.on('stage_changed', (args) => {
    const { playerId, newLevel } = JSON.parse(args);
    const partyId = playerToParty.get(playerId);
    
    if (partyId) {
      const dungeon = partyDungeons.get(partyId);
      if (dungeon) {
        dungeon.level = newLevel;
        dungeon.enemies = [];
        dungeon.chests = [];
        dungeon.portalActive = false;
        
        // Broadcast to all party members
        const party = parties.get(partyId);
        if (party) {
          party.members.forEach(memberId => {
            if (memberId !== playerId) {
              const socketId = playerToSocket.get(memberId);
              if (socketId) {
                io.to(socketId).emit('stage_changed_sync', JSON.stringify({ newLevel }));
              }
            }
          });
        }
      }
    }
  });

  socket.on('combat_start', (args) => {
    const { playerId, enemyId } = JSON.parse(args);
    const partyId = playerToParty.get(playerId);
    
    if (partyId) {
      // Broadcast to all party members
      const party = parties.get(partyId);
      if (party) {
        party.members.forEach(memberId => {
          if (memberId !== playerId) {
            const socketId = playerToSocket.get(memberId);
            if (socketId) {
              io.to(socketId).emit('combat_started', JSON.stringify({ playerId, enemyId }));
            }
          }
        });
      }
    }
  });

  socket.on('player_damaged', (args) => {
    const { playerId, damage, currentHp } = JSON.parse(args);
    const partyId = playerToParty.get(playerId);
    
    if (partyId) {
      // Broadcast to all party members
      const party = parties.get(partyId);
      if (party) {
        party.members.forEach(memberId => {
          if (memberId !== playerId) {
            const socketId = playerToSocket.get(memberId);
            if (socketId) {
              io.to(socketId).emit('party_member_damaged', JSON.stringify({ playerId, damage, currentHp }));
            }
          }
        });
      }
    }
  });

  socket.on('disconnect', () => {
    // Remove player from tracking
    const disconnectedPlayer = Array.from(playerToSocket.entries())
      .find(([_, socketId]) => socketId === socket.id);
    
    if (disconnectedPlayer) {
      const playerId = disconnectedPlayer[0];
      playerToSocket.delete(playerId);
      
      // Remove from players array
      const playerIndex = players.findIndex(p => p.playerId === playerId);
      if (playerIndex !== -1) {
        players.splice(playerIndex, 1);
        io.emit('joined', players);
      }
    }
  });
});
