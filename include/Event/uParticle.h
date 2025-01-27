#ifndef uPARTICLE_H
#define uPARTICLE_H 1 

#include <iostream>
#include "Event/TrackState.h"


#include "Math/Vector4D.h"

struct uVertex; 

struct uParticle  {

  uParticle() = default;
  uParticle( const std::vector<uParticle>& tracks, const std::vector<float>& masses = {} ); 
  TrackState firstState; 
  double     mass {139.577}; /// everything is a pion 
  int        trueID{211}; 
  unsigned   index{0}; 
  int        mcParticleIndex{-1}; 
  float ip( const uVertex& vertex ) const; 
  float ip_t( const uVertex& vertex ) const; 
  float ipchi2_4d( const uVertex& vertex ) const; 
  float ipchi2( const uVertex& vertex)const; 
  float min_ip( const std::vector<uVertex>& vertices ) const; 
  float min_ip( const std::vector<uVertex>& vertices, float max_ipt ) const; 
  float min_ipchi2_4d( const std::vector<uVertex>& vertices ) const; 
  float min_ipchi2( const std::vector<uVertex>& vertex) const; 
  const uVertex& bpv_4d(const std::vector<uVertex>& vertices ) const; 
  ROOT::Math::XYZTVector p4(const float m = -1.f) const {
    auto norm = sqrt( 1. + firstState.tx *  firstState.tx + firstState.ty * firstState.ty ); 
    auto pz   = 1 /( norm * std::fabs( firstState.qop ) );
    auto px   = pz * firstState.tx;
    auto py   = pz * firstState.ty; 
    return ROOT::Math::XYZTVector(px,py,pz, sqrt( (m == -1.f ? mass * mass : m*m ) + px*px + py *py + pz*pz) ); 
  }
  float phi() const { return atan2( firstState.ty, firstState.tx) ; }
  float eta() const { return asinh( 1/sqrt( firstState.ty*firstState.ty +  firstState.tx*firstState.tx) ) ; };
  float p()   const { return std::fabs( 1 / firstState.qop ); }
  float pt()  const { 
    auto norm = sqrt( 1. + firstState.tx *  firstState.tx + firstState.ty * firstState.ty ); 
    auto pz   = 1 /( norm * std::fabs( firstState.qop ) );
    return pz * sqrt( firstState.tx * firstState.tx + firstState.ty * firstState.ty ) ; 
  }
  int charge() const { return firstState.qop > 0 ? +1 : -1 ; }
  void scale_uncertainty( const double sf, const unsigned i)
  {
    firstState.cov.Array()[ i * 5 + i ] *= sf ; 
  }
}; 

std::vector<uParticle> select( const std::vector<uParticle>&,
                               const std::vector<uVertex>&,
                               float, float, float ); 

std::vector<std::tuple<uParticle, uParticle, uParticle, uVertex>> combine ( 
    const std::vector<uParticle>& container1, 
    const std::vector<uParticle>& container2,
    double doca_max, 
    double chi2ndof_max,
    unsigned charge );

std::vector<std::tuple<uParticle, uParticle, uParticle, uParticle, uVertex>> combine ( 
    const std::vector<uParticle>& container1, 
    const std::vector<uParticle>& container2,
    const std::vector<uParticle>& container3,
    double doca_max,
    double chi2ndof_max,
    unsigned intermediate_charge,
    unsigned charge );
#endif
