#include "Event/TrackState.h"

ROOT::Math::XYZVector    TrackState::pos() const { return ROOT::Math::XYZVector( x0, y0, z ); }
ROOT::Math::XYZVector  TrackState::slope() const { return ROOT::Math::XYZVector( tx, ty, 1 ); }
float TrackState::doca(const TrackState& other) const 
{ 
  auto r1 = pos();
  auto s1 = slope();
  auto r2 = other.pos();
  auto s2 = other.slope();
  auto D  = (r1 - s1 * z) - ( r2 - s2 * other.z );
  auto T  = s1 - s2  ;
  auto z  = - D.Dot(T) / ( T.Mag2() );
  return sqrt( ( D + T * z ).Mag2() );
}
TrackState::TrackState( const TrackState& state, const double& new_z )
  : TrackState::TrackState(state) {

    auto dz = new_z - z; 
    auto dz2 = dz*dz;
    constexpr double c_light = 299.792458; 
    
    double tb = sqrt( 1 + tx*tx + ty*ty ) / c_light; 
    x0 = x0 + tx * dz;
    y0 = y0 + ty * dz;
    t  =  t + tb * dz; 
    z = new_z;
    const auto C = cov; 
    enum i { x,y,tx,ty,qop,t}; 

    cov(i::x, i::x ) += dz2 * C(i::tx, i::tx) + 2 * dz * C(i::x, i::tx); // C_xx
    cov(i::x, i::tx) +=  dz * C(i::tx, i::tx);
    
    cov(i::y, i::y ) += dz2 * C(i::ty, i::ty) + 2 * dz * C(i::y, i::ty); // C_yy 
    cov(i::y, i::ty) +=  dz * C(i::ty, i::ty);
   
    /// cross-terms that are probably not so important ...  
    cov(i::x, i::y ) += dz2 * C(i::tx, i::ty) + dz * ( C( i::x, i::ty ) + C( i::y, i::tx ) ); // C_xy
    cov(i::y, i::tx) += dz  * C(i::tx, i::ty);
    cov(i::x, i::ty) += dz  * C(i::tx, i::ty);

    #if RECO_4D
        const auto nb = dz / ( tb * c_light * c_light ); 
        cov(i::x , i::t) += dz * C(i::tx, i::t) + nb * ( tx * C(i::x, i::tx) + ty * C(i::x,i::ty) + dz * tx*C(i::tx,i::tx) + dz*ty*C(i::tx,ty) );
        cov(i::y , i::t) += dz * C(i::ty, i::t) + nb * ( ty * C(i::y, i::ty) + tx * C(i::y,i::tx) + dz * ty*C(i::ty,i::ty) + dz*tx*C(i::tx,ty) );
        cov(i::tx, i::t) += nb * ( tx * C(i::tx,i::tx) + ty*C(i::tx, i::ty) ); 
        cov(i::ty, i::t) += nb * ( tx * C(i::tx,i::ty) + ty*C(i::ty, i::ty) );
        cov(i::t , i::t) += nb*nb * ( tx*tx * C(i::tx,i::tx) + 2 * tx * ty * C(i::tx, i::ty ) + ty*ty*C(i::ty*i::ty) ) 
                         + 2 * nb * ( tx * C(i::tx, i::t) + ty * C(i::ty, i::t ) );  
    #else 
        cov(i::t, i::t) = 1; 
    #endif
}
