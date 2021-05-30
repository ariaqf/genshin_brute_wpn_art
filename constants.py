all_stats = ["BATK", "BDEF", "BHP", "PYRO_DMG", "CRYO_DMG", "HYDRO_DMG", "GEO_DMG", "ELEC_DMG", "ANEMO_DMG", 
            "ELE_DMG", "PHYS_DMG", "REACT_DMG", "DMG", "HP", "ATK", "DEF", "HP%", "ATK%", "DEF%", "EM", "ER", 
            "CRATE", "CDMG", "NORM_DMG", "CHARGE_DMG", "ELE_SKILL_DMG", "BURST_DMG"]

subs_buffs = ["HP", "ATK", "DEF", "HP%", "ATK%", "DEF%", "EM", "ER", "CRATE", "CDMG"]

max_total_rolls = 9

min_subroll = {
                'HP': 209,
                'ATK': 14,
                'DEF': 16,
                'HP%': 4.1,
                'ATK%': 4.1,
                'DEF%': 5.1,
                'EM': 16,
                'ER': 4.5,
                'CRATE': 2.7,
                'CDMG': 5.4
                }

mean_subroll = {
                'HP': 254.0,
                'ATK': 16.75,
                'DEF': 19.75,
                'HP%': 4.975,
                'ATK%': 4.975,
                'DEF%': 6.2,
                'EM': 19.75,
                'ER': 5.5,
                'CRATE': 3.3,
                'CDMG': 6.6
                }

max_subroll = {
                'HP': 299,
                'ATK': 19,
                'DEF': 23,
                'HP%': 5.8,
                'ATK%': 5.8,
                'DEF%': 7.3,
                'EM': 23,
                'ER': 6.5,
                'CRATE': 3.9,
                'CDMG': 7.8
                }

artifact_slots = {
    "HEAD": ["CRATE", "CDMG", "EM", "ATK%", "HP%", "DEF%"],
    "SANDS": ["ER", "EM", "ATK%", "HP%", "DEF%"],
    "GOBLET": ["ELE_DMG", "PHYS_DMG", "ATK%", "HP%", "DEF%", "EM"],
    "FLOWER": ["HP"],
    "PLUME": ["ATK"],
}

Base_Multiplier = {
    "Burning":0.25,
    "Superconduct":0.5,
    "Swirl":0.6,
    "Electro-Charged":1.2,
    "Shattered":1.5,
    "Overloaded":2
}

artifact_main_buff = {
    "HP": 4780,
    "ATK": 311,
    "HP%": 46.6,
    "ATK%": 46.6,
    "DEF%": 46.6,
    "EM": 187,
    "ER": 51.8,
    "ELE_DMG": 46.6,
    "PHYS_DMG": 58.3,
    "CRATE": 31.1,
    "CDMG": 62.2
}