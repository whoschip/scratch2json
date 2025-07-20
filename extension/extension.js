// Name: Scratch2Json
// ID: S2J
// Description: Scratch to json made easier with ts
// By: Chip
// License MIT prob

class ChipS2J {
    constructor(runtime) {
        this.runtime = runtime;
        this.saveTimeout = null;

        this.runtime.on("PROJECT_CHANGED", () => {
            this.scheduleSave();
        });
    }

    getInfo() {
        return {
            id: "S2J",
            name: "Scratch2Json",
            blocks: [] // No blocks needed
        };
    }

    scheduleSave() {
        if (this.saveTimeout) {
            clearTimeout(this.saveTimeout);
        }
        this.saveTimeout = setTimeout(() => {
            this.exportPMP();
        }, 10000);
    }

    async exportPMP() {
        const vm = this.runtime?.vm || window.vm;
        if (!vm) {
            console.warn('VM instance not found! Are you in PenguinMod or TurboWarp?');
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
                console.log("Uploaded successfully: " + (result.msg || "Success"));
            } else {
                console.warn("Upload failed: " + (result.error || "unknown error"));
            }
        } catch (err) {
            console.error("Error posting to backend: " + (err.message || err));
        }
    }
}

Scratch.extensions.register(new ChipS2J(Scratch.vm.runtime));
