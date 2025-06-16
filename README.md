# 🛠️ sh00k3ms-toolkit

Welcome to `sh00k3ms-toolkit` — a beginner-friendly, growing collection of Python scripts focused on recon, automation, and data parsing.

---
## 📃 License

This project is licensed under the [MIT License](LICENSE).
---

![Tool Preview](https://img.shields.io/badge/python-3.9%2B-blue?logo=python)  
Created with curiosity and caffeine by [Shookems](https://github.com/Shookems)

---

## 🚀 Quick Start

```bash
git clone https://github.com/Shookems/sh00k3ms-toolkit.git
cd sh00k3ms-toolkit
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
=======
A growing collection of beginner-friendly Python scripts for automation, recon, and data parsing — built by Shookems.

## 📦 Tools Included

### 1. `domain_recon/`
> Lookup WHOIS info and DNS records (A, NS) for a given domain  
> Outputs results to terminal or CSV file

```bash
python domain_recon/domain_recon.py openai.com -o output.csv

