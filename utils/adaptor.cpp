#include <iostream> 
#include <TFile.h>
#include <TTree.h>

#include <Event/uParticle.h> 
#include <Event/uMCParticle.h> 
#include <Event/uComposite.h> 
#include <Event/uVertex.h> 
#include <Event/uPi0.h>

struct EventID { 
  ULong_t evtNo {0}; 
  unsigned  runNo {0}; 
  bool operator!=( const EventID& other ) const { return !( evtNo == other.evtNo && runNo == other.runNo ); }
  bool operator< ( const EventID& other ) const { return ( (uint64_t(runNo) << 32) + evtNo ) < ( (uint64_t(other.runNo) << 32) + other.evtNo ) ; }
};

auto get_vertices(
                   TTree* tree_pv)
{
  float x, y,z; 
  float cov[6];
  EventID id; 
  tree_pv->SetBranchAddress("Hlt1PVDumper__x_t",&x); 
  tree_pv->SetBranchAddress("Hlt1PVDumper__y_t",&y); 
  tree_pv->SetBranchAddress("Hlt1PVDumper__z_t",&z); 
  tree_pv->SetBranchAddress("Hlt1PVDumper__c_t",&cov); 
  tree_pv->SetBranchAddress("Hlt1PVDumper__evtNo_t", &id.evtNo);
  tree_pv->SetBranchAddress("Hlt1PVDumper__runNo_t", &id.runNo);
  std::map<EventID, std::vector<uVertex>> rt; 
  for(unsigned i = 0 ; i != tree_pv->GetEntries(); ++i )
  {
    tree_pv->GetEntry(i); 
    uVertex vertex; 
    vertex.x = x; 
    vertex.y = y; 
    vertex.z = z;
    vertex.cov(0,0) = cov[0];  
    vertex.cov(1,0) = cov[1];  
    vertex.cov(1,1) = cov[2];  
    vertex.cov(2,0) = cov[3];  
    vertex.cov(2,1) = cov[4];  
    vertex.cov(2,2) = cov[5];  
    rt[id].push_back( vertex ); 
  }
  return rt; 
}

auto get_pi0s(TTree* tree_pi0s )
{
  std::map<EventID, std::vector<uPi0>> rt; 
  if( tree_pi0s == nullptr ) {
    std::cout << "warning, no tree" << std::endl; 
    return rt; 
  }
  uPi0 tmp; 
  EventID id; 
  tree_pi0s->SetBranchAddress("Hlt1Pi02GammaGamma__x1_t", &std::get<0>(tmp.photons).x); 
  tree_pi0s->SetBranchAddress("Hlt1Pi02GammaGamma__x2_t", &std::get<1>(tmp.photons).x); 
  tree_pi0s->SetBranchAddress("Hlt1Pi02GammaGamma__y1_t", &std::get<0>(tmp.photons).y); 
  tree_pi0s->SetBranchAddress("Hlt1Pi02GammaGamma__y2_t", &std::get<1>(tmp.photons).y); 
  tree_pi0s->SetBranchAddress("Hlt1Pi02GammaGamma__et1_t", &std::get<0>(tmp.photons).Et); 
  tree_pi0s->SetBranchAddress("Hlt1Pi02GammaGamma__et2_t", &std::get<1>(tmp.photons).Et);
  tree_pi0s->SetBranchAddress("Hlt1Pi02GammaGamma__e19_1_t", &std::get<0>(tmp.photons).E19); 
  tree_pi0s->SetBranchAddress("Hlt1Pi02GammaGamma__e19_2_t", &std::get<1>(tmp.photons).E19);

  tree_pi0s->SetBranchAddress("Hlt1Pi02GammaGamma__evtNo_t", &id.evtNo);
  tree_pi0s->SetBranchAddress("Hlt1Pi02GammaGamma__runNo_t", &id.runNo);
  tree_pi0s->SetBranchAddress("Hlt1Pi02GammaGamma__mass_t", &tmp.mass ); 
  for( unsigned i = 0 ; i != tree_pi0s->GetEntries(); ++i )
  {
    tree_pi0s->GetEntry(i);

//     std::cout << ( std::get<0>(tmp.photons).p4() +  std::get<1>(tmp.photons).p4() ).mag() << " " << tmp.mass << std::endl; 
    rt[id].push_back( tmp );
  }
  return rt; 
}

