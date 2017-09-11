import matplotlib as mpl
mpl.rc('text',usetex=True)
mpl.rcParams['legend.numpoints']=1
mpl.rcParams['font.size'] =36
mpl.rcParams['font.weight']   = 'bold'
mpl.rcParams['text.latex.preamble']=[r'\usepackage{bm} \boldmath']
mpl.rcParams['lines.linewidth'] = 5
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import ROOT

FILEPATH    = '/home/roar/master/qgsm_analysis_tool/qgsmpy/src/'
ETALIM      = {'1eta5':'1 < \\eta < 5','3eta7':'3 < \\eta < 7','2eta6':'2 < \\eta < 6',\
              '4eta8':'4 < \\eta < 8','xf01':'|x_F| \\le 0.1','01xf':'|x_F| \\ge 0.1'}

class histogram:
    def __init__(self,f,LIM=[],NBNF='NF',DIAS=[]):
        DIA = '{0}_{1}_{2}' 
        if 'NBNF'== NBNF:
            dianbnf = DIA.format(DIAS[0],lim[0],NBNF) 
            dia     = DIA.format(DIAS[0],lim[0],'NF') 
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
            
    def draw(self,fig,ax,lab_add):
        labels = []
        for l in self.LIM:
            temp_dias = [str(d) for d in self.DIAS]
            labels.append('${0}$ dia: {1}'.format(ETALIM[l],', '.join(temp_dias)))

        NF              = np.asarray([self.th1f.GetBinContent(i) for i in range(1,self.nb+1)])
        NF              = NF[:35] if self.NBNF == 'NBNF' else NF
        self.limit[1]   = len(NF)-1 if self.NBNF=='NBNF' else self.limit[1] 
        NFx             = np.linspace(self.limit[0],self.limit[1],len(NF))

        for label in labels:
            ax.plot(NFx,NF,linestyle='-',markersize=10,marker='o',label=label+lab_add)
        #ax.set_title(title)
        #ax.set_ylim([0,6])
        #ax.set_xlim([0,7])
        ax.set_xlabel('$n_F$')
        ax.set_ylabel('$<n_B(n_F)>$') if self.NBNF=='NBNF' else ax.set_ylabel('$\eta$')
        ax.grid('on')
        ax.legend(loc='best')

    def draw_w_wo_decay(self,fig,ax,lab_add):
        labels = []
        linestyles = {11:'',21:'-',31:'--'}
        #colors = {11:'black',21:'black',31:'black'}
        colors = {11:'magenta',21:'blue',31:'red'}
        markers= {11:'o',21:'s',31:'^'}
        dias = self.DIAS[0]
        markerfacecolor = 'white' if lab_add=='wo decay' else colors[dias]
        markeredgecolor = colors[dias]
        markeredgewidth = 3 if lab_add=='wo decay' else 0
        linestyle       = '' if lab_add=='wo decay' else linestyles[dias]
        zorder          = 2 if lab_add=='wo decay' else 3
        marker = markers[dias]

        label = '${0}$ dia: {1}'.format(ETALIM[self.LIM[0]],dias)

        NF              = np.asarray([self.th1f.GetBinContent(i) for i in range(1,self.nb+1)])
        NF              = NF[:35] if self.NBNF == 'NBNF' else NF
        self.limit[1]   = len(NF)-1 if self.NBNF=='NBNF' else self.limit[1] 
        NFx             = np.linspace(self.limit[0],self.limit[1],len(NF))
        NF_err          = np.asarray([self.th1f.GetBinError(i) for i in range(1,self.nb+1)])[:35]


        ax.plot(NFx,NF,linestyle=linestyle,\
                color=colors[dias],\
                markersize=24,\
                marker=marker,markerfacecolor=markerfacecolor,\
                markeredgewidth=markeredgewidth,\
                markeredgecolor=markeredgecolor,\
                zorder=zorder,\
                label=label+lab_add)
        #ax.errorbar(NFx,NF,yerr=NF_err,\
        #            linestyle=linestyle,\
        #            color=colors[dias],\
        #            markersize=24,\
        #            marker=marker,\
        #            markerfacecolor=markerfacecolor,\
        #            markeredgewidth=markeredgewidth,\
        #            markeredgecolor=markeredgecolor,\
        #            zorder=zorder,\
        #            label=label+lab_add)

        if self.LIM[0]=='01xf':
            ax.set_ylim([0,6])
            ax.set_xlim([0,7])
        else:
            ax.set_ylim([0,30])
        ax.set_xlabel('$n_F$',fontsize=48)
        ax.set_ylabel('$<n_B(n_F)>$',fontsize=48) if self.NBNF=='NBNF' else ax.set_ylabel('$\eta$',fontsize=48)
        ax.grid('on')
        ax.legend(loc='best',prop={'size':38})

    def close_file(self):
        self.f.Close()

            
if __name__=='__main__':

    '''
    Diagrams:   1,6,10,11,21,31
    limits:     1eta5, 3eta7, 2eta6, 4eta8, 01xf, xf01   
    '''
    #DIAS = [[11,21,31]]
    #limits = [['2eta6'],['1eta5'],['3eta7'],['4eta8'],['01xf'],['xf01']]
    #limits = [['01xf']]
    #for NBNF in ['NBNF']:#,'NF']:
    #    fig,ax = plt.subplots()
    #    for i in limits:
    #        for DIA in DIAS:
    #            f           = ROOT.TFile(FILEPATH+F_NAME)
    #            lim         = i 
    #            hist        = histogram(f,lim,NBNF,DIA)
    #            hist.draw(fig,ax)
    #            hist.close_file()

    fig,ax = plt.subplots()
    DIAS = [[11],[21],[31]]
    limits = [['01xf']]
    #F_NAME      = ['900_4m.root','900_4m_wodr.root']
    F_NAME      = ['900_4m.root','900_4m_wodr.root']
    #F_NAME      = ['900_1m_wd.root']
    for name,lab in zip(F_NAME,['w decay','wo decay']):
        for NBNF in ['NBNF']:#,'NF']:
            for lim in limits:
                for DIA in DIAS:
                    f           = ROOT.TFile(FILEPATH+name)
                    hist        = histogram(f,lim,NBNF,DIA)
                    hist.draw_w_wo_decay(fig,ax,lab)
                    hist.close_file()
            

    plt.show()
