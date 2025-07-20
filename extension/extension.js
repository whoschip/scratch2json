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
            id: "S2J",
            name: "Scratch2Json",
            blocks: [
                {
                    opcode: "exportPMP",
                    blockType: Scratch.BlockType.COMMAND,
                    text: "export project as .pmp and upload"
                }
            ]
        };
    }

    async exportPMP() {
        // Try to get the sb3 serializer and JSZip from the environment
        const sb3 = window.PenguinMod?.sb3 || window.TurboWarp?.sb3;
        const JSZip = window.JSZip;
        if (!sb3 || !JSZip) {
            alert("sb3 serializer or JSZip is missing! Make sure you're in PenguinMod or TurboWarp.");
            return;
        }

        // Serialize the project
        const projectJson = sb3.serialize(this.runtime);
        const zip = new JSZip();
        zip.file("project.json", JSON.stringify(projectJson));

        // Add assets (costumes and sounds), avoiding duplicates
        const storage = this.runtime.storage;
        const costumesAdded = new Set();
        const soundsAdded = new Set();

        for (const target of projectJson.targets) {
            for (const costume of target.costumes || []) {
                if (!costume.md5ext || costumesAdded.has(costume.md5ext)) continue;
                costumesAdded.add(costume.md5ext);
                try {
                    const asset = await storage.load(
                        storage.AssetType.ImageBitmap,
                        costume.assetId,
                        costume.dataFormat
                    );
                    zip.file(costume.md5ext, asset.data);
                } catch (e) {
                    // Could not load asset, skip
                }
            }
            for (const sound of target.sounds || []) {
                if (!sound.md5ext || soundsAdded.has(sound.md5ext)) continue;
                soundsAdded.add(sound.md5ext);
                try {
                    const asset = await storage.load(
                        storage.AssetType.Sound,
                        sound.assetId,
                        sound.dataFormat
                    );
                    zip.file(sound.md5ext, asset.data);
                } catch (e) {
                    // Could not load sound, skip
                }
            }
        }

        try {
            const blob = await zip.generateAsync({ type: "blob" });
            const formData = new FormData();
            formData.append("file", blob, "project.pmp");

            const res = await fetch("http://localhost:5000/api/upload", {
                method: "POST",
                body: formData
            });

            const result = await res.json();
            if (res.ok) {
                alert("✅ Uploaded successfully: " + (result.msg || "Success"));
            } else {
                alert("❌ Upload failed: " + (result.error || "unknown error"));
            }
        } catch (err) {
            alert("💥 Error posting to backend: " + (err.message || err));
        }
    }
}

Scratch.extensions.register(new ChipS2J(Scratch.vm.runtime));