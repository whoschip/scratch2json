import shutil
import ijson
import json
import os
from ..tui.tui import tui 
from pathlib import Path

tl = tui()
class ConvertProject:
    def __init__(self):
        pass
    
    def convert(self, path, zip_path, clear=False):
        # init stuff
        prj_home = Path(path)
        prj_src = Path(zip_path)
        sprite_fl = prj_home / "sprites"
        extension_fl = prj_home / "extensions"
        fonts_fl = prj_home / "fonts"
        stage_dir = prj_home / "stage"
        json_file = prj_src / "project.json"
        
        # nuke
        def safe_nuke(path):
            if os.path.isdir(path):
                for item in os.listdir(path):
                    full_path = os.path.join(path, item)
                    if os.path.isfile(full_path) or os.path.islink(full_path):
                        os.remove(full_path)
                    elif os.path.isdir(full_path):
                        shutil.rmtree(full_path)
        
                
        if clear is True:
            safe_nuke(sprite_fl)
            safe_nuke(extension_fl)
            safe_nuke(stage_dir)
            safe_nuke(extension_fl)
            safe_nuke(fonts_fl)

        extension_fl.mkdir(parents=True, exist_ok=True)

        
        with open(json_file, "r") as f:
            try:
                project_data = json.load(f)
                monitors = project_data.get('monitors', [])
                targets = project_data.get('targets', [])

                if 'extensions' in project_data and 'extensionURLs' in project_data:
                    self.process_extension(prj_src, extension_fl, project_data['extensions'], project_data['extensionURLs'])
                else:
                    pass
                
                print("\n Saving monitors...")
                monitors_path = prj_home / "monitors.json"
                with open(monitors_path, 'w') as config_file:
                    json.dump(monitors, config_file, indent=4)

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
                    # Process Fonts
                    custom_fonts = project_data.get("customFonts", [])
                    if isinstance(custom_fonts, list) and custom_fonts:
                        self.process_fonts(custom_fonts, prj_src, fonts_fl)
                    
            except json.JSONDecodeError as e: 
                print(f"Error decoding project.json: {e}")
            except Exception as e:
                print(f"An unexpected error occurred during conversion: {e}")


    def process_stage(self, target, prj_src, prj_home):
        print(f"Processing Stage...")

        # region create meta data
        stage_dir = prj_home / "stage"
        stage_dir.mkdir(parents=True, exist_ok=True)

        # Collect stage metadata into a single dictionary
        stage_meta_info = {}
        if 'id' in target:
            stage_meta_info["id"] = target["id"]
        if "comments" in target:
            stage_meta_info["comments"] = target["comments"]
        if "currentCostume" in target:
            stage_meta_info["currentCostume"] = target["currentCostume"]
        if "variables" in target:
            stage_meta_info["variables"] = target["variables"]
        if "lists" in target:
            stage_meta_info["lists"] = target["lists"]
        if "broadcasts" in target:
            stage_meta_info["broadcasts"] = target["broadcasts"]
        if "customVars" in target:
            stage_meta_info["customVars"] = target["customVars"]
        if "volume" in target:
            stage_meta_info["volume"] = target["volume"]
        if "layerOrder" in target:
            stage_meta_info["layerOrder"] = target["layerOrder"]
        if "tempo" in target:
            stage_meta_info["tempo"] = target["tempo"]
        if "videoTransparency" in target:
            stage_meta_info["videoTransparency"] = target["videoTransparency"]
        if "videoState" in target:
            stage_meta_info["videoState"] = target["videoState"]
        if "textToSpeechLanguage" in target:
            stage_meta_info["textToSpeechLanguage"] = target["textToSpeechLanguage"]
        if "extensionData" in target:
            stage_meta_info["extensionData"] = target["extensionData"]
        
        if stage_meta_info: 
            stage_meta_file = stage_dir / "stage_meta.json"
            with open(stage_meta_file, 'w') as f:
                json.dump(stage_meta_info, f, indent=4)
            print(f"Stage metadata written to {stage_meta_file}")

        # region end
            
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
            scripts = prj_home / "stage" 
            scripts.mkdir(parents=True, exist_ok=True)
            script_name = scripts / "script.json"
            with open(script_name, 'w') as script:
                blocks_str = json.dumps(target["blocks"], indent=4)
                script.write(blocks_str)

    def process_sprite(self, target, prj_src, sprite_fl):
        raw_sprite_name = target['name']
        sprite_name = raw_sprite_name.replace("/", "_")  
        sprite = sprite_fl / sprite_name
        sprite.mkdir(parents=True, exist_ok=True)
        print(f"Processing Sprites : {sprite_name}")

        # region create metadata
        sprite_meta_info = {}
        if "id" in target:
            sprite_meta_info["id"] = target['id']
        if "comments" in target:
            sprite_meta_info["comments"] = target["comments"]
        if "currentCostume" in target:
            sprite_meta_info["currentCostume"] = target["currentCostume"]
        if "variables" in target:
            sprite_meta_info["variables"] = target["variables"]
        if "lists" in target:
            sprite_meta_info["lists"] = target["lists"]
        if "broadcasts" in target:
            sprite_meta_info["broadcasts"] = target["broadcasts"]
        if "customVars" in target:
            sprite_meta_info["customVars"] = target["customVars"]
        if "volume" in target:
            sprite_meta_info["volume"] = target["volume"]
        if "layerOrder" in target:
            sprite_meta_info["layerOrder"] = target["layerOrder"]
        if "visible" in target:
            sprite_meta_info["visible"] = target["visible"]
        if "x" in target:
            sprite_meta_info["x"] = target["x"]
        if "y" in target:
            sprite_meta_info["y"] = target["y"]
        if "size" in target:
            sprite_meta_info["size"] = target["size"]
        if "direction" in target:
            sprite_meta_info["direction"] = target["direction"]
        if "draggable" in target:
            sprite_meta_info["draggable"] = target["draggable"]
        if "rotationStyle" in target:
            sprite_meta_info["rotationStyle"] = target["rotationStyle"]
        if "extensionData" in target:
            sprite_meta_info["extensionData"] = target["extensionData"]


        if sprite_meta_info: 
            sprite_meta_file_path = sprite / "sprite_meta.json" 
            with open(sprite_meta_file_path, 'w') as f:
                json.dump(sprite_meta_info, f, indent=4)
            print(f"Sprite metadata written to {sprite_meta_file_path}")

        # region end

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
            scripts = sprite
            scripts.mkdir(parents=True, exist_ok=True)
            script_name = scripts / "script.json"
            with open(script_name, 'w') as script:
                blocks_str = json.dumps(target["blocks"], indent=4)
                script.write(blocks_str)
                
    def process_extension(self, prj_src, extension_fl, extensions_list, extension_urls_dict):
        extension_data = {}
        extension_extra_data = {}

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

        project_json_path = prj_src / "project.json"
        if project_json_path.exists():
            try:
                with open(project_json_path, "r") as f:
                    raw = json.load(f)
                    if "extensionData" in raw:
                        extension_extra_data = raw["extensionData"]
                        ext_data_file = extension_fl / "extension_data.json"
                        with open(ext_data_file, "w") as f2:
                            json.dump(extension_extra_data, f2, indent=4)
                        print(f"\nextensionData saved to {ext_data_file}")
            except Exception as e:
                print(f"Error extracting extensionData: {e}")
    
    def process_fonts(self, custom_fonts, prj_src, fonts_fl):
        print("\nProcessing fonts...")
        fonts_fl.mkdir(parents=True, exist_ok=True)
        config = []

        for font in custom_fonts:
            config.append(font)
            if "md5ext" in font:
                font_file = font["md5ext"]
                font_src = prj_src / font_file
                if font_src.exists():
                    shutil.copy(font_src, fonts_fl)
                    print(f"Copied font file: {font_file}")
                else:
                    print(f"Font file not found: {font_file}")

        config_path = fonts_fl / "config.json"
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
        print(f"\nSaved font config to: {config_path}")