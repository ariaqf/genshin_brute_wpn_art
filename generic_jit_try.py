import numpy as np
import pandas as pd
import json
from itertools import permutations, combinations, chain, combinations_with_replacement
import time

characters = {"Diluc": {
    "HP": 12068,
    "BATK": 311,
    "BDEF": 729,
    "CRATE": 24.2,
    "CDMG": 50,
    "EM": 0,
    "EDMG": 0,
    "PDMG": 0,
    "ER": 100,
    #"DT": "Pyro",
    #"WT": "Claymore",
    #"Talents": {
    #    "Normal":[
    #        {"ATK":153.32, "HP": 0, "DEF": 0},
    #        {"ATK":149.79, "HP": 0, "DEF": 0},
    #        {"ATK":168.9, "}HP": 0, "DEF": 0},
    #        {"ATK":229.03, "HP": 0, "DEF": 0}
    #    ], 
    #    "Charge":[], 
    #    "Elemental":[
    #        {"ATK":151.04, "HP": 0, "DEF": 0},
    #        {"ATK":156.16, "HP": 0, "DEF": 0},
    #        {"ATK":206.08, "HP": 0, "DEF": 0}
    #    ], 
    #    "Burst":[
    #        {"ATK":326.4, "HP": 0, "DEF": 0},
    #        {"ATK":96, "HP": 0, "DEF": 0},
    #        {"ATK":326.4, "HP": 0, "DEF": 0}
    #    ]
    #},
    #"Rotation": "NNNENNNENNNENNNQNNNENNNENNNE"
}}

#subs = ["HP", "ATK", "DEF", "HP%", "ATK%", "DEF%", "EM", "ER", "CRATE", "CDMG"]
allStats = ["BATK", "BDEF", "BHP", "EDMG", "PDMG", "RDMG", "DMG", "HP", "ATK", "DEF", "HP%", "ATK%", "DEF%", "EM", "ER", "CRATE", "CDMG"]
subs = ["ATK", "ATK%", "CRATE", "CDMG", "O1"]
artifact_set_2pc = {
    "BC": {"PDMG":25},
    "GF": {"ATK%":18},
    "WT": {"EM":80},
    "PF": {"PDMG":25},
    #"TF": {"EDMG":15},#, "DT": "Electro" },
    #"VV": {"EDMG":15},#, "DT": "Anemo"  },
    #"AP": {"EDMG":15},#, "DT": "Geo"},
    "CW": {"EDMG":15},#, "DT": "Pyro"},
    #"BS": {"EDMG":15},#, "DT": "Cryo"},
    #"HD": {"EDMG":15},#, "DT": "Hydro", },
    "NO": {"DMG":20},#, "T": "Burst"},
    #"TM": {"HP%": 20}
}
artifact_set_4pc = {
    "BC": {"PDMG":25},
    "GF": {"ATK%":18},#, "AT": "Normal", "WT": ["Claymore", "Polearm", "Sword"]},
    "GF!": {"ATK%":18, "DMG": 35},#, "AT": "Normal", "WT": ["Claymore", "Polearm", "Sword"]},
    "WT!": {"EM":80, "DMG": 35}, #"AT": "Charge", "WT": ["Bow", "Catalyst"]},
    "WT": {"EM":80}, #"AT": "Charge", "WT": ["Bow", "Catalyst"]},
    "RT!": {"DMG": 40},#, "AT": ["Charge","Normal"]},
    "TS": {"DMG": 35},
    "LW": {"DMG": 35},
    "PF": {"PDMG":25},
    "PF!": {"PDMG":50, "ATK%": 18},
    #"TF": {"EDMG":15, "RDMG":40},#, "DT": "Electro" },
    #"VV": {"EDMG":15, "RDMG":60},#, "DT": "Anemo"  },
    #"AP": {"EDMG":15},#, "DT": "Geo"},
    "CW": {"EDMG":15, "RDMG":40},#, "DT": "Pyro"},
    "CW!": {"EDMG":37.5, "RDMG":40},#, "DT": "Pyro"},
    #"BS": {"EDMG":15, "CRATE": 20},#, "DT": "Cryo"},
    #"BS!": {"EDMG":15, "CRATE": 40},#, "DT": "Cryo"},
    #"HD": {"EDMG":15},#, "DT": "Hydro", },
    "NO": {"DMG":20},#, "T": "Burst"},
    "NO!": {"DMG":20, "ATK%": 20},#, "T": "Burst"},
    "TM": {"HP%": 20},
    "TM!": {"HP%": 20, "ATK%": 20}    
}

