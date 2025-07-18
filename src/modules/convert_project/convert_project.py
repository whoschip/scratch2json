import shutil
import ijson
import json
from modules.tui.tui import tui
from pathlib import Path

tl = tui()
class ConvertProject:
    def __init__(self):
        pass
    
    def convert(self, path, zip_path):
        tl.info()
        prj_home = Path(path)
        prj_src = Path(zip_path)
        sprite_fl = prj_home / "sprites"
        extension_fl = prj_home / "extensions"

        json_file = prj_src / "project.json"
        
        extension_fl.mkdir(parents=True, exist_ok=True)

        with open(json_file, "r") as f:
            try:
                project_data = json.load(f)
                targets = project_data.get('targets', [])

                if 'extensions' in project_data and 'extensionURLs' in project_data:
                    self.process_extension(prj_src, extension_fl, project_data['extensions'], project_data['extensionURLs'])
                else:
                    pass

                stage_processed = False
                
                for target_index, target in enumerate(targets):
                    print(f"\nProcessing target {target_index}:")
                    if 'extensions' in target and 'extensionURLs' in target:
                        self.process_extension(prj_src, extension_fl, target['extensions'], target['extensionURLs'])
                    else:
                        pass

                    # Process Stage
                    if 'isStage' in target and target['isStage'] and not stage_processed:
                        self.process_stage(target, prj_src, prj_home)
                        stage_processed = True
                    
                    # Process Sprites
                    elif 'name' in target:
                        self.process_sprite(target, prj_src, sprite_fl)
            except json.JSONDecodeError as e: 
                print(f"Error decoding project.json: {e}")
            except Exception as e:
                print(f"An unexpected error occurred during conversion: {e}")


    def process_stage(self, target, prj_src, prj_home):
        print(f"Processing Stage...")

        if "variables" in target:
            variables = prj_home / "stage" / "global_variables"
            variables.mkdir(parents=True, exist_ok=True)
            variables_name = variables / "variables.json"
            with open(variables_name, "w") as config_file:
                json.dump(target["variables"], config_file, indent=4)
            
        if 'sounds' in target:
            sounds = prj_home / "stage" / "sounds"
            sounds.mkdir(parents=True, exist_ok=True)
            sounds_name = sounds / "config.json"
            with open(sounds_name, "w") as config_file:
                json.dump(target["sounds"], config_file, indent=4)

            for sound in target["sounds"]:
                sound_name = sound["assetId"]
                sound_format = sound["md5ext"]
                sound_path = prj_src / f"{sound_format}"
                if sound_path.exists():
                    shutil.copy(sound_path, sounds)  
        
        if 'costumes' in target:
            costumes = prj_home / "stage" 
            costumes.mkdir(parents=True, exist_ok=True)
            costumes_name = costumes / "config.json"
            with open(costumes_name, "w") as config_file:
                json.dump(target["costumes"], config_file, indent=4)

            for costume in target["costumes"]:
                costume_name = costume["assetId"]
                costume_format = costume["md5ext"]
                costume_path = prj_src / f"{costume_format}"
                if costume_path.exists():
                    shutil.copy(costume_path, costumes) 

        if 'blocks' in target:
            scripts = prj_home / "stage" / "scripts"
            scripts.mkdir(parents=True, exist_ok=True)
            script_name = scripts / "script.json"
            with open(script_name, 'w') as script:
                blocks_str = json.dumps(target["blocks"], indent=4)
                script.write(blocks_str)

    def process_sprite(self, target, prj_src, sprite_fl):
        sprite_name = target['name']
        sprite = sprite_fl / sprite_name
        sprite.mkdir(parents=True, exist_ok=True)
        print(f"Processing Sprites : {sprite_name}")

        if 'sounds' in target:
            sounds = sprite / "sounds"
            sounds.mkdir(parents=True, exist_ok=True)
            sounds_name = sounds / "config.json"
            with open(sounds_name, "w") as config_file:
                json.dump(target["sounds"], config_file, indent=4)

            for sound in target["sounds"]:
                sound_name = sound["assetId"]
                sound_format = sound["md5ext"]
                sound_path = prj_src / f"{sound_format}"
                if sound_path.exists():
                    shutil.copy(sound_path, sounds)  
        
        if 'costumes' in target:
            costumes = sprite / "costumes"
            costumes.mkdir(parents=True, exist_ok=True)
            costumes_name = costumes / "config.json"
            with open(costumes_name, "w") as config_file:
                json.dump(target["costumes"], config_file, indent=4)

            for costume in target["costumes"]:
                costume_name = costume["assetId"]
                costume_format = costume["md5ext"]
                costume_path = prj_src / f"{costume_format}"
                if costume_path.exists():
                    shutil.copy(costume_path, costumes)  

        if 'blocks' in target:
            scripts = sprite / "scripts"
            scripts.mkdir(parents=True, exist_ok=True)
            script_name = scripts / "script.json"
            with open(script_name, 'w') as script:
                blocks_str = json.dumps(target["blocks"], indent=4)
                script.write(blocks_str)
            
    def process_extension(self, prj_src, extension_fl, extensions_list, extension_urls_dict):
        extension_data = {}

        if not isinstance(extensions_list, list):
            print(f"Error: 'extensions' data is not a list. Type found: {type(extensions_list)}")
            return
        
        if not isinstance(extension_urls_dict, dict):
            print(f"Error: 'extensionURLs' data is not a dictionary. Type found: {type(extension_urls_dict)}")
            return

        for ext in extensions_list:
            print(f"Processing Extension: '{ext}'")
            
            if ext in extension_urls_dict:
                extension_data[ext] = extension_urls_dict[ext]
            else:
                extension_data[ext] = "URL not available in extensionURLs"

        extension_file = extension_fl / "extensions.json"
        try:
            with open(extension_file, "w") as f:
                json.dump(extension_data, f, indent=4)
        except Exception as e:
            print(f"Error writing extensions.json to file: {e}")
