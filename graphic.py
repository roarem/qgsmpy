import ROOT
import numpy as np
import rootplot.root2matplotlib as r2m
import matplotlib.pyplot as plt

DIAS = ['1','6','10','11','21','31']

class SINDOU_plot:
    def __init__(self,dias=[]):
        limits      = {'1eta5':[1,5],'3eta7':[3,7],'2eta6':[2,6],'4eta8':[4,8],\
                       '01xf':[-np.inf,0.1],'xf01':[0.1,np.inf]}
            

f           = ROOT.TFile('900_4m.root')
th1f_nbnf   = f.FindObjectAny('1_1eta5_NBNF')
th1f_nf     = f.FindObjectAny('1_1eta5_NF')
nb          = th1f_nbnf.GetNbinsX()

for dia in dias:
    for limit in limits: 
        if '{}_{}_NBNFNBNF'.format(dia,limit)=='1_1eta5_NBNF':
            continue
        th1f_nbnf.Add(f.FindObjectAny('{}_{}_NBNF'.format(dia,limit)))
        th1f_nf.Add(f.FindObjectAny('{}_{}_NF'.format(dia,limit)))
        
th1f_nbnf.Divide(th1f_nf)

nb = 35
NBNF    = [th1f_nbnf.GetBinContent(i) for i in range(1,nb+1)]
x       = xrange(0,nb)

plt.plot(x,NBNF,linestyle='--',marker='o')
plt.show()
