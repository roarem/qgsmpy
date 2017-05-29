import matplotlib as mpl
mpl.rc('text',usetex=True)
mpl.rcParams['legend.numpoints']=1
mpl.rcParams['font.size'] = 27
mpl.rcParams['font.weight']   = 'bold'
mpl.rcParams['text.latex.preamble']=[r'\usepackage{bm} \boldmath']
mpl.rcParams['lines.linewidth'] = 5
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import ROOT

FILEPATH    = '/home/roar/master/qgsm_analysis_tool/qgsmpy/src/'
F_NAME      = '900_4m.root'
#DIAS        = ['1','6','10','11','21','31']
ETALIM      = {'0':'1 < \\eta < 5','1':'3 < \\eta < 7','2':'2 < \\eta < 6',\
               '3':'|x_F| \\le 0.1','4':'|x_F| \\ge 0.1'}

class histogram:
    def __init__(self,f,LIM=[],NBNF='NF',DIAS=[]):
        DIA = '{0}_{1}_{2}' 
        if 'NBNF'== NBNF:
            dianbnf = DIA.format(DIAS[0],lim[0],NBNF) 
            dia     = DIA.format(DIAS[0],lim[0],'NF') 
            print(dianbnf)
            self.th1f       = f.FindObjectAny(dianbnf) 
            self.th1fnf     = f.FindObjectAny(dia) 
            self.nb         = self.th1f.GetNbinsX()
            self.limit      = [self.th1f.GetXaxis().GetXmin(),self.th1f.GetXaxis().GetXmax()]
            self.dianbnf    = []
            self.dia        = []
            for l in LIM:
                for d in DIAS:
                    self.dianbnf.append(DIA.format(d,l,'NBNF'))
                    self.dia    .append(DIA.format(d,l,'NF'))
        else:
            dia     = DIA.format(DIAS[0],lim,'NF')
            self.th1f   = f.FindObjectAny(dia) 
            self.nb     = self.th1f.GetNbinsX()
            self.limit  = [self.th1f.GetXaxis().GetXmin(),self.th1f.GetXaxis().GetXmax()]
            self.dia    = []
            for l in LIM:
                for d in DIA:
                    self.dia.append(DIA.format(d,l,'NF'))

        self.f      = f 
        self.NBNF   = NBNF
        self.LIM    = LIM 
        self.DIAS   = DIAS
        self.adding()

    def adding(self):
        if 'NBNF' == self.NBNF:
            for nbnf,nf in zip(self.dianbnf[1:],self.dia[1:]):
                print(nbnf)
                self.th1f  .Add(self.f.FindObjectAny(nbnf))
                self.th1fnf.Add(self.f.FindObjectAny(nf))
            self.th1f.Divide(self.th1fnf)

        else:
            for nf in self.dia[1:]:
                print(nf)
                self.th1f.Add(self.f.FindObjectAny(nf))
            
    def draw(self,fig,ax):
        labels = []
        for l in self.LIM:
            temp_dias = [str(d) for d in self.DIAS]
            labels.append('{0} dia: {1}'.format(l,', '.join(temp_dias)))

        #diagrams        = [l.split('_')[0] for l in self.dia]#['{}'.format(DIA[l[:3]+l[-1]]) for l in self.dia]
        #limits          = [l.split('_')[1] for l in self.dia]
        #labels          = ['{} {}'.format('{} Diagrams '.format(lim),', '.join(diagrams))\
        #                for lim in limits]
        #title           = '{} with ${:s}$'\
        #                .format('$<n_B(n_F)>$'if self.NBNF else '$\eta$',ETALIM[self.dia[0][-2]])
        #print(title)
        NF              = np.asarray([self.th1f.GetBinContent(i) for i in range(1,self.nb+1)])
        NF              = NF[:35] if self.NBNF == 'NBNF' else NF
        self.limit[1]   = len(NF)-1 if self.NBNF=='NBNF' else self.limit[1] 
        NFx             = np.linspace(self.limit[0],self.limit[1],len(NF))

        #fig,ax  = plt.subplots()

        for label in labels:
            ax.plot(NFx,NF,linestyle='-',markersize=10,marker='o',label=label)
        #ax.set_title(title)
        ax.set_ylim([0,10])
        ax.set_xlabel('$n_F$')
        ax.set_ylabel('$<n_B(n_F)>$') if self.NBNF=='NBNF' else ax.set_ylabel('$\eta$')
        ax.grid('on')
        ax.legend()
        #filename =\
        #'temp_plots/{}_eta{}_dia{}.pdf'.\
        #format(self.NBNF,ETALIM[self.dia[0][-2]][-2:],DIA[self.dia[0][:3]+self.dia[0][-1]])\
        #        .replace(" ","")
        #fig.savefig(filename)

    def close_file(self):
        self.f.Close()

            
if __name__=='__main__':

    '''
    Diagrams:   1,6,10,11,21,31
    limits:     1eta5, 3eta7, 2eta6, 4eta8, 01xf, xf01   
    '''
    DIAS = [[1,6,10]]
    limits = [['2eta6'],['1eta5'],['3eta7'],['4eta8'],['01xf'],['xf01']]
    for NBNF in ['NBNF']:#,'NF']:
        fig,ax = plt.subplots()
        for i in limits:
            for DIA in DIAS:
                f           = ROOT.TFile(FILEPATH+F_NAME)
                lim         = i 
                hist        = histogram(f,lim,NBNF,DIA)
                hist.draw(fig,ax)
                hist.close_file()
            

    #f           = ROOT.TFile(FILEPATH+F_NAME)
    #lim         = 0 
    #SIN         = [0]#[0,1,2]
    #DOU         = []#[0,1,2]
    #NBNF        = 'NF'
    #hist        = histogram(f,lim,NBNF,SIN,DOU)
    #hist.draw()
    #hist.close_file()
    plt.show()
