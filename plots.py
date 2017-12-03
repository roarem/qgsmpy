import matplotlib as mpl
mpl.rc('text',usetex=True)
mpl.rcParams['legend.numpoints']=1
mpl.rcParams['font.size'] = 27
mpl.rcParams['font.weight']   = 'bold'
mpl.rcParams['text.latex.preamble']=[r'\usepackage{bm} \boldmath']
mpl.rcParams['lines.linewidth'] = 3
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import ROOT

FILEPATH    = '/home/roar/master/qgsm_analysis_tool/qgsmpy/src/'
ETALIM      = {'1eta5':'1 < |\\eta| < 5','3eta7':'3 < |\\eta| < 7','2eta6':'2 < |\\eta| < 6',\
               '4eta8':'4 < |\\eta| < 8','02eta08':'0.2 < |\\eta| < 0.8',\
               'xf01':'|x_F| \\le 0.1','01xf':'|x_F| \\ge 0.1',\
               'all':'all'}

class histogram:
    def __init__(self,f,LIM=[],DIST='NF',DIAS=[]):
        DIA = '{0}_{1}_{2}' 
        if DIST=='NBNF':
            dianbnf = DIA.format(DIAS[0],lim[0],DIST) 
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

        elif DIST=='NF':
            dia     = DIA.format(DIAS[0],lim,'NF')
            self.th1f   = f.FindObjectAny(dia) 
            self.nb     = self.th1f.GetNbinsX()
            self.limit  = [self.th1f.GetXaxis().GetXmin(),self.th1f.GetXaxis().GetXmax()]
            self.dia    = []
            for l in LIM:
                for d in DIAS:
                    self.dia.append(DIA.format(d,l,'NF'))

        elif DIST=='Y':
            self.th1f_list = []
            for dia in DIAS:
                self.th1f_list.append('y_{}'.format(dia))

            self.th1f   = f.FindObjectAny('y_{}'.format(DIAS[0]))
            self.nb     = self.th1f.GetNbinsX()
            self.limit  = [self.th1f.GetXaxis().GetXmin(),self.th1f.GetXaxis().GetXmax()]

        elif DIST=='ETA':
            self.th1f_list = []
            for dia in DIAS:
                self.th1f_list.append('y_{}'.format(dia))
            self.th1f   = f.FindObjectAny('eta_{}'.format(DIAS[0]))
            self.nb         = self.th1f.GetNbinsX()
            self.limit      = [self.th1f.GetXaxis().GetXmin(),self.th1f.GetXaxis().GetXmax()]


        self.f      = f 
        self.DIST   = DIST
        self.LIM    = LIM 
        self.DIAS   = DIAS
        self.adding()

    def adding(self):
        if self.DIST == 'NBNF':
            for nbnf,nf in zip(self.dianbnf[1:],self.dia[1:]):
                self.th1f  .Add(self.f.FindObjectAny(nbnf))
                self.th1fnf.Add(self.f.FindObjectAny(nf))
            self.th1f.Divide(self.th1fnf)

        elif self.DIST == 'NF':
            for nf in self.dia[1:]:
                print(nf)
                self.th1f.Add(self.f.FindObjectAny(nf))

        elif self.DIST == 'Y':
            for y in self.th1f_list:
                self.th1f.Add(self.f.FindObjectAny(y))

        elif self.DIST == 'ETA':
            for eta in self.th1f_list:
                self.th1f.Add(self.f.FindObjectAny(eta))

    def draw_nbnf(self,fig,ax,lab_add):
        labels = []
        for l in self.LIM:
            temp_dias = [str(d) for d in self.DIAS]
            labels.append('${0}$ dia: {1}'.format(ETALIM[l],', '.join(temp_dias)))

        NF              = np.asarray([self.th1f.GetBinContent(i) for i in range(1,self.nb+1)])
        NF_err          = np.asarray([self.th1f.GetBinError(i) for i in range(1,self.nb+1)])
        NF_err          = NF_err[:35] if self.DIST == 'NBNF' else NF_err
        NF              = NF[:35] if self.DIST == 'NBNF' else NF
        self.limit[1]   = len(NF)-1 if self.DIST =='NBNF' else self.limit[1] 
        NFx             = np.linspace(self.limit[0],self.limit[1],len(NF))

        for label in labels:
            #ax.plot(\
            #        NFx,\
            #        NF,\
            #        linestyle='-',\
            #        markersize=10,\
            #        marker='o',\
            #        label=label+lab_add\
            #        )
            ax.errorbar(
                        NFx,NF,yerr=NF_err,\
                        linestyle='-',\
                        #color=colors[dias],\
                        #markersize=24,\
                        #marker=marker,\
                        #markerfacecolor=markerfacecolor,\
                        #markeredgewidth=markeredgewidth,\
                        #markeredgecolor=markeredgecolor,\
                        #zorder=zorder,\
                        label=label+lab_add\
                        )
        #ax.set_title(title)
        #ax.set_ylim([0,6])
        #ax.set_xlim([0,7])
        ax.set_xlabel('$n_F$')
        ax.set_ylabel('$<n_B(n_F)>$') if self.DIST=='NBNF' else ax.set_ylabel('$\eta$')
        ax.grid('on')
        ax.legend(loc='best')

    def draw_w_wo_decay(self,fig,ax,lab_add):
        #markerfacecolor = 'white' if lab_add=='wo decay' else colors[dias]
        #markeredgecolor = colors[dias]
        #markeredgewidth = 3 if lab_add=='wo decay' else 0
        #linestyle       = '' if lab_add=='wo decay' else linestyles[dias]
        #zorder          = 2 if lab_add=='wo decay' else 3
        #marker = markers[dias]

        #label = '${0}$ dia: {1}'.format(ETALIM[self.LIM[0]],dias)

        NF              = np.asarray([self.th1f.GetBinContent(i) for i in range(1,self.nb+1)])
        NF              = NF[:35] if self.DIST == 'NBNF' else NF
        self.limit[1]   = len(NF)-1 if self.DIST=='NBNF' else self.limit[1] 
        NFx             = np.linspace(self.limit[0],self.limit[1],len(NF))
        NF_err          = np.asarray([self.th1f.GetBinError(i) for i in range(1,self.nb+1)])[:35]

        #NF[18] = None if dias==31 and lab_add=='wo decay' else NF[18]
        #NF_err[18] = None if dias==31 and lab_add=='wo decay' else NF_err[18]
        ax.errorbar(
                    NFx,NF,yerr=NF_err,\
                    linestyle='--',\
                    color='black',\
                    markersize=22,\
                    marker='o',\
                    markerfacecolor=markerfacecolors[lab],\
                    markeredgewidth=3,\
                    #markeredgecolor=markeredgecolor,\
                    #zorder=zorder,\
                    label=lab_add\
                    )

        ax.set_ylim([0,15])
        ax.set_xlim([0,15])
        ax.set_xlabel('$n_F$',fontsize=48)
        ax.set_ylabel('$<n_B(n_F)>$',fontsize=48) if self.DIST=='NBNF' else ax.set_ylabel('$\eta$',fontsize=48)
        ax.grid('on')
        ax.legend(handles=handles,loc='best',prop={'size':38})

    def draw_eta(self,fig,ax,title):
        Y       = np.asarray([self.th1f.GetBinContent(i) for i in range(1,self.nb+1)])
        Y_err   = np.asarray([self.th1f.GetBinError(i) for i in range(1,self.nb+1)])
        Y_x     = np.linspace(self.limit[0],self.limit[1],len(Y))
        label = '$\eta$' if self.DIST=='ETA' else 'y'
        ax.plot(Y_x,Y,label=label)
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        ax.set_title('${}$ GeV'.format(title))
        ax.set_xlabel('$y/\eta$')
        ax.set_ylabel('$\\frac{dN}{dy/\eta}$',rotation=0)
        ax.legend(loc=9,prop={'size':38})

    def draw_eta_900_7000_13000(self,fig,ax,index,title):
        Y       = np.asarray([self.th1f.GetBinContent(i) for i in range(1,self.nb+1)])
        Y_err   = np.asarray([self.th1f.GetBinError(i) for i in range(1,self.nb+1)])
        Y_x     = np.linspace(self.limit[0],self.limit[1],len(Y))
        label = '$\eta$' if self.DIST=='ETA' else 'y'
        ax[index].plot(Y_x,Y,label=label)

        #if title=='900':
        #    ax[index].yaxis.tick_right()
        #ax[index].annotate('${}$ GeV'.format(title),xy=(2,1e5))
        #if index==1:
        ax[index].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        #ax[index].set_title('${}$ GeV'.format(title))
        ax[index].grid()
        if title=='13000':
            ax[index].set_xlabel('$y/\eta$')
            for ti,(a,xF) in zip(['0.9','7','13'],zip(ax,[4.56,6.61,7.23])):
                a.set_ylim(0,Y.max())
                x_F_x   = [-xF,-xF,xF,xF]
                x_F   = [0,Y.max(),0,Y.max()]

                a.plot(x_F_x[:2],x_F[:2],color='black',linestyle='--')
                a.plot(x_F_x[2:],x_F[2:],color='black',linestyle='--')
                a.annotate('{} TeV'.format(ti),xy=(-xF+0.1*xF,Y.max()-0.2*Y.max()))

        if index==0 and title=='900':
            ax[index].legend(loc='best',prop={'size':38})
        if index==1 and title=='7000':
            ax[index].text(-11.8,Y.max()/2.0,'$\\mathbf{\\frac{dN}{dy/\\eta}}$',\
                    size=36,weight='bold')
            plt.subplots_adjust(left=0.15)

    def diffraction_events(self,fig,ax,lab_add):
        #labels = []
        #for l in self.LIM:
        #    temp_dias = [str(d) for d in self.DIAS]
        #    labels.append('${0}$ dia: {1}'.format(ETALIM[l],', '.join(temp_dias)))

        if 'all' in self.LIM:
            label = 'Full phase space'
            marker = 'o'
        else:
            label = '${}$'.format(ETALIM[self.LIM[0]])
            marker = '^'
        NF = np.asarray([self.th1f.GetBinContent(i) for i in range(1,self.nb+1)])
        NF_err = np.asarray([self.th1f.GetBinError(i) for i in range(1,self.nb+1)])
        NF_err = NF_err[:35] if self.DIST == 'NBNF' else NF_err
        NF = NF[:35] if self.DIST == 'NBNF' else NF
        self.limit[1] = len(NF)-1 if self.DIST =='NBNF' else self.limit[1] 
        NFx = np.linspace(self.limit[0],self.limit[1],len(NF))

    
        ax.plot(NFx,NF,\
                linestyle='--',\
                color='black',\
                marker=marker,\
                markersize=16,\
                label=label)
        #ax.set_title(title)
        #ax.set_ylim([0,6])
        #ax.set_xlim([0,7])
        ax.set_xlabel('$n_F$')
        ax.set_ylabel('$<n_B(n_F)>$') if self.DIST=='NBNF' else ax.set_ylabel('$\eta$')
        ax.grid('on')
        ax.legend(handles=handles,loc=2)

    def long_short(self,fig,ax,lab_add):
        #labels = []
        #for l in self.LIM:
        #    temp_dias = [str(d) for d in self.DIAS]
        #    labels.append('${0}$ dia: {1}'.format(ETALIM[l],', '.join(temp_dias)))

        if 'xf01' in self.LIM:
            label = '${}$'.format(ETALIM[self.LIM[0]])
            marker = 'o'
        else:
            label = '${}$'.format(ETALIM[self.LIM[0]])
            marker = '^'
        NF = np.asarray([self.th1f.GetBinContent(i) for i in range(1,self.nb+1)])
        NF_err = np.asarray([self.th1f.GetBinError(i) for i in range(1,self.nb+1)])
        NF_err = NF_err[:35] if self.DIST == 'NBNF' else NF_err
        NF = NF[:35] if self.DIST == 'NBNF' else NF
        self.limit[1] = len(NF)-1 if self.DIST =='NBNF' else self.limit[1] 
        NFx = np.linspace(self.limit[0],self.limit[1],len(NF))

    
        ax.plot(NFx,NF,\
                linestyle='--',\
                color='black',\
                marker=marker,\
                markersize=22,\
                label=label)
        #ax.set_title(title)
        ax.set_ylim([0,15])
        ax.set_xlim([0,10])
        ax.set_xlabel('$n_F$')
        ax.set_ylabel('$<n_B(n_F)>$') if self.DIST=='NBNF' else ax.set_ylabel('$\eta$')
        ax.grid('on')
        ax.legend(handles=handles,loc=2)

    def eta_limits(self,fig,ax,markers):

        marker = markers[self.LIM[0]]        
        label = ''
        NF = np.asarray([self.th1f.GetBinContent(i) for i in range(1,self.nb+1)])
        NF_err = np.asarray([self.th1f.GetBinError(i) for i in range(1,self.nb+1)])
        NF_err = NF_err[:35] if self.DIST == 'NBNF' else NF_err
        NF = NF[:35] if self.DIST == 'NBNF' else NF
        self.limit[1] = len(NF)-1 if self.DIST =='NBNF' else self.limit[1] 
        NFx = np.linspace(self.limit[0],self.limit[1],len(NF))

    
        ax.plot(NFx,NF,\
                linestyle='--',\
                color='black',\
                marker=marker,\
                markersize=22,\
                label=label)
        #ax.set_title(title)
        ax.set_ylim([0,7])
        ax.set_xlim([0,18])
        ax.set_xlabel('$n_F$')
        ax.set_ylabel('$<n_B(n_F)>$') if self.DIST=='NBNF' else ax.set_ylabel('$\eta$')
        ax.grid('on')
        ax.legend(handles=handles,loc=2)

    def close_file(self):
        self.f.Close()

