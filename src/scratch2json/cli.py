#!/usr/bin/env python3
import os
import platform
import argparse
from scratch2json.modules.tui.tui import tui
from scratch2json.modules.compile_project.compile import ReconstructProject
from scratch2json.modules.convert_project.convert_project import ConvertProject
from scratch2json.modules.backend.backend import app  

from threading import Thread

tl = tui()

def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def server_cmd(dst, start=False):
    print("🚀 starting backend server for auto-convert...")

    os.environ["SCRATCH2JSON_BACKEND_DST"] = dst

    if start:
        def run_flask():
            import flask
            from flask import Flask
            import logging
            import scratch2json.modules.backend.backend as backend
            backend.app.run(host="0.0.0.0", port=5000, debug=False)
        
        Thread(target=run_flask).start()
        print(f"✅ backend running at http://localhost:5000 — output dir: {dst}")
    else:
        print("ℹ️  --start not passed, backend server not launched")

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
• convert      : unzip .sb3 and save it as structured JSON + assets
• compile      : take structured project and rebuild a .sb3 file
• fastcompile  : rebuild using current dir as input/output
• server       : spin up Flask backend for auto converting ZIPs
• --turbowarp  : optional flag to add TurboWarp-compatible meta
• author       : dachip
• license      : MIT
• repo         : https://github.com/whoschip/scratch2github
""")

def main():
    parser = argparse.ArgumentParser(prog="scratch2json", description="scratch project CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # convert
    convert_parser = subparsers.add_parser("convert", help="convert scratch project to JSON")
    convert_parser.add_argument("src", help="path to extracted Scratch project")
    convert_parser.add_argument("dst", help="path to save converted JSON")

    # server
    server_parser = subparsers.add_parser("server", help="auto convert using a backend & ext")
    server_parser.add_argument("dst", nargs="?", default=os.getcwd(), help="where to output")
    server_parser.add_argument("--start", action="store_true", help="start the backend server")

    # compile
    compile_parser = subparsers.add_parser("compile", help="compile structured JSON to .sb3")
    compile_parser.add_argument("src", help="path to structured project")
    compile_parser.add_argument("dst", help="path to save compiled .sb3")
    compile_parser.add_argument("--turbowarp", action="store_true", help="use TurboWarp meta")

    # fastcompile
    fastcompile_parser = subparsers.add_parser("fastcompile", help="input is the current folder, output is also the current folder")
    fastcompile_parser.add_argument("--turbowarp", action="store_true", help="use TurboWarp meta")

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
            case "server":
                server_cmd(args.dst, args.start)
    except Exception as e:
        print("💔 ayo something broke:")
        print("👉", e)

if __name__ == "__main__":
    main()
