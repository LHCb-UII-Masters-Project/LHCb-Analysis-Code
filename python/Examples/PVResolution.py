from Selections import load_event_library 
import ROOT 
from ROOT import TFile, TH1D, TH2D, TCanvas
from math import * 
from MCTools import get_true_pv 

load_event_library()
file = TFile("/eos/lhcb/user/t/tevans/public/b2jpsiX.root", "READ") 

plot = TH1D("hist", ";\\Delta z[mm] ; Entries", 100,-2,2)

for event in file.Events : 
    for vertex in event.Vertices : 
        true_vertex = get_true_pv(vertex, event.MCVertices)
        if true_vertex == None : 
            for v in event.MCVertices : 
                if v.type != 1 : continue
                if abs(vertex.z - v.pos.z() ) < 2 and abs(vertex.t - v.pos.t() ) < 0.05 : 
                    print( f"rec: {vertex.z:.4}, {vertex.t:.3} true: {v.pos.z():.4}, {v.pos.t():.3} {v.nProducts}" )
            continue
        else : 
            plot.Fill( vertex.z - true_vertex.pos.z() )

plot.Draw()
