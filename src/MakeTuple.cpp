/*****************************************************************************\
 * (c) Copyright 2000-2018 CERN for the benefit of the LHCb Collaboration      *
 *                                                                             *
 * This software is distributed under the terms of the GNU General Public      *
 * Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   *
 *                                                                             *
 * In applying this licence, CERN does not waive the privileges and immunities *
 * granted to it by virtue of its status as an Intergovernmental Organization  *
 * or submit itself to any jurisdiction.                                       *
 \*****************************************************************************/
// Include files

// from Gaudi
#include "Event/MCVertex.h"
#include "Event/RecVertex_v2.h"
#include "Event/LinksByKey.h"
#include "Event/MCHit.h"
#include "Event/MCParticle.h"
#include "Event/MCProperty.h"
#include "Event/MCTrackInfo.h"
#include "Event/MCVertex.h"
#include "Event/RecVertex.h"
#include "Event/Track.h"

#include "MCInterfaces/IMCReconstructible.h"

#include "GaudiAlg/Consumer.h"
#include "GaudiAlg/GaudiHistoAlg.h"
#include "GaudiAlg/GaudiHistoTool.h"
#include "GaudiAlg/IHistoTool.h"
#include "GaudiKernel/ToolHandle.h"
// local
#include "TRandom3.h"
#include "TTree.h"
#include "TFile.h"

#include <fstream>

#include "Event/Event.h"

// Declaration of the Algorithm Factory
class MakeTuple
: public Gaudi::Functional::Consumer<
  void( const std::vector<LHCb::Event::v2::Track>&, const std::vector<LHCb::Event::v2::RecVertex>&,
      const LHCb::MCParticles&, const LHCb::MCVertices&, const LHCb::MCProperty&, const LHCb::LinksByKey& )> {
    public:
      /// Standard constructor
      MakeTuple( const std::string& name, ISvcLocator* pSvcLocator );

      virtual ~MakeTuple(); ///< Destructor
      StatusCode initialize();
      StatusCode finalize();

      void operator()( const std::vector<LHCb::Event::v2::Track>&, const std::vector<LHCb::Event::v2::RecVertex>&,
          const LHCb::MCParticles&, const LHCb::MCVertices&, const LHCb::MCProperty&,
          const LHCb::LinksByKey& ) const override;
      
      Gaudi::Property<std::string> m_filename{this,"File", "output.root"}; 
      TTree* m_tree;
      mutable TFile* m_file; 
      mutable Event  m_event;
  };
DECLARE_COMPONENT( MakeTuple )

  typedef LHCb::Event::v2::Track track;

  StatusCode MakeTuple::initialize() { 
    m_file  = TFile::Open(m_filename.value().c_str(), "RECREATE"); 
    m_tree  = new TTree("Events","event tree");
    m_tree->Branch("Particles",  &m_event.particles); 
    m_tree->Branch("Vertices",   &m_event.vertices); 
    m_tree->Branch("MCVertices", &m_event.mcvertices); 
    m_tree->Branch("MCParticles", &m_event.mcparticles); 
    return StatusCode::SUCCESS;
  }
StatusCode MakeTuple::finalize() 
{
  auto tmp = gFile; 
  m_file->cd();
  m_tree->Write();
  m_file->Close(); 
  if( gFile != nullptr ) gFile->cd(); 
  return StatusCode::SUCCESS;
}

  namespace { 
    std::vector<std::pair<LHCb::MCVertex*, std::vector<LHCb::MCParticle*>>>
      getVisiblePVs( const LHCb::MCVertices& vertices, const LHCb::MCParticles& particles, const MCTrackInfo& trackInfo ) {
        std::vector<std::pair<LHCb::MCVertex*, std::vector<LHCb::MCParticle*>>> pvs;
        for ( const auto& vertex : vertices ) {
          if ( !vertex->isPrimary() ) continue;
          std::vector<LHCb::MCParticle*> particlesForThisVertex;
          for ( const auto& particle : particles ) {
            if ( particle->primaryVertex() != vertex ) continue;
            if ( trackInfo.hasVelo( particle ) ) particlesForThisVertex.push_back( particle );
          }
          if ( particlesForThisVertex.size() >= 4 ) pvs.emplace_back( vertex, particlesForThisVertex );
        }
        return pvs;
      }

    template <class object>
      unsigned int hash( const object& obj ) {
        unsigned int rv = 2166136261;
        for ( auto& key : obj.lhcbIDs() ) {
          rv ^= key.lhcbID();
          rv *= 16777619;
        }
        return rv;
      }
  }

//=============================================================================
// Standard constructor, initializes variables
//=============================================================================
MakeTuple::MakeTuple( const std::string& name, ISvcLocator* pSvcLocator )
  : Consumer( name, pSvcLocator,
      {KeyValue{"Tracks", ""}, 
      KeyValue{"Vertices", ""},
      KeyValue{"MCParticles", LHCb::MCParticleLocation::Default},
      KeyValue{"MCVertices", LHCb::MCVertexLocation::Default},
      KeyValue{"MCTrackInfo", LHCb::MCPropertyLocation::TrackInfo}, KeyValue{"Links", ""}}) {}

//=============================================================================
// Destructor
//=============================================================================
MakeTuple::~MakeTuple() {}