sets_4pc = {k:v for (k,v) in artifact_set_4pc.items()}

for (i,v1) in artifact_set_2pc.items():
    for (j,v2) in artifact_set_2pc.items():
        if (i!=j):
            sets_4pc[i+j] = {**v1, **v2}

artifact_slots = {
    #"HEAD": ["CRATE", "CDMG", "EM", "ATK%", "HP%", "DEF%"],
    #"SANDS": ["ER", "EM", "ATK%", "HP%", "DEF%"],
    #"GOBLET": ["EDMG", "PDMG", "ATK%", "HP%", "DEF%"],
    "HEAD": ["CRATE", "CDMG", "ATK%"],
    "SANDS": ["ER", "ATK%", "EM"],
    "GOBLET": ["EDMG","ATK%"],
    "FLOWER": ["HP"],
    "PLUME": ["ATK"],
}
subrolls = {
    "HP":[209,239,269,299],
    "ATK":[14,16,18,19],
    "DEF":[16,19,21,23],
    "HP%":[4.10,4.70,5.30,5.80],
    "ATK%":[4.10,4.70,5.30,5.80],
    "DEF%":[5.10,5.80,6.60,7.30],
    "EM":[16,19,21,23],
    "ER":[4.50,5.20,5.80,6.50],
    "CRATE":[2.70,3.10,3.50,3.90],
    "CDMG":[5.40,6.20,7,7.80],
    "O1":[0],
    "O2":[0],
    "O3":[0]
}
expected_subroll_value = {
    k: float(sum(v))/len(v) for (k,v) in subrolls.items()
}
artifact_main_buff = {
    "HP": 4780,
    "ATK": 311,
    "HP%": 46.6,
    "ATK%": 46.6,
    "DEF%": 46.6,
    "EM": 187,
    "ER": 51.8,
    "EDMG": 46.6,
    "PDMG": 58.3,
    "CRATE": 31.1,
    "CDMG": 62.2
}

weapons = {
    "SKY": {"BATK": 674, "ER%": 36.8, "DMG":8},
    "WGS": {"BATK": 608, "ATK%": 69.6},
    "WGS!": {"BATK": 608, "ATK%": 109.6},
    "UNF(0)": {"BATK": 608, "ATK%": 49.6},
    "UNF(1)": {"BATK": 608, "ATK%": 53.6},
    "UNF(2)": {"BATK": 608, "ATK%": 57.6},
    "UNF(3)": {"BATK": 608, "ATK%": 61.6},
    "UNF(4)": {"BATK": 608, "ATK%": 65.6},
    "UNF(5)": {"BATK": 608, "ATK%": 69.6},
    "UNF(1)!": {"BATK": 608, "ATK%": 57.6},
    "UNF(2)!": {"BATK": 608, "ATK%": 65.6},
    "UNF(3)!": {"BATK": 608, "ATK%": 73.6},
    "UNF(4)!": {"BATK": 608, "ATK%": 81.6},
    "UNF(5)!": {"BATK": 608, "ATK%": 89.6},
    "SBP":{"BATK": 741, "PDMG": 20.7},
    "SBP!":{"BATK": 741, "PDMG": 20.7, "ATK%": 20.6},
    "ARC":{"BATK": 565, "ATK%": 27.6},
    "BLK(0)":{"BATK": 510, "CMDG": 55.1},
    "BLK(1)":{"BATK": 510, "CMDG": 55.1, "ATK%": 12},
    "BLK(2)":{"BATK": 510, "CMDG": 55.1, "ATK%": 24},
    "BLK(3)":{"BATK": 510, "CMDG": 55.1, "ATK%": 36},
    "RYL(0)":{"BATK": 565, "CRATE": 0, "ATK%": 27.6},
    "RYL(1)":{"BATK": 565, "CRATE": 8, "ATK%": 27.6},
    "RYL(2)":{"BATK": 565, "CRATE": 16, "ATK%": 27.6},
    "RYL(3)":{"BATK": 565, "CRATE": 24, "ATK%": 27.6},
    "RYL(4)":{"BATK": 565, "CRATE": 32, "ATK%": 27.6},
    "RYL(5)":{"BATK": 565, "CRATE": 40, "ATK%": 27.6},
}

