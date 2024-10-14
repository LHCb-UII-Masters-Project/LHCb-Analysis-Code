#ifndef uCOMPOSITE_H
#define uCOMPOSITE_H 1 

#include <iostream>
#include "Event/uParticle.h"
#include "Event/uVertex.h" 

#include "Math/Vector4D.h"

struct uVertex; 

struct uComposite 
{
  uComposite() = default;  
  float mass; 
  float x, y, z, px, py, pz;
  std::array<int, 4> tracks_index; 
  std::vector<const uParticle*> tracks; 

  ROOT::Math::XYZTVector p4() const {
    return ROOT::Math::XYZTVector(px,py,pz, sqrt(mass*mass + px*px + py *py + pz*pz) ); 
  }
  const uParticle& child( const unsigned index){ return *tracks[index]; } 
  float phi() const { return atan2( py, px) ; }
  float eta() const { return asinh( pz/sqrt(px*px + py*py));}
  float p()   const { return sqrt( px *px + py*py + pz*pz); }
  float pt()  const { return sqrt( px*px + py*py); }
  float ip( const uVertex& vertex ) const {
    auto x_v = x + ( vertex.z - z ) * px / pz; 
    auto y_v = y + ( vertex.z - z ) * py / pz;   
    return sqrt( (x_v - vertex.x)*(x_v-vertex.x) + (y_v - vertex.y)*(y_v - vertex.y)); 
  }

  static void rebuild_sv_pointers( std::vector<uComposite>& composites, const std::vector<uParticle>& particles);
}; 


#endif
