# ComfyUI-Saeed-Nodes

<div dir="rtl">

**مجموعه‌ای از نودهای حرفه‌ای و خودکفا برای ComfyUI**  
طراحی‌شده برای فیلم‌سازان، هنرمندان هوش مصنوعی و هر کسی که به‌دنبال کنترل سینمایی کامل بر تصاویر خود است.

---

## ✨ امکانات

- 🎥 **Cinematic Aspect Ratio Selector** – انتخاب نسبت ابعاد سینمایی با قابلیت تنظیم کیفیت (K) و ساخت latent.
- 🧠 **Model Loader (Diffusion, CLIP, VAE, LoRA)** – بارگذاری یک‌پارچه‌ی مدل دیفیوژن، CLIP، VAE و حداکثر ۵ لورا با قدرت و کلمهٔ تریگر.
- 📷 **Camera Selector** – ساخت پرامپت دوربین حرفه‌ای (زاویه، اندازهٔ شات، موقعیت، لنز، حرکت، لرزش، سرعت) با ایموجی‌های راهنما.
- 💡 **Light Selector** – نورپردازی سینمایی داخلی/بیرونی، رنگ، جهت، کیفیت، کنتراست، دمای رنگ و ژانر.
- 🚀 **Image Generator** – ترکیب نهایی پرامپت‌ها، اعمال AuraFlow (در صورت وجود) و تولید تصویر با KSampler و VAEDecode.

تمامی نودها **بدون نیاز به هیچ نود خارجی** کار می‌کنند و می‌توان آن‌ها را به‌صورت مجزا یا زنجیره‌ای استفاده کرد.

---

## 📦 نصب

1. پوشه‌ی `ComfyUI-Saeed-Nodes` را در مسیر `ComfyUI/custom_nodes/` کپی کنید.
2. ComfyUI را ری‌استارت کنید.
3. نودها در دسته‌ی **Saeed** ظاهر خواهند شد.

---

## 🛠️ نودها و ورودی/خروجی‌ها

### Cinematic Aspect Ratio Selector
- **ورودی:** Aspect Ratio, Quality (K)
- **خروجی:** Name, Width, Height, Latent

### Model Loader (Diffusion, CLIP, VAE, LoRA)
- **ورودی:** مدل دیفیوژن، CLIP (با نوع)، VAE، ۵ اسلات لورا (نام، قدرت، کلمهٔ تریگر)
- **خروجی:** MODEL, CLIP, VAE, trigger_words

### Camera Selector
- **ورودی:** زاویه، شات، موقعیت، لنز (کرکره‌ای)، حرکت، چرخش، لرزش، سرعت
- **خروجی:** camera_prompt (متن آمادهٔ ترکیب با پرامپت مثبت)

### Light Selector
- **ورودی:** داخلی/بیرونی، زمان روز، آب‌وهوا، نوع نور، رنگ، جهت، کیفیت، کنتراست، دمای رنگ، ژانر
- **خروجی:** lighting_prompt

### Image Generator
- **ورودی:** MODEL, CLIP, VAE, Latent، پرامپت مثبت و منفی، camera_prompt، light_prompt، trigger_words، تنظیمات سمپلر و نام پروژه
- **خروجی:** IMAGE, file_name

---

## 📝 نحوهٔ استفاده

1. یک Latent با **Cinematic Aspect Ratio Selector** بسازید.
2. مدل‌ها را با **Model Loader** بارگذاری کنید.
3. پرامپت‌های دوربین و نور را با **Camera Selector** و **Light Selector** تولید کنید.
4. همه را به **Image Generator** متصل کنید و تصویر نهایی را بگیرید.

---

## 🧩 نقشهٔ راه (آینده)

- [ ] Style & Mood Selector
- [ ] Character Director
- [ ] Composition / Grid
- [ ] Film Stock & Post‑Processing
- [ ] Negative Prompt Builder

---

## 📄 لایسنس

این پروژه تحت لایسنس MIT منتشر می‌شود. برای اطلاعات بیشتر فایل `LICENSE` را مطالعه کنید.

---

## 🤝 تقدیر و تشکر

با عشق برای جامعهٔ ComfyUI ساخته شده است. اگر از این نودها استفاده می‌کنید، خوشحال می‌شوم نظرتان را بدانم!

</div>