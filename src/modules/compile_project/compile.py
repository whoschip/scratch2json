import shutil
import json
from pathlib import Path
import uuid

from modules.tui.tui import tui
tl = tui()

class ReconstructProject:
    def __init__(self):
        pass

    def reconstruct(self, structured_project_path, output_dir, meta_data=None):
        tl.info()
        prj_home = Path(structured_project_path)
        output_zip_content = Path(output_dir)
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
            "meta": meta_data if meta_data is not None else default_meta 
        }

        self._reconstruct_extensions(prj_home, project_data)
        self._reconstruct_stage(prj_home, output_zip_content, project_data)
        self._reconstruct_sprites(prj_home, output_zip_content, project_data)

        with open(output_zip_content / "project.json", "w") as f:
            json.dump(project_data, f, indent=4)

    def _reconstruct_extensions(self, prj_home, project_data):
        extension_file = prj_home / "extensions" / "extensions.json"
        if extension_file.exists():
            with open(extension_file, "r") as f:
                extensions_info = json.load(f)
                project_data['extensions'] = list(extensions_info.keys())
                project_data['extensionURLs'] = extensions_info

    def _reconstruct_stage(self, prj_home, output_zip_content, project_data):
        stage_dir = prj_home / "stage"
        if not stage_dir.exists():
            return

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
            "id": str(uuid.uuid4().hex),
            "volume": 100,
            "layerOrder": 0,
            "tempo": 60,
            "videoTransparency": 50,
            "videoState": "on",
            "textToSpeechLanguage": None,
            "extensionData": {}
        }

        sounds_config_path = stage_dir / "sounds" / "config.json"
        if sounds_config_path.exists():
            with open(sounds_config_path, "r") as f:
                sounds_data = json.load(f)
                stage_target['sounds'] = sounds_data
                for sound in sounds_data:
                    if "md5ext" in sound:
                        src_path = stage_dir / "sounds" / sound["md5ext"]
                        if src_path.exists():
                            shutil.copy(src_path, output_zip_content / sound["md5ext"])

        costumes_config_path = stage_dir / "config.json"
        if costumes_config_path.exists():
            with open(costumes_config_path, "r") as f:
                costumes_data = json.load(f)
                stage_target['costumes'] = costumes_data
                for costume in costumes_data:
                    if "md5ext" in costume:
                        src_path = stage_dir / costume["md5ext"]
                        if src_path.exists():
                            shutil.copy(src_path, output_zip_content / costume["md5ext"])

        blocks_script_path = stage_dir / "scripts" / "script.json"
        if blocks_script_path.exists():
            with open(blocks_script_path, "r") as f:
                stage_target['blocks'] = json.load(f)

        project_data['targets'].append(stage_target)

    def _reconstruct_sprites(self, prj_home, output_zip_content, project_data):
        sprites_dir = prj_home / "sprites"
        if not sprites_dir.exists():
            return

        for sprite_path in sprites_dir.iterdir():
            if sprite_path.is_dir():
                sprite_name = sprite_path.name
                sprite_target = {
                    "isStage": False,
                    "name": sprite_name,
                    "variables": {},
                    "lists": {},
                    "broadcasts": {},
                    "customVars": [],
                    "blocks": {},
                    "comments": {},
                    "currentCostume": 0,
                    "costumes": [],
                    "sounds": [],
                    "id": str(uuid.uuid4().hex),
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

                sounds_config_path = sprite_path / "sounds" / "config.json"
                if sounds_config_path.exists():
                    with open(sounds_config_path, "r") as f:
                        sounds_data = json.load(f)
                        sprite_target['sounds'] = sounds_data
                        for sound in sounds_data:
                            if "md5ext" in sound:
                                src_path = sprite_path / "sounds" / sound["md5ext"]
                                if src_path.exists():
                                    shutil.copy(src_path, output_zip_content / sound["md5ext"])

                costumes_config_path = sprite_path / "costumes" / "config.json"
                if costumes_config_path.exists():
                    with open(costumes_config_path, "r") as f:
                        costumes_data = json.load(f)
                        sprite_target['costumes'] = costumes_data
                        for costume in costumes_data:
                            if "md5ext" in costume:
                                src_path = sprite_path / "costumes" / costume["md5ext"]
                                if src_path.exists():
                                    shutil.copy(src_path, output_zip_content / costume["md5ext"])

                blocks_script_path = sprite_path / "scripts" / "script.json"
                if blocks_script_path.exists():
                    with open(blocks_script_path, "r") as f:
                        sprite_target['blocks'] = json.load(f)

                project_data['targets'].append(sprite_target)
