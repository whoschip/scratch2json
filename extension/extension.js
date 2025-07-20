// Name: Scratch2Json
// ID: S2J
// Description: Scratch to json made easier with ts
// By: Chip
// License: MIT prob

const IconURI = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjYiIGhlaWdodD0iNjIiIHZpZXdCb3g9IjAgMCA2NiA2MiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZmlsbC1ydWxlPSJldmVub2RkIiBjbGlwLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik00MS45NjYgMC4wOTk5OTkyQzQyLjI2NiAtMC4xMDAwMDEgNDIuNzY2IDIuMjY0OThlLTA2IDQyLjg2Ni...";
const localhost = "http://localhost:5000";

class ChipS2J {
    constructor(runtime) {
        this.runtime = runtime;
        this.saveTimeout = null;
        this.ping();
        this.runtime.on("PROJECT_CHANGED", () => {
            this.scheduleSave();
        });
    }

    getInfo() {
        return {
            id: "S2J",
            name: "Scratch2Json",
            menuIconURI: IconURI,
            blocks: []
        };
    }

    scheduleSave() {
        if (this.saveTimeout) clearTimeout(this.saveTimeout);
        this.saveTimeout = setTimeout(() => this.exportPMP(), 10000);
    }

    async ping() {
        const vm = this.runtime?.vm || window.vm;
        if (!vm) {
            console.warn("VM instance not found! Are you in PenguinMod or TurboWarp?");
            return;
        }

        try {

            const res = await fetch(localhost + "/api/fetch", {
                method: "GET"
            });

            const result = await res.json();
            if (res.ok) {
                console.log("Ping success: " + (result.msg || "ok"));
            } else {
                console.warn("Ping failed: " + (result.error || "unknown error"));
            }
        } catch (err) {
            console.error("Ping error: " + (err.message || err));
            alert("Cannot ping server. Is the server on?")
        }
    }

    async exportPMP() {
        const vm = this.runtime?.vm || window.vm;
        if (!vm) {
            console.warn("VM instance not found! Are you in PenguinMod or TurboWarp?");
            return;
        }

        try {
            const blob = await vm.saveProjectSb3("blob");
            const formData = new FormData();
            formData.append("file", blob, "project.pmp");

            const res = await fetch(localhost + "/api/upload", {
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
