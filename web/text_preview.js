import { app } from "../../scripts/app.js";
import { ComfyWidgets } from "../../scripts/widgets.js";

app.registerExtension({
    name: "Saeed.TextPreview",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name !== "TextPreview") return;

        const onExecuted = nodeType.prototype.onExecuted;
        nodeType.prototype.onExecuted = function (message) {
            onExecuted?.apply(this, arguments);

            if (message?.text !== undefined) {
                if (!this.previewWidget) {
                    this.previewWidget = ComfyWidgets["STRING"](
                        this,
                        "Preview",
                        ["STRING", { multiline: true }],
                        app
                    ).widget;
                    this.previewWidget.inputEl.readOnly = true;
                    this.previewWidget.inputEl.style.opacity = 0.6;
                }
                this.previewWidget.value = message.text[0];
            }
        };
    },
});