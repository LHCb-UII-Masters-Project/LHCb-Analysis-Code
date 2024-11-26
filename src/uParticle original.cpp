#include "Event/uVertex.h"
#include "Event/uParticle.h"

float uParticle::ip( const uVertex& vertex ) const 
{
  auto x_v = firstState.x0 + ( vertex.z - firstState.z ) * firstState.tx; 
  auto y_v = firstState.y0 + ( vertex.z - firstState.z ) * firstState.ty;   
  return sqrt( (x_v - vertex.x)*(x_v-vertex.x) + (y_v - vertex.y)*(y_v - vertex.y)); 
}

float uParticle::ipchi2( const uVertex& vertex ) const 
{
  float tx = firstState.tx;
  float ty = firstState.ty;
  float dz = vertex.z - firstState.z;
  float dx = firstState.x0 + dz * tx - vertex.x;
  float dy = firstState.y0 + dz * ty - vertex.y;
  float cov00 = vertex.cov(0,0) + firstState.cov(0,0);
  float cov10 = vertex.cov(1,0); 
  float cov11 = vertex.cov(1,1) + firstState.cov(1,1);
  cov00 += dz * dz * firstState.cov(2,2) + 2 * dz * firstState.cov(2,0) ;
  cov11 += dz * dz * firstState.cov(3,3) + 2 * dz * firstState.cov(3,1) ;
  cov00 += tx * tx * vertex.cov(2,2) - 2 * tx * vertex.cov(2,0); 
  cov10 += tx * ty * vertex.cov(2,2) - ty * vertex.cov(2,0) - tx * vertex.cov(2,1);
  cov11 += ty * ty * vertex.cov(2,2) - 2 * ty * vertex.cov(2,1);
  float D = cov00 * cov11 - cov10 * cov10;
  float invcov00 = cov11 / D;
  float invcov10 = -cov10 / D;
  float invcov11 = cov00 / D;
  return dx * dx * invcov00 + 2 * dx * dy * invcov10 + dy * dy * invcov11;
}

float uParticle::ipchi2_4d( const uVertex& vertex ) const 
{
  auto state = TrackState( firstState, vertex.z );
  auto rt = 
    ( state.x0 - vertex.x  ) * ( state.x0 - vertex.x  ) / state.cov(0,0) + 
    ( state.y0 - vertex.y  ) * ( state.y0 - vertex.y  ) / state.cov(1,1) + 
    ( state.t  - vertex.t  ) * ( state.t - vertex.t  ) / state.cov(5,5); 

  if ( std::isnan(rt)  or std::isinf(rt) )
  {
    std::cout << "{x,y,t}: " << state.x0 << " " << state.y0 << " " << state.t << std::endl; 
    std::cout << firstState.cov(0,0) << std::endl; 
    std::cout << "{cov(x), cov(y), cov(t)} : " <<  state.cov(0,0) << " " << state.cov(1,1) << " " << state.cov(5,5) << std::endl; 
  }
  return rt; 
}

float uParticle::ip_t( const uVertex& vertex ) const 
{
  auto& s = firstState;
  constexpr double c_light = 299.792458; 
  auto t  = s.t + ( vertex.z - s.z ) * sqrt( 1 + s.tx*s.tx + s.ty*s.ty) / c_light; 
  return std::fabs( t - vertex.t ); 
}

float uParticle::min_ip( const std::vector<uVertex>& vertices ) const 
{
  float rt = ip( vertices[0] );
  for( unsigned j = 1 ; j < vertices.size(); ++j ) 
  {
    rt = std::min( ip(vertices[j]), rt );
  }
  return rt; 
}

float uParticle::min_ipchi2( const std::vector<uVertex>& vertices ) const 
{
  float rt = ipchi2( vertices[0] );
  for( unsigned j = 1 ; j < vertices.size(); ++j ) 
  {
    rt = std::min( ipchi2(vertices[j]), rt );
  }
  return rt; 
}

float uParticle::min_ip( const std::vector<uVertex>& vertices, float max_ipt ) const 
{
  auto ip_with_ipt_cut = [this, max_ipt]( auto& vertex ){ return this->ip_t(vertex) < max_ipt ? this->ip(vertex) : 9999; };
  float rt = ip_with_ipt_cut(vertices[0] );
  for( unsigned j = 1 ; j < vertices.size(); ++j ) rt = std::min( ip_with_ipt_cut(vertices[j]), rt );
  return rt; 
}

float uParticle::min_ipchi2_4d( const std::vector<uVertex>& vertices ) const 
{
  float rt = ipchi2_4d( vertices[0] );
  for( unsigned j = 1 ; j < vertices.size(); ++j ) 
  {
    rt = std::min( ipchi2_4d(vertices[j]), rt );
  }
  return rt; 
}

const uVertex& uParticle::bpv_4d( const std::vector<uVertex>& vertices ) const 
{
  float rt = ipchi2_4d( vertices[0] );
  const uVertex* bpv = &vertices[0];
  for( unsigned j = 1 ; j < vertices.size(); ++j ) 
  {
    auto ip = ipchi2_4d(vertices[j]);
    if( ip < rt ) 
    {
      bpv = &vertices[j];
      rt = ip;
    }
    //  rt = std::min( ipchi2_4d(vertices[j]), rt );
  }
  return *bpv; 
}

