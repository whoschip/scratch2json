// Name: Scratch2Json
// ID: S2J
// Description: Scratch to json made easier with ts
// By: Chip

class ChipS2J {
    constructor(runtime) {
        this.runtime = runtime;
    }

    getInfo() {
        return {
            id: "SJ2",
            name: "Scratch2Json",
            blocks: [
                {
                    opcode: "exportPMP",
                    blockType: Scratch.BlockType.COMMAND,
                    text: "export project as .pmp"
                }
            ]
        };
    }

    async exportPMP() {
        // Access sb3 serializer from global
        const sb3 = window.PenguinMod?.sb3 || window.TurboWarp?.sb3;
        const JSZip = window.JSZip;
        if (!sb3 || !JSZip) {
            alert("sb3 serializer or JSZip is missing!");
            return;
        }

        // 1. Serialize project
        const projectJson = sb3.serialize(this.runtime);
        const zip = new JSZip();
        zip.file("project.json", JSON.stringify(projectJson));

        // 2. Add assets (costumes and sounds)
        const storage = this.runtime.storage;
        const costumesAdded = new Set();
        const soundsAdded = new Set();

        for (const target of projectJson.targets) {
            for (const costume of target.costumes) {
                if (!costume.md5ext || costumesAdded.has(costume.md5ext)) continue;
                costumesAdded.add(costume.md5ext);
                try {
                    const asset = await storage.load(
                        storage.AssetType.ImageBitmap,
                        costume.assetId,
                        costume.dataFormat
                    );
                    zip.file(costume.md5ext, asset.data);
                } catch (e) {}
            }
            for (const sound of target.sounds) {
                if (!sound.md5ext || soundsAdded.has(sound.md5ext)) continue;
                soundsAdded.add(sound.md5ext);
                try {
                    const asset = await storage.load(
                        storage.AssetType.Sound,
                        sound.assetId,
                        sound.dataFormat
                    );
                    zip.file(sound.md5ext, asset.data);
                } catch (e) {}
            }
        }

        // 3. Trigger file download
        zip.generateAsync({ type: "blob" }).then(blob => {
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "project.pmp";
            document.body.appendChild(a);
            a.click();
            setTimeout(() => {
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            }, 100);
        });
    }
}

Scratch.extensions.register(new ExportProjectExtension(Scratch.vm.runtime));