std::vector<const LHCb::MCParticle*> getMCParticles( const std::vector<LHCb::Event::v2::Track>&     tracks,
                                                      const LHCb::MCParticles& mcparticles,
                                                      const LHCb::LinksByKey& tr2McLink)
{
  std::map<const LHCb::MCParticle*, std::map<unsigned, double>> tracksForParticle;
  std::vector<const LHCb::MCParticle*>  mcParticleForTrack ( tracks.size() ); 
  std::vector<double> weights( tracks.size() , -1 );
  unsigned counter = 0; 
  
  tr2McLink.applyToAllLinks([&]( int trackKey, unsigned int mcPartKey, float weight ) mutable {
      if ( unsigned( trackKey ) >= tracks.size() ){ counter++; return; }
      tracksForParticle[mcparticles(mcPartKey)][trackKey] += weight;
  });
  for ( const auto& [mcp, tracks] : tracksForParticle ) {
    for ( const auto& [index,weight] : tracks ) {
      if( weight > weights[index] )  mcParticleForTrack[index] = mcp;
    }
  }

  return mcParticleForTrack; 
}

void MakeTuple::operator()( const std::vector<LHCb::Event::v2::Track>&     tracks,
    const std::vector<LHCb::Event::v2::RecVertex>& vertices,
    const LHCb::MCParticles& mcparticles, const LHCb::MCVertices& mcvertices,
    const LHCb::MCProperty& trackproperty, const LHCb::LinksByKey& tr2McLink ) const {


  MCTrackInfo trackInfo = {trackproperty};
  auto        mcpvs     = getVisiblePVs( mcvertices, mcparticles, trackInfo );
  auto ordered_mcp      = getMCParticles( tracks, mcparticles, tr2McLink ); 
  
  std::map<const LHCb::Event::v2::RecVertex*, std::map<const LHCb::MCVertex*, unsigned>> recToTrueVertices;
  std::map<const LHCb::MCVertex*, std::map<const LHCb::Event::v2::RecVertex*, unsigned>> trueToRecVertices;

  m_event.particles.resize(tracks.size()); 
  m_event.vertices.resize(vertices.size());
  m_event.mcvertices.resize(mcvertices.size());
  m_event.mcparticles.resize(mcparticles.size());

  std::map<const LHCb::MCParticle*, unsigned> mcParticleIndex; 
  for( auto& mcp : mcparticles ) mcParticleIndex[mcp] = mcParticleIndex.size(); 
  std::map<const LHCb::MCVertex*, unsigned> mcVertexIndex; 
  for( auto& mcp : mcvertices ) mcVertexIndex[mcp] = mcVertexIndex.size(); 

  for(unsigned int i = 0 ; i != tracks.size(); ++i )
  {
    m_event.particles[i].firstState.x0  = tracks[i].firstState().x();
    m_event.particles[i].firstState.y0  = tracks[i].firstState().y();
    m_event.particles[i].firstState.tx  = tracks[i].firstState().tx();
    m_event.particles[i].firstState.ty  = tracks[i].firstState().ty();
    m_event.particles[i].firstState.qop = tracks[i].firstState().qOverP();
    m_event.particles[i].firstState.t   = tracks[i].firstState().time();
    m_event.particles[i].firstState.z   = tracks[i].firstState().z();
    m_event.particles[i].index = i; 
    auto cov = tracks[i].firstState().covariance();
    for( int j=0; j != 5; ++j ){
      for( int k = j ; k != 5; ++k ) m_event.particles[i].firstState.cov(j,k) = cov(j,k);
    }
    m_event.particles[i].firstState.cov(5,5) = pow( tracks[i].firstState().errT(), 2 );
    if( ordered_mcp[i] != nullptr )
    { 
      m_event.particles[i].trueID   = ordered_mcp[i]->particleID().pid();
      m_event.particles[i].mass = sqrt( mass2( * ordered_mcp[i] ) );
      m_event.particles[i].mcParticleIndex = mcParticleIndex[ ordered_mcp[i] ];
    }
    else m_event.particles[i].trueID = 0; 
  }
  for( unsigned int i = 0 ; i != vertices.size(); ++i )
  {
    m_event.vertices[i].x = vertices[i].position().x();
    m_event.vertices[i].y = vertices[i].position().y();
    m_event.vertices[i].z = vertices[i].position().z();
    m_event.vertices[i].t = vertices[i].time();
    auto cov = vertices[i].covMatrix();
    for( int j = 0; j != 3; ++j ){
      for( int k = j ; k != 3; ++k ) m_event.vertices[i].cov(j,k) = cov(j,k);
    }
    m_event.vertices[i].nTracks  = vertices[i].tracks().size();
    m_event.vertices[i].chi2 = vertices[i].chi2 ();
    m_event.vertices[i].ndof = vertices[i].nDoF();
  }
  for( const auto& vertex : mcvertices )
  {
    auto index = mcVertexIndex[vertex];
    m_event.mcvertices[index].pos       = vertex->position4vector();
    m_event.mcvertices[index].nProducts = vertex->products().size(); 
    m_event.mcvertices[index].type      = vertex->type(); 
  }
  for( const auto& particle : mcparticles ) 
  {
    auto index = mcParticleIndex[particle];
    m_event.mcparticles[index].p  = particle->momentum(); 
    m_event.mcparticles[index].ID = particle->particleID().pid(); 
    m_event.mcparticles[index].motherID = particle->mother() == nullptr ? 0 : particle->mother()->particleID().pid();
    if( particle->mother() != nullptr ) 
    {
      m_event.mcparticles[index].GDmotherID = particle->mother()->mother() == nullptr ? 0 : particle->mother()->mother()->particleID().pid();
    }
    else m_event.mcparticles[index].GDmotherID = 0; 
    if( mcVertexIndex.count( particle->originVertex() ) != 0 )
    {
      m_event.mcparticles[index].vertexIndex = mcVertexIndex[ particle->originVertex() ];
    }
    else m_event.mcparticles[index].vertexIndex = -1;
  }

  m_tree->Fill();
  //return rt; 
  // std::cout << "nTracks: " << tracks.size() << " vertices: " << vertices.size()  << std::endl; 
}
