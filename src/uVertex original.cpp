#include "Event/uVertex.h"

namespace {
  template <typename T=float>
    struct var {
      T x{0};
      T y{0};
      T xy{0};
      T N{0};
      double operator()() const { return xy / N - (x*y)/(N*N) ; }
      void add( T _x, T _y, T _N=1)
      {
        x += _N * _x;
        y += _N * _y;
        xy += _N * _x*_y;
        N += _N;
      }
      double v1() const { return x / N; }
      double v2() const { return y / N; }
    };
};

std::tuple< std::vector<TrackState>, std::array<double,4>> 
  fit( const std::vector<TrackState>& states )
{
  constexpr float c_light = 299.792458; 
  var rxtx, ryty, tx2, ty2, tx2z, ty2z, rttt, tt2, tt2z;
  for( const auto& s : states ) 
  {
    auto beta = sqrt( 1 + s.tx * s.tx + s.ty * s.ty ) / c_light; 
    rxtx.add( s.x0, s.tx      , 1./s.cov(0,0));
    ryty.add( s.y0, s.ty      ,  1./s.cov(1,1));
    tx2.add( s.tx, s.tx       , 1./s.cov(0,0));
    ty2.add( s.ty, s.ty       , 1./s.cov(1,1));
    tx2z.add( s.tx * s.z, s.tx, 1/s.cov(0,0));
    ty2z.add( s.ty * s.z, s.ty, 1/s.cov(1,1));
    rttt.add( s.t, beta, 1/s.cov(5,5)); 
    tt2.add( beta, beta, 1/s.cov(5,5));
    tt2z.add( beta * s.z, beta, 1/s.cov(5,5) ); 
  }
#if RECO4D 
  auto z = ( tx2z() + ty2z() + tt2z() - rxtx() - ryty() - rttt() ) / ( tx2() + ty2() + tt2() );
#else 
  auto z = ( tx2z() + ty2z()  - rxtx() - ryty()  ) / ( tx2() + ty2() );
#endif 
  
  auto x = (rxtx.v1() + rxtx.v2() * z - tx2z.v1() );
  auto y = (ryty.v1() + ryty.v2() * z - ty2z.v1() );
  auto t = (rttt.v1() + rttt.v2() * z - tt2z.v1() );
  std::vector<TrackState> rt; 
  for( auto& state : states ) rt.emplace_back( state, z ); 
  return std::make_tuple( rt, std::array<double,4>{x,y,z,t} );
}


uVertex::uVertex( const std::vector<uParticle>& tracks )
{
  std::vector<TrackState> states;
  for( const auto& track : tracks ) states.emplace_back( track.firstState ) ; 
  auto [new_states, pos] = fit( states ); 
  auto [updated_states, pos2] = fit( new_states ); 
  x = pos2[0];
  y = pos2[1];
  z = pos2[2];
  t = pos2[3];
  #if RECO4D
  ndof =  3* tracks.size() - 4;
  #else
    ndof = 2 * tracks.size() - 3;
  #endif 
  constexpr float c_light = 299.792458; 
  for( const auto& s : updated_states )
  {
    auto beta = sqrt( 1 + s.tx * s.tx + s.ty * s.ty ) / c_light; 
    auto dx = ( s.x0 - x ); 
    auto dy = ( s.y0 - y );
    auto dt = ( s.t  - t ); 
    double det = s.cov(0,0) * s.cov(1,1) - s.cov(0,1) * s.cov(1,0); 
    ROOT::Math::SMatrix<float,2,2, ROOT::Math::MatRepSym<float, 2>> C; 

    C(0,0) = s.cov(1,1) / det; 
    C(1,1) = s.cov(0,0) / det; 
    C(1,0) = -s.cov(1,0) / det; 
    chi2 += (dx*dx * C(0,0)   + dy*dy *C(1,1) + 2 * dx * dy * C(1,0) ); 
    cov(0,0) += C(0,0);
    cov(0,1) += C(0,1);  
    cov(1,1) += C(1,1); 
    cov(0,2) += C(0,0) * s.tx + C(1,0) * s.ty; 
    cov(1,2) += C(1,0) * s.tx + C(1,1) * s.ty; 
    cov(2,2) += s.tx*s.tx * C(0,0) + s.ty * s.ty * C(1,1) + 2 * s.tx * s.ty * C(1,0); 
    
    #if RECO4D
    cov(2,2) +=  beta * beta / s.cov(5,5) ;
    chi2 += dt*dt / s.cov(5,5);
    cov(3,2) += beta / s.cov(5,5);
    cov(3,3) += 1./s.cov(5,5);  
    #else
    cov(3,3) += 1;
    #endif
  }
  cov.Invert();
}

float uVertex::chi2_distance( const uVertex& other ) const 
{
  float dx = ( x - other.x ); 
  float dy = ( y - other.y ); 
  float dz = ( z - other.z ); 
  float dt = ( t - other.t ); 
  #if RECO4D 
  return (dx*dx) / ( cov(0,0) + other.cov(0,0) )+ 
         (dy*dy) / ( cov(1,1) + other.cov(1,1) )+ 
         (dz*dz) / ( cov(2,2) + other.cov(2,2) )+ 
         (dt*dt) / ( cov(3,3) + other.cov(3,3) );
  #else
  return (dx*dx) / ( cov(0,0) + other.cov(0,0) )+ 
         (dy*dy) / ( cov(1,1) + other.cov(1,1) )+ 
         (dz*dz) / ( cov(2,2) + other.cov(2,2) ); 
  #endif 
}
