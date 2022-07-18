import time; import json; import pandas as pd; import numpy as np; import copy;

file2 = open('system.json','r');system_dict = json.load(file2);file2.close()
file3 = open('starsinfo.json','r');stars_dict = json.load(file3);file3.close()
file4 = open('materials.json','r');mats_dict = json.load(file4);file4.close()
file5 = open('starssystem.json','r');stars_system_dict = json.load(file5);file5.close()
file6 = open('recipes-tier1.json','r');recipes_dict = json.load(file6);file6.close()
matpph_dict = {'H2O_Umbra':44.955982522130846,'H2O_Etherwind':64.2000025510788,'H2O_KW-602c':49.3981248914246,'H2O_Milliways':46.34518442538274}
matresource_dict = {'H2O_Umbra':'Etherwind','H2O_Etherwind':'Etherwind','H2O_KW-602c':'Etherwind','H2O_Milliways':'Etherwind'}
jumpsample_dict = {'EtherwindUmbra':4,'EtherwindEtherwind':0,'EtherwindKW-602c':1,'EtherwindMilliways':3,'UmbraUmbra':0,'MilliwaysUmbra':1,'KW-602cUmbra':3,'KW-602cKW-602c':0,'KW-602cMilliways':2,'MilliwaysMilliways':0}
buildfactors = {'MCG':1,'AEF':1.7,'HSE':1.35,'INS':1.99,'SEA':1.04,'TSH':2.2,'MGC':1.3,'BL':1.06}
states = {'MINERAL':70,'GASEOUS':60,'LIQUID':70}
buildtype = {'EXT':2.5, 'RIG':3.8, 'COL':3.4, 'BMP':3.3, 'FRM': 1.4, 'FP':2.8, 'INC':3.3, 'PP1':2.3, 'SME': 3, 'WEL':2.8, 'CHP':2.1, 'CLF':2.3, 'EDM':4.6, 'FER':2.5, 'FS':2, 'GF':3.4, 'HYF':7.8, 'PPF':3.1, 'POL':4.4, 'PP2':2.4, 'REF':2.5, 'UPF':2.4, 'WPL':2.2, 'CLR':6.1, 'ELP':14.6, 'ECA':17.3, 'HWP':3.5, 'IVP':16.1, 'LAB':9.5, 'MCA':14.4, 'ORC':4.5, 'PHF':6.2, 'PP3':4.9, 'SKF':2.1, 'SCA':12.1, 'SD':12.6, 'TNP':9.9, 'AML':31.9, 'ASM':7.8, 'APF':34.7, 'DRS':22.2, 'PP4':20.8, 'SE':35, 'SPP':15.8, 'AAF':32.6, 'EEP':17.9, 'SL':51, 'SPF':25}
tier = {'EXT':1, 'RIG':1, 'COL':1, 'BMP':1, 'FRM': 1, 'FP':1, 'INC':1, 'PP1':1, 'SME': 1, 'WEL':1, 'CHP':1.3, 'CLF':1.3, 'EDM':1.3, 'FER':1.3, 'FS':1.3, 'GF':1.3, 'HYF':1.3, 'PPF':1.3, 'POL':1.3, 'PP2':1.3, 'REF':1.3, 'UPF':1.3, 'WPL':1.3, 'CLR':2, 'ELP':2, 'ECA':2, 'HWP':2, 'IVP':2, 'LAB':2, 'MCA':2, 'ORC':2, 'PHF':2, 'PP3':2, 'SKF':2, 'SCA':2, 'SD':2, 'TNP':2, 'AML':4, 'ASM':4, 'APF':4, 'DRS':4, 'PP4':4, 'SE':4, 'SPP':4, 'AAF':7, 'EEP':7, 'SL':7, 'SPF':7}
buildnum = {'EXT':15, 'RIG':36, 'COL':23, 'BMP':21, 'FRM': 13, 'FP':29, 'INC':33, 'PP1':17, 'SME': 21, 'WEL':18, 'CHP':16, 'CLF':11, 'EDM':13, 'FER':14, 'FS':15, 'GF':12, 'HYF':21, 'PPF':21, 'POL':24, 'PP2':15, 'REF':13, 'UPF':8, 'WPL':9, 'CLR':14, 'ELP':11, 'ECA':11, 'HWP':15, 'IVP':11, 'LAB':12, 'MCA':11, 'ORC':3, 'PHF':11, 'PP3':11, 'SKF':10, 'SCA':11, 'SD':17, 'TNP':11, 'AML':8, 'ASM':10, 'APF':8, 'DRS':11, 'PP4':9, 'SE':18, 'SPP':6, 'AAF':7, 'EEP':4, 'SL':20, 'SPF':8}
buildprogram = {'EXT':'ADVERTISING_RESOURCE_EXTRACTION', 'RIG':'ADVERTISING_RESOURCE_EXTRACTION', 'COL':'ADVERTISING_RESOURCE_EXTRACTION', 'BMP':'ADVERTISING_MANUFACTURING', 'FRM': 'ADVERTISING_AGRICULTURE', 'FP':'ADVERTISING_FOOD_INDUSTRIES', 'INC':'ADVERTISING_RESOURCE_EXTRACTION', 'PP1':'ADVERTISING_CONSTRUCTION', 'SME': 'ADVERTISING_METALLURGY', 'WEL':'ADVERTISING_CONSTRUCTION', 'CHP':'ADVERTISING_CHEMISTRY', 'CLF':'ADVERTISING_MANUFACTURING', 'EDM':'ADVERTISING_ELECTRONICS', 'FER':'ADVERTISING_FOOD_INDUSTRIES', 'FS':'ADVERTISING_METALLURGY', 'GF':'ADVERTISING_METALLURGY', 'HYF':'ADVERTISING_AGRICULTURE', 'PPF':'ADVERTISING_MANUFACTURING', 'POL':'ADVERTISING_CHEMISTRY', 'PP2':'ADVERTISING_CONSTRUCTION', 'REF':'ADVERTISING_FUEL_REFINING', 'UPF':'ADVERTISING_CONSTRUCTION', 'WPL':'ADVERTISING_MANUFACTURING', 'CLR':'ADVERTISING_ELECTRONICS', 'ELP':'ADVERTISING_ELECTRONICS', 'ECA':'ADVERTISING_ELECTRONICS', 'HWP':'ADVERTISING_METALLURGY', 'IVP':'ADVERTISING_FOOD_INDUSTRIES', 'LAB':'ADVERTISING_CHEMISTRY', 'MCA':'ADVERTISING_MANUFACTURING', 'ORC':'ADVERTISING_AGRICULTURE', 'PHF':'ADVERTISING_CHEMISTRY', 'PP3':'ADVERTISING_CONSTRUCTION', 'SKF':'ADVERTISING_METALLURGY', 'SCA':'ADVERTISING_MANUFACTURING', 'SD':'ADVERTISING_ELECTRONICS', 'TNP':'ADVERTISING_CHEMISTRY', 'AML':'ADVERTISING_CHEMISTRY', 'ASM':'ADVERTISING_METALLURGY', 'APF':'ADVERTISING_MANUFACTURING', 'DRS':'ADVERTISING_ELECTRONICS', 'PP4':'ADVERTISING_CONSTRUCTION', 'SE':'ADVERTISING_ELECTRONICS', 'SPP':'ADVERTISING_MANUFACTURING', 'AAF':'ADVERTISING_MANUFACTURING', 'EEP':'ADVERTISING_CHEMISTRY', 'SL':'ADVERTISING_ELECTRONICS', 'SPF':'ADVERTISING_MANUFACTURING'}
buildprogpio = {'BMP':'WORKFORCE_PIONEERS','FRM':'WORKFORCE_PIONEERS','FP':'WORKFORCE_PIONEERS','INC':'WORKFORCE_PIONEERS','PP1':'WORKFORCE_PIONEERS','SME':'WORKFORCE_PIONEERS','WEL':'WORKFORCE_PIONEERS','EXT':'WORKFORCE_PIONEERS','RIG':'WORKFORCE_PIONEERS','COL':'WORKFORCE_PIONEERS'}
minfactor = 0
def fert(counterpph):
    fertileplanet = stars_dict[counterpph]
    fertility = float(fertileplanet['Fertility'])
    if fertility == -1:
        return 0
    else:
        return 1+fertility*.303
