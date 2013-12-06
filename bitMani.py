#!/user/bin/python

#id_ = 637566980
#id_ = 637566982
#id_ = 637566984
#id_ = 637566986
#id_ = 637566989
#id_ = 637632817
#id_ = 637653704
#  This in intented to unpack the RPCDetId stored in the RAW_ID column of the RPCEFFICCIENCY table
# it uses the python bit manupation by doing an and between the id and the mask selecting the useful bit
# and the shifting the bit to the most significant
# that packed data are here described 

def raw_id (id_) : 
    result = [99, 99, 99, 99, 99, 99]
    # Region is stored in 2 bits starting from bit 0
    RegionNumBits_  =  2;
    RegionStartBit_ =  0;
    RegionMask_     =  0X3;
    # Ring or Wheel is stored in 3 bits starting soon after region  
    RingNumBits_  =  3;
    RingStartBit_ =  RegionStartBit_+RegionNumBits_;
    RingMask_     =  0X7;
    # Station is stored in 2 bits starting soon after ring/wheel
    StationNumBits_  =  2;
    StationStartBit_ =  RingStartBit_+RingNumBits_;
    StationMask_     =  0X3;
    # Sector is stored in 4 bits starting soon after Station
    SectorNumBits_  =  4;
    SectorStartBit_ =  StationStartBit_+StationNumBits_;
    SectorMask_     =  0XF;
    # Layer is stored in 1 bits starting soon after Sector
    LayerNumBits_  =  1;
    LayerStartBit_ =  SectorStartBit_+SectorNumBits_;
    LayerMask_     =  0X1;
    # Subsector is stored in 3 bits starting soon after Layer
    SubSectorNumBits_  =  3;
    SubSectorStartBit_ =  LayerStartBit_+LayerNumBits_;
    SubSectorMask_     =  0X7;
    # the etaPartition is stored in 3 bits starting soon after SubSector
    RollNumBits_  =  3;
    RollStartBit_ =  SubSectorStartBit_+SubSectorNumBits_;
    RollMask_     =  0X7;

    chamberIdMask_ = ~(RollMask_<<RollStartBit_);

    # The region start from -1 and not 0... so the 2 bits need to be subtracted by ths offset
    minRegionId=     -1
    region = ( ( id_>>RegionStartBit_) & RegionMask_) + minRegionId
    result[0] = region
    #The ring(endcap) is number bertween 1 and 3 while wheel(barrel) are in -2,2 range 
    minRingForwardId=   1
    minRingBarrelId=   -2
    RingBarrelOffSet=   3
    tmpring = (id_>>RingStartBit_) & RingMask_
    if region == 0:
        ring = tmpring - RingBarrelOffSet + minRingBarrelId
    else:
        ring = tmpring + minRingForwardId 

    # Station is [1,4] (in endcap these is the disk)
    minStationId=     1
    station = ((id_>>StationStartBit_) & StationMask_) + minStationId
    #sector sextante
    sector=((id_>>SectorStartBit_) & SectorMask_) + 1
    subsec=((id_>>SubSectorStartBit_) & SubSectorMask_) + 1
    fwchamb=subsec + 6 * ( sector - 1)

    #layer (RB1 e RB2)
    minLayerId=     1
    layer = ((id_>>LayerStartBit_) & LayerMask_) + minLayerId

    # roll or etaPartitiob
    roll=((id_>>RollStartBit_) & RollMask_)

    #print "region="+str(region)
    if region == 0:
        #print "wheel="+str(ring) 
        result[1] = ring
        #print "station="+str(station)
        result[3] = station
        #print "sector="+str(sector)
        result[4] = sector
        if station>2:
            #print "subsector="+str(subsec)
            result[5] = subsec
        else:
            #print "layer="+str(layer)
            result[5] = layer
    else:
        #print "disk="+str(station)
        result[1] = station
        #print "ring="+str(ring)
        result[3] = ring
        #print "chamber="+str(fwchamb) 
        result[4] = fwchamb
    #print "roll="+str(roll)
    result[2] = roll

    return result

#raw_id (id)