def diff_plot_setup():
    majorLocator = ticker.MultipleLocator(5)
    minorLocator = ticker.MultipleLocator(1)

    fig, ax = plt.subplots()
    size = 1000

    DPI = fig.get_dpi()
    fig.set_size_inches(size/DPI,size/DPI)
    ax.set_xlim(0,12)
    ax.set_ylim(0,13)
    #x0,x1 = ax.get_xlim()
    #y0,y1 = ax.get_ylim()
    #ax.set_aspect((x1-x0)/(y1-y0))

    ax.grid(which='minor',alpha=0.5)

    majorFormatter = ticker.FormatStrFormatter('%d')
    minorFormatter = ticker.FormatStrFormatter('%d')
    ax.yaxis.set_minor_locator(minorLocator)
    ax.xaxis.set_minor_locator(minorLocator)
    ax.yaxis.set_major_locator(majorLocator)
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_major_formatter(majorFormatter)
    #ax.xaxis.set_minor_formatter(minorFormatter)

    [tick.label.set_fontsize(20) for tick in ax.xaxis.get_major_ticks()]
    [tick.label.set_fontsize(20) for tick in ax.yaxis.get_major_ticks()]

    ax.xaxis.set_tick_params(which='major',length=12,width=4)
    ax.yaxis.set_tick_params(which='major',length=12,width=4)
    ax.xaxis.set_tick_params(which='minor',length=8 ,width=2)
    ax.yaxis.set_tick_params(which='minor',length=8 ,width=2)

    return fig,ax
            
