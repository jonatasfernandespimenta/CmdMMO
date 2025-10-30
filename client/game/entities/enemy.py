import time
import random
from game.mechanics.combat import CombatSystem
from game.entities.combat_entity import CombatEntity

class Enemy(CombatEntity):
  def __init__(self, position, lines, level=1, isBoss=False, elementType=None, term=None, mp=0, skills=None):
    # Initialize combat entity
    CombatEntity.__init__(self)
    
    self.enemyPosition = position
    self.level = level
    self.isBoss = isBoss
    self.lines = lines
    self.isInCombat = False
    self.id = random.randint(0, 1000000)
    self.term = term
    self.elementType = elementType

    # Combat system - initialize even without term for now
    self.combat = CombatSystem(term) if term else None
    self.skills = skills if skills else []

    if not hasattr(self, 'base_hp'):
      self.base_hp = 10
    if not hasattr(self, 'base_attack'):
      self.base_attack = 5
    if not hasattr(self, 'base_defense'):
      self.base_defense = 2
    if not hasattr(self, 'base_luck'):
      self.base_luck = 2
    if not hasattr(self, 'base_mp'):
      self.base_mp = 10
    if not hasattr(self, 'name'):
      self.name = "Enemy"
    if not hasattr(self, 'skills'):
      self.skills = []  # List of skill IDs this enemy can use
    
    self._calculate_stats()
    
    # Drops padrão
    self._calculate_drops()
    self.item_drops = []  # Lista de possíveis items com chance
  
  def _calculate_stats(self):
    """Calcula os stats baseado no level e se é boss"""
    if self.isBoss:
      self.hp = (self.base_hp + (self.level - 1) * 5) * 3
      self.maxHp = self.hp
      self.attack = (self.base_attack + (self.level - 1) * 2) * 2
      self.defense = (self.base_defense + (self.level - 1) * 1) * 2
      self.luck = (self.base_luck + (self.level - 1)) * 2
      self.mp = (self.base_mp + (self.level - 1) * 3) * 2
      self.maxMp = self.mp
      if not self.name.endswith('(BOSS)'):
        self.name = self.name + ' (BOSS)'
    else:
      self.hp = self.base_hp + (self.level - 1) * 5
      self.maxHp = self.hp
      self.attack = self.base_attack + (self.level - 1) * 2
      self.defense = self.base_defense + (self.level - 1) * 1
      self.luck = self.base_luck + (self.level - 1)
      self.mp = self.base_mp + (self.level - 1) * 3
      self.maxMp = self.mp
  
  # Combat methods (getStun, setStun, DoT methods) are inherited from CombatEntity


  def _calculate_drops(self):
    """Calcula os drops baseado no level e se é boss"""
    if self.isBoss:
      self.goldDrop = random.randint(self.level * 50, self.level * 100)
      self.xpDrop = random.randint(self.level * 100, self.level * 200)
    else:
      self.goldDrop = random.randint(self.level * 5, self.level * 15)
      self.xpDrop = random.randint(self.level * 10, self.level * 25)

  def moveEnemy(self, boardWidth, boardHeight, lines):
    if self.isInCombat == False:
      newEnemyPosition = self.enemyPosition.copy()
      direction = random.randint(0, 3)

      if direction == 0:
        if self.pathIsBlocked([self.enemyPosition[0]-1, self.enemyPosition[1]], boardWidth, boardHeight) == False:
          newEnemyPosition[0] -= 1
          self.removeEnemy(lines)
          self.enemyPosition = newEnemyPosition
          self.drawEnemy(lines)
      elif direction == 1:
        if self.pathIsBlocked([self.enemyPosition[0]+1, self.enemyPosition[1]], boardWidth, boardHeight) == False:
          newEnemyPosition[0] += 1
          self.removeEnemy(lines)
          self.enemyPosition = newEnemyPosition
          self.drawEnemy(lines)
      elif direction == 2:
        if self.pathIsBlocked([self.enemyPosition[0], self.enemyPosition[1]-1], boardWidth, boardHeight) == False:
          newEnemyPosition[1] -= 1
          self.removeEnemy(lines)
          self.enemyPosition = newEnemyPosition
          self.drawEnemy(lines)
      elif direction == 3:
        if self.pathIsBlocked([self.enemyPosition[0], self.enemyPosition[1]+1], boardWidth, boardHeight) == False:
          newEnemyPosition[1] += 1
          self.removeEnemy(lines)
          self.enemyPosition = newEnemyPosition
          self.drawEnemy(lines)


  def getIsInCombat(self):
    return self.isInCombat
  
  def setIsInCombat(self, isInCombat):
    self.isInCombat = isInCombat

  def getElementType(self):
    """Get enemy's elemental type"""
    return self.elementType

  def pathIsBlocked(self, enemyPosition, boardWidth, boardHeight):
    if enemyPosition[0] < 0 or enemyPosition[0] > boardHeight-1 or enemyPosition[1] < 0 or enemyPosition[1] > boardWidth-1:
      return True
    
    if self.lines[enemyPosition[0]][enemyPosition[1]] == '#':
      return True

    return False

  def getEnemyPosition(self):
    return self.enemyPosition
  
  def drawEnemy(self, lines):
    if self.isBoss:
      lines[self.enemyPosition[0]][self.enemyPosition[1]] = 'B'
    else:
      lines[self.enemyPosition[0]][self.enemyPosition[1]] = 'E'

  # getHp, setHp, getMP, setMP, getAttack, setAttack, getDefense, getLuck are inherited from CombatEntity

  def getID(self):
    return self.id
  
  def getLevel(self):
    return self.level
  
  def getGoldDrop(self):
    return self.goldDrop
  
  def getXpDrop(self):
    return self.xpDrop
  
  # getMaxHp, getMP, getMaxMP, setMP are inherited from CombatEntity
  
  def getSkills(self):
    """Get list of skills this enemy can use"""
    return self.skills
  
  def getName(self):
    return self.name
  
  def getIsBoss(self):
    return self.isBoss

  def removeEnemy(self, lines):
    lines[self.enemyPosition[0]][self.enemyPosition[1]] = '.'
  
  def get_drops(self):
    """Retorna os drops do inimigo (gold, xp e items)"""
    drops = {
      'gold': self.goldDrop,
      'xp': self.xpDrop,
      'items': []
    }
    
    # Calcular drops de items baseado em chance
    for item_drop in self.item_drops:
      if random.random() < item_drop['chance']:
        drops['items'].append(item_drop['item'])
    
    return drops

  # setDefense is inherited from CombatEntity

  def attackPlayer(self, player):
    """Attack player using combat system if available"""
    if self.combat:
      skillId = None
      
      # 40% chance to use a skill if enemy has skills and MP
      if self.skills and len(self.skills) > 0 and random.random() < 0.4:
        # Try to find a skill we can afford
        from game.skills.fighting_abilities import fighting_abilities
        affordable_skills = []
        
        for skill_id in self.skills:
          skill = next((s for s in fighting_abilities if s["id"] == skill_id), None)
          if skill and self.mp >= skill["mpCost"]:
            affordable_skills.append(skill_id)
        
        # Pick a random affordable skill
        if affordable_skills:
          skillId = random.choice(affordable_skills)
      
      self.combat.attack(self, player, "The enemy", "you", skillId)
    else:
      # Fallback if no combat system available
      damage = max(1, self.getAttack() - player.getDefense())
      player.setHp(player.getHp() - damage)