def sfcalc(jumps,mats,pph):
    if jumps ==0:
        sfburn = 0
    else:
        sfburn = 120
    sfperton=((sfburn+jumps*20)*4)
    weight = mats_dict[mats]
    weight = max(weight['Weight'],weight['Volume'])
    return ((pph*weight)/41.67)*sfperton*.002735
def pph(planjumps,startplanet,resourceplanet,recipe):
    counterpph = 0
    missing = 0
    for x in stars_dict:
        if x['PlanetName']==startplanet:
            break
        counterpph = counterpph + 1
    planetlist = stars_dict[counterpph]
    recipecount = 0
    for x in recipes_dict:
        if x['RecipeName'] == recipe:
            break
        recipecount = recipecount +1
    recipeid = recipes_dict[recipecount]
    inputs = []
    inputs.extend(recipeid['Inputs'])
    output = []
    output.extend(recipeid['Outputs'])
    output = output[0]
    outticker = output['Ticker']
    outquant = output['Amount'] * (24/(recipeid['TimeMs'] / (1000*60*60)))
    building = recipeid['BuildingTicker']
    buildings = buildnum[building]
    basecost = buildtype[building]
    #########################################################Fertility
    if building == 'ORC' or building == 'FRM':
        fertfactor = fert(counterpph)
    else:
        fertfactor = 1
    ########################################################## COGC
    try:
        cogc = planetlist['COGCPrograms']
        cogc = cogc[0]
        cogc = cogc['ProgramType']
        if cogc == buildprogram[building]:
            cogc = 1.25
        else:
            try:
                if cogc == buildprogpio[building]:
                        cogc = 1.1
                else:
                    cogc = 1
            except:
                cogc = 1
    except:
        cogc = 1
    ########################################################### INPUT PPH
    inputpph = 0
    for y in inputs:
        tempmat = y['Ticker']
        rstring = str(tempmat+'_'+startplanet)
        try:
            temppph = float(matpph_dict[rstring])
        except:
            missing = 1
            return 'missing'
        temppph = 1 / temppph
        inputpph = inputpph + temppph*int(y['Amount'])* (24/(recipeid['TimeMs'] / (1000*60*60)))*buildings*1.284*cogc*fertfactor
        ########################################################### BASE
    basemats = planetlist['BuildRequirements']
    for x in basemats:
        try:
            basecost = 2.5 * buildfactors[x['MaterialTicker']] -2.5 + basecost
        except:
            continue
    ##########################################################output
    output = outquant*buildings*1.284*cogc*fertfactor

    ################################################################sfcalc
    sf = sfcalc(planjumps,outticker,output)


    ######################################################### Build Dict and list
    pph = (output) / (24 + 10*tier[building] + basecost+sf+inputpph)
    key10 = outticker+'_'+resourceplanet
    value10 = pph
    key11 = resourceplanet+'_'+outticker
    value11 = startplanet
    try:
        cogctest = planetlist['COGCPrograms']
        cogctest = cogctest[0]
        cogctest = cogctest['ProgramType']
    except:
        cogctest = 'NA'
    try:
        og = matpph_dict[key10]
        og = float(og)
        if og <= pph:
            matpph_dict[key10] = pph
            return 'recipe '+recipe+' building ' +building+ ' pph ' +str(pph)+' start '+startplanet+' dest '+resourceplanet+' cogctest '+str(cogctest)+' cogc '+str(cogc)+' output '+str(output)+' inputhours '+str(inputpph)+' basecost '+str(basecost)+'sf hours '+str(sf)+' fert '+str(fertfactor)+' buildings '+str(buildings)
        else:
            if startplanet == resourceplanet:
                return 'break'
    except:
        matpph_dict[key10] = pph
        return 'recipe '+recipe+' building ' +building+ ' pph ' +str(pph)+' start '+startplanet+' dest '+resourceplanet+' cogctest '+str(cogctest)+' cogc '+str(cogc)+' output '+str(output)+' inputhours '+str(inputpph)+' basecost '+str(basecost)+'sf hours '+str(sf)+' fert '+str(fertfactor)+' buildings '+str(buildings)
def jumps(star,pln):
    if star < pln:
        key=str(star + pln)
    else:
        key=str(pln + star)
    return int(jumpsample_dict[key])
cx = ['UV-351','OT-580','VH-331','ZV-307','AM-783','TD-203']
cxcode = ['BEN','MOR','HRT','ANT','ARC','HUB']
t = time.time()
starslist = ['Umbra','KW-602c','Etherwind','Milliways']
completemats = 0
listcounter = 0
for xxx in recipes_dict[1:2]:
    missinginput = 0
    qq = xxx['RecipeName']
    for zzz in starslist:
        currentstar = starslist[listcounter]
        newlist = [currentstar]
        for xyz in starslist:
            if xyz != currentstar:
                newlist.extend([xyz])
        if missinginput == 'missing':
            break
        for yyy in newlist:
            vpjumps = jumps(yyy,zzz)
            missinginput = pph(vpjumps,zzz,yyy,qq)
            print(missinginput)
            if missinginput == 'missing':
                completedmat = 0
                break
            if missinginput == 'break':
                completedmat = 0
                print('break')
                break
        listcounter = listcounter + 1
print(time.time()-t)
