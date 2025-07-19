#!/usr/bin/env python3
import os
import platform
import argparse
from .modules.tui.tui import tui
from scratch2json.modules.compile_project.compile import ReconstructProject
from scratch2json.modules.convert_project.convert_project  import ConvertProject

tl = tui()

def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def convert_cmd(src, dst):
    if not src or not dst:
        print("🛑 missing paths 😭")
        return
    rc = ConvertProject()
    rc.convert(dst, src)
    print("✅ converted successfully!\n")

def compile_cmd(src, dst, turbowarp=False):
    if not src or not dst:
        print("🛑 missing paths 😭")
        return

    rk = ReconstructProject()

    if turbowarp:
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
            structured_project_path=src,
            output_dir=dst,
            meta_data=turbowarp_meta
        )
        print("✅ compiled w/ TurboWarp meta 🌀")
    else:
        rk.reconstruct(
            structured_project_path=src,
            output_dir=dst
        )
        print("✅ compiled w/o TurboWarp meta")

def fastcompile_cmd(turbowarp=False):
    src = os.getcwd()
    dst = os.getcwd()

    rk = ReconstructProject()

    if turbowarp:
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
            structured_project_path=src,
            output_dir=dst,
            meta_data=turbowarp_meta
        )
        print("✅ compiled w/ TurboWarp meta 🌀")
    else:
        rk.reconstruct(
            structured_project_path=src,
            output_dir=dst
        )
        print("✅ compiled w/o TurboWarp meta")

def about_cmd():
    print("""
scratch2json — CLI for converting and compiling Scratch projects
---------------------------------------------------------------
• convert  : unzip .sb3 and save it as structured JSON + assets
• compile  : take structured project and rebuild a .sb3 file
• --turbowarp : optional flag to add TurboWarp-compatible meta
• author   : dachip
• license  : MIT
• repo     : https://github.com/yourname/scratch2github
""")

def main():
    parser = argparse.ArgumentParser(prog="scratch2json", description="scratch project CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # convert
    convert_parser = subparsers.add_parser("convert", help="convert scratch project to JSON")
    convert_parser.add_argument("src", help="path to extracted Scratch project")
    convert_parser.add_argument("dst", help="path to save converted JSON")

    # compile
    fastcompile_parser = subparsers.add_parser("fastcompile", help="input is the current folder, ouput is also the current folder")
    fastcompile_parser.add_argument("--turbowarp", action="store_true", help="use TurboWarp meta")

    compile_parser = subparsers.add_parser("compile", help="compile structured JSON to .sb3")
    compile_parser.add_argument("src", help="path to structured project")
    compile_parser.add_argument("dst", help="path to save compiled .sb3")
    compile_parser.add_argument("--turbowarp", action="store_true", help="use TurboWarp meta")

    # about
    subparsers.add_parser("about", help="show info about this CLI tool")

    args = parser.parse_args()

    try:
        clear()
        tl.info()
        match args.command:
            case "convert":
                convert_cmd(args.src, args.dst)
            case "compile":
                compile_cmd(args.src, args.dst, args.turbowarp)
            case "fastcompile":
                fastcompile_cmd(args.turbowarp)
            case "about":
                about_cmd()
    except Exception as e:
        print("💔 ayo something broke:")
        print("👉", e)

if __name__ == "__main__":
    main()
