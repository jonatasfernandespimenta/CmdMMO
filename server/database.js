const Database = require('better-sqlite3');
const crypto = require('crypto');
const db = new Database('cmdmmo.db');

// Criar tabela Player se não existir
db.exec(`
  CREATE TABLE IF NOT EXISTS Player (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    class TEXT NOT NULL,
    maxDungeonLevel INTEGER DEFAULT 0,
    maxGold INTEGER DEFAULT 0,
    maxLevelReached INTEGER DEFAULT 1,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
  )
`);

// Criar tabela BankAccount
db.exec(`
  CREATE TABLE IF NOT EXISTS BankAccount (
    accountId TEXT PRIMARY KEY,
    playerId INTEGER NOT NULL,
    password TEXT NOT NULL,
    gold INTEGER DEFAULT 0,
    items TEXT DEFAULT '[]',
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (playerId) REFERENCES Player(id)
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

// Leaderboard queries
const getTop3ByGold = db.prepare(`
  SELECT id, name, class, maxGold, maxLevelReached, maxDungeonLevel
  FROM Player 
  ORDER BY maxGold DESC 
  LIMIT 3
`);

const getTop3ByLevel = db.prepare(`
  SELECT id, name, class, maxLevelReached, maxGold, maxDungeonLevel
  FROM Player 
  ORDER BY maxLevelReached DESC 
  LIMIT 3
`);

const getTop3ByDungeonLevel = db.prepare(`
  SELECT id, name, class, maxDungeonLevel, maxLevelReached, maxGold
  FROM Player 
  ORDER BY maxDungeonLevel DESC 
  LIMIT 3
`);

// Full ranking queries (for rank board UI)
const getAllByGold = db.prepare(`
  SELECT id, name, class, maxGold as value
  FROM Player 
  ORDER BY maxGold DESC
`);

const getAllByLevel = db.prepare(`
  SELECT id, name, class, maxLevelReached as value
  FROM Player 
  ORDER BY maxLevelReached DESC
`);

const getAllByDungeonLevel = db.prepare(`
  SELECT id, name, class, maxDungeonLevel as value
  FROM Player 
  ORDER BY maxDungeonLevel DESC
`);

// Bank Account queries
const createBankAccount = db.prepare(`
  INSERT INTO BankAccount (accountId, playerId, password, gold, items)
  VALUES (@accountId, @playerId, @password, @gold, @items)
`);

const getBankAccountById = db.prepare('SELECT * FROM BankAccount WHERE accountId = ?');

const updateBankAccountGold = db.prepare(`
  UPDATE BankAccount 
  SET gold = @gold,
      updatedAt = CURRENT_TIMESTAMP
  WHERE accountId = @accountId
`);

const updateBankAccountItems = db.prepare(`
  UPDATE BankAccount 
  SET items = @items,
      updatedAt = CURRENT_TIMESTAMP
  WHERE accountId = @accountId
`);

// Helper functions
function hashPassword(password) {
  return crypto.createHash('sha256').update(password).digest('hex');
}

function verifyPassword(password, hashedPassword) {
  return hashPassword(password) === hashedPassword;
}

module.exports = {
  db,
  createPlayer,
  updatePlayer,
  getPlayerById,
  getPlayerByName,
  getAllPlayers,
  getTop3ByGold,
  getTop3ByLevel,
  getTop3ByDungeonLevel,
  getAllByGold,
  getAllByLevel,
  getAllByDungeonLevel,
  createBankAccount,
  getBankAccountById,
  updateBankAccountGold,
  updateBankAccountItems,
  hashPassword,
  verifyPassword
};
