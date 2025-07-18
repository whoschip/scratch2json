import os
import platform
import subprocess
import json
import ijson
from modules.tui.tui import tui
from modules.compile_project.compile import ReconstructProject
from modules.convert_project.convert_project import ConvertProject

tl = tui()

def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def main():
    try:
        clear()
        tl.info()
        print("===== MENU =====")
        print("[1] Convert a scratch project to json")
        print("[2] Compile a json project to scratch")
        print("[3] Exit")
        print("===== END =====")

        pick = input("\nPick: ").strip()

        match pick:
            case "1":
                prj_src = input("\nExtracted Scratch project folder path: ").strip()
                prj_path = input("Where to save converted JSON: ").strip()

                if not prj_src or not prj_path:
                    print("🛑 pmo bro u left something empty 😭")
                    return

                rc = ConvertProject()
                rc.convert(prj_path, prj_src)
                print("✅ converted successfully!\n")

            case "2":
                prj_src = input("\nPath to structured scratch2json folder: ").strip()
                prj_savepath = input("Where to save compiled .sb3: ").strip()
                turbowarp = input("Use TurboWarp meta? [Y/N]: ").strip().upper()

                if not prj_src or not prj_savepath:
                    print("🛑 twin… u gotta enter the paths 😭")
                    return

                rk = ReconstructProject()

                match turbowarp:
                    case "Y":
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
                            structured_project_path=prj_src,
                            output_dir=prj_savepath,
                            meta_data=turbowarp_meta
                        )
                        print("✅ compiled w/ TurboWarp meta 🌀")

                    case "N":
                        rk.reconstruct(
                            structured_project_path=prj_src,
                            output_dir=prj_savepath,
                        )
                        print("✅ compiled w/o TurboWarp meta")

                    case _:
                        print("🛑 that wasn’t Y or N twin 😭")

            case "3":
                print("👋 bye twin")
                exit()

            case _:
                print("❓ idk what u picked fr 😭 try 1, 2, or 3")

    except Exception as e:
        print("💔 ayo something broke:")
        print("👉", e)

if __name__ == "__main__":
    while True:
        main()
        input("\npress enter to continue twin...")  # wait before restarting