auto get_composites( TTree* tree_sv )
{
  EventID id; 
  uComposite tmp;  
  tree_sv->SetBranchAddress("Hlt1SVDumper__x_t",&tmp.x); 
  tree_sv->SetBranchAddress("Hlt1SVDumper__y_t",&tmp.y); 
  tree_sv->SetBranchAddress("Hlt1SVDumper__z_t",&tmp.z); 
  tree_sv->SetBranchAddress("Hlt1SVDumper__px_t",&tmp.px); 
  tree_sv->SetBranchAddress("Hlt1SVDumper__py_t",&tmp.py); 
  tree_sv->SetBranchAddress("Hlt1SVDumper__pz_t",&tmp.pz); 
 // tree_sv->SetBranchAddress("Hlt1SVDumper__c_t",&tmp.cov); 
  tree_sv->SetBranchAddress("Hlt1SVDumper__tracks_t",&tmp.tracks_index); 
  tree_sv->SetBranchAddress("Hlt1SVDumper__evtNo_t", &id.evtNo);
  tree_sv->SetBranchAddress("Hlt1SVDumper__runNo_t", &id.runNo);

  std::map<EventID, std::vector<uComposite>> rt; 
  for(unsigned i = 0 ; i != tree_sv->GetEntries(); ++i )
  {
    tree_sv->GetEntry(i);
    rt[id].push_back( tmp ); 
  }
  return rt; 
}

auto get_mc_particles(TTree* tree_mc)
{
  uMCParticle tmp;  
  std::map<unsigned, double> masses;
  masses[211] = 1.3957018E+02;
  masses[22]  = 0;
  masses[11] = 5.10998910E-01;
  masses[13] = 1.05658367E+02;
  masses[321] = 4.93677E+02;
  masses[2212] = 9.3827203E+02; 
  masses[3222] = 1.60E+03; 
  EventID id; 
  double* p4 = reinterpret_cast<double*>( &tmp.p ); 
  std::array<float,3> p3;
  tree_mc->Print(); 
  tree_mc->SetBranchStatus("*",1); 
  tree_mc->SetBranchAddress("px"     , p3.data() ); 
  tree_mc->SetBranchAddress("py"     , p3.data() + 1); 
  tree_mc->SetBranchAddress("pz"     , p3.data() + 2); 
  tree_mc->SetBranchAddress("ID"          , &tmp.ID); 
  tree_mc->SetBranchAddress("MOTHERID"    , &tmp.motherID); 
  tree_mc->SetBranchAddress("GDMOTHERID"  , &tmp.GDmotherID); 
  tree_mc->SetBranchAddress("evtNo", &id.evtNo);
  tree_mc->SetBranchAddress("runNo", &id.runNo);
  std::map<EventID, std::vector<uMCParticle>> rt; 
  for(unsigned i = 0 ; i != tree_mc->GetEntries(); ++i )
  {
    tree_mc->GetEntry(i);
    p4[0] = p3[0]; 
    p4[1] = p3[1]; 
    p4[2] = p3[2]; 
    double p2 = p4[0] * p4[0] + p4[1] * p4[1] + p4[2] * p4[2]; 
    if( abs(tmp.ID) < 1000000000 ){
      auto it_mass = masses.find( abs(tmp.ID) );
      if( it_mass == masses.end() ){
        p4[3] = sqrt(p2); 
        std::cout << "warning: " << tmp.ID << " " << tmp.p4().x() << " " << id.evtNo << std::endl; 
      }
      else p4[3] = sqrt( it_mass->second * it_mass->second + p2 ); 
    }
    else p4[3] = sqrt(p2);
    rt[id].push_back( tmp ); 
  }
  return rt; 
}

