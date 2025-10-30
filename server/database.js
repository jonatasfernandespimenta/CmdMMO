const Database = require('better-sqlite3');
const db = new Database('cmdmmo.db');

// Criar tabela Player se não existir
db.exec(`
  CREATE TABLE IF NOT EXISTS Player (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    class TEXT NOT NULL,
    maxDungeonLevel INTEGER DEFAULT 0,
    maxGold INTEGER DEFAULT 0,
    maxLevelReached INTEGER DEFAULT 1,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
  )
`);

// Prepared statements para operações
const createPlayer = db.prepare(`
  INSERT INTO Player (name, class, maxDungeonLevel, maxGold, maxLevelReached)
  VALUES (@name, @class, @maxDungeonLevel, @maxGold, @maxLevelReached)
`);

const updatePlayer = db.prepare(`
  UPDATE Player 
  SET class = COALESCE(@class, class),
      maxDungeonLevel = COALESCE(@maxDungeonLevel, maxDungeonLevel),
      maxGold = COALESCE(@maxGold, maxGold),
      maxLevelReached = COALESCE(@maxLevelReached, maxLevelReached),
      updatedAt = CURRENT_TIMESTAMP
  WHERE id = @id
`);

const getPlayerById = db.prepare('SELECT * FROM Player WHERE id = ?');
const getPlayerByName = db.prepare('SELECT * FROM Player WHERE name = ?');
const getAllPlayers = db.prepare('SELECT * FROM Player');

module.exports = {
  db,
  createPlayer,
  updatePlayer,
  getPlayerById,
  getPlayerByName,
  getAllPlayers
};
