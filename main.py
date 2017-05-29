import numpy as np
import matplotlib.pyplot as plt
import ROOT as R
import time,datetime

class SINDOU:
    def __init__(self):
        nb              = 300
        start           = 0
        stop            = 300
        self.idiags     = ['1','6','10','11','21','31']
        self.hist_nbnf  = {}
        self.hist_nf    = {}
        self.nbnf       = {}
        self.coun       = {}
        self.limits     = {'1eta5':[1,5],'3eta7':[3,7],'2eta6':[2,6],'4eta8':[4,8],\
                           '01xf':[-np.inf,0.1],'xf01':[0.1,np.inf]}
        #self.names = ['1eta5','3eta7','2eta6','4eta8','01xf','xf01'] 
        titles= ['1 <eta< 5','3 <eta< 7','2 <eta< 6','4 <eta< 8','x_F < 0.1', 'x_F > 0.1']
        for idiag in self.idiags: 
            for name, title in zip(self.limits,titles):
                self.NBNF('{}_{}_'.format(idiag,name),title,nb,start,stop)

    def check(self,nbnf_index,psrap,IDIAG,x_F):
        app = abs(psrap)
        for name in self.limits:
            key = '{}_{}_'.format(int(IDIAG),name)
            if app > self.limits[name][0] and app < self.limits[name][1]:
                self.nbnf[key][nbnf_index] += 1
                self.coun[key] = 1
                #break

    def fill(self):
        for key in self.hist_nbnf:
            if self.coun[key]:
                self.hist_nbnf[key].Fill(self.nbnf[key][0],self.nbnf[key][1])
                self.hist_nf  [key].Fill(self.nbnf[key][1])
            self.coun[key] = 0
            self.nbnf[key] = [0,0]

    def NBNF(self,name,title,nb,start,stop):
        th1fnbnf    = R.TH1F(name+'NBNF',title,nb,start,stop)
        th1fnf      = R.TH1F(name+'NF',title,nb,start,stop) 
	th1fnbnf.Sumw2(True)
	th1fnf  .Sumw2(True)
        self.hist_nbnf[name] = th1fnbnf
        self.hist_nf[name] = th1fnf
        self.nbnf[name] = [0,0]
        self.coun[name] = 0

class ETADIST:

    def __init__(self,hist_input):
        self.hist_input = hist_input

    def ETA(self):
        name,title,nb,start,stop = self.hist_input
        th1f    = R.TH1F(name+'ETA',title,nb,start,stop)
	th1f.Sumw2(True)
        self.hist = th1f

    
class Counter():
    def __init__(self,path,outfile,sindou):
	self.path       = path
        self.sindou     = sindou
        self.outfile    = outfile

    def Count(self):
        B_MULT  = open(self.path+'B_MULT','r')
        finalpr = open(self.path+'finalpr.bin','rb')
        t0 = time.time()     
        sindou_diag = [1,6,10,11,21,31]
	for bline in B_MULT.readlines():
            tbline = bline.strip().split()
            EVENTNR = int(tbline[0]) 
            PARTNR  = int(tbline[2])
            if EVENTNR%100==0:
                print '{}    {}\r'.format(str(datetime.timedelta(seconds=time.time()-t0)),EVENTNR),
            for i in range(PARTNR):
                FREEZJ,XXJ,YYJ,ZZJ,EPAT,PXJ,PYJ,PZJ,AMJ,IDENT,IDIAG,IBJ,ISJ,ICHJ,TFORMJ,\
                    XXJI,YYJI,ZZJI,IORGJ,TFORMRJUK = \
                    np.fromfile(finalpr,count=20)
                    #[float(v) for v in finalpr.readline().strip().split()]
                if i==0 and IDIAG==4:
                    np.fromfile(finalpr,count=20)
                    #finalpr.readline()
                    break
                else:
                    p_L         = np.sqrt(PXJ*PXJ + PYJ*PYJ)
                    p_abs       = np.sqrt(PXJ*PXJ + PYJ*PYJ + PZJ*PZJ)
                    x_F         = 2*p_L/900.0 
                    ps_rap      = 0.5*np.log((p_abs+PZJ)/(p_abs-PZJ))
                    nbnf_index  = 0 if ps_rap<0 else 1
                
                    if ICHJ!=0:
                        if IDIAG in sindou_diag:
                            self.sindou.check(nbnf_index,ps_rap,IDIAG,x_F)

            self.sindou.fill()
        print '\n'
        print 'Total time = {}'.format(str(datetime.timedelta(seconds=time.time()-t0)))
        self.write()
        B_MULT.close()
        finalpr.close()

    def write(self):
        output = R.TFile(self.outfile,'recreate')
        output.mkdir('NBNF')
        output.cd('NBNF')
        for key in self.sindou.hist_nf:
            self.sindou.hist_nbnf[key].Write()
            self.sindou.hist_nf  [key].Write()
        output.Close()


if __name__=='__main__':
    test = SINDOU()
    
    test1 = Counter("/home/roar/DISKS/1/19-31_oct/4mln/code_recieved_2810/900/build/data/",\
                    '900_4m.root',\
                    test)
    
    #test1 = Counter('/home/roar/DISKS/1/13000_attempts/',\
    #                '13000_4m.root',\
    #                test)
    test1.Count()
    
