import ROOT
from ROOT import TFile, TTree
import argparse
import numpy as np
import os
import numpy as np
from scipy.stats import norm

binomialError = lambda eff,N : np.sqrt(eff*(1-eff)/N)
bayesianError = lambda eff,N : np.sqrt((N*eff+1)*(N*eff+2)/(N+2)/(N+3) - ((N*eff+1)/(N+2))**2)

def wilsonError(eff,N,level=0.68,bUpper=True):
    if N==0:
        if bUpper:
            return 1
        else:
            return 0
    
    alpha = (1-level)/2
    kappa = norm.ppf(1-alpha)
    mode = (eff*N+kappa**2/2)/(N+kappa**2)
    delta = kappa/(N+kappa**2)*np.sqrt(eff*N*(1-eff)+kappa**2/4)
    
    if bUpper:
        return (1 if mode+delta>1 else mode+delta)
    else:
        return (0 if mode-delta<0 else mode-delta)

def wilsonEffErr(eff,N,level=0.68,useWilsonAdjEff = False):
    upper = wilsonError(eff,N,level=level,bUpper=True)
    lower = wilsonError(eff,N,level=level,bUpper=False)
    if useWilsonAdjEff:
        return (upper + lower)/2 ,(upper - lower)/2
    else:
        return eff ,(upper - lower)/2

def wilsonEffGet(eff,N,level=0.68):
    upper = wilsonError(eff,N,level=level,bUpper=True)
    lower = wilsonError(eff,N,level=level,bUpper=False)
    return (upper + lower)/2

def wilsonErrGet(eff,N,level=0.68):
    upper = wilsonError(eff,N,level=level,bUpper=True)
    lower = wilsonError(eff,N,level=level,bUpper=False)
    return (upper - lower)/2

effErrTypeDict = {"binomial":binomialError, "bayesian":bayesianError,"wilson":wilsonErrGet}


def effError(efficiency, N, efficType="wilson"):
    '''
    Get efficiency error for a given efficiency calculation
    efficiency - Calculated value of efficiency
    N - denominator
    efficType - "binomial", "bayesian"
    '''


    return effErrTypeDict[efficType](efficiency,N)