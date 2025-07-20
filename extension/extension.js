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
        const vm = this.runtime?.vm || window.vm;
        if (!vm) {
            alert('VM instance not found! Are you in PenguinMod or TurboWarp?');
            return;
        }

        try {
            const blob = await vm.saveProjectSb3('blob');
            const formData = new FormData();
            formData.append("file", blob, "project.pmp");
            const res = await fetch("http://localhost:5000/api/upload", {
                method: "POST",
                body: formData
            });
            const result = await res.json();
            if (res.ok) {
                alert("Uploaded successfully: " + (result.msg || "Success"));
            } else {
                alert(" Upload failed: " + (result.error || "unknown error"));
            }
        } catch (err) {
            alert(" Error posting to backend: " + (err.message || err));
        }
    }
}

Scratch.extensions.register(new ChipS2J(Scratch.vm.runtime));
