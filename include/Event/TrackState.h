#ifndef TRACKSTATE_H 
#define TRACKSTATE_H 1 

#include <Math/SMatrix.h>
#include <Math/Vector3D.h>

struct TrackState {

  public:
    typedef ROOT::Math::SMatrix<float,6,6, ROOT::Math::MatRepSym<float,6>> SMatrixSym6; 

    TrackState() = default; 
    Float_t x0; 
    Float_t y0; 
    Float_t tx; 
    Float_t ty;
    Float_t qop; 
    Float_t t;  
    Float_t chi2; 
    int ndof; 
    SMatrixSym6 cov;     
    Float_t z;  
    ROOT::Math::XYZVector    pos() const;
    ROOT::Math::XYZVector  slope() const;
    float doca(const TrackState& other) const; 
    TrackState( const TrackState& state, const double& new_z );

};

#endif
