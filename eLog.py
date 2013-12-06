#!/user/bin/python
import os, sys, shutil
from string import *
from subprocess import call
import bitMani

print "Automatic Shift ELog Writer!"
#print "Please, before continuing, make sure "
#print "1) you have all the root file from DQM and WBM."
#print "you have got the initial and final luminosity of the run."
#print "3) you checked Barrel and Endcap occupancies."

#proceed = raw_input("Continue? (y or n): ")
#if proceed=="y":
if (1>0) :
    myrun = raw_input("Insert run number: ")
    print ""
    #intlumi = raw_input("Insert initial luminosity: ")
    #endlumi = raw_input("Insert end luminosity: ")
    print ""
    #occB = raw_input("Flag Barrel Occupancy (OK or NOT OK): ")
    #occE = raw_input("Flag Endcap Occupancy (OK or NOT OK): ")
    print ""
    #if (occB!="OK" and occB!="NOT OK") or (occE!="OK" and occE!="NOT OK"):
    if (1<0) :
        print "Occupancy state not recognized. Allowed values are OK or NOT OK"
        print "Exiting. Non Elog file produced"
    else:
        
        DetId = []        

        bho=99
        irun=99
        rpc_ev=99
    	fed=98
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

        ###############################
        #ottimizza la connessione
        #conn_string = "oracle://CMS_COND_GENERAL_R:q9312krl@cms_orcoff_prep"
    	conn_string = "oracle://CMS_COND_RPC_NOISE:j6XFEznqH9f92WUf@cms_orcoff_prep"

        #conn_string = "oracle://CMS_COND_GENERAL_R:p3105rof@cms_orcoff_prod"
        #conn_string = "oracle://CMS_COND_RPC_NOISE:GgWzAUure3t3AhBy@cms_orcoff_prep"
	#conn_string = "oracle://CMS_RPC_R:rpcr34d3r@cms_omds_adg"

    	from sqlalchemy.engine import create_engine
    	engine = create_engine(conn_string,echo=True)
    	connection = engine.connect()

        #result = connection.execute("SELECT owner,table_name from all_all_tables where owner like 'CMS_COND_RPC_NOISE'")
    	result = connection.execute("SELECT owner,table_name from all_all_tables")
        
	for row in result:
            print row['owner'],row['table_name']
    	result.close()


        #myrun=194120
        #myquery_rpcgeneral="SELECT * from CMS_COND_RPC_NOISE.RPCGENERAL where run_number="+str(myrun)
    	myquery_rpcgeneral="SELECT * from CMS_COND_RPC_NOISE.RPCGENERALNEW where run_number="+str(myrun)
    	myquery_rpceff="SELECT * from CMS_COND_RPC_NOISE.RPCEFFICIENCY where run_number="+str(myrun)
    	myquery_rpcdqm="SELECT * from CMS_COND_RPC_NOISE.RPCDQMNEW where run_number="+str(myrun)
        #myquery_rpcdqm="SELECT * from CMS_COND_RPC_NOISE.RPCDQM where run_number="+str(myrun)
        #
        #myquery_rpc_noise_roll="SELECT * from CMS_COND_RPC_NOISE.RPC_NOISE_ROLLS where run_number="+str(myrun)
        #
    	myquery_rpc_noise_strips="SELECT * from CMS_COND_RPC_NOISE.RPC_NOISE_STRIPS where run_number="+str(myrun)
        #myquery_runs="SELECT * from CMS_COND_RPC_NOISE.RUNS where run="+str(myrun)

    	irun = 0
    	getInfos =  connection.execute(myquery_rpcgeneral)
    	print "CMS_COND_RPC_NOISE.RPCGENERAL"
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
            anshB=info['N_DIGIS_BARREL']
            anshB=info['N_DIGIS_BARREL_ALLHITS']
            #anshEm=info['N_DIGIS_EM']
            anshEm=info['N_DIGIS_EM_ALLHITS']
            #anshEp=info['N_DIGIS_EP']
            anshEp=info['N_DIGIS_EP_ALLHITS']
            for d in range(0,3) :
                print d
                bx_dp = 'BX_DP%s' % str(d+1)
                bx_rms_dp = 'BX_RMS_DP%s' % str(d+1)
                bx_dm = 'BX_DM%s' % str(d+1)
                bx_rms_dm = 'BX_RMS_DM%s' % str(d+1)
                print bx_dp
                bxdp[d]=info[bx_dp]
                bx_rmsdp[d]=info[bx_rms_dp]
                bxdm[d]=info[bx_dm]
                bx_rmsdm[d]=info[bx_rms_dm]
                print bxdp[d]     
            for w in range(0,2) :
                print w
                bx_wp = 'BX_WP%s' % str(w+1)
                print bx_wp
                bx_rms_wp = 'BX_RMS_WP%s' % str(w+1)
                print bx_rms_wp
                bx_wm = 'BX_WM%s' % str(w+1)
                bx_rms_wm = 'BX_RMS_WM%s' % str(w+1)
                bxwp[w]=info[bx_wp]
                print bxwp[w]     
                bx_rmswp[w]=info[bx_rms_wp]
                bxwm[w]=info[bx_wm]
                bx_rmswm[w]=info[bx_rms_wm]
            bxw0[0]=info['BX_W0']
            bx_rmsw0[0]=info['BX_RMS_W0']
            #message ="Run="+str(info['RUN_NUMBER'])+"   RPC_EVENTS="+str(info['RPC_EVENTS'])+ "\n   BX_WM2="+str(info['BX_WM2'])+"  BX_RMS_WM2="+str(info['BX__RMS_WM2'])+"     BX_WM1="+str(info['BX_WM1'])+"  BX_RMS_WM1="+str(info['BX__RMS_WM1'])+"     BX_W0="+str(info['BX_W0'])+"    BX_RMS_W0="+str(info['BX__RMS_W0'])+"    BX_WP1="+str(info['BX_WP1'])+" BX_RMS_WP1="+str(info['BX__RMS_W1P1'])+"    BX_WP2="+str(info['BX_WP2'])+"  BX_RMS_WP2="+str(info['BX__RMS_WP2'])+"     BX_DM3="+str(info['BX_DM3'])+"  BX_RMS_DM3="+str(info['BX__RMS_DM3'])+"     BX_DM2="+str(info['BX_DM2'])+"  BX_RMS_DM2="+str(info['BX__RMS_DM2'])+"     BX_DM1="+str(info['BX_DM1'])+"  BX_RMS_DM1="+str(info['BX__RMS_DM1'])+"     BX_DP1="+str(info['BX_DP1'])+"  BX_RMS_DP1"+str(info['BX__RMS_DP1'])+"  BX_DP2="+str(info['BX_DP2'])+"  BX_RMS_DP2="+str(info['BX__RMS_DP2'])+"     BX_DP3="+str(info['BX_DP3'])+"  BX_RMS_DP3="+str(info['BX__RMS_DP3'])+"\n   N_DIGIS_EM="+str(info['N_DIGIS_EM'])+"  N_CLUSTERS_EM="+str(info['N_CLUSTERS_EM'])+"    CLUSTER_SIZE_EM="+str(info['CLUSTER_SIZE_EM'])+"\n  N_DIGIS_BARREL="+str(info['N_DIGIS_BARREL'])+"  N_CLUSTERS_BARREL="+str(info['N_CLUSTERS_BARREL'])+"    CLUSTER_SIZE_BARREL="+str(info['CLUSTER_SIZE_BARREL'])+"\n  N_DIGIS_EP="+str(info['N_DIGIS_EP'])+"  N_CLUSTERS_EP="+str(info['N_CLUSTERS_EP'])+"    CLUSTER_SIZE_EP="+str(info['CLUSTER_SIZE_EP'])
            print irun," +++++Run="+str(info['RUN_NUMBER'])+"   RPC_EVENTS="+str(info['RPC_EVENTS']) 
            print "   BX_WM2="+str(info['BX_WM2'])+"    BX_RMS_WM2="+str(info['BX_RMS_WM2'])+"     BX_WM1="+str(info['BX_WM1'])+"   BX_RMS_WM1="+str(info['BX_RMS_WM1'])+"     BX_W0="+str(info['BX_W0'])+"    BX_RMS_W0="+str(info['BX_RMS_W0'])+"    BX_WP1="+str(info['BX_WP1'])+" BX_RMS_WP1="+str(info['BX_RMS_WP1'])+"    BX_WP2="+str(info['BX_WP2'])+"  BX_RMS_WP2="+str(info['BX_RMS_WP2'])
            print "     BX_DM3="+str(info['BX_DM3'])+"  BX_RMS_DM3="+str(info['BX_RMS_DM3'])+"     BX_DM2="+str(info['BX_DM2'])+"  BX_RMS_DM2="+str(info['BX_RMS_DM2'])+"     BX_DM1="+str(info['BX_DM1'])+"  BX_RMS_DM1="+str(info['BX_RMS_DM1'])+"     BX_DP1="+str(info['BX_DP1'])+"  BX_RMS_DP1"+str(info['BX_RMS_DP1'])+"  BX_DP2="+str(info['BX_DP2'])+"  BX_RMS_DP2="+str(info['BX_RMS_DP2'])+"     BX_DP3="+str(info['BX_DP3'])+"  BX_RMS_DP3="+str(info['BX_RMS_DP3'])
            print "  N_DIGIS_BARREL="+str(info['N_DIGIS_BARREL'])+"  N_CLUSTERS_BARREL="+str(info['N_CLUSTERS_BARREL'])+"    CLUSTER_SIZE_BARREL="+str(info['CLUSTER_SIZE_BARREL'])
            print "   N_DIGIS_EM="+str(info['N_DIGIS_EM'])+"  N_CLUSTERS_EM="+str(info['N_CLUSTERS_EM'])+"    CLUSTER_SIZE_EM="+str(info['CLUSTER_SIZE_EM'])
            print "  N_DIGIS_EP="+str(info['N_DIGIS_EP'])+"  N_CLUSTERS_EP="+str(info['N_CLUSTERS_EP'])+"    CLUSTER_SIZE_EP="+str(info['CLUSTER_SIZE_EP'])
            #print irun," +++++",message
    	getInfos.close()
    	print irun,"-----------------"

        #getInfos =  connection.execute(myquery_rpceff)
        #print "CMS_COND_RPC_NOISE.RPCEFFICIENCY"
        #for info in getInfos:
            #irun=info['RUN_NUMBER']
            #message = "Run="+str(info['RUN_NUMBER'])+"   DetId="+str(info['RAW_ID'])+"   Eff="+str(info['EFF_SEG'])+"+-"+str(info['EFF_SEG_ERROR'])  
            #print irun," +++++",message
        #getInfos.close()

        getInfos =  connection.execute(myquery_rpcdqm)
        #rawInfos =  connection.execute("SELECT * from CMS_COND_RPC_NOISE.RPC_GEOMETRY")
        print "CMS_COND_RPC_NOISE.RPCDQM"

        for info in getInfos:
            irun=info['RUN_NUMBER']
            #for raws in rawInfos:
                #if raws == info['RAW_ID']:
            myraw=info['RAW_ID']
            DetId = bitMani.raw_id(myraw)
            message="Run="+str(info['RUN_NUMBER'])+"    DetId="+str(info['RAW_ID'])+"      OCCUPANCY="+str(info['OCCUPANCY'])+"    N_DIGIS="+str(info['N_DIGIS'])+"    N_CLUSTERS="+str(info['N_CLUSTERS'])+"  CLUSTER_SIZE="+str(info['CLUSTER_SIZE'])+"  BX="+str(info['BX'])+"  BX_RMS="+str(info['BX_RMS'])+"  EFF_SEG="+str(info['EFF_SEG'])+"    STATUS="+str(info['STATUS'])
            #message="STATUS="+str(info['STATUS'])+" STATUS_ALLHITS="+str(info['STATUS_ALLHITS'])
            print irun,"\n +++++",bitMani.raw_id(myraw),message, "\n"
            print DetId, "  region=", DetId[0], "   weel o disk=", DetId[1],
            if DetId[0] == 0: 
                #cqW[DetId[1]+2][info['STATUS']-1].append(info['STATUS'])
                cqW[DetId[1]+2][info['STATUS_ALLHITS']-1].append(info['STATUS_ALLHITS'])
            elif DetId[0] == 1:
                #cqDp[DetId[1]-1][info['STATUS']-1].append(info['STATUS'])
                cqDp[DetId[1]-1][info['STATUS_ALLHITS']-1].append(info['STATUS_ALLHITS'])
            elif DetId[0] == -1:
                #cqDm[DetId[1]-1][info['STATUS']-1].append(info['STATUS'])
                cqDm[DetId[1]-1][info['STATUS_ALLHITS']-1].append(info['STATUS_ALLHITS'])
                    
        #rawInfos.close()
        print cqW,"\n"
        print "cq D p: ",cqDp,"\n"
        print "cq D m:", cqDm,"\n"
        getInfos.close()

        #
        connection.close()
