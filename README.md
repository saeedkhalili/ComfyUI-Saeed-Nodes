# ComfyUI-Saeed-Nodes

A collection of professional, self‑contained nodes for **ComfyUI**, designed for filmmakers, AI artists, and anyone who wants full cinematic control over their generated images.

---

## ✨ Features

- 🎥 **Cinematic Aspect Ratio Selector** – Pick a cinematic ratio, adjust quality (K), and get a ready‑to‑use latent.
- 🧠 **Model Loader (Diffusion, CLIP, VAE, LoRA)** – Load diffusion model, CLIP (with type), VAE, and up to 5 LoRAs (strength + trigger words) in one node.
- 📷 **Camera Selector** – Generate detailed camera prompts (angle, shot size, position, lens, movement, shake, speed) with emoji‑enhanced dropdowns.
- 💡 **Light Selector** – Cinematic lighting: outdoor/indoor, time of day, weather, light type, color, direction, quality, contrast, Kelvin, and genre.
- 🚀 **Image Generator** – Merges all prompts, optionally applies AuraFlow, runs KSampler + VAEDecode, and outputs the final image with a smart filename.

All nodes work **without any external dependencies** and can be used separately or chained together.

---

## 📦 Installation

1. Copy the `ComfyUI-Saeed-Nodes` folder into your `ComfyUI/custom_nodes/` directory.
2. Restart ComfyUI.
3. The nodes will appear under the **Saeed** category.

---

## 🛠️ Nodes & I/O

### Cinematic Aspect Ratio Selector
- **Inputs:** Aspect Ratio, Quality (K)
- **Outputs:** Name, Width, Height, Latent

### Model Loader (Diffusion, CLIP, VAE, LoRA)
- **Inputs:** Diffusion model, CLIP (with type), VAE, 5 LoRA slots (name, strength, trigger word)
- **Outputs:** MODEL, CLIP, VAE, trigger_words

### Camera Selector
- **Inputs:** Angle, shot, position, lens (dropdown), movement, turn, shake, speed
- **Output:** camera_prompt (ready to mix with positive prompt)

### Light Selector
- **Inputs:** Indoor/outdoor, time of day, weather, light type, color, direction, quality, contrast, Kelvin, genre
- **Output:** lighting_prompt

### Image Generator
- **Inputs:** MODEL, CLIP, VAE, Latent, positive/negative prompt, camera_prompt, light_prompt, trigger_words, sampler settings, project name
- **Outputs:** IMAGE, file_name

---

## 📝 Basic Workflow

![image generator workflow](https://raw.githubusercontent.com/saeedkhalili/ComfyUI-Saeed-Nodes/refs/heads/main/ComfyUI-Saeed-Nodes%20image%20generator%20workflow.jpg)

1. Create a latent with **Cinematic Aspect Ratio Selector**.
2. Load models with **Model Loader**.
3. Build camera & lighting prompts using **Camera Selector** and **Light Selector**.
4. Plug everything into **Image Generator** and get your final image.

---

## 🧩 Roadmap (planned)

- [ ] Style & Mood Selector
- [ ] Character Director
- [ ] Composition / Grid Guide
- [ ] Film Stock & Post‑Processing
- [ ] Negative Prompt Builder

---

## 📄 License

MIT – see the `LICENSE` file for details.

---

Built with love for the ComfyUI community.  
If you find this useful, I’d love to hear your feedback!
