import os
import json
import traceback
from SCOFunctions.S2Parser import s2_parse_replay


AllReplays = set()
for root, directories, files in os.walk(r'C:\Users\Maguro\Documents\StarCraft II\Accounts'):
    for file in files:
        if file.endswith('.SC2Replay'):
            file_path = os.path.join(root,file)
            if len(file_path) > 255:
                file_path = '\\\?\\' + file_path
            file_path = file_path = os.path.normpath(file_path)
            if not '[MM]' in file_path:
                AllReplays.add(file_path)


level_data = list()

for r in AllReplays:
    try:
        rep = s2_parse_replay(r, try_lastest=True, parse_events=False, onlyBlizzard=True, withoutRecoverEnabled=True, return_raw=False)
        if rep == None:
            continue

        for p in (1,2):
            handle = rep['players'][p]['handle']
            level = rep['players'][p]['commander_mastery_level']
            name = rep['players'][p]['name']
            date = rep['date']

            if name in ('Maguro','BigMaguro','SeaMaguro','Ziemson','Ancalagon','Potato') or handle[:3] == '98-':
                continue

            level_data.append((handle, name, level, date))

    except:
        print(traceback.format_exc())



with open('player_levels.json','w') as f:
    json.dump(level_data, f, indent=3)