std::pair<ROOT::Math::SVector<double,3>, ROOT::Math::SMatrix<double,3,3>> get_p_with_cov( const uParticle& particle )
{
  auto t = particle.firstState;   
  const auto& cov = particle.firstState.cov;
  const auto n   = sqrt( 1 + t.tx * t.tx + t.ty * t.ty ) ;
  const auto pz  = 1./ ( std::fabs(t.qop) * n );
  ROOT::Math::SMatrix<double,3,3, ROOT::Math::MatRepSym<double, 3>> C_track;
  C_track(0,0) = cov(2,2);
  C_track(1,1) = cov(3,3);
  C_track(2,2) = cov(4,4);
  C_track(0,1) = cov(2,3);
  C_track(0,2) = cov(2,4);
  C_track(1,2) = cov(3,4);
  ROOT::Math::SMatrix<double,3,3> H;
  H(0,0) = (1 + t.ty * t.ty )/ ( 1 + t.tx*t.tx + t.ty*t.ty);
  H(0,1) = -t.tx * t.ty / ( n * n );
  H(0,2) = -t.tx / ( std::fabs(t.qop)  );

  H(1,0) = -t.tx * t.ty / ( n * n ) ;                /// dpy / dtx
  H(1,1) = (1 + t.tx*t.tx ) / ( 1 + t.tx * t.tx + t.ty * t.ty );  /// dpy / dty
  H(1,2) = -t.ty / ( std::fabs(t.qop)  );                       /// dpy / dqop 

  H(2,0) = -t.tx / ( n * n );                        /// dpz / dtx 
  H(2,1) = -t.ty / ( n * n );                        /// dpz / dty
  H(2,2) = - 1 / ( std::fabs(t.qop)  );                          /// dpz / dqop 
  ROOT::Math::SVector<double, 3> p { t.tx * pz, t.ty * pz, pz };
  return {p, pz * pz * ROOT::Math::Similarity(H, C_track)};
}


uParticle::uParticle( const std::vector<uParticle>& tracks, const std::vector<float>& masses )
{
  auto decay_vertex = uVertex(tracks); 
  ROOT::Math::XYZTVector p;

  for(unsigned int i = 0 ; i != tracks.size(); ++i ) 
    p += masses.size() == 0 ? tracks[i].p4() : tracks[i].p4( masses[i] );
  
  firstState.x0 = decay_vertex.x;
  firstState.y0 = decay_vertex.y;
  firstState.z  = decay_vertex.z;
  firstState.t  = decay_vertex.t;
  firstState.tx = p.x() / p.z(); 
  firstState.ty = p.y() / p.z(); 
  firstState.qop = 1 / p.P(); 
  
  for( unsigned i = 0 ; i != tracks.size(); ++i ){
    auto [pi,cov_p] = get_p_with_cov(tracks[i]); 
    firstState.cov(2,2) += ( cov_p(0,0)  - 2 * firstState.tx * cov_p(2,0) +  firstState.tx * firstState.tx * cov_p(2,2) ) / ( p.z() * p.z() );
    firstState.cov(3,3) += ( cov_p(1,1)  - 2 * firstState.ty * cov_p(2,1) +  firstState.ty * firstState.ty * cov_p(2,2) ) / ( p.z() * p.z() );
  }
  mass   = p.mass();
  firstState.cov(0,0) = decay_vertex.cov(0,0) + 
                        firstState.tx * firstState.tx * decay_vertex.cov(2,2) 
                        - 2 * firstState.tx * decay_vertex.cov(2,0);
  
  firstState.cov(1,1) = decay_vertex.cov(1,1) + 
                        firstState.ty * firstState.ty * decay_vertex.cov(2,2)
                        - 2 * firstState.ty * decay_vertex.cov(2,1);

  firstState.cov(5,5) = decay_vertex.cov(3,3);
}

std::vector<uParticle> select( const std::vector<uParticle>& input,
                               const std::vector<uVertex>& vertices, 
                               const float min_pt,
                               const float min_p,
                               const float min_ipchi2_4d )
{
  std::vector<uParticle> particles;
  for( auto& particle : input ) if( particle.pt() > min_pt && particle.p() > min_p && particle.min_ipchi2_4d(vertices) > min_ipchi2_4d ) particles.push_back( particle);
  return particles; 
}


std::vector<std::tuple<uParticle, uParticle, uParticle, uVertex>> combine ( 
    const std::vector<uParticle>& container1, 
    const std::vector<uParticle>& container2,
    double doca_max, 
    double chi2ndof_max,
    unsigned charge )
{
  std::vector<std::tuple<uParticle, uParticle, uParticle, uVertex>> rt; 
  for( const auto& p1 : container1 )
  {
    for( const auto& p2 : container2 )
    {
      if( p1.charge() + p2.charge() != charge ) continue; 
      if( p1.firstState.doca( p2.firstState ) > doca_max ) continue;
      auto vtx = uVertex( {p1,p2} );
      if( vtx.chi2 / vtx.ndof > chi2ndof_max ) continue; 
      rt.push_back( std::make_tuple(p1,p2, uParticle({p1,p2}), vtx ));
    }
  }
  return rt; 
}
