# scratch2json

A command-line tool for converting Scratch `.sb3` projects into structured JSON and compiling structured JSON back into Scratch `.sb3` format.  
Supports compatibility with [TurboWarp](https://turbowarp.org) and [PenguinMod](https://penguinmod.com).

## Features

- Convert `.sb3` projects into clean, structured folders (JSON + assets)
- Compile structured projects back to valid `.sb3` files
- Modular design, suitable for extension or automation

---
### What & Why

`scratch2json` helps you convert Scratch `.sb3` files into structured, readable folders — and back again.

This structure makes it easier to:

- Use Git for version control (track code changes, manage history)
- Collaborate with others on Scratch projects

Whether you're modding, extending, or just organizing your projects better, this tool gives you full control over how Scratch data is stored and handled.

---

## Installation

```bash
git clone https://github.com/yourname/scratch2github
cd scratch2json
pip install .
```
### For extension

Grab [one of these](https://github.com/whoschip/scratch2json/blob/main/extension/extension.js) into your project, then start the server by running: 

```bash
scratch2json server --start
```
make sure you're in the folder you want your project save to

---

## TODO

- [x] Make convert work  
- [x] Make compile work  
- [x] Write scratch2json CLI  
- [x] Learn js and make a ext to auto load & Make backend for the js ext (help needed)
- [x] All good  
