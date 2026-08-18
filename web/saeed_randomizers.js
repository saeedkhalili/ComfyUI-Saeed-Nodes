import { app } from "../../scripts/app.js";

const TARGET_NODES = [
    "CameraSelector",
    "CameraMovementSelector",
    "LightSelector",
    "LandscapePromptGenerator",
    "CharacterGenerator",
    "ActionGenerator",
    "SceneElementGenerator",
    "StyleSelector",
    "FramingSelector",
];

app.registerExtension({
    name: "Saeed.Randomizers",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (!TARGET_NODES.includes(nodeData.name)) return;

        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            onNodeCreated?.apply(this, arguments);

            this.addWidget("button", "🎲 Randomize", null, () => {
                const required = this.constructor.nodeData?.input?.required || {};

                for (const [inputName, inputSpec] of Object.entries(required)) {
                    const list = Array.isArray(inputSpec) ? inputSpec[0] : inputSpec;
                    if (!Array.isArray(list) || list.length === 0) continue;

                    const widget = this.widgets?.find(w => w.name === inputName);
                    if (widget && widget.type === "combo") {
                        const randomIndex = Math.floor(Math.random() * list.length);
                        widget.value = list[randomIndex];
                        widget.callback?.(widget.value);
                    }
                }

                this.setDirtyCanvas(true, true);
            });
        };
    },
});