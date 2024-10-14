#ifndef uPi0_H 
#define uPi0_H 1 

#include "Math/Vector4D.h" 

struct uVertex; 
struct uParticle; 

struct uPi0 {
  struct Photon {
    float x; 
    float y; 
    float Et; 
    float E19;
    ROOT::Math::XYZTVector p4() const {
      double pz = Et * 12500 / sqrt(x * x  + y * y);
      double px = Et * x / sqrt( x * x + y*y );   
      double py = Et * y / sqrt( x * x + y*y );   
      double  E = sqrt( px * px + py*py + pz*pz ); 
      return ROOT::Math::XYZTVector( px,py,pz,E ); 
    };
  };

  uPi0() = default;  
  float mass; 
  ROOT::Math::XYZTVector p4() const { return std::get<0>(photons).p4() + std::get<1>(photons).p4() ; }
  std::tuple<Photon, Photon> photons; 
  Photon photon( const unsigned int i ) 
  {
    if( i == 0 ) return std::get<0>(photons);
    else return std::get<1>(photons); 
  }
}; 

#endif
