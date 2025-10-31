import json
import random
from engine.core.player import Player as BasePlayer
from game.helper import blockers
from game.mechanics.farm import Farm
from game.mechanics.combat import CombatSystem
from game.entities.combat_entity import CombatEntity

class Player(BasePlayer, CombatEntity):
  """MMO Player - extends engine Player with MMO-specific features"""
  
  CLASSES = {
    'rogue': {
      'hp': 80,
      'attack': 15,
      'defense': 4,
      'luck': 8,
      'elementType': 'poison',
      'mp': 20
    },
    'knight': {
      'hp': 120,
      'attack': 12,
      'defense': 10,
      'luck': 3,
      'elementType': 'earth',
      'mp': 20
    },
    'ice_wizard': {
      'hp': 70,
      'attack': 18,
      'defense': 3,
      'luck': 5,
      'elementType': 'ice',
      'mp': 50
    },
    'fire_mage': {
      'hp': 75,
      'attack': 20,
      'defense': 2,
      'luck': 4,
      'elementType': 'fire',
      'mp': 60
    },
  }

  def __init__(self, lines, windowWidth, windowHeight, playerPosition, name, playerClass, term, api_client=None):
    # Initialize base player (movement, inventory, etc)
    BasePlayer.__init__(self, lines, windowWidth, windowHeight, playerPosition, name, term, blockers)
    
    # Initialize combat entity (hp, mp, stun, DoT, etc)
    CombatEntity.__init__(self)
    
    # MMO-specific: Player class system
    self.playerClass = playerClass.lower()
    classStats = self.CLASSES[self.playerClass]
    
    # Override base stats with class stats
    self.hp = classStats['hp']
    self.maxHp = classStats['hp']
    self.attack = classStats['attack']
    self.defense = classStats['defense']
    self.luck = classStats['luck']
    self.mp = classStats['mp']
    self.maxMp = classStats['mp']
    self.skillPoints = 0  # Skill points to spend on abilities (starting with 5 for testing)

    self.skills = []  # List of skill IDs the player has learned
    self.skillLevels = {}  # Track level for each skill for scaling
    self.isSkillsMenuOpen = False  # Skills menu state
    self.isPartyMenuOpen = False  # Party menu state
    self.isHouseEditorOpen = False  # House editor state
    self.pendingLevelUp = False  # Flag to show level up UI

    ## MMO-specific: Rank System
    self.maxDungeonLevel = 1
    self.maxGoldEarned = 0
    
    # MMO-specific: Properties (houses, farms, etc)
    self.property = []
    self.currentMap = 'dungeon'
    
    # MMO-specific: Farm system
    self.farm = Farm(self)
    
    # Combat system
    self.combat = CombatSystem(term)
    
    # API client for syncing with server
    self.api_client = api_client
    
    # Track previous values to detect changes
    self._prev_maxGold = 0
    self._prev_maxDungeonLevel = 1
    self._prev_maxLevelReached = 1
  # ==================== MMO-Specific ====================
  
  def getPlayerClass(self):
    """Get player class"""
    return self.playerClass.capitalize()
  
  # getLuck() is now inherited from CombatEntity
  
  def getElementType(self):
    """Get player's elemental type based on class"""
    return self.CLASSES[self.playerClass]['elementType']

  def addProperty(self, property):
    """Add property to player (house, farm, etc)"""
    self.property.append(property)

  def getProperties(self):
    """Get all owned properties"""
    return self.property
  
  def getCurrentMap(self):
    """Get current map name"""
    return self.currentMap
  
  def setCurrentMap(self, mapName):
    """Set current map name"""
    self.currentMap = mapName

  # ==================== Overrides ====================
  
  def movePlayer(self, sio):
    """Override to add multiplayer network sync"""
    def network_callback(new_position):
      sio.emit('move', json.dumps({"playerId": self.name, "playerPosition": new_position}))
    
    super().movePlayer(network_callback)
  
  def levelUp(self):
    """Override to add luck stat increase and trigger UI"""
    super().levelUp()  # Call base levelUp
    self.luck += 1  # MMO-specific: increase luck

    skillPointsAmount = 1 + (self.level // 5)

    self.skillPoints += skillPointsAmount  # MMO-specific: gain skill point
    self.upgradeMP(5)  # MMO-specific: increase MP
    
    # Upgrade all learned skills
    for skillId in self.skills:
      if skillId not in self.skillLevels:
        self.skillLevels[skillId] = 1
      self.skillLevels[skillId] += 1
    
    self.pendingLevelUp = True  # Set flag to show level up UI
    self._syncStatsToServer()  # Sync max level to server

  def interactWithChest(self, chest, sio=None, party=None):
    """Interact with chest and collect loot"""
    if chest.getPosition() == self.playerPosition and chest.open == False:
      loot = chest.openChest()
      self.addToInventory(loot)  # Use base class method
      
      # Sync chest opening with party if in party
      if sio and party and party.is_in_party():
        import json
        sio.emit('chest_opened', json.dumps({
          'playerId': self.name,
          'chestId': chest.getID(),
          'position': chest.getPosition()
        }))

  def addSkill(self, skillId):
    """Add a new skill to the player's skill list"""
    if skillId not in self.skills:
      self.skills.append(skillId)
      self.skillLevels[skillId] = 1  # Start at level 1
  
  def getIsSkillsMenuOpen(self):
    """Check if skills menu is open"""
    return self.isSkillsMenuOpen
  
  def setIsSkillsMenuOpen(self, isOpen):
    """Set skills menu state"""
    self.isSkillsMenuOpen = isOpen
  
  def getSkillLevel(self, skillId):
    """Get the level of a specific skill"""
    return self.skillLevels.get(skillId, 1)
  
  def getScaledSkillDamage(self, skillId, baseDamage):
    """Get scaled damage for a skill based on its level"""
    skillLevel = self.getSkillLevel(skillId)
    # Each skill level adds 10% to base damage
    return int(baseDamage * (1 + (skillLevel - 1) * 0.1))
  
  def getScaledSkillMpCost(self, skillId, baseMpCost):
    """Get scaled MP cost for a skill based on its level"""
    skillLevel = self.getSkillLevel(skillId)
    # Each skill level adds 5% to MP cost (rounded up)
    return int(baseMpCost * (1 + (skillLevel - 1) * 0.05))

  # ==================== Combat ====================
  # Combat methods (getStun, setStun, getMP, setMP, DoT methods) are inherited from CombatEntity
  
  def upgradeMP(self, amount):
    """Increase max MP"""
    self.maxMp += amount
    self.mp = self.maxMp  # Refill MP when upgrading

  def collidedWithEnemy(self, enemies):
    """Check if player collided with any enemy"""
    for enemy in enemies:
      if enemy.getEnemyPosition() == self.playerPosition:
        return True
    return False

  def attackEnemy(self, enemy):
    """Attack an enemy using the combat system"""
    enemyDied = self.combat.attack(self, enemy, "You", "the enemy")
    
    if enemyDied:
      print(self.term.bold_green("You killed the enemy!"))
      enemy.removeEnemy(self.lines)
      return True
    
    # Enemy counterattacks if still alive
    enemy.attackPlayer(self)
    return False

  # ==================== Override Base Methods ====================
  
  def addGold(self, amount: int):
    """Override addGold to sync maxGoldEarned changes to server"""
    prev_max = self.maxGoldEarned
    super().addGold(amount)  # Call base method
    
    # If maxGoldEarned increased, sync to server
    if self.maxGoldEarned > prev_max:
      self._syncStatsToServer()

  # ==================== Update ====================
  
  def init(self, sio):
    """Main update method called every frame"""
    self.movePlayer(sio)
    self.inventoryControl()
  
  def inventoryControl(self):
    """Handle inventory-related input (can be extended)"""
    pass

  # ==================== Rank ====================
  def getMaxGoldEarned(self):
    """Get maximum gold ever earned by the player"""
    return self.maxGoldEarned
  
  def setMaxDungeonLevel(self, level):
    """Set maximum dungeon level (triggers API sync)"""
    if level > self.maxDungeonLevel:
      self.maxDungeonLevel = level
      self._syncStatsToServer()
  
  def getMaxDungeonLevel(self):
    """Get maximum dungeon level reached by the player"""
    return self.maxDungeonLevel
  
  def getMaxLevelReached(self):
    """Get maximum player level reached"""
    return self.maxLevelReached
  
  # ==================== API Sync ====================
  def _syncStatsToServer(self):
    """Sync player stats to server if they changed"""
    if not self.api_client:
      return
    
    # Check what changed
    changed = False
    updates = {}
    
    if self.maxGoldEarned != self._prev_maxGold:
      updates['maxGold'] = self.maxGoldEarned
      self._prev_maxGold = self.maxGoldEarned
      changed = True
    
    if self.maxDungeonLevel != self._prev_maxDungeonLevel:
      updates['maxDungeonLevel'] = self.maxDungeonLevel
      self._prev_maxDungeonLevel = self.maxDungeonLevel
      changed = True
    
    if self.maxLevelReached != self._prev_maxLevelReached:
      updates['maxLevelReached'] = self.maxLevelReached
      self._prev_maxLevelReached = self.maxLevelReached
      changed = True
    
    # Send PATCH request if anything changed
    if changed:
      self.api_client.updatePlayer(**updates)
