import numpy as np
import time

from characters import Kaeya
from constants import all_stats, subs_buffs, artifact_slots, artifact_main_buff
from weapons import swords as weapons
from artifacts import all_sets, artifact_permutations, sub_sets

constraints = {
    "EM": {"minimum":None, "maximum": None},
    "ER": {"minimum":100, "maximum": None}
}

weapons = {name:{"Name":name, "Lv":90, **weapon} for (name,weapon) in weapons.items()}

characters = {"Kaeya": Kaeya}

stat_vectors = np.zeros((len(characters)*len(weapons)*len(all_sets),len(all_stats)), dtype= np.float32)

stat_indexing = {k:all_stats.index(k) for k in all_stats}

char_weapon_set_index = {}

row = 0
for (char, char_stats) in characters.items():
    for (weapon, weapon_stats) in weapons.items():
        for (set_, set_stats) in all_sets.items():
            sv = stat_vectors[row]
            char_weapon_set_index[char+"_"+weapon+"_"+set_] = row
            for (stat, index) in stat_indexing.items():
                sv[index] += char_stats.get(stat,0)
                sv[index] += weapon_stats.get(stat,0)
                sv[index] += set_stats.get(stat,0)
            row += 1

def my_fit_function(stats):
    b_atk = stats[0]
    p_atk = stats[17]
    atk = stats[14]
    edmg = stats[12] + stats[9] + stats[3]
    pdmg = stats[12] + stats[10]
    normal_dmg = stats[23]
    skill_dmg = stats[25]
    burst_dmg = stats[26]
    c_rate = min(stats[21],100)
    c_dmg = stats[22]
    em = stats[19]
    react_dmg = stats[12]
    # 2.78 for melt/vap or 6.67 for everything else
    reaction_type_multiplier = 2.78
    # 1.5 for reverse vap, reverse melt; 2 for vap/melt
    # For everything else: Base Multiplier × Character Level Multiplier
    # Base Multiplier up there. Level Multiplier: 80 -> 946.4, 90 -> 1202.8, 100 -> 1674.8
    react_multiplier = 1.5
    # for vap/melt
    react_final_multiplier = react_multiplier * (1+(em/(1400+em))*reaction_type_multiplier + react_dmg/100.0)
    #QAAAEAAAEAAAEAAA (vap on Q and E)
    #return 1.51*(b_atk*(1.0+p_atk/100.0) + atk) *  (edmg/100.0 + 1.0) * (min(c_rate/100.0,1) * c_dmg/100.0 + 1.0)
    return ((1+burst_dmg/100.0) * react_final_multiplier*(b_atk*(1.0+p_atk/100.0) + atk) *  (edmg/100.0 + 1.0) * (min(c_rate/100.0,1) * c_dmg/100.0 + 1.0))

plume_main = np.zeros(len(all_stats), dtype= np.float32)
plume_main[all_stats.index("ATK")] += artifact_main_buff["ATK"]
plume_subs = np.zeros((len(artifact_permutations["PLUME"]["ATK"]),len(all_stats)), dtype= np.float32)
row = 0
for sub_id in artifact_permutations["PLUME"]["ATK"]:
    for sub in sub_sets[sub_id]:
        plume_subs[row][all_stats.index(sub)] += sub_sets[sub_id][sub]

flower_main = np.zeros(len(all_stats), dtype= np.float32)
flower_main[all_stats.index("HP")] += artifact_main_buff["HP"]
flower_subs = np.zeros((len(artifact_permutations["FLOWER"]["HP"]),len(all_stats)), dtype= np.float32)
for sub_id in artifact_permutations["FLOWER"]["HP"]:
    for sub in sub_sets[sub_id]:
        flower_subs[row][all_stats.index(sub)] += sub_sets[sub_id][sub]

sands_mains = np.zeros((len(artifact_slots["SANDS"]),len(all_stats)), dtype= np.float32)
row = 0
for main in artifact_slots["SANDS"]:
    sands_mains[row][all_stats.index(main)] += artifact_main_buff[main]
    row += 1
    for sub_id in artifact_permutations["SANDS"][main]:
        for sub in sub_sets[sub_id]:
        flower_subs[row][all_stats.index(sub)] += sub_sets[sub_id][sub]
    
goblet_mains = np.zeros((len(artifact_slots["GOBLET"]),len(all_stats)), dtype= np.float32)
row = 0
for main in artifact_slots["GOBLET"]:
    sands_mains[row][all_stats.index(main)] += artifact_main_buff[main]
    row += 1
    
circlet_mains = np.zeros((len(artifact_slots["HEAD"]),len(all_stats)), dtype= np.float32)
row = 0
for main in artifact_slots["HEAD"]:
    sands_mains[row][all_stats.index(main)] += artifact_main_buff[main]
    row += 1


for (build,index) in char_weapon_set_index.items():
    #build_stats = run_all_artifact_permutations(np.copy(stat_vectors[index]), artifacts, stat_indexing, )
    best_stats = stat_vectors[index]
    for (plumeMain, plumeSubs) in artifact_permutations["PLUME"].items():
        for plumeSub in plumeSubs:
            for (flowerMain, flowerSubs) in artifact_permutations["FLOWER"].items():
                for flowerSub in flowerSubs:
                    for (sandsMain, sandsSubs) in artifact_permutations["SANDS"].items():
                        for sandsSub in sandsSubs:
                            print("Total Time for a build --- %s seconds ---" % (time.time() - start))
                            for (gobletMain, gobletSubs) in artifact_permutations["GOBLET"].items():
                                for gobletSub in gobletSubs:
                                    for (headMain, headSubs) in artifact_permutations["HEAD"].items():
                                        for headSub in headSubs:
                                            temp_stats = np.copy(best_stats)
                                            temp_stats +=
#                                            temp_build = np.copy(build)