possible_rolls = [
    [6,1,1,1],
    [5,2,1,1],
    [4,3,1,1],
    [4,2,2,1],
    [3,3,2,1],
    [3,2,2,2]
]

possible_rolls = list(chain.from_iterable(set(permutations(possible_rolls[i])) for i in range(len(possible_rolls))))

all_subs = list(combinations(subs,4))

subs_per_slot = {}
sub_sets = {}

for _subs in all_subs:
    for roll in possible_rolls:
        base_key = _subs[0]+str(roll[0])+"_"+_subs[1]+str(roll[1])+"_"+_subs[2]+str(roll[2])+"_"+_subs[3]+str(roll[3])
        sub_set = {key:0 for key in subs }
        sub_set[_subs[0]] = float(roll[0])*float(expected_subroll_value[_subs[0]])
        sub_set[_subs[1]] = float(roll[1])*float(expected_subroll_value[_subs[1]])
        sub_set[_subs[2]] = float(roll[2])*float(expected_subroll_value[_subs[2]])
        sub_set[_subs[3]] = float(roll[3])*float(expected_subroll_value[_subs[3]])
        sub_sets[base_key] = sub_set
                
for (slot,atts) in artifact_slots.items():
    subs_per_slot[slot] = {}
    for att in atts:
        subs_per_slot[slot][att] = []
        for i in sub_sets.keys():
            m_subs = i.split("_")
            not_in = True
            for j in m_subs:
                not_in = not_in and att != j[:len(j)-1]
            if(not_in):
                subs_per_slot[slot][att].append(i)
                
artifact_df = pd.DataFrame({k:{k:v} for (k,v) in artifact_main_buff.items()}).fillna(0)
weapon_df = pd.DataFrame(weapons).fillna(0)
character_df = pd.DataFrame(characters).fillna(0)
sub_sets_df = pd.DataFrame(sub_sets).fillna(0)
_4pc_df = pd.DataFrame(sets_4pc).fillna(0)

builds = pd.DataFrame({"Character": ["Diluc"]}).merge(pd.DataFrame({"Weapon": weapons.keys()}).fillna(0), how="cross")
builds = builds.merge(pd.DataFrame({"SET":sets_4pc.keys()}), how="cross")   


