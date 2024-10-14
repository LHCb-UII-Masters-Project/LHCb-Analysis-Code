#include "Event/uComposite.h"
#include <map>
#include <vector> 

void uComposite::rebuild_sv_pointers( std::vector<uComposite>& svs, 
                          const std::vector<uParticle>& tracks )
{
  std::map<unsigned, const uParticle*> track_index; 
  for( const auto& track : tracks){
    if( track_index.count( track.index) != 0 ) 
      std::cout << "ERROR, duplicated index??" << " " << track.index << std::endl; 
    track_index[track.index] = &track; 
  }
/*
  for( const auto& [key, track] : track_index )
  {
    std::cout << key << " " << track->firstState.tx << " " << track->firstState.ty << " "  << track->firstState.qop << std::endl; 
  }
*/
  for( auto& sv : svs ) 
  {
    for( int i = 0 ; i != 4; ++i )
    {
      if( sv.tracks_index[i] != -1 ) sv.tracks.push_back( track_index[ sv.tracks_index[i]] ); 
    }
  }
}
