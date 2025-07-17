import subprocess
from pathlib import Path

class InitProject:
    def __init__(self):
        pass
    def Init(self, path):
        prj_src = Path(path)

        print("Init a project")
        
        sprite = prj_src / "sprites"
        try :
            sprite.mkdir()
        except FileExistsError :
            print("sprite folder exist, skipping...")
        
        sounds = prj_src / "sounds"
        try :
            sounds.mkdir()
        except FileExistsError:
            print("Sounds folder exist, skipping...")
        