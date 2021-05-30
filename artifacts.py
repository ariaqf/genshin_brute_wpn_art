from constants import all_stats, subs_buffs, artifact_slots, mean_subroll
from itertools import permutations, combinations, chain, combinations_with_replacement


artifact_set_2pc = {
    "BC": {"PHYS_DMG":25},
    "GF": {"ATK%":18},
    "WT": {"EM":80},
    "PF": {"PHYS_DMG":25},
    "TF": {"ELEC_DMG":15},#, "DT": "Electro" },
    "VV": {"ANEMO_DMG":15},#, "DT": "Anemo"  },
    "AP": {"GEO_DMG":15},#, "DT": "Geo"},
    "CW": {"PYRO_DMG":15},#, "DT": "Pyro"},
    "BS": {"CRYO_DMG":15},#, "DT": "Cryo"},
    "HD": {"HYDRO_DMG":15},#, "DT": "Hydro", },
    "NO": {"BURST_DMG":20},#, "T": "Burst"},
    "TM": {"HP%": 20}
}
artifact_set_4pc = {
    "BC": {"PHYS_DMG":25},
    "GF": {"ATK%":18},#, "AT": "Normal", "WT": ["Claymore", "Polearm", "Sword},
    "GF!": {"ATK%":18, "NOMR_DMG": 35, "CHARGE_DMG": 35},#, "AT": "Normal", "WT": ["Claymore", "Polearm", "Sword},
    "WT!": {"EM":80, "CHARGE_DMG": 35}, #"AT": "Charge", "WT": ["Bow", "Catalyst},
    "WT": {"EM":80}, #"AT": "Charge", "WT": ["Bow", "Catalyst},
    "RT!": {"NORM_DMG": 40, "CHARGE_DMG": 40},#, "AT": ["Charge","Normal},
    "TS": {"DMG": 35},
    "LW": {"DMG": 35},
    "PF": {"PHYS_DMG":25},
    "PF!": {"PHYS_DMG":50, "ATK%": 18},
    "TF": {"ELEC_DMG":15, "REACT_DMG":40},#, "DT": "Electro" },
    "VV": {"ANEMO_DMG":15, "REACT_DMG":60},#, "DT": "Anemo"  },
    "AP": {"GEO_DMG":15},#, "DT": "Geo"},
    "AP!": {"GEO_DMG":15, "ELE_DMG":35},#, "DT": "Geo"}
    "CW": {"PYRO_DMG":15, "REACT_DMG":40},#, "DT": "Pyro"},
    "CW!": {"PYRO_DMG":37.5, "REACT_DMG":40},#, "DT": "Pyro"},
    "BS": {"CRYO_DMG":15, "CRATE": 20},#, "DT": "Cryo"},
    "BS!": {"CRYO_DMG":15, "CRATE": 40},#, "DT": "Cryo"},
    "HD": {"HYDRO_DMG":15},#, "DT": "Hydro", },
    "NO": {"BURST_DMG":20},#, "T": "Burst"},
    "NO!": {"BURST_DMG":20, "ATK%": 20},#, "T": "Burst"},
    "TM": {"HP%": 20},
    "TM!": {"HP%": 20, "ATK%": 20}    
}

sets_4pc = {k:v for (k,v) in artifact_set_4pc.items()}

for (i,v1) in artifact_set_2pc.items():
    for (j,v2) in artifact_set_2pc.items():
        set_s = {k:0.0 for k in all_stats}
        if (i!=j):
            for sub in v1:
                set_s[sub] += v1[sub]
            for sub2 in v2:
                set_s[sub2] += v2[sub2]
            sets_4pc[i+j] = set_s


for (k,v) in sets_4pc.items():
    sec_stats = {k:0.0 for k in all_stats}
    sets_4pc[k] = {**sec_stats,**v}
    
all_sets = {name:{"Name":name, **_set} for (name,_set) in sets_4pc.items()}

possible_rolls = [
    [6,1,1,1],
    [5,2,1,1],
    [4,3,1,1],
    [4,2,2,1],
    [3,3,2,1],
    [3,2,2,2]
]

possible_rolls = list(chain.from_iterable(set(permutations(possible_rolls[i])) for i in range(len(possible_rolls))))

all_subs = list(combinations(subs_buffs,4))

subs_per_slot = {}
sub_sets = {}

for _subs in all_subs:
    for roll in possible_rolls:
        base_key = _subs[0]+str(roll[0])+"_"+_subs[1]+str(roll[1])+"_"+_subs[2]+str(roll[2])+"_"+_subs[3]+str(roll[3])
        sub_set = {key:0 for key in all_stats }
        sub_set[_subs[0]] = float(roll[0])*float(mean_subroll[_subs[0]])
        sub_set[_subs[1]] = float(roll[1])*float(mean_subroll[_subs[1]])
        sub_set[_subs[2]] = float(roll[2])*float(mean_subroll[_subs[2]])
        sub_set[_subs[3]] = float(roll[3])*float(mean_subroll[_subs[3]])
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
        
artifact_permutations = subs_per_slot