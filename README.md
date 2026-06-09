# CN Lab 5 — IPv4 Address Classification

> Classful IPv4 analyzer · runs live in the browser  
> *Computer Networks Lab · VIT*

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-7c6af7?style=flat-square&logo=github)](https://YOUR_USERNAME.github.io/cn-lab-5-ipv4-classifier/)
[![RFC 791](https://img.shields.io/badge/Standard-RFC%20791-4ade80?style=flat-square)](https://datatracker.ietf.org/doc/html/rfc791)
[![No dependencies](https://img.shields.io/badge/Dependencies-None-fbbf24?style=flat-square)](.)

---

## Live demo

**[→ Open in browser](https://shrutmpatil.github.io/IPv4-Class-Analyser/)**  
*(Replace `YOUR_USERNAME` with your GitHub username after deploying)*

---

## What it does

Given any IPv4 address, the tool resolves all classful addressing properties instantly:

| Field | Example (Class C — `192.168.1.1`) |
|---|---|
| IP Class | C |
| NetID bits | 24 |
| HostID bits | 8 |
| Default Subnet Mask | 255.255.255.0 |
| Supported Networks | 2,097,152 |
| Hosts per Network | 254 |
| Class Range | 192.0.0.0 – 223.255.255.255 |

Special addresses — Loopback `127.x`, Multicast D, Experimental E, and reserved `0.x` — are identified and explained inline.

---

## Theory

RFC 791 divides the 32-bit IPv4 space into five fixed classes determined by the **leading bits of the first octet**:

| Class | First octet | Leading bits | Purpose |
|---|---|---|---|
| A | 1 – 126 | `0xxxxxxx` | Large networks (ISPs, governments) |
| B | 128 – 191 | `10xxxxxx` | Medium networks (universities, enterprises) |
| C | 192 – 223 | `110xxxxx` | Small networks (most LANs) |
| D | 224 – 239 | `1110xxxx` | Multicast — no host assignment |
| E | 240 – 255 | `1111xxxx` | Experimental — reserved |

### Formulas

```
Networks (Class A) = 2^7  − 2  =        126
Networks (Class B) = 2^14      =     16,384
Networks (Class C) = 2^21      =  2,097,152

Hosts per network  = 2^(host bits) − 2
```

---

## Run locally

No install needed — just open the file:

```bash
git clone https://github.com/YOUR_USERNAME/cn-lab-5-ipv4-classifier.git
cd cn-lab-5-ipv4-classifier
open index.html          # macOS
start index.html         # Windows
xdg-open index.html      # Linux
```

Also included: `cn_lab_5.py` — the original Tkinter desktop version (Python 3.8+).

---

## Deploy to GitHub Pages

```bash
# 1. Create repo on github.com → Public, no README checkbox

# 2. Push from your project folder
git init
git add .
git commit -m "feat: IPv4 classful address analyzer"
git remote add origin https://github.com/YOUR_USERNAME/cn-lab-5-ipv4-classifier.git
git branch -M main
git push -u origin main

# 3. GitHub repo → Settings → Pages
#    Source: Deploy from branch → main / (root) → Save

# 4. Live in ~1 minute at:
#    https://YOUR_USERNAME.github.io/cn-lab-5-ipv4-classifier/
```

---

## Edge cases handled

| Input | Behaviour |
|---|---|
| `127.0.0.1` | Identified as **Loopback**, not Class A |
| `0.x.x.x` | Flagged as reserved "This" network |
| `224–239.x.x.x` | Class D — Multicast notice |
| `240–255.x.x.x` | Class E — Experimental notice |
| Bad octet value or count | Descriptive error shown immediately |
| Live typing | Border turns green (valid) or red (invalid) in real time |

---

## Project structure

```
cn-lab-5-ipv4-classifier/
├── index.html      ← web app (GitHub Pages entry point)
├── cn_lab_5.py     ← Tkinter desktop version
└── README.md
```

---

## Concepts covered

- RFC 791 classful addressing
- NetID / HostID bit partitioning and leading-bit encoding
- Default subnet masks (A / B / C)
- Network and host count formulas (`2ⁿ − 2`)
- Special-purpose address ranges: loopback, multicast, experimental, reserved

### **Collaborators:**

## 👥 Collaborators

<p align="center">
  <a href="https://github.com/shrutmpatil"><img src="https://img.shields.io/badge/Shrut-Patil-blue?style=for-the-badge&logo=github" alt="Shrut Patil GitHub"></a>
  <a href="https://github.com/siddhilad920"><img src="https://img.shields.io/badge/Siddhi-Lad-lightgrey?style=for-the-badge&logo=github" alt="Siddhi Lad GitHub"></a>
</p>
<p align="center">
  <a href="https://www.linkedin.com/in/shrutmpatil/">
    <img src="https://img.icons8.com/color/48/000000/linkedin.png" width="50"/>
  <a href="https://www.linkedin.com/in/lad-siddhi/">
    <img src="https://img.icons8.com/color/48/000000/linkedin.png" width="50"/>
  </a>
</p>
