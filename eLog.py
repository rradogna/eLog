#!/user/bin/python

###################
# Original Author:  Raffaella Radogna,
###################
import os, sys, shutil, re, commands,  xmlrpclib
from string import *
from subprocess import call
import bitMani
import simplejson as json
from rrapi import RRApi, RRApiError

print "Automatic Shift ELog Writer!"


myrun = raw_input("Insert run number: ")
print ""
#intlumi = raw_input("Insert initial luminosity: ")
#endlumi = raw_input("Insert end luminosity: ")
print "you checked Barrel and Endcap occupancies."
occB = raw_input("Flag Barrel Occupancy (OK or NOT OK): ")
occE = raw_input("Flag Endcap Occupancy (OK or NOT OK): ")
print ""
if (occB!="OK" and occB!="NOT OK") or (occE!="OK" and occE!="NOT OK"):
#if (1<0) :
        print "Occupancy state not recognized. Allowed values are OK or NOT OK"
        print "Exiting. Non Elog file produced"

else:
        
        DetId = []        

        bho=99
        irun=99
        rpc_ev=99
    	fed=98
	run_duration=99
	run_inLumi=99
	run_enLumi=99
	run_LS=0
	run_lsLOST=0
        ancpeB=99 
        ancpeEm=99 
        ancpeEp=99
        acsB=99
        acsEm=99
        acsEp=99
        anshB=99
        anshEm=99
        anshEp=99

        bxdp = [99,99,99]
        bxdm = [99,99,99]
        bxwp = [99,99]
        bxwm = [99,99]
        bxw0 = [99]
        bx_rmsdp = [99,99,99]
        bx_rmsdm = [99,99,99]
        bx_rmswp = [99,99]
        bx_rmswm = [99,99]
        bx_rmsw0 = [99]

        cqW = [[[] for x in range(7)] for y in range(5)]
        cqDp = [[[] for x in range(7)] for y in range(3)]
        cqDm = [[[] for x in range(7)] for y in range(3)]

        disabled = 99
        dead = 99
        toEn = 99
        toDis = 99
        Num_noiseB = 99
        Num_noiseE = 99
        Den_noiseB = 1
        Den_noiseE = 1

	#Get runs from run registry
	print "From run registry..."
	print "Connecting to RunRegistry..."
	URL  = "http://runregistry.web.cern.ch/runregistry/"
	api = RRApi(URL, debug = True)
	
	print api.workspaces()
	
	print "from GLOBAL runsummary..."
	runData =  api.data('GLOBAL', 'runsummary', 'json', ['number','duration','initLumi','endLumi','runClassName'], {'datasetExists': '= true', 'number': '= '+str(myrun),'duration': '> '+str(0),'rpcPresent' : 'true'})
	for runPair in runData:
       		type_run = runPair["runClassName"]
       		run_duration = runPair["duration"]
       		run_duration = int(run_duration)
		run_inLumi = runPair["initLumi"]
		run_enLumi = runPair["endLumi"]

	h=int(run_duration/3600)
	min=int((run_duration-h*3600)/60)
	sec=run_duration - h*3600 - min*60
	
	print "--------------------------"
	print "Run Class Name ",type_run
	print "Init Lumi ", run_inLumi, "(check please)"
	print "End Lumi ", run_enLumi, "(check please)"
        print "Run duration:", run_duration, "sec =", h,":",min,":",sec	
	print "--------------------------"
	
	print "from GLOBAL runlumis..."
	runLumis = api.data('GLOBAL', 'runlumis', 'json', ['runNumber','sectionFrom','sectionTo','sectionCount','beam1Stable','beam2Stable','cmsActive','rpcReady'], {'runNumber': '= '+str(myrun)})
	for runPair in runLumis:
		secFrom = runPair["sectionFrom"]
		secTo = runPair["sectionTo"]
		nSec = runPair["sectionCount"]
		cmsOK = runPair["cmsActive"]
		rpcOK = runPair["rpcReady"]
		beam1OK = runPair["beam1Stable"]
		beam2OK = runPair["beam2Stable"]
		#print str(myrun), "from-to", secFrom, secTo, "tot lumis", nSec, "cms Active?", cmsOK, "beam1?", beam1OK, "beam2?", beam2OK, "rpc", rpcOK 
		if(cmsOK==True & rpcOK==True & beam1OK==True & beam2OK==True):
			run_LS += nSec
			
		if(cmsOK==True & rpcOK==False & beam1OK==True & beam2OK==True):
			run_lsLOST += nSec
		
	print "---------------------------"
	print "Total LS having cmsOK-beam1OK-beam2OK-rpcOK: ", run_LS
	print "Lost LS having cmsOK-beam1OK-beam2OK-rpc NOT Ready: ", run_lsLOST
	print "---------------------------"
	print " "	
	print "-------------------------------------------------------------"
	print "From OMDS..."
        ###############################
	
        #conn_string = "oracle://CMS_COND_GENERAL_R:q9312krl@cms_orcoff_prep" 
	
	#/afs/cern.ch/cms/DB/conddb/rpc 
	#OWNER			       TABLE_NAME
	#------------------------------ ------------------------------
	#CMS_COND_RPC_NOISE	       RPCDQM
	#CMS_COND_RPC_NOISE	       RPCEFFICIENCY
	#CMS_COND_RPC_NOISE	       RPCGENERAL
	#CMS_COND_RPC_NOISE	       RPCPVSSPERRUN
	#CMS_COND_RPC_NOISE	       RPCPVSSTEMPPERRUN
	#CMS_COND_RPC_NOISE	       RPC_GEOMETRY
	#CMS_COND_RPC_NOISE	       RPC_NOISE_ROLLS
	#CMS_COND_RPC_NOISE	       RPC_NOISE_STRIPS
	#CMS_COND_RPC_NOISE	       RUNS

	###############################
	
	#conn_string = "oracle://CMS_RPC_R:rpcr34d3r@cms_omds_adg"
	
	#/afs/cern.ch/cms/DB/conddb/readOnlyOMDS.xml
	#OWNER			       TABLE_NAME
	#------------------------------ ------------------------------
	#CMS_RPC_COND		       RPC_NOISE_ROLLS
	#CMS_RPC_COND		       RPC_NOISE_STRIPS
	#CMS_RPC_COND		       RPCGENERAL
	#CMS_RPC_COND		       RPCDQM
	#CMS_RPC_COND		       RPCEFFICIENCY
	
	## non contiene le tabelle con all hits o fed error di orso
	
        #conn_string = "oracle://CMS_COND_GENERAL_R:p3105rof@cms_orcoff_prod"
	
	##per le tabelle NEW di orso conn_string = "oracle://CMS_COND_RPC_NOISE:j6XFEznqH9f92WUf@cms_orcoff_prep"
        conn_string = "oracle://CMS_COND_RPC_NOISE:I7yeDAMPk0G83vrE@cms_orcoff_prep"
	
	#OWNER			       TABLE_NAME
	#------------------------------ ------------------------------
	#CMS_COND_RPC_NOISE	       RPCPVSSPERLUMI
	#CMS_COND_RPC_NOISE	       RPCPVSSPERRUN
	#CMS_COND_RPC_NOISE	       RPCEFFICIENCY
	#CMS_COND_RPC_NOISE	       RPCDQM
	#CMS_COND_RPC_NOISE	       RPCGENERAL
	#CMS_COND_RPC_NOISE	       RPCPVSSTEMPPERRUN
	#CMS_COND_RPC_NOISE	       RUNS
	#CMS_COND_RPC_NOISE	       RPC_NOISE_STRIPS
	#CMS_COND_RPC_NOISE	       RPC_NOISE_ROLLS
	#CMS_COND_RPC_NOISE	       RPCPVSSPERLUMIDEV
	#CMS_COND_RPC_NOISE	       RPCPVSSPERRUNDEV

	#OWNER			       TABLE_NAME
	#------------------------------ ------------------------------
	#CMS_COND_RPC_NOISE	       RPCDQMNEW
	#CMS_COND_RPC_NOISE	       RPCGENERALNEW
	#CMS_COND_RPC_NOISE	       RPC_GEOMETRY
	
	###############################

    	from sqlalchemy.engine import create_engine
    	engine = create_engine(conn_string,echo=True)
    	connection = engine.connect()

        #result = connection.execute("SELECT owner,table_name from all_all_tables where owner like 'CMS_COND_RPC_NOISE'")
    	#result = connection.execute("SELECT owner,table_name from all_all_tables")  
	#for row in result:
        #print row['owner'],row['table_name']
    	#result.close()

        #myrun=194120
        #myquery_rpcgeneral="SELECT * from CMS_COND_RPC_NOISE.RPCGENERAL where run_number="+str(myrun)
    	myquery_rpcgeneral="SELECT * from CMS_COND_RPC_NOISE.RPCGENERALNEW where run_number="+str(myrun)
    	myquery_rpceff="SELECT * from CMS_COND_RPC_NOISE.RPCEFFICIENCY where run_number="+str(myrun)
	#myquery_rpcdqm="SELECT * from CMS_COND_RPC_NOISE.RPCDQM where run_number="+str(myrun)
    	myquery_rpcdqm="SELECT * from CMS_COND_RPC_NOISE.RPCDQMNEW where run_number="+str(myrun)
        
        
        #myquery_rpc_noise_roll="SELECT * from CMS_COND_RPC_NOISE.RPC_NOISE_ROLLS where run_number="+str(myrun)
    	#myquery_rpc_noise_strips="SELECT * from CMS_COND_RPC_NOISE.RPC_NOISE_STRIPS where run_number="+str(myrun)
        #myquery_runs="SELECT * from CMS_COND_RPC_NOISE.RUNS where run="+str(myrun)

    	irun = 0
	print "CMS_COND_RPC_NOISE.RPCGENERAL"
    	getInfos =  connection.execute(myquery_rpcgeneral)
    	
        for info in getInfos:
            irun=info['RUN_NUMBER']
            rpc_ev=info['RPC_EVENTS']
            fed=info['FED_FATAL']
            ancpeB=info['N_CLUSTERS_BARREL']
            ancpeEm=info['N_CLUSTERS_EM']
            ancpeEp=info['N_CLUSTERS_EP']
            acsB=info['CLUSTER_SIZE_BARREL']
            acsEm=info['CLUSTER_SIZE_EM']
            acsEp=info['CLUSTER_SIZE_EP']
            #anshB=info['N_DIGIS_BARREL']
            anshB=info['N_DIGIS_BARREL_ALLHITS']
            #anshEm=info['N_DIGIS_EM']
            anshEm=info['N_DIGIS_EM_ALLHITS']
            #anshEp=info['N_DIGIS_EP']
            anshEp=info['N_DIGIS_EP_ALLHITS']
            for d in range(0,3) :
                
                bx_dp = 'BX_DP%s' % str(d+1)
                bx_rms_dp = 'BX_RMS_DP%s' % str(d+1)
                bx_dm = 'BX_DM%s' % str(d+1)
                bx_rms_dm = 'BX_RMS_DM%s' % str(d+1)
                
                bxdp[d]=info[bx_dp]
                bx_rmsdp[d]=info[bx_rms_dp]
                bxdm[d]=info[bx_dm]
                bx_rmsdm[d]=info[bx_rms_dm]
                     
            for w in range(0,2) :
                
                bx_wp = 'BX_WP%s' % str(w+1)
                
                bx_rms_wp = 'BX_RMS_WP%s' % str(w+1)
                
                bx_wm = 'BX_WM%s' % str(w+1)
                bx_rms_wm = 'BX_RMS_WM%s' % str(w+1)
                bxwp[w]=info[bx_wp]
                     
                bx_rmswp[w]=info[bx_rms_wp]
                bxwm[w]=info[bx_wm]
                bx_rmswm[w]=info[bx_rms_wm]
            bxw0[0]=info['BX_W0']
            bx_rmsw0[0]=info['BX_RMS_W0']
           
    	getInfos.close()
    	print "run:", irun,"-----------------info from CMS_COND_RPC_NOISE.RPCGENERAL retrived"

        
	print "CMS_COND_RPC_NOISE.RPCDQM"
        getInfos =  connection.execute(myquery_rpcdqm)
        #rawInfos =  connection.execute("SELECT * from CMS_COND_RPC_NOISE.RPC_GEOMETRY")
        
        for info in getInfos:
            irun=info['RUN_NUMBER']
            myraw=info['RAW_ID']
            DetId = bitMani.raw_id(myraw)

            if DetId[0] == 0: 
                #cqW[DetId[1]+2][info['STATUS']-1].append(info['STATUS'])
                cqW[DetId[1]+2][info['STATUS_ALLHITS']-1].append(info['STATUS_ALLHITS'])
            elif DetId[0] == 1:
                #cqDp[DetId[1]-1][info['STATUS']-1].append(info['STATUS'])
                cqDp[DetId[1]-1][info['STATUS_ALLHITS']-1].append(info['STATUS_ALLHITS'])
            elif DetId[0] == -1:
                #cqDm[DetId[1]-1][info['STATUS']-1].append(info['STATUS'])
                cqDm[DetId[1]-1][info['STATUS_ALLHITS']-1].append(info['STATUS_ALLHITS'])
                    
        
        getInfos.close()
	print "run:", irun,"-----------------info from CMS_COND_RPC_NOISE.RPCDQM retrived"
        
        connection.close()
	
	
	#query noise prep
	#myquery_rpc_noise_roll="SELECT * from CMS_COND_RPC_NOISE.RPC_NOISE_ROLLS where run_number="+str(myrun)
	#query noise omds
        myquery_rpc_noise_roll="SELECT * from CMS_RPC_COND.RPC_NOISE_ROLLS where run_number="+str(myrun)
	#omds
        conn_string = "oracle://CMS_RPC_R:rpcr34d3r@cms_omds_adg"
        #conn_string = "oracle://CMS_COND_RPC_NOISE:GgWzAUure3t3AhBy@cms_orcoff_prep"
	#db test
	#conn_string = "oracle://CMS_COND_GENERAL_R:q9312krl@cms_orcoff_prep"
	#conn_string = "oracle://CMS_COND_RPC_NOISE:j6XFEznqH9f92WUf@cms_orcoff_prep"
 
	
        from sqlalchemy.engine import create_engine
        engine = create_engine(conn_string,echo=True)
        connection = engine.connect()
        print "new connession! \n"
        
	print "CMS_COND_RPC_NOISE.RPC_NOISE_ROLLS"
        getInfos =  connection.execute(myquery_rpc_noise_roll)
        
        disabled = 0
        dead = 0
        toEn = 0
        toDis = 0
        for info in getInfos:
            myraw=info['RAW_ID']
            DetId = bitMani.raw_id(myraw)
            #irun=info['RUN_NUMBER']
            disabled += info['MASKED_STRIPS']
            dead += info['DEAD_STRIPS']
            toEn += info['STRIPS_TO_UNMASK']
            toDis += info['STRIPS_TO_MASK']
            if DetId[0] == 0: 
                Num_noiseB += info['RATE_HZ_CM2'] 
                Den_noiseB += 1
            else :
                Num_noiseE += info['RATE_HZ_CM2'] 
                Den_noiseE += 1
            
        getInfos.close()
 	print "run:", irun,"-----------------info from CMS_COND_RPC_NOISE.RPC_NOISE_ROLLS retrived"
	
        connection.close()

	print " "
        print "-----------------"
        ########################################

        
        print "Producing automatic ELog with name ",myrun+".log"
        
        out_file = open(myrun+".log","w")
        out_file.write("This Text is automatically produced \nPlease check all values and fill all areas\n")

        out_file.write("==================================================================================================\n")
        out_file.write("	Run		Type			RPC Flag		Events		duration	#Processed LS \n")
        out_file.write("	"+str(irun)+"		"+str(type_run)+"		(ADD RUN FLAG)		"+str(rpc_ev)+"		"+str(h)+":"+str(min)+":"+str(sec)+"         "+str(run_LS)+"\n")
        out_file.write("==================================================================================================\n")
        out_file.write(" \n \n")
        out_file.write("***** Using Offline DQM ==> Data: /SingleMu/\n")
        out_file.write(" \n \n")
        out_file.write("a.) Luminosity : Initial "+str(run_inLumi)+" x 10^30 cm-2sec-1 (CHECK PLEASE)\n")
        out_file.write("                 Ending: "+str(run_enLumi)+" x 10^30 cm-2sec-1 (CHECK PLEASE)\n")
        out_file.write("\n")
        #UXC Pressure
        out_file.write("b.) UXC pressure XXX  mbar \n")  
        out_file.write("\n")
        #Current
        out_file.write("c.) HV_Current_Barrel\n")
        for w in range(0,5) :
            out_file.write("   Wheel "+str(w-2)+" XXX\n")
        out_file.write("\n")
        out_file.write("d.) HV_Current_Endcap\n")
        for d in range(0,3) :
            out_file.write("   Disk "+str(d-3)+" XXX\n")
        for d in range(3,6) :
            out_file.write("   Disk "+str(d-2)+" XXX\n")
        out_file.write("\n")
        out_file.write("e.) HV_Voltage_Barrel\n")
        out_file.write("-->Ignore until WBM expert says not to\n")
        out_file.write("f.) HV_Voltage_Endcap\n")
        out_file.write("-->Ignore until WBM expert says not to\n")
        out_file.write("\n")
        #Temperature
        out_file.write("g.) Temperature_Barrel\n")
        for w in range(0,5) :
            out_file.write("   Wheel "+str(w-2)+" XXX, X chamber with T > 22\n")

        out_file.write("\n")
        out_file.write("h.) Temperature_Endcap\n")
        for d in range(0,3) :
            out_file.write("   Disk "+str(d-3)+" XXX, X chamber with T > 22\n")
  
        for d in range(3,6) :
            out_file.write("   Disk "+str(d-2)+" XXX, X chamber with T > 22\n")
  
        out_file.write("\n")
    
        out_file.write("1. # of RPC events = "+str(rpc_ev)+"\n")
        out_file.write("\n")
        out_file.write("2. # of FED errors = "+str(fed)+"\n")
        out_file.write("\n")


        out_file.write("3. Noise tool output\n")
        out_file.write("   Disabled: "+str(disabled)+"    Dead:  "+str(dead)+"\n")
        out_file.write("   Enable:   "+str(toEn)+"  To Disable: "+str(toDis)+"\n")
        out_file.write("   Average Barrel Noise Rate (arithmetic mean): "+str(Num_noiseB/Den_noiseB)+"\n")     
        out_file.write("   Average Endcap Noise Rate (arithmetic mean): "+str(Num_noiseE/Den_noiseE)+"\n")
        out_file.write("\n")
        #Chamber Quality  
        out_file.write("4. Barrel_RPCChamberQuality_Distribution\n")
        out_file.write("   			W-2	W-1	W0	W+1	W+2\n")
        #for x in range(0,7) :
        #out_file.write("-"+str(len(cqW[0][0]))+"-"+str(len(cqW[1][0]))+"-"+str(len(cqW[2][0]))+"-"+str(len(cqW[3][0]))+"-"+str(len(cqW[4][0]))+"\n")
        #out_file.write("-"+str(len(cqW[0][1]))+"-"+str(len(cqW[1][1]))+"-"+str(len(cqW[2][1]))+"-"+str(len(cqW[3][1]))+"-"+str(len(cqW[4][1]))+"\n")
        out_file.write("   Noisy Strip    	"+str(len(cqW[0][2]))+"	"+str(len(cqW[1][2]))+"	"+str(len(cqW[2][2]))+"	"+str(len(cqW[3][2]))+"	"+str(len(cqW[4][2]))+"\n")
        out_file.write("   Noisy Chamber  	"+str(len(cqW[0][3]))+"	"+str(len(cqW[1][3]))+"	"+str(len(cqW[2][3]))+"	"+str(len(cqW[3][3]))+"	"+str(len(cqW[4][3]))+"\n")
        out_file.write("   Partially Dead 	"+str(len(cqW[0][4]))+"	"+str(len(cqW[1][4]))+"	"+str(len(cqW[2][4]))+"	"+str(len(cqW[3][4]))+"	"+str(len(cqW[4][4]))+"\n")
        out_file.write("   Dead   	 	"+str(len(cqW[0][5]))+"	"+str(len(cqW[1][5]))+"	"+str(len(cqW[2][5]))+"	"+str(len(cqW[3][5]))+"	"+str(len(cqW[4][5]))+"\n")
        out_file.write("   Bad Shape      	"+str(len(cqW[0][6]))+"	"+str(len(cqW[1][6]))+"	"+str(len(cqW[2][6]))+"	"+str(len(cqW[3][6]))+"	"+str(len(cqW[4][6]))+"\n")

        out_file.write("   Endcap_RPCChamberQuality_Distribution\n")
        out_file.write("   			D-3	D-2	D-1	D+1	D+2	D+3\n")
        #for x in range(0,7) :
        #    out_file.write("-"+str(len(cqDm[2][x]))+"-"+str(len(cqDm[1][x]))+"-"+str(len(cqDm[0][x]))+"-"+str(len(cqDp[0][x]))+"-"+str(len(cqDp[1][x]))+"-"+str(len(cqDp[2][x]))+"\n")
        out_file.write("   Noisy Strip    	"+str(len(cqDm[2][2]))+"	"+str(len(cqDm[1][2]))+"	"+str(len(cqDm[0][2]))+"	"+str(len(cqDp[0][2]))+"	"+str(len(cqDp[1][2]))+"	"+str(len(cqDp[2][2]))+"\n")
        out_file.write("   Noisy Chamber  	"+str(len(cqDm[2][3]))+"	"+str(len(cqDm[1][3]))+"	"+str(len(cqDm[0][3]))+"	"+str(len(cqDp[0][3]))+"	"+str(len(cqDp[1][3]))+"	"+str(len(cqDp[2][3]))+"\n")
        out_file.write("   Partially Dead 	"+str(len(cqDm[2][4]))+"	"+str(len(cqDm[1][4]))+"	"+str(len(cqDm[0][4]))+"	"+str(len(cqDp[0][4]))+"	"+str(len(cqDp[1][4]))+"	"+str(len(cqDp[2][4]))+"\n")
        out_file.write("   Dead           	"+str(len(cqDm[2][5]))+"	"+str(len(cqDm[1][5]))+"	"+str(len(cqDm[0][5]))+"	"+str(len(cqDp[0][5]))+"	"+str(len(cqDp[1][5]))+"	"+str(len(cqDp[2][5]))+"\n")
        out_file.write("   Bad Shape      	"+str(len(cqDm[2][6]))+"	"+str(len(cqDm[1][6]))+"	"+str(len(cqDm[0][6]))+"	"+str(len(cqDp[0][6]))+"	"+str(len(cqDp[1][6]))+"	"+str(len(cqDp[2][6]))+"\n")
        out_file.write("\n")
        # mancano punti 3 e 4

        out_file.write("5. BunchCrossing Distribution/Wheel (mean value)\n")
        for w in range(-2,0) :
            out_file.write("   Wheel "+str(w)+" = "+str(bxwm[w*(-1)-1])+" +- "+str(bx_rmswm[w*(-1)-1])+"\n")  
        out_file.write("   Wheel 0 = "+str(bxw0[0])+" +- "+str(bx_rmsw0[0])+"\n")  
        for w in range(0,2) :
            out_file.write("   Wheel +"+str(w+1)+" = "+str(bxwp[w])+" +- "+str(bx_rmswp[w])+"\n")  

        out_file.write("   BunchCrossing Distribution/Disk (mean value)\n")
        for d in range(-3,0) :
            out_file.write("   Disk "+str(d)+" = "+str(bxdm[d*(-1)-1])+" +- "+str(bx_rmsdm[d*(-1)-1])+"\n")  
        for d in range(0,3) :
            out_file.write("   Disk +"+str(d+1)+" = "+str(bxdp[d])+" +- "+str(bx_rmsdp[d])+"\n")

        out_file.write("\n")

        out_file.write("7. Average number of clusters per event Barrel  ="+str(ancpeB)+"\n")
        out_file.write("   Average number of clusters per event E-      ="+str(ancpeEm)+"\n")
        out_file.write("   Average number of clusters per event E+      ="+str(ancpeEp)+"\n")
        out_file.write("   Average cluster size Barrel                  ="+str(acsB)+"\n")
        out_file.write("   Average cluster size E-                      ="+str(acsEm)+"\n")
        out_file.write("   Average cluster size E+                      ="+str(acsEp)+"\n")
        out_file.write("\n")

        out_file.write("8. Average number of single hits Barrel         ="+str(anshB)+"\n")
        out_file.write("   Average number of single hits E-             ="+str(anshEm)+"\n")
        out_file.write("   Average number of single hits E+             ="+str(anshEp)+"\n")
        out_file.write("\n")

        out_file.write("9. Barrel Occupancy "+str(occB)+"\n")
        out_file.write("   EndCap Occupancy "+str(occE)+"\n")
	out_file.write("\n")
	
	out_file.write("   LS lost by RPC: "+str(run_lsLOST)+"\n")
        out_file.write("\n")
        out_file.close()
        