#query noise prep
	#myquery_rpc_noise_roll="SELECT * from CMS_COND_RPC_NOISE.RPC_NOISE_ROLLS where run_number="+str(myrun)
#query noise omds
        myquery_rpc_noise_roll="SELECT * from CMS_RPC_COND.RPC_NOISE_ROLLS where run_number="+str(myrun)
# connessione omds
        conn_string = "oracle://CMS_RPC_R:rpcr34d3r@cms_omds_adg"
        #conn_string = "oracle://CMS_COND_RPC_NOISE:GgWzAUure3t3AhBy@cms_orcoff_prep"
# connessione db test
	#conn_string = "oracle://CMS_COND_GENERAL_R:q9312krl@cms_orcoff_prep"
	#conn_string = "oracle://CMS_COND_RPC_NOISE:j6XFEznqH9f92WUf@cms_orcoff_prep"
 
	
        from sqlalchemy.engine import create_engine
        engine = create_engine(conn_string,echo=True)
        connection = engine.connect()
        print "nuova connessione! \n"
        #

        getInfos =  connection.execute(myquery_rpc_noise_roll)
        print "CMS_COND_RPC_NOISE.RPC_NOISE_ROLLS"
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
            message="Run="+str(info['RUN_NUMBER'])+"    DetId="+str(info['RAW_ID'])+"   DEAD_STRIPS="+str(info['DEAD_STRIPS'])+"    MASKED_STRIPSS="+str(info['MASKED_STRIPS'])+"   STRIPS_TO_UNMASK="+str(info['STRIPS_TO_UNMASK'])+"  STRIPS_TO_MASK="+str(info['STRIPS_TO_MASK'])+"  RATE_HZ_CM2="+str(info['RATE_HZ_CM2'])
            #print irun," +++++",message
            print irun," +++++",bitMani.raw_id(myraw),message
            print DetId, "\n  region=", DetId[0], "   weel o disk=", DetId[1],
            if info['STRIPS_TO_UNMASK'] >0:
                print "to En div da zero!\n"
            if info['STRIPS_TO_MASK'] >0:
                print "to Dis div da zero! \n"
        print " Num ",Num_noiseB," Den ",Den_noiseB," Av barrel noise rate: ",Num_noiseB/Den_noiseB
        print " Num ",Num_noiseE," Den ",Den_noiseE," Av endcap noise rate: ",Num_noiseE/Den_noiseE
        getInfos.close()

        #getInfos =  connection.execute(myquery_rpc_noise_strips)
        #print "CMS_COND_RPC_NOISE.RPC_NOISE_STRIPS"
        #for info in getInfos:
            #irun=info['RUN_NUMBER']
            #message="Run="+str(info['RUN_NUMBER'])+"    DetId="+str(info['RAW_ID'])+"   CHANNEL_NUMBER="+str(info['CHANNEL_NUMBER'])+"    STRIP_NUMBER="+str(info['STRIP_NUMBER'])+"   IS_DEAD="+str(info['IS_DEAD'])+"  IS_MASKED="+str(info['IS_MASKED'])+"  RATE_HZ_CM2="+str(info['RATE_HZ_CM2'])
            #print irun," +++++",message
        #getInfos.close()        

        #getInfos =  connection.execute(myquery_runs)
        #print "CMS_COND_RPC_NOISE.RUNS"
        #for info in getInfos:
            #irun=info['RUN']
            #message="Run="+str(info['RUN'])+"   START_TIME="+str(info['START_TIME'])+"   STOP_TIMER="+str(info['STOP_TIME'])
            #print irun," +++++",message
        #getInfos.close()


        connection.close()

        print irun,"-----------------"
        ########################################

        #If all files are found start Automatic Elog writing
        print "Producing automatic ELog with name ",myrun+".log"
        #Execute some SHELL commands!
        #Write macro for given run


        # Scrive un file.
        out_file = open(myrun+".log","w")
        out_file.write("This Text is going to out file\nLook at it and see\n")

        out_file.write("==================================================================================================\n")
        out_file.write("    Run             Type            RPC Flag        Events          duration        #Processed LS \n")
        out_file.write("    "+str(irun)+"       Collisions13    (ADD RUN FLAG)      "+str(bho)+"         "+str(bho)+"         "+str(bho)+"\n")
        out_file.write("==================================================================================================\n")
        out_file.write(" \n \n")
        out_file.write("***** Using Offline DQM ==> Data: /SingleMu/\n")
        out_file.write(" \n \n")
        out_file.write("a.) Luminosity : Initial "+str(bho)+"  cm-2sec-1\n")
        out_file.write("                 Ending: "+str(bho)+"  cm-2sec-1\n")
        out_file.write("\n")
        #UXC Pressure
        out_file.write("b.) UXC pressure -<<fixed<<setprecision(3)<<uxc_pressure<<-  mbar \n")  
        out_file.write("\n")
        #Current
        out_file.write("c.) HV_Current_Barrel\n")
        for w in range(0,5) :
            out_file.write("   Wheel << setfill('+') <<setw(2)<<w-2<<<<fixed<<setprecision(3)<<wheel_[w]<<\n")
        out_file.write("\n")
        out_file.write("d.) HV_Current_Endcap\n")
        for d in range(0,3) :
            out_file.write("   Disk <<d-3<<<<fixed<<setprecision(3)<<disk_[d]<<\n")
        for d in range(3,6) :
            out_file.write("   Disk +<<d-2<<<<fixed<<setprecision(3)<<disk_[d]<<\n")
        out_file.write("\n")
        out_file.write("e.) HV_Voltage_Barrel\n")
        out_file.write("-->Ignore until WBM expert says not to\n")
        out_file.write("f.) HV_Voltage_Endcap\n")
        out_file.write("-->Ignore until WBM expert says not to\n")
        out_file.write("\n")
        #Temperature
        out_file.write("g.) Temperature_Barrel\n")
        for w in range(0,5) :
            out_file.write("   Wheel << setfill('+') << setw(2)<<w-2<<<<fixed<<setprecision(2)<<temp_w[w]<< -><<fixed<<setprecision(0)<<num_ht_w[w]<< chamber with T > 22 <<final_w[w]<<\n")

        out_file.write("\n")
        out_file.write("h.) Temperature_Endcap\n")
        for d in range(0,3) :
            out_file.write("   Disk < setfill('+') <<setw(2)<<d-3<<<<fixed<<setprecision(2)<<temp_d[d]<<--><<fixed<<setprecision(0)<<num_ht_d[d]<< chamber with T > 22<<final_d[d]<<\n")
  
        for d in range(3,6) :
            out_file.write("   Disk << setfill('+') << setw(2)<<d-2<<<<fixed<<setprecision(2)<<temp_d[d]<< --><<fixed<<setprecision(0)<<num_ht_d[d]<< chamber with T > 22 <<final_d[d]<<\n")
  
        out_file.write("\n")
    
        out_file.write("1. # of RPC events = "+str(rpc_ev)+"\n")
        out_file.write("\n")
        out_file.write("2. # of FED errors = "+str(fed)+"\n")
        out_file.write("\n")


        out_file.write("3. Noise tool output\n")
        out_file.write("Disabled: "+str(disabled)+"    Dead:  "+str(dead)+"\n")
        out_file.write("Enable:   "+str(toEn)+"  To Disable: "+str(toDis)+"\n")
        out_file.write("Average Barrel Noise Rate: "+str(Num_noiseB/Den_noiseB)+"\n")     
        out_file.write("Average Endcap Noise Rate: "+str(Num_noiseE/Den_noiseE)+"\n")
        out_file.write("\n")
        #Chamber Quality  
        out_file.write("3. Barrel_RPCChamberQuality_Distribution\n")
        out_file.write("    W-2   W-1   W0    W+1   W+2\n")
        for x in range(0,7) :
            out_file.write("-"+str(len(cqW[0][x]))+"-"+str(len(cqW[1][x]))+"-"+str(len(cqW[2][x]))+"-"+str(len(cqW[3][x]))+"-"+str(len(cqW[4][x]))+"\n")
        out_file.write("3. Endcap_RPCChamberQuality_Distribution\n")
        out_file.write("    D-3   D-2   D-1   D+1    D+2   D+3\n")
        for x in range(0,7) :
            out_file.write("-"+str(len(cqDm[2][x]))+"-"+str(len(cqDm[1][x]))+"-"+str(len(cqDm[0][x]))+"-"+str(len(cqDp[0][x]))+"-"+str(len(cqDp[1][x]))+"-"+str(len(cqDp[2][x]))+"\n")

        
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

        out_file.write("9. Barrel Occupancy  <<occupancy_b<<\n")
        out_file.write("   EndCap Occupancy  <<occupancy_e<<\n")

        out_file.close()
        