int main( int argc, char** argv )
{
  TFile* f = TFile::Open(argv[1],"READ"); 
  TFile* output = TFile::Open(argv[2],"RECREATE"); 

  std::vector<uParticle>* particles = new std::vector<uParticle>(); 
  std::vector<uVertex>* vertices    = new std::vector<uVertex>(); 
  std::vector<uComposite>* secondary_vertices    = new std::vector<uComposite>(); 
  std::vector<uMCParticle>* mc_particles = new std::vector<uMCParticle>(); 
  std::vector<uPi0>* pi0s = new std::vector<uPi0>(); 
 

  EventID id; 
 
  TTree* tree     = (TTree*)f->Get("particle_validator/Particles"); 
  TTree* mctree     = (TTree*)f->Get("particle_validator/MCParticles"); 
  TTree* tree_pv = (TTree*)f->Get("Hlt1PVDumper/monitor_tree");
  TTree* tree_sv = (TTree*)f->Get("Hlt1SVDumper/monitor_tree");
  TTree* tree_pi0s = (TTree*)f->Get("Hlt1Pi02GammaGamma/monitor_tree"); 
  auto all_mc_particles = get_mc_particles( mctree ); 
  auto all_vertex       = get_vertices(tree_pv); 
  auto all_secondary_vertices = get_composites(tree_sv); 
  auto all_pi0s               = get_pi0s( tree_pi0s ); 
  
  float cov[6];
  uParticle particle; 

  tree->SetBranchAddress("x",&particle.firstState.x0); 
  tree->SetBranchAddress("y",&particle.firstState.y0); 
  tree->SetBranchAddress("z",&particle.firstState.z); 
  tree->SetBranchAddress("tx",&particle.firstState.tx); 
  tree->SetBranchAddress("ty",&particle.firstState.ty); 
  tree->SetBranchAddress("qop",&particle.firstState.qop); 
  tree->SetBranchAddress("cov", &cov); 
  tree->SetBranchAddress("evtNo", &id.evtNo);
  tree->SetBranchAddress("runNo", &id.runNo);  
  tree->SetBranchAddress("chi2",&particle.firstState.chi2); 
  tree->SetBranchAddress("ndof",&particle.firstState.ndof); 
  tree->SetBranchAddress("TrackID",&particle.index); 
  tree->SetBranchAddress("TRUE_ID",&particle.trueID); 
  tree->SetBranchAddress( "MCParticleIndex", &particle.mcParticleIndex);  
  EventID lastID; 
  lastID.runNo = 0; 
  TTree* tree_output = new TTree("Events", "event tree"); 
  tree_output->Branch("Particles", &particles );   
  tree_output->Branch("MCParticles", &mc_particles );   
  tree_output->Branch("Vertices", &vertices );   
  tree_output->Branch("CompositeParticles", &secondary_vertices );   
  tree_output->Branch("Pi0s", &pi0s); 
  tree_output->Branch("eventNumber", &lastID.evtNo ); 
  tree_output->Branch("runNumber", &lastID.runNo ); 

  unsigned offset = 0;  

  auto fill_tree = [&]( auto lastID ) mutable {
    const auto& these_vertices     = all_vertex[lastID];
    auto& these_svs                = all_secondary_vertices[lastID];
    const auto& these_mc_particles = all_mc_particles[lastID]; 
    const auto& these_pi0s         = all_pi0s[lastID]; 
    for( auto& particle : *particles ) if( particle.mcParticleIndex != -1 ) particle.mcParticleIndex -= offset; 
    offset += these_mc_particles.size();
    for( auto& vertex : these_vertices ) vertices->push_back(vertex); 
    for( auto& vertex : these_svs ) secondary_vertices->push_back(vertex);
    for( auto& mc_particle : these_mc_particles ) mc_particles->push_back( mc_particle ); 
    for( auto& pi0 : these_pi0s ) pi0s->push_back( pi0 ); 
    tree_output->Fill(); 
    particles->clear();
    vertices->clear();
    mc_particles->clear(); 
    pi0s->clear(); 
    secondary_vertices->clear();  
  }; 

  for( unsigned i = 0 ; i != tree->GetEntries(); ++i )
  {
    if( i % 100000 == 0 ) std::cout << "Processed: " << i  << " entries" << std::endl ;
    tree->GetEntry(i); 
    particle.firstState.cov(0,0) = cov[0];  
    particle.firstState.cov(0,2) = cov[1];  
    particle.firstState.cov(2,2) = cov[2];  
    particle.firstState.cov(1,1) = cov[3];  
    particle.firstState.cov(1,3) = cov[4];  
    particle.firstState.cov(3,3) = cov[5];  
    if( id != lastID && lastID.runNo != 0 ) fill_tree(lastID); 
    particles->push_back( particle ); 
    lastID=id; 
  }
  fill_tree(lastID); 
  output->cd();
  tree_output->Write(); 
  output->Close();  
}
