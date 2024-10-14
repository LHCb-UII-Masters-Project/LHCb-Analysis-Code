#ifndef VERTEX_H
#define VERTEX_H 1 

#include <iostream>
#include <TObject.h>
#include "Event/uParticle.h"
#include "Event/TrackState.h"

struct uVertex 
{
  typedef ROOT::Math::SMatrix<float, 4, 4, ROOT::Math::MatRepSym<float, 4>> SMatrixSym; 
  typedef ROOT::Math::SVector<float, 4> SVector3; 

  uVertex() = default;     
  virtual ~uVertex() {};
  float x;
  float y;
  float z;
  float t;
  SMatrixSym cov; 
  int   trueVertexIndex{-1}; 
  float chi2{0};
  float ndof{0}; 
  unsigned nTracks{0}; 
  uVertex( const std::vector<uParticle>& tracks ); 
  float chi2_distance( const uVertex& other ) const; 
}; 

#endif
