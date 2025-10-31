import requests
import json

class APIClient:
  """Client for communicating with the game API"""
  
  def __init__(self, base_url='http://localhost:3001'):
    self.base_url = base_url
    self.player_id = None
  
  def createPlayer(self, name, player_class, maxDungeonLevel=0, maxGold=0, maxLevelReached=1):
    """
    Create a new player via POST request
    
    Args:
      name: Player name
      player_class: Player class (rogue, knight, wizard)
      maxDungeonLevel: Initial max dungeon level
      maxGold: Initial max gold
      maxLevelReached: Initial max level
    
    Returns:
      Player data from server or None if failed
    """
    try:
      response = requests.post(
        f'{self.base_url}/api/player',
        json={
          'name': name,
          'class': player_class,
          'maxDungeonLevel': maxDungeonLevel,
          'maxGold': maxGold,
          'maxLevelReached': maxLevelReached
        },
        headers={'Content-Type': 'application/json'}
      )
      
      if response.status_code == 201:
        player_data = response.json()
        self.player_id = player_data['id']
        return player_data
      else:
        print(f"Error creating player: {response.status_code} - {response.text}")
        return None
    except Exception as e:
      print(f"Failed to create player: {e}")
      return None
  
  def updatePlayer(self, player_class=None, maxDungeonLevel=None, maxGold=None, maxLevelReached=None):
    """
    Update player stats via PATCH request
    
    Args:
      player_class: Updated class (optional)
      maxDungeonLevel: Updated max dungeon level (optional)
      maxGold: Updated max gold (optional)
      maxLevelReached: Updated max level (optional)
    
    Returns:
      Updated player data or None if failed
    """
    if not self.player_id:
      print("No player ID set. Create player first.")
      return None
    
    try:
      # Build payload with only provided values
      payload = {}
      if player_class is not None:
        payload['class'] = player_class
      if maxDungeonLevel is not None:
        payload['maxDungeonLevel'] = maxDungeonLevel
      if maxGold is not None:
        payload['maxGold'] = maxGold
      if maxLevelReached is not None:
        payload['maxLevelReached'] = maxLevelReached
      
      response = requests.patch(
        f'{self.base_url}/api/player/{self.player_id}',
        json=payload,
        headers={'Content-Type': 'application/json'}
      )
      
      if response.status_code == 200:
        return response.json()
      else:
        print(f"Error updating player: {response.status_code} - {response.text}")
        return None
    except Exception as e:
      print(f"Failed to update player: {e}")
      return None
  
  def getPlayer(self, player_id=None):
    """
    Get player data by ID
    
    Args:
      player_id: Player ID (uses stored ID if not provided)
    
    Returns:
      Player data or None if failed
    """
    pid = player_id or self.player_id
    if not pid:
      print("No player ID provided")
      return None
    
    try:
      response = requests.get(f'{self.base_url}/api/player/{pid}')
      
      if response.status_code == 200:
        return response.json()
      else:
        return None
    except Exception as e:
      print(f"Failed to get player: {e}")
      return None
  
  # ==================== Bank API Methods ====================
  
  def createBankAccount(self, account_id, password, initial_gold=0):
    """
    Create a new bank account
    
    Args:
      account_id: Unique account identifier
      password: Account password (will be hashed server-side)
      initial_gold: Initial gold deposit (default 0)
    
    Returns:
      Bank account data or None if failed
    """
    if not self.player_id:
      print("No player ID set. Create player first.")
      return None
    
    try:
      response = requests.post(
        f'{self.base_url}/api/bank/account',
        json={
          'accountId': account_id,
          'playerId': self.player_id,
          'password': password,
          'gold': initial_gold
        },
        headers={'Content-Type': 'application/json'}
      )
      
      if response.status_code == 201:
        return response.json()
      elif response.status_code == 409:
        print(f"Account ID '{account_id}' already exists")
        return None
      else:
        print(f"Error creating bank account: {response.status_code} - {response.text}")
        return None
    except Exception as e:
      print(f"Failed to create bank account: {e}")
      return None
  
  def verifyBankAccount(self, account_id, password):
    """
    Verify bank account exists and password is correct
    
    Args:
      account_id: Account identifier
      password: Account password
    
    Returns:
      Account data if valid, None otherwise
    """
    try:
      response = requests.post(
        f'{self.base_url}/api/bank/account/verify',
        json={
          'accountId': account_id,
          'password': password
        },
        headers={'Content-Type': 'application/json'}
      )
      
      if response.status_code == 200:
        return response.json()
      else:
        return None
    except Exception as e:
      print(f"Failed to verify bank account: {e}")
      return None
  
  def getBankAccount(self, account_id, password):
    """
    Get bank account information
    
    Args:
      account_id: Account identifier
      password: Account password
    
    Returns:
      Account data or None if failed
    """
    try:
      response = requests.get(
        f'{self.base_url}/api/bank/account/{account_id}',
        params={'password': password}
      )
      
      if response.status_code == 200:
        return response.json()
      else:
        return None
    except Exception as e:
      print(f"Failed to get bank account: {e}")
      return None
  
  def depositGold(self, account_id, password, amount):
    """
    Deposit gold into bank account
    
    Args:
      account_id: Account identifier
      password: Account password
      amount: Amount of gold to deposit
    
    Returns:
      Updated account data or None if failed
    """
    try:
      response = requests.post(
        f'{self.base_url}/api/bank/deposit/gold',
        json={
          'accountId': account_id,
          'password': password,
          'amount': amount
        },
        headers={'Content-Type': 'application/json'}
      )
      
      if response.status_code == 200:
        return response.json()
      else:
        print(f"Error depositing gold: {response.status_code} - {response.text}")
        return None
    except Exception as e:
      print(f"Failed to deposit gold: {e}")
      return None
  
  def withdrawGold(self, account_id, password, amount):
    """
    Withdraw gold from bank account
    
    Args:
      account_id: Account identifier
      password: Account password
      amount: Amount of gold to withdraw
    
    Returns:
      Updated account data or None if failed
    """
    try:
      response = requests.post(
        f'{self.base_url}/api/bank/withdraw/gold',
        json={
          'accountId': account_id,
          'password': password,
          'amount': amount
        },
        headers={'Content-Type': 'application/json'}
      )
      
      if response.status_code == 200:
        return response.json()
      else:
        print(f"Error withdrawing gold: {response.status_code} - {response.text}")
        return None
    except Exception as e:
      print(f"Failed to withdraw gold: {e}")
      return None
  
  def depositItem(self, account_id, password, item_id):
    """
    Deposit item into bank account
    
    Args:
      account_id: Account identifier
      password: Account password
      item_id: Item ID to deposit
    
    Returns:
      Updated account data or None if failed
    """
    try:
      response = requests.post(
        f'{self.base_url}/api/bank/deposit/item',
        json={
          'accountId': account_id,
          'password': password,
          'itemId': item_id
        },
        headers={'Content-Type': 'application/json'}
      )
      
      if response.status_code == 200:
        return response.json()
      else:
        print(f"Error depositing item: {response.status_code} - {response.text}")
        return None
    except Exception as e:
      print(f"Failed to deposit item: {e}")
      return None
  
  def withdrawItem(self, account_id, password, item_id):
    """
    Withdraw item from bank account
    
    Args:
      account_id: Account identifier
      password: Account password
      item_id: Item ID to withdraw
    
    Returns:
      Updated account data or None if failed
    """
    try:
      response = requests.post(
        f'{self.base_url}/api/bank/withdraw/item',
        json={
          'accountId': account_id,
          'password': password,
          'itemId': item_id
        },
        headers={'Content-Type': 'application/json'}
      )
      
      if response.status_code == 200:
        return response.json()
      else:
        print(f"Error withdrawing item: {response.status_code} - {response.text}")
        return None
    except Exception as e:
      print(f"Failed to withdraw item: {e}")
      return None
