# idk what im doin
import subprocess
import json
import ijson
from modules.init_project.init_project import InitProject
from modules.read_project.read_project import ReadProject

rp = ReadProject()

rp.read("./example.json")

ip = InitProject()

ip.Init("/home/dachip/Documents/my scratch project")


    