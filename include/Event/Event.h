#ifndef EVENT_H
#define EVENT_H 1 

#include "Event/uParticle.h"
#include "Event/uVertex.h"
#include "Event/uMCVertex.h"
#include "Event/uMCParticle.h"

class Event /*: public TObject*/ {
  
  public:
    virtual ~Event() {} ; 
    std::vector<uParticle> particles; 
    std::vector<uVertex>   vertices; 
    std::vector<uMCVertex> mcvertices; 
    std::vector<uMCParticle> mcparticles; 
};

#endif 
