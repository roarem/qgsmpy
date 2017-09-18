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
                           'xf01':[-np.inf,0.1],'01xf':[0.1,np.inf],\
                           'all':[-np.inf,np.inf]}
        #self.names = ['1eta5','3eta7','2eta6','4eta8','01xf','xf01'] 
        titles= ['1 <eta< 5','3 <eta< 7','2 <eta< 6','4 <eta< 8',\
                 'x_F < 0.1', 'x_F > 0.1',\
                 'all']
        for idiag in self.idiags: 
            for name, title in zip(self.limits,titles):
                self.NBNF('{}_{}_'.format(idiag,name),title,nb,start,stop)

    def check(self,nbnf_index,psrap,IDIAG,x_F):
        app = abs(psrap)
        for name in self.limits:
            key = '{}_{}_'.format(int(IDIAG),name)
            comp = app if not 'xf' in name else x_F
            if comp > self.limits[name][0] and comp < self.limits[name][1]:
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
	th1fnbnf.Get._creates = True
	th1fnf  .Get._creates = True
        self.hist_nbnf[name] = th1fnbnf
        self.hist_nf[name] = th1fnf
        self.nbnf[name] = [0,0]
        self.coun[name] = 0

class ETADIST:

    def __init__(self,nb=1000,start=-10,stop=10):
        idiags = ['1','6','10','11','21','31']
        self.th1f_rap = {}
        self.th1f_eta = {}
        for dia in idiags:
            self.th1f_rap['y_{}'.format(dia)] = R.TH1F('y_{}'.format(dia),\
                                                       'dN/dy {}'.format(dia),\
                                                       nb,start,stop)
            self.th1f_eta['eta_{}'.format(dia)] = R.TH1F('eta_{}'.format(dia),\
                                                       'dN/d\eta {}'.format(dia),\
                                                       nb,start,stop)
            self.th1f_rap['y_{}'.format(dia)]   .Get._creates = True
            self.th1f_eta['eta_{}'.format(dia)] .Get._creates = True
            self.th1f_rap['y_{}'.format(dia)]   .Sumw2(True)
            self.th1f_eta['eta_{}'.format(dia)] .Sumw2(True)

    
    def fill(self,y,eta,IDIAG):
        IDIAG=int(IDIAG)
        self.th1f_rap['y_{}'.format(IDIAG)].Fill(y)
        self.th1f_eta['eta_{}'.format(IDIAG)].Fill(eta)

    
class Counter():
    def __init__(self,path,outfile,sindou,etadist):
	self.path       = path
        self.sindou     = sindou
        self.etadist    = etadist
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
                if i==0 and IDIAG==4:
                    np.fromfile(finalpr,count=20)
                    break
                else:
                    p_T         = np.sqrt(PXJ*PXJ + PYJ*PYJ)
                    p_abs       = np.sqrt(PXJ*PXJ + PYJ*PYJ + PZJ*PZJ)
                    x_F         = 2*p_T/900.0 
                    rap         = 0.5*np.log((EPAT+PZJ)/(EPAT-PZJ))
                    #rap         = 0.5*np.log(EPAT+PZJ)/np.sqrt(PXJ**2+PYJ**2+AMJ**2)
                    ps_rap      = 0.5*np.log((p_abs+PZJ)/(p_abs-PZJ))
                    nbnf_index  = 0 if ps_rap<0 else 1
                
                    if ICHJ!=0 and IDIAG in sindou_diag:
                        self.sindou.check(nbnf_index,ps_rap,IDIAG,x_F)
                        self.etadist.fill(rap,ps_rap,IDIAG)

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
        output.cd('..')
        output.mkdir('ETA')
        output.cd('ETA')
        for rap_key,eta_key in zip(self.etadist.th1f_rap,self.etadist.th1f_eta):
            self.etadist.th1f_rap[rap_key].Write()
            self.etadist.th1f_eta[eta_key].Write()
        output.Close()
        print('Written to {}'.format(self.outfile))


if __name__=='__main__':

    #path    = ["/home/roar/DISKS/1/19-31_oct/4mln/code_recieved_2810/900/build/data/"]
    #out     = ['900_4m.root']
    #path    = ["/home/roar/DISKS/1/19-31_oct/4mln/code_recieved_2810/7000/build/data/"]
    #out     = ['7000_4m.root']
    path    = [\
               '/home/roar/DISKS/1/13000_attempts/',\
               '/home/roar/DISKS/1/19-31_oct/4mln/code_recieved_2810/7000/build/data/',\
               '/home/roar/DISKS/1/19-31_oct/4mln/code_recieved_2810/900/build/data/'\
              ]
    out     = [\
               '13000_4m.root',\
               '7000_4m.root',\
               '900_4m.root'\
              ]
    #path    = ["/home/roar/DISKS/1/19-31_oct/1mln/w_decay/build/data/"]
    #out     = ['900_1m.root']

    for pa,ou in zip(path,out):
        sindou  = SINDOU()
        etadist = ETADIST()
        dist_class = Counter(pa,ou,sindou,etadist)
        dist_class.Count()
    #dist_900_4m = Counter("/home/roar/DISKS/1/19-31_oct/4mln/code_recieved_2810/900/build/data/",\
    #                '900_4m.root',\
    #                sindou,etadist)
    #dist_900_4m.Count()

    #sindou_wodr = SINDOU()
    #sindou_900_4m_wodr =\
    #                Counter("/home/roar/DISKS/1/19-31_oct/4mln/code_recieved_2810/900/wo_decay/data/",\
    #                '900_4m_wodr.root',\
    #                sindou_wodr)
    #sindou_900_4m_wodr.Count()

    #sindou_wod = SINDOU()
    #etadist_wod= ETADIST()
    #sindou_900_1m_wod =\
    #                Counter("/home/roar/DISKS/1/19-31_oct/1mln/wo_decay/data/",\
    #                '900_1m_wod.root',\
    #                sindou_wod,etadist_wod)
    #sindou_900_1m_wod.Count()

    #sindou      = SINDOU()
    #etadist     = ETADIST()
    #dist_900_1m =\
    #                Counter("/home/roar/DISKS/1/19-31_oct/1mln/w_decay/build/data/",\
    #                '900_1m.root',\
    #                sindou,etadist)
    #dist_900_1m.Count()
    
    #test1 = Counter('/home/roar/DISKS/1/13000_attempts/',\
    #                '13000_4m.root',\
    #                test)
    