if __name__=='__main__':

    '''
    Diagrams:   1,6,10,11,21,31
    limits:     all,1eta5, 3eta7, 2eta6, 4eta8, 0.2eta0.8, 01xf, xf01   
    '''

    choice = 3

    if choice==0:
        fig,ax  = plt.subplots(1,sharex=True)
        DIAS    = [[1,6,10,11,21,31]] 
        LABEL   = '13000'
        F_NAME  = '13000_4m.root'
        DISTS   = ['Y','ETA']
        for dist in DISTS:
            for DIA in DIAS:
                f       = ROOT.TFile(FILEPATH+F_NAME)
                hist    = histogram(f,DIST=dist,DIAS=DIA)
                hist.draw_eta(fig,ax,LABEL)
                hist.close_file()

    elif choice==1:
        from mpl_toolkits.axes_grid1 import Grid
        fig = plt.figure()
        ax = Grid(fig, rect=111, nrows_ncols=(3,1),\
                    axes_pad=0.40)
        DIAS    = [[11]] 
        LABELS  = ['900','7000','13000']
        #F_NAME  = ['900_4m_test.root','7000_4m_test.root','13000_4m_test.root']
        F_NAME  = ['900_4m.root','7000_4m.root','13000_4m.root']
        DISTS   = ['Y']
        for i,(name,lab) in enumerate(zip(F_NAME,LABELS)):
            for dist in DISTS:
                for DIA in DIAS:
                    f       = ROOT.TFile(FILEPATH+name)
                    hist    = histogram(f,DIST=dist,DIAS=DIA)
                    hist.draw_eta_900_7000_13000(fig,ax,i,lab)
                    hist.close_file()
    
    elif choice==2:
        #DIAS = [[1],[6],[21],[31]]
        DIAS = [[1,6,10,11,21,31]]
        limits = [['2eta6'],['3eta7'],['4eta8']]#,['01xf'],['xf01']]
        #limits = [['all'],['02eta08']]#,['01xf'],['xf01']]
        F_NAME = ['900_1m_2.root']
        #F_NAME = ['900_1m_wod_2.root']
        fig,ax = plt.subplots()
        for name,labl in zip(F_NAME,['w decay','wo decay']):
            for NBNF in ['NBNF']:#,'NF']:
                for lim in limits:
                    for DIA in DIAS:
                        print(name)
                        f           = ROOT.TFile(FILEPATH+name)
                        hist        = histogram(f,lim,NBNF,DIA)
                        hist.draw_nbnf(fig,ax,labl)
                        hist.close_file()

    elif choice==3:
        fig,ax = plt.subplots()
        DIAS = [[11,21,31]]
        limits = [['all']]
        F_NAME      = ['900_1m_2.root','900_1m_wod.root']
        labels = ['With decay','Without decay']
        markerfacecolors = {'With decay':'black','Without decay':'white'}
        handle = lambda lab: mpl.lines.Line2D([],[],color='black',\
                              marker='o',markersize=22,linestyle='',\
                              markerfacecolor=markerfacecolors[lab],\
                              label=lab)
        handles = [handle(lab) for lab in labels]
        for name,lab in zip(F_NAME,['With decay','Without decay']):
            for NBNF in ['NBNF']:#,'NF']:
                for lim in limits:
                    for DIA in DIAS:
                        f           = ROOT.TFile(FILEPATH+name)
                        hist        = histogram(f,lim,NBNF,DIA)
                        hist.draw_w_wo_decay(fig,ax,lab)
                        hist.close_file()
    elif choice==4:
        fig,ax  = plt.subplots()
        DIAS    = [[1,6,10,11,21,31]]
        limits  = [['all'],['02eta08']]
        #F_NAME  = ['13000_4m_test.root']
        F_NAME  = ['900_1m_2.root']
        lab     = ''
        for NBNF in ['NBNF']:#,'NF']:
            for lim in limits:
                for DIA in DIAS:
                    f           = ROOT.TFile(FILEPATH+F_NAME[0])
                    hist        = histogram(f,lim,NBNF,DIA)
                    hist.draw_nbnf(fig,ax,lab)
                    hist.close_file()

    elif choice==5:
        fig,ax  = diff_plot_setup()
        handles = [mpl.lines.Line2D([],[],color='black',marker='o',\
                                        markersize=16,linestyle='',\
                                        label='Full phase space'),\
                   mpl.lines.Line2D([],[],color='black',marker='^',\
                                        markersize=16,linestyle='',\
                                        label='${}$'.format(ETALIM['02eta08']))]
        DIAS    = [[1,6,10,11,21,31]]
        limits  = [['all'],['02eta08']]
        #F_NAME  = ['13000_4m_test.root']
        F_NAME  = ['900_1m_2.root']
        lab     = ''
        for NBNF in ['NBNF']:#,'NF']:
            for lim in limits:
                for DIA in DIAS:
                    f           = ROOT.TFile(FILEPATH+F_NAME[0])
                    hist        = histogram(f,lim,NBNF,DIA)
                    hist.diffraction_events(fig,ax,lab)
                    hist.close_file()

    elif choice==6:
        fig,ax  = plt.subplots()
        handles = [mpl.lines.Line2D([],[],color='black',marker='o',\
                                        markersize=22,linestyle='',\
                                        label='$x_F<0.1$'),\
                   mpl.lines.Line2D([],[],color='black',marker='^',\
                                        markersize=22,linestyle='',\
                                        label='$x_F>0.1$')]
        DIAS    = [[1,6,10,11,21,31]]
        limits  = [['xf01'],['01xf']]
        #F_NAME  = ['13000_4m_test.root']
        F_NAME  = ['900_1m_2.root']
        lab     = ''
        for NBNF in ['NBNF']:#,'NF']:
            for lim in limits:
                for DIA in DIAS:
                    f           = ROOT.TFile(FILEPATH+F_NAME[0])
                    hist        = histogram(f,lim,NBNF,DIA)
                    hist.long_short(fig,ax,lab)
                    hist.close_file()
    elif choice==7:
        handle = lambda mark: mpl.lines.Line2D([],[],color='black',\
                              marker=markers[mark],markersize=22,linestyle='',\
                              label='${}$'.format(ETALIM[mark]))
        fig,ax  = plt.subplots()
        limits = [['1eta5'],['2eta6'],['3eta7'],['4eta8']]
        markers = {'1eta5':'D','2eta6':'o','3eta7':'^','4eta8':'*'}
        handles = [handle(limit[0]) for limit in limits]
        DIAS = [[1,6,10,11,21,31]]
        F_NAME = ['900_1m_2.root']
        lab     = ''
        for NBNF in ['NBNF']:#,'NF']:
            for lim in limits:
                for DIA in DIAS:
                    f           = ROOT.TFile(FILEPATH+F_NAME[0])
                    hist        = histogram(f,lim,NBNF,DIA)
                    hist.eta_limits(fig,ax,markers)
                    hist.close_file()
    plt.show()
