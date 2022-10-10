import time; import json; import pandas as pd; import numpy as np; import copy; import redis
r3 = redis.Redis(host='docker4.sun.lan', port=6380, db=3, decode_responses=True)
cons = r3.json().get('systemcons2');stars_dict = r3.json().get('starsinfo2');mats_dict = r3.json().get('materials');stars_system_dict = r3.json().get('starssystem');masterlist = r3.json().get('masterlist'); re = r3.json().get('all_resources')
buildfactors = r3.json().get('buildfactors');states = r3.json().get('states');buildtype = r3.json().get('buildtype');tier = r3.json().get('tier');buildnum = r3.json().get('buildnum'); resource_recipes = r3.json().get('resource_recipes')
buildprogram = r3.json().get('buildprogram');buildprogpio = r3.json().get('buildprogpio');recipes = r3.json().get('recipes2');output_recipes = r3.json().get('output_recipes2');craft = r3.json().get('craft');systemstars = r3.json().get('systemstars2')
r5 = redis.Redis(host='docker4.sun.lan', port=6380, db=5, decode_responses=True)
r4 = redis.Redis(host='docker4.sun.lan', port=6380, db=4, decode_responses=True)

def fert(planet):
    fertileplanet = stars_dict[planet]
    fertility = float(fertileplanet['Fertility'])
    if fertility == -1:
        return 0
    else:
        return 1+fertility*.303

def sfcalc(jumps,sf_partial):
    sfperton=((120+jumps*20)*4)
    return sf_partial*sfperton*.002735

def pph(planet,recipeid,outticker):
    planetlist = stars_dict[planet]
    recipeinfo = recipes[recipe]
    if recipeid in resource_recipes:
        retype = planetlist['Resources']
        for x in retype:
            if x['MaterialId'] == outticker:
                retype = x['ResourceType']
                factor = x['Factor']
                if retype == 'MINERAL':
                    building = 'EXT'
                    outquant = states[retype] * factor
                    inputs = []
                if retype == 'GASEOUS':
                    building = 'COL'
                    inputs = []
                    outquant = states[retype] * factor
                if retype == 'LIQUID':
                    building = 'RIG'
                    outquant = states[retype] * factor
                    inputs = []
    else:
        inputs = []
        inputs.extend(recipeinfo['Inputs'])
        output = []
        output.extend(recipeinfo['Outputs'])
        output = output[0]
        outquant = output['Amount'] * (24/(recipeinfo['TimeMs'] / (1000*60*60)))
        building = recipeinfo['BuildingTicker']
    buildings = buildnum[building]
    basecost = buildtype[building]

    #########################################################Fertility
    if building == 'ORC' or building == 'FRM':
        fertfactor = fert(planet)
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
        temppph = masterdict[tempmat]
        temppph = temppph[planet]
        temppph = temppph[0]
        if temppph == 'None':
            return 'missing'
        temppph = 1 / float(temppph)
        inputpph = inputpph + temppph*int(y['Amount'])* (24/(recipeinfo['TimeMs'] / (1000*60*60)))*buildings*1.284*cogc*fertfactor
        ########################################################### BASE
    basemats = planetlist['BuildRequirements']
    for x in basemats:
        try:
            basecost = 2.5 * buildfactors[x['MaterialTicker']] -2.5 + basecost
        except:
            continue
    ##########################################################output
    numerator = outquant*buildings*1.284*cogc*fertfactor
    ############################################################# partial fuel calc, using 1k ship
    weight = mats_dict[outticker]
    weight = max(weight['Weight'],weight['Volume'])
    sf_partial = (numerator*weight)/41.67

    ######################################################### Build Dict and list
    denominator = 24 + 10*tier[building] + basecost+inputpph
    return [numerator, denominator,sf_partial]

t = time.time()
alloutputs_dict = {}
####################################### create dict with all outputs for recipeloader
for x in output_recipes.keys():
    #for x in re:
    key = x
    value = 0
    alloutputs_dict[key] = value
recipesdone = 0
recipe_queue = []
completemats = 0
listcounter = 0
masterdict = {}   ############################# main Dict loading it 0 vals for everything
for x in alloutputs_dict.keys():
    try:
        tempcraftlist = craft[x]
    except:
        tempcraftlist = craft['DA']
    outtempdict = {}
    for y in tempcraftlist:
        outtempdict[y] = [0,0,0,0,0,0,0]
    masterdict[x] = outtempdict
