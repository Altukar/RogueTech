import json, copy

# writes additional lances configs for Mission Control support lances & launcher option patchdefs
# run with python3 mc_configurator
# adjust script, run script, inspect git diff for changes

path_to_missioncontrol = "../../Core/MissionControl/config/AdditionalLances/"

patchdef_template = json.loads("""{
    "version" : 1,
    "patches" : []
}""")

patch_base = json.loads("""{
    "targetFile" : "Core/MissionControl/config/AdditionalLances/Difficulty1.json",
    "priority" : 20,
    "patch" : {
        "Enemy": {
            "Max": 0,
            "ChanceToSpawn": 0.0
        }
    }
}""")

patchdef_template_kt = json.loads("""{
    "version" : 1,
    "patches" : [
        {
            "targetFile" : "Core/MissionControl/settings.json",
            "priority" : 20,
            "arrayHandle" : "Replace",
            "patch" : {
                "AdditionalLances": {
                    "Enable": true,
                    "ExcludeContractTypes": [
                        "SoloDuel",
                        "DuoDuel"
                    ],
                    "IsPrimaryObjectiveIn": [
                        "SimpleBattle",
                        "CaptureBase"
                    ]
                }
            }
        }
    ]
}""")

patch_base_kt = json.loads("""{
    "targetFile" : "Core/MissionControl/config/AdditionalLances/Difficulty1.json",
    "priority" : 20,
    "arrayHandle" : "Replace",
    "patch" : {
        "Enemy": {
            "Max": 1,
            "ChanceToSpawn": 2.0,
            "LancePool": {
                "ALL": [
                    "Mixed_Battle_KillTeams"
                ]
            }
        }
    }
}""")

patchdef_hugs = copy.deepcopy(patchdef_template)
patchdef_easy = copy.deepcopy(patchdef_template)
patchdef_kt = copy.deepcopy(patchdef_template_kt)

for diff in range(1, 50+1):

    filename = "Difficulty" + str(diff) + ".json"
    filepath = path_to_missioncontrol + filename
    diff_config = {}

    with open(filepath) as json_file:
        diff_config = json.load(json_file)

    ally_lances = []
    opfor_lances = []

    if diff < 3:
        ally_lances = ["Standard_MCSupport", "Damaged_Lightly_MCSupport", "Damaged_Heavily_MCSupport"]
        opfor_lances = ["Standard_MCSupport", "Damaged_Lightly_MCSupport", "Damaged_Heavily_MCSupport"]
    elif diff < 6:
        ally_lances = ["Standard_MCSupport", "Damaged_Lightly_MCSupport"]
        opfor_lances = ["Standard_MCSupport", "Damaged_Lightly_MCSupport"]
    elif diff < 12:
        ally_lances = ["Standard_MCSupport"]
        opfor_lances = ["Standard_MCSupport", "Standard_MCSupport_Easy", "Standard_MCSupport_Hard", "Standard_Support_NoVTOL"]
    elif diff < 18:
        ally_lances = ["Standard_MCSupport"]
        opfor_lances = ["Standard_MCSupport", "Standard_MCSupport_Easy", "Standard_MCSupport_Hard", "Standard_Support_NoVTOL", "Standard_Battle", "Standard_Battle_Mech"]
    else:
        ally_lances = ["Standard_MCSupport"]
        opfor_lances = ["Standard_MCSupport", "Standard_Support", "Standard_Battle", "Standard_Battle_Mech", "Standard_Fire"]

    diff_config["LancePool"] = {}
    diff_config["LancePool"]["ALL"] = []
    diff_config["Enemy"]["LancePool"] = {}
    diff_config["Enemy"]["LancePool"]["ALL"] = opfor_lances
    diff_config["Allies"]["LancePool"] = {}
    diff_config["Allies"]["LancePool"]["ALL"] = ally_lances

    diff_config["Enemy"]["EliteLances"] = {}
    diff_config["Allies"]["EliteLances"] = {}

    diff_config["Allies"]["Max"] = 1
    diff_config["Enemy"]["Max"] = 1 if diff < 10 else 2 

    # .5 .45 .4 .35 ... .05 .01 .01 .01
    diff_config["Allies"]["ChanceToSpawn"] = round(max(0.01, 0.5 - 0.05*(diff-1)), ndigits=2)

    if diff < 10:
        diff_config["Enemy"]["ChanceToSpawn"] = round(0.1 + 0.05*(diff-1), ndigits=2)
    else:
        diff_config["Enemy"]["ChanceToSpawn"] = round(0.25 + 0.05*(diff-10), ndigits=2)

    with open(filepath, 'w', newline='\r\n') as new_file:
        json.dump(diff_config, new_file, indent=2)

    # no support
    patch_hugs = copy.deepcopy(patch_base)
    patch_hugs["targetFile"] = "Core/MissionControl/config/AdditionalLances/" + filename
    patchdef_hugs["patches"].append(patch_hugs)
    
    # max 1 + lower chances 
    patch_easy = copy.deepcopy(patch_base)
    patch_easy["targetFile"] = "Core/MissionControl/config/AdditionalLances/" + filename
    patch_easy["patch"]["Enemy"]["Max"] = 1
    patch_easy["patch"]["Enemy"]["ChanceToSpawn"] = round(max(0.0, 0.1 + 0.05*(diff-4)), ndigits=2)
    patchdef_easy["patches"].append(patch_easy)
    
    # higher chance max 1 before KTs from 16 onwards
    if diff > 9:
        if diff > 15:
            patch_kt = copy.deepcopy(patch_base_kt)
            patch_kt["targetFile"] = "Core/MissionControl/config/AdditionalLances/" + filename
        else:
            patch_kt = copy.deepcopy(patch_base)
            patch_kt["targetFile"] = "Core/MissionControl/config/AdditionalLances/" + filename
            patch_kt["patch"]["Enemy"]["Max"] = 1
            patch_kt["patch"]["Enemy"]["ChanceToSpawn"] = round(0.1 + 0.05*(diff+3), ndigits=2)
        patchdef_kt["patches"].append(patch_kt)

with open("../../InstallOptions/SupportLances/MC-Hugs/patchdef.json", 'w', newline='\r\n') as new_file:
        json.dump(patchdef_hugs, new_file, indent=2)

with open("../../InstallOptions/SupportLances/MC-Easy/patchdef.json", 'w', newline='\r\n') as new_file:
        json.dump(patchdef_easy, new_file, indent=2)

with open("../../InstallOptions/SupportLances/MC-KillTeams/patchdef.json", 'w', newline='\r\n') as new_file:
        json.dump(patchdef_kt, new_file, indent=2)
