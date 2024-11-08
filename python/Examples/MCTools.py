
def npvs( event ) :
  return sum( 1 for vertex in event.MCVertices if vertex.type ==1 )

def from_charm( track, event ):
  if track.mcParticleIndex == -1: return False 
  mcp = event.MCParticles[track.mcParticleIndex]
  charm_ids = [411, 421, 413, 423, 431, 4122, 4222, 4212, 4112, 4232, 4132]
  if abs(mcp.motherID) in charm_ids or abs(mcp.GDmotherID) in charm_ids : return True
  return False 

def true_origin_vertex( particle, event ) :
  if particle.mcParticleIndex == -1 : return None
  return event.MCVertices[ event.MCParticles[particle.mcParticleIndex].vertexIndex ]

def from_beauty( track, event ):
  if track.mcParticleIndex == -1: return False 
  mcp = event.MCParticles[track.mcParticleIndex]
  b_ids = [511, 521, 531, 541, 5122, 5112, 5222, 5132] 
  if abs(mcp.motherID) in b_ids or abs(mcp.GDmotherID) in b_ids : return True
  return False

def is_from( track, event, index ):
  if track.mcParticleIndex == -1 : return False
  if track.mcParticleIndex >= len(event.MCParticles) : return False 
  mcp = event.MCParticles[track.mcParticleIndex] 
  return abs(mcp.motherID) == index or abs(mcp.GDmotherID) == index

def print_mc_particle(track, mcParticles ) :
  if track.mcParticleIndex == -1 : return False
  mcp = mcParticles[track.mcParticleIndex]
  print( "{} {} {}".format(mcp.ID, mcp.motherID, mcp.GDmotherID ) )

def get_mc_particle(track, event) : 
  return None if track.mcParticleIndex == -1 else event.MCParticles[track.mcParticleIndex]  

def get_true_pv(vertex, mcVertices) : 
  if vertex.trueVertexIndex != -1 and vertex.trueVertexIndex >= len( mcVertices ) : 
    print(f"Error, vertex {vertex.trueVertexIndex} out of range {len(event.MCVertices)}")
    return None
  return None if vertex.trueVertexIndex == -1 else mcVertices[vertex.trueVertexIndex] 

def true_origin_vertex( particle, event ) :
  if particle.mcParticleIndex == -1 : return None
  true_particle = event.MCParticles[particle.mcParticleIndex]
  return event.MCVertices[ true_particle.vertexIndex ]