recipecounter = 1
################################################################################### run loops
while recipesdone != 1:
    recipesdone = 1
    for x in re:                              ######################### RE
        if alloutputs_dict[x] == 0:
            reciperun = '=>'+ x
    ############################################################################### recipes
    if len(recipe_queue) > 0:
        reciperun = recipe_queue[0]
    else:
        for x in alloutputs_dict.keys():
            if x in re:
                continue
            if alloutputs_dict[x] == 0:
                outrec = output_recipes[x][0]
                outrecval = 1
                for y in outrec:
                    outrecval = outrecval * alloutputs_dict[y]
                if outrecval == 1:
                    for h in output_recipes[x][1]:
                        recipe_queue.append(h)
                    reciperun = recipe_queue[0]
                    #print('top '+str(recipe_queue))
                    break
    ########################################################################################################
    if type(reciperun) == list:
        reciperun = reciperun[0]
    recipeinfo = recipes[reciperun]
    print(reciperun+'          '+ str(recipecounter)+str('/392'))
    recipecounter = recipecounter + 1
    missinginput = 0
    newoutput = {}
    recipe = recipeinfo['RecipeName']
    outticker = recipeinfo['Outputs']
    outticker = outticker[0]
    outticker = outticker['Ticker']
    if alloutputs_dict[outticker] == 1:
        ranalready = 'yes'
    else:
        ranalready = 'no'
    try:
        craftlist = craft[outticker]
    except:
        craftlist = craft['DA']
    cp_pph_dict = {}
    run = 1
    ########################### calc pph at each crafting planet
    for cp in craftlist:
        cp_value = [0,cp,recipe,0,0,0,0]
        ### CP VALUE [highest pph, crafting planet, recipe used, partial fuel calc, on-site crafting pph, numerator, denominator]
        pphcalc = pph(cp,recipe,outticker)
        cp_value[3] = pphcalc[2]
        cp_value[5] = pphcalc[0]
        cp_value[6] = pphcalc[1]
        pphcalc = pphcalc[0] / pphcalc[1]
        cp_value[0] = pphcalc
        cp_value[4] = pphcalc
        startcheck = masterdict[outticker]
        if startcheck[cp][0] < cp_value[0]:
            cp_pph_dict[cp] = cp_value
        else:
            cp_pph_dict[cp] = startcheck[cp]
        run = run + 1
        #if run == 4155:   ## 4155 for max vlaue
            #print(cp_value)
            #break
    #for x in cxcode:
    #    cp_value2 = [0,'NA','NA',0,0,0,0]
    #    cp_pph_dict[x] = cp_value2
    ############################################################################################## calc shipped pph
    #print('starting ship calc'+str(outticker))
    run = 1
    for cp in craftlist:
        jumps = 1
        #if cp == 'Pyrgos':
            #break
        #print(cp)
        startsystem = stars_system_dict[cp]
        currentsystems = startsystem
        nextsystemscons = cons[currentsystems]
        nextsystemscons.append(startsystem)
        cpstart = cp_pph_dict[cp]
        #print(cpstart)
        while len(nextsystemscons) != 0:
            finalsf = sfcalc(jumps,cpstart[3])
            #print(finalsf)
            try:
                pphrecalc = cpstart[5] / (cpstart[6]+finalsf)
            except:
                pphrecalc = 0
            #print(pphrecalc)
            aftercons = []
            for x in nextsystemscons:
                systemcheck = 1
                nextplans = systemstars[x]
                for y in nextplans:
                    try:
                        pphstart = cp_pph_dict[y]
                    except:
                        cp_pph_dict[y] = [0,'NA','NA',0,0,0,0]
                        pphstart = [0,'NA','NA',0,0,0,0]
                    if pphrecalc > pphstart[0]:
                        cp_pph_dict[y][0] = pphrecalc
                        cp_pph_dict[y][1] = cp
                        cp_pph_dict[y][2] = recipe
                    else:
                        systemcheck = systemcheck * 0
                if systemcheck == 1:
                    aftercons.append(x)
            #print(aftercons)
            nextsystemscons = []
            for x in aftercons:
                temp = cons[x]
                for y in temp:
                    nextsystemscons.append(y)
            #print(nextsystemscons)
            run = run + 1
            jumps = jumps + 1
            #if run == 2:
                #break
        #if run == 2:
            #break
    ###################################################################################################
    #print(recipe_queue)
    try:
        del(recipe_queue[0])
    except:
        pass
    if len(recipe_queue) == 0:
        alloutputs_dict[outticker] = 1 #################### trigger for ending loop
    masterdict[outticker] = cp_pph_dict
    for x in alloutputs_dict.values(): ################ kills loop once all outputs have ran
        recipesdone = recipesdone * x
######################################################################################################### complete
for x in masterdict.keys():
    value = masterdict[x]
    r5.json().set(x,'$',value)
############################Json
json = json.dumps(masterdict)
file = open('pph.json','w')
file.write(json)
file.close()
