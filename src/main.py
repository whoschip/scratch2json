# idk what im doin
import subprocess
import json
import ijson
from modules.compile_project.compile import ReconstructProject
from modules.convert_project.convert_project import ConvertProject


rc = ConvertProject()

rc.convert("/home/dachip/Documents/my scratch project", "../test/Test scratch2json")

rk = ReconstructProject()

turbowarp_meta = {
    "semver": "3.0.0",
    "vm": "0.2.0",
    "agent": "",
    "platform": {
        "name": "TurboWarp",
        "url": "https://turbowarp.org/"
    }
}


rk.reconstruct(
    structured_project_path="/home/dachip/Documents/my scratch project",
    output_dir="/home/dachip/Documents/compiled",
    meta_data=turbowarp_meta
)