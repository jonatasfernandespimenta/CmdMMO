class CombatEntity:
  """Base class for entities that can participate in combat (Player, Enemy, etc)"""
  
  def __init__(self):
    """Initialize combat-related attributes"""
    # Combat stats
    self.hp = 0
    self.maxHp = 0
    self.attack = 0
    self.defense = 0
    self.luck = 0
    self.mp = 0
    self.maxMp = 0
    
    # Status effects
    self.stun = {'isStunned': False, 'duration': 0}
    self.dot_effects = []  # List of active damage-over-time effects
  
  # ==================== HP ====================
  
  def getHp(self):
    """Get current HP"""
    return self.hp
  
  def getMaxHp(self):
    """Get max HP"""
    return self.maxHp
  
  def setHp(self, hp):
    """Set current HP (capped at maxHp)"""
    self.hp = max(0, min(hp, self.maxHp))
  
  # ==================== MP ====================
  
  def getMP(self):
    """Get current MP"""
    return self.mp
  
  def getMaxMP(self):
    """Get max MP"""
    return self.maxMp
  
  def setMP(self, mp):
    """Set current MP (capped at maxMp)"""
    self.mp = max(0, min(mp, self.maxMp))
  
  # ==================== Combat Stats ====================
  
  def getAttack(self):
    """Get attack stat"""
    return self.attack
  
  def setAttack(self, attack):
    """Set attack stat"""
    self.attack = attack
  
  def getDefense(self):
    """Get defense stat"""
    return self.defense
  
  def setDefense(self, defense):
    """Set defense stat"""
    self.defense = defense
  
  def getLuck(self):
    """Get luck stat"""
    return self.luck
  
  def setLuck(self, luck):
    """Set luck stat"""
    self.luck = luck
  
  # ==================== Stun System ====================
  
  def getStun(self):
    """Get stun status"""
    return self.stun
  
  def setStun(self, isStunned, duration=0):
    """Set stun status and duration"""
    self.stun['isStunned'] = isStunned
    self.stun['duration'] = duration
  
  # ==================== DoT (Damage over Time) System ====================
  
  def addDotEffect(self, skillName, damage, duration):
    """Add a damage-over-time effect"""
    # Check if effect already exists and update it
    for effect in self.dot_effects:
      if effect['name'] == skillName:
        effect['damage'] = damage
        effect['duration'] = duration
        return
    
    # Add new effect
    self.dot_effects.append({
      'name': skillName,
      'damage': damage,
      'duration': duration
    })
  
  def getDotEffects(self):
    """Get all active DoT effects"""
    return self.dot_effects
  
  def processDotEffects(self):
    """Process DoT effects, applying damage and decreasing duration
    
    Returns:
      tuple: (total_damage, list of expired effect indices)
    """
    total_damage = 0
    effects_to_remove = []
    
    for i, effect in enumerate(self.dot_effects):
      total_damage += effect['damage']
      effect['duration'] -= 1
      
      if effect['duration'] <= 0:
        effects_to_remove.append(i)
    
    # Remove expired effects (in reverse order to avoid index issues)
    for i in reversed(effects_to_remove):
      self.dot_effects.pop(i)
    
    return total_damage, effects_to_remove
