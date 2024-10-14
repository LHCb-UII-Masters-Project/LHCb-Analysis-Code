#ifndef uMCVERTEX_H
#define uMCVERTEX_H 1 

#include <iostream>
#include <TObject.h>
#include "Event/TrackState.h"
#include "Math/Vector4D.h"

struct uMCVertex {
  ROOT::Math::XYZTVector pos; 
  unsigned type; 
  unsigned nProducts; 
}; 

#endif
