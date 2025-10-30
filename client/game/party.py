import json

class Party:
  """Manages party state on the client side"""
  
  def __init__(self, sio, player_id):
    self.sio = sio
    self.player_id = player_id
    self.party_id = None
    self.leader = None
    self.members = []
    self.pending_invites = []
    self.online_players = []
    
    # Setup event listeners
    self._setup_listeners()
  
  def _setup_listeners(self):
    """Setup WebSocket event listeners"""
    self.sio.on('party_invite_received', self._on_invite_received)
    self.sio.on('party_updated', self._on_party_updated)
    self.sio.on('party_left', self._on_party_left)
    self.sio.on('online_players_list', self._on_online_players)
    self.sio.on('pending_invites_list', self._on_pending_invites)
    self.sio.on('current_party_info', self._on_current_party_info)
  
  def _on_invite_received(self, data):
    """Called when player receives a party invite"""
    invite = json.loads(data)
    # Add to pending invites if not already there
    if not any(i['partyId'] == invite['partyId'] for i in self.pending_invites):
      self.pending_invites.append(invite)
  
  def _on_party_updated(self, data):
    """Called when party state changes"""
    party = json.loads(data)
    self.party_id = party['id']
    self.leader = party['leader']
    self.members = party['members']
  
  def _on_party_left(self, data):
    """Called when player successfully leaves party"""
    self.party_id = None
    self.leader = None
    self.members = []
  
  def _on_online_players(self, data):
    """Called when online players list is received"""
    self.online_players = json.loads(data)
  
  def _on_pending_invites(self, data):
    """Called when pending invites list is received"""
    self.pending_invites = json.loads(data)
  
  def _on_current_party_info(self, data):
    """Called when current party info is received"""
    party = json.loads(data)
    if party:
      self.party_id = party['id']
      self.leader = party['leader']
      self.members = party['members']
    else:
      self.party_id = None
      self.leader = None
      self.members = []
  
  # Public methods
  def invite_player(self, target_player_id):
    """Send party invite to another player"""
    self.sio.emit('party_invite', json.dumps({
      'fromPlayer': self.player_id,
      'toPlayer': target_player_id
    }))
  
  def accept_invite(self, party_id):
    """Accept a party invite"""
    self.sio.emit('party_accept', json.dumps({
      'playerId': self.player_id,
      'partyId': party_id
    }))
    # Remove from pending invites
    self.pending_invites = [i for i in self.pending_invites if i['partyId'] != party_id]
  
  def decline_invite(self, party_id):
    """Decline a party invite"""
    self.sio.emit('party_decline', json.dumps({
      'playerId': self.player_id,
      'partyId': party_id
    }))
    # Remove from pending invites
    self.pending_invites = [i for i in self.pending_invites if i['partyId'] != party_id]
  
  def leave_party(self):
    """Leave current party"""
    if self.party_id:
      self.sio.emit('party_leave', json.dumps({
        'playerId': self.player_id
      }))
  
  def request_online_players(self):
    """Request list of online players"""
    self.sio.emit('get_online_players', json.dumps({
      'requesterId': self.player_id
    }))
  
  def request_pending_invites(self):
    """Request list of pending invites"""
    self.sio.emit('get_pending_invites', json.dumps({
      'playerId': self.player_id
    }))
  
  def request_current_party(self):
    """Request current party info"""
    self.sio.emit('get_current_party', json.dumps({
      'playerId': self.player_id
    }))
  
  # Getters
  def is_in_party(self):
    """Check if player is in a party"""
    return self.party_id is not None
  
  def is_leader(self):
    """Check if player is party leader"""
    return self.leader == self.player_id
  
  def get_members(self):
    """Get list of party members"""
    return self.members.copy()
  
  def get_pending_invites(self):
    """Get list of pending invites"""
    return self.pending_invites.copy()
  
  def get_online_players(self):
    """Get list of online players"""
    return self.online_players.copy()
  
  def get_party_id(self):
    """Get current party ID"""
    return self.party_id