def genBuild(charName, weapon, artSet, plumeMain, plumeSubs, flowerMain, flowerSubs, sandsMain, sandsSubs, gobletMain, gobletSubs, headMain,headSubs):
    _b = {}
    _b["Character"] = charName
    _b["Weapon"] = weapon
    _b["Set"] = artSet
    _b["Plume"] = plumeMain
    _b["Plume_Subs"] = plumeSubs
    _b["Flower"] = flowerMain
    _b["Flower_Subs"] = flowerSubs
    _b["Sands"] = sandsMain
    _b["Sands_Subs"] = sandsSubs
    _b["Goblet"] = gobletMain
    _b["Goblet_Subs"] = gobletSubs
    _b["Head"] = headMain
    _b["Head_Subs"] = headSubs
    build_stats = pd.DataFrame([{k:0.0 for k in allStats}])
    build_stats = build_stats.add(pd.DataFrame(character_df[charName]).transpose().reset_index(drop=True), fill_value=0.0)
    build_stats = build_stats.add(pd.DataFrame(weapon_df[weapon]).transpose().reset_index(drop=True), fill_value=0.0)
    build_stats = build_stats.add(pd.DataFrame(_4pc_df[artSet]).transpose().reset_index(drop=True), fill_value=0.0)
    build_stats = build_stats.add(pd.DataFrame(artifact_df[plumeMain]).transpose().reset_index(drop=True), fill_value=0.0)
    build_stats = build_stats.add(pd.DataFrame(artifact_df[flowerMain]).transpose().reset_index(drop=True), fill_value=0.0)
    build_stats = build_stats.add(pd.DataFrame(artifact_df[sandsMain]).transpose().reset_index(drop=True), fill_value=0.0)
    build_stats = build_stats.add(pd.DataFrame(artifact_df[gobletMain]).transpose().reset_index(drop=True), fill_value=0.0)
    build_stats = build_stats.add(pd.DataFrame(artifact_df[headMain]).transpose().reset_index(drop=True), fill_value=0.0)
    build_stats = build_stats.add(pd.DataFrame(sub_sets_df[plumeSubs]).transpose().reset_index(drop=True), fill_value=0.0)
    build_stats = build_stats.add(pd.DataFrame(sub_sets_df[flowerSubs]).transpose().reset_index(drop=True), fill_value=0.0)
    build_stats = build_stats.add(pd.DataFrame(sub_sets_df[sandsSubs]).transpose().reset_index(drop=True), fill_value=0.0)
    build_stats = build_stats.add(pd.DataFrame(sub_sets_df[gobletSubs]).transpose().reset_index(drop=True), fill_value=0.0)
    build_stats = build_stats.add(pd.DataFrame(sub_sets_df[headSubs]).transpose().reset_index(drop=True), fill_value=0.0)
    totalAtk = (build_stats["BATK"][0]*(1.0+build_stats["ATK%"][0]/100.0)+build_stats["ATK"][0])
    totalDef = (build_stats["BDEF"][0]*(1.0+build_stats["DEF%"][0]/100.0)+build_stats["DEF"][0])
    totalHP = (build_stats["BHP"][0]*(1.0+build_stats["HP%"][0]/100.0)+build_stats["HP"][0])
    _b["Total_Attack"] = totalAtk
    _b["Total_Defense"] = totalDef
    _b["Total_HP"] = totalHP
    _b["Total_EM"] = build_stats["EM"][0]
    _b["Total_ER"] = build_stats["ER"][0]
    _b["Total_Crate"] = build_stats["CRATE"][0]
    _b["Total_Cdmg"] = build_stats["CDMG"][0]
    _b["Total_Pdmg"] = build_stats["PDMG"][0]
    _b["Total_Edmg"] = build_stats["EDMG"][0]
    _b["Final_E_Damage"] = totalAtk *  (build_stats["DMG"][0]/100.0 + build_stats["EDMG"][0]/100.0 + 1.0) * (build_stats["CRATE"][0]/100.0 * build_stats["CDMG"][0]/100.0 + 1.0)
    _b["Final_P_Damage"] = totalAtk *  (build_stats["DMG"][0]/100.0 + build_stats["PDMG"][0]/100.0 + 1.0) * (build_stats["CRATE"][0]/100.0 * build_stats["CDMG"][0]/100.0 + 1.0)
    return _b

constraints = {
    "ER": 0,
    "EM": 0
}

for build in builds[:].itertuples():
    tempBuilds = []
    start_time = time.time()
    for (plumeMain, plumeSubs) in subs_per_slot["PLUME"].items():
        for plumeSub in plumeSubs:
            for (flowerMain, flowerSubs) in subs_per_slot["FLOWER"].items():
                for flowerSub in flowerSubs:
                    for (sandsMain, sandsSubs) in subs_per_slot["SANDS"].items():
                        for sandsSub in sandsSubs:
                            print("Total Time for a build for goblet-head all weapon/set --- %s seconds ---" % (time.time() - start_time))
                            for (gobletMain, gobletSubs) in subs_per_slot["GOBLET"].items():
                                for gobletSub in gobletSubs:
                                    print("Total Time for a build for goblet-head all weapon/set --- %s seconds ---" % (time.time() - start_time))
                                    for (headMain, headSubs) in subs_per_slot["HEAD"].items():
                                        for headSub in headSubs:
                                            build_ = genBuild(build.Character, build.Weapon, build.SET, 
                                                            plumeMain, plumeSub, 
                                                            flowerMain, flowerSub, 
                                                            sandsMain, sandsSub, 
                                                            gobletMain, gobletSub, 
                                                            headMain, headSub)
                                            if(constraints["EM"] <= build_["Total_EM"] 
                                            and constraints["ER"] <= build_["Total_ER"]):
                                                tempBuilds.append(build_)
                                            if(len(tempBuilds) > 10):
                                                tempBuilds.sort(key=lambda b : b["Final_E_Damage"],reverse=True)
                                                tempBuilds.pop()
                    print("Total Time for a build for goblet-head all weapon/set --- %s seconds ---" % (time.time() - start_time))
    print("Total Time to filter all builds for a weapon/set --- %s seconds ---" % (time.time() - start_time))
    builds.merge(pd.Dataframe(tempBuilds), how="left", left_on=["Character","Weapon","SET"], right_on=["Character","Weapon","Set"])
    print("Total Time after merge --- %s seconds ---" % (time.time() - start_time))
    
builds.to_csv("out.csv")