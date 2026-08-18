import { app } from "../../scripts/app.js";

const TARGET_MAP = {
    camera: "CameraSelector",
    camera_movement: "CameraMovementSelector",
    light: "LightSelector",
    landscape: "LandscapePromptGenerator",
    character: "CharacterGenerator",
    action: "ActionGenerator",
    scene_element: "SceneElementGenerator",
    style: "StyleSelector",
    framing: "FramingSelector",
};

function randomizeNodeCombos(node) {
    if (!node?.widgets) return;
    for (const widget of node.widgets) {
        if (widget.type !== "combo") continue;
        const values = widget.options?.values;
        if (!Array.isArray(values) || values.length === 0) continue;
        const idx = Math.floor(Math.random() * values.length);
        widget.value = values[idx];
        widget.callback?.(widget.value);
    }
    node.setDirtyCanvas?.(true, true);
}

function resetNodeCombos(node) {
    if (!node?.widgets) return;
    for (const widget of node.widgets) {
        if (widget.type !== "combo") continue;
        const values = widget.options?.values;
        if (!Array.isArray(values) || values.length === 0) continue;
        widget.value = values[0];
        widget.callback?.(widget.value);
    }
    node.setDirtyCanvas?.(true, true);
}

function getSelectedToggles(randomizerNode) {
    const selected = {};
    for (const widget of randomizerNode.widgets) {
        if (widget.type === "toggle") {
            selected[widget.name] = !!widget.value;
        }
    }
    return selected;
}

function forEachSelectedTarget(app, randomizerNode, callback) {
    const selected = getSelectedToggles(randomizerNode);
    const nodes = app.graph._nodes || app.graph.nodes || [];
    for (const node of nodes) {
        for (const [key, nodeType] of Object.entries(TARGET_MAP)) {
            if (selected[key] && node.type === nodeType) {
                callback(node);
            }
        }
    }
}

app.registerExtension({
    name: "Saeed.PromptRandomizer",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name !== "PromptRandomizer") return;

        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            onNodeCreated?.apply(this, arguments);

            this.addWidget("button", "🎲 Randomize Selected", null, () => {
                forEachSelectedTarget(app, this, randomizeNodeCombos);
            });

            this.addWidget("button", "↩️ Reset Selected", null, () => {
                forEachSelectedTarget(app, this, resetNodeCombos);
            });
        };
    },
});