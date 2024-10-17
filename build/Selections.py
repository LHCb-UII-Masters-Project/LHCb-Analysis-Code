
def load_event_library() : 
    from ROOT import gSystem, gInterpreter 
    gInterpreter.AddIncludePath('/disk/homedisk/home/user294/Documents/selections/include')
    gSystem.Load( '/disk/homedisk/home/user294/Documents/selections/build/libEvent.so')

def get_secondary_vertices( event ) :
    from ROOT import uComposite
    svs = event.CompositeParticles
    uComposite.rebuild_sv_pointers(svs, event.Particles )
    return svs 
