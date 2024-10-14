#ifndef uMCParticle_H
#define uMCParticle_H 1 

#include <iostream>
#include <TObject.h>
#include "Event/TrackState.h"
#include "Math/Vector4D.h"

struct uMCParticle {
  ROOT::Math::XYZTVector p;
  int vertexIndex;
  int ID;
  int motherID; 
  int GDmotherID; 
  ROOT::Math::XYZTVector p4() const { return p ; } 
}; 

#endif
