import shutil
import json
from pathlib import Path
import uuid
from ..tui.tui import tui 

tl = tui()

class ReconstructProject:
    def __init__(self):
        pass

    def reconstruct(self, structured_project_path, output_dir, meta_data=None):
        print("Starting project reconstruction...")
        prj_home = Path(structured_project_path)
        output_zip_content = prj_home / "builddir"
        output_zip_content.mkdir(parents=True, exist_ok=True)

        default_meta = {
            "semver": "3.0.0",
            "vm": "0.2.0",
            "agent": "",
            "platform": {
                "name": "PenguinMod",
                "url": "https://penguinmod.com/",
                "version": "stable"
            }
        }

        project_data = {
            "targets": [],
            "monitors": [],
            "extensionData": {},
            "extensions": [],
            "extensionURLs": {},
            "customFonts" : {},
            "meta": meta_data if meta_data is not None else default_meta
        }

        self._reconstruct_extensions(prj_home, project_data)
        self._reconstruct_monitors(prj_home, project_data)
        self._reconstruct_stage(prj_home, output_zip_content, project_data)
        self._reconstruct_sprites(prj_home, output_zip_content, project_data)
        self._reconstruct_fonts(prj_home, output_zip_content, project_data)

        print("\nWriting project.json...")
        with open(output_zip_content / "project.json", "w", encoding="utf-8") as f:
            json.dump(project_data, f, indent=4, ensure_ascii=False)
        
        print("Compressing to zip...")
        shutil.make_archive(output_dir, 'zip', output_zip_content)

        print("Project reconstruction complete!")
    
    def _reconstruct_fonts(self, prj_home, output_zip_content, project_data):
        print("\nReconstructing font...")
        fonts_dir = prj_home / "fonts"
        fonts_config = fonts_dir / "config.json"

        if not fonts_dir.exists():
            print("\nFont folder not exist, skipping...")
            return

        if not fonts_config.exists():
            print("\nFont config.json not found, skipping...")
            return

        with open(fonts_config, 'r', encoding="utf-8") as f:
            font_info = json.load(f)
            project_data["customFonts"] = font_info

            for font in font_info:
                if "md5ext" in font:
                    font_file = font["md5ext"]
                    src = fonts_dir / font_file
                    dst = output_zip_content / font_file
                    if src.exists():
                        shutil.copy(src, dst)
                        print(f"Copied font file: {font_file}")
                    else:
                        print(f"Missing font file: {font_file}")
        
    def _reconstruct_extensions(self, prj_home, project_data):
        print("Reconstructing extensions...")
        extension_file = prj_home / "extensions" / "extensions.json"
        extension_data_file = prj_home / "extensions" / "extension_data.json"

        project_data['extensions'] = []
        project_data['extensionURLs'] = {}

        if extension_file.exists():
            with open(extension_file, "r", encoding="utf-8") as f:
                extensions_info = json.load(f)
                clean_urls = {}

                for ext_id, url in extensions_info.items():
                    project_data['extensions'].append(ext_id)
                    if isinstance(url, str) and url.startswith("http"):
                        clean_urls[ext_id] = url

                project_data['extensionURLs'] = clean_urls
                print(f"Loaded extensions: {list(extensions_info.keys())}")
                print(f"Filtered URLs: {list(clean_urls.keys())}")

        if extension_data_file.exists():
            with open(extension_data_file, "r", encoding="utf-8") as f:
                extension_data = json.load(f)
                project_data["extensionData"] = extension_data
                print("Loaded extension data")

    def _reconstruct_monitors(self, prj_home, project_data):
        print("\nReconstructing monitors...")
        monitors_path = prj_home / "monitors.json"
        if monitors_path.exists():
            with open(monitors_path, "r", encoding="utf-8") as f:
                project_data["monitors"] = json.load(f)
                print("Monitors loaded")

    def _reconstruct_stage(self, prj_home, output_zip_content, project_data):
        stage_dir = prj_home / "stage"
        if not stage_dir.exists():
            print("\nStage directory not found, skipping...")
            return

        print("\n Reconstructing stage...")
        stage_target = {
            "isStage": True,
            "name": "Stage",
            "variables": {},
            "lists": {},
            "broadcasts": {},
            "customVars": [],
            "blocks": {},
            "comments": {},
            "currentCostume": 0,
            "costumes": [],
            "sounds": [],
            "id": str(uuid.uuid4()),
            "volume": 100,
            "layerOrder": 0,
            "tempo": 60,
            "videoTransparency": 50,
            "videoState": "on",
            "textToSpeechLanguage": None,
            "extensionData": {}
        }

        meta_file = stage_dir / "stage_meta.json"
        if meta_file.exists():
            with open(meta_file, "r", encoding="utf-8") as f:
                stage_target.update(json.load(f))
                print("Stage metadata loaded")

        self._load_media(stage_dir, "sounds", output_zip_content, stage_target, "sounds")
        self._load_media(stage_dir, "", output_zip_content, stage_target, "costumes")
        self._load_script(stage_dir, "script.json", stage_target, "blocks")

        project_data["targets"].append(stage_target)
        print("\nStage reconstructed")

    def _reconstruct_sprites(self, prj_home, output_zip_content, project_data):
        sprites_dir = prj_home / "sprites"
        if not sprites_dir.exists():
            print("No sprites folder found, skipping...")
            return

        print("\nReconstructing sprites...")
        for sprite_dir in sprites_dir.iterdir():
            if not sprite_dir.is_dir():
                continue

            sprite_target = {
                "isStage": False,
                "name": sprite_dir.name.replace("_", "/"),
                "variables": {},
                "lists": {},
                "broadcasts": {},
                "customVars": [],
                "blocks": {},
                "comments": {},
                "currentCostume": 0,
                "costumes": [],
                "sounds": [],
                "id": str(uuid.uuid4()),
                "volume": 100,
                "layerOrder": 1,
                "visible": True,
                "x": 0,
                "y": 0,
                "size": 100,
                "direction": 90,
                "draggable": False,
                "rotationStyle": "all around",
                "extensionData": {}
            }
            meta_file = sprite_dir / "sprite_meta.json"
            if meta_file.exists():
                with open(meta_file, "r", encoding="utf-8") as f:
                    sprite_target.update(json.load(f))
                    print(f"\nSprite meta loaded for {sprite_dir.name.replace("_", "/")}")

            self._load_media(sprite_dir, "sounds", output_zip_content, sprite_target, "sounds")
            self._load_media(sprite_dir, "costumes", output_zip_content, sprite_target, "costumes")
            self._load_script(sprite_dir, "script.json", sprite_target, "blocks")

            project_data["targets"].append(sprite_target)
            print(f"Sprite '{sprite_dir.name.replace("_", "/")}' reconstructed")

    def _load_media(self, base_path, subfolder, output_path, target_obj, key):
        config_path = base_path / subfolder / "config.json" if subfolder else base_path / "config.json"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                target_obj[key] = data
                for item in data:
                    if "md5ext" in item:
                        file_path = base_path / subfolder / item["md5ext"] if subfolder else base_path / item["md5ext"]
                        if file_path.exists():
                            shutil.copy(file_path, output_path / item["md5ext"])
                            print(f"Copied {item['md5ext']}")

    def _load_script(self, base_path, file_name, target_obj, key):
        script_path = base_path / file_name
        if script_path.exists():
            with open(script_path, "r", encoding="utf-8") as f:
                target_obj[key] = json.load(f)
                print(f"Loaded {file_name}")
