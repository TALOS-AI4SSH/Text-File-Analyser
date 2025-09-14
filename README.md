# TALOS Text File Analyser

[![Python](https://img.shields.io/badge/Python-3.8%2B-informational.svg)](#-run)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-lightgrey.svg)](#-run)
[![spaCy](https://img.shields.io/badge/NLP-spaCy-lightgrey.svg)](#-run)
[![Stanza](https://img.shields.io/badge/NLP-Stanza-lightgrey.svg)](#-run)

Available languages: [English](README.md) | [Ελληνικά](README.el.md)

---

This repository provides a lightweight **desktop GUI** application for analyzing, extracting, and exporting linguistic information from plain-text files.

---

## 📂 Contents

This repository contains:

- `Talos_Text_Analyser.py` — the complete source code (all-in-one Tkinter application) 
- `Talos_Text_Analyser_Documentation.pdf` — installation & usage guide (Version 2.0)

---

## Overview

The **TALOS Text File Analyser (TFA)** is a cross-platform **desktop** tool (Tkinter) for **interactive text analysis**. It can:

- Perform **Word** frequency analysis  
- Extract **Nouns** (POS-based)  
- Detect **Person** and **Location** names (NER)  
- Run **Lemmatization**  
- Extract **Lexico-Syntactic Patterns** (predefined & custom up to 5 tokens)  
- **Export** results to **Excel (.xlsx)** and **CSV**  

Designed for **researchers, educators, and developers**, with special support for **Ancient Greek** via Stanza and **modern languages** via spaCy.

---

## Features

- **Language detection** (automatic) with tuned English/Greek heuristics; supports Ancient & Modern Greek distinctions. 
- **Six analysis modes:** Words, Nouns, Person names, Location names, Lemmas, Pattern extraction.  
- **Custom pattern builder** (POS templates, wildcard, up to 5 positions).  
- **Export** to Excel (multi-sheet) and CSV.  
- **Multilingual NLP:** spaCy models for modern languages; Stanza for **Ancient Greek (grc)**.  
- **Modern dark UI** with progress bars and responsive feedback.

---

## Run

```bash
# 1) Ensure Python 3.8+ is installed
python --version

# 2) Install core libraries
pip install pandas openpyxl spacy langdetect stanza

# 3) Install spaCy language models (essential)
python -m spacy download en_core_web_sm
python -m spacy download el_core_news_sm   # Greek

# 4) Install Stanza Ancient Greek model (one-time)
python - << 'PY'
import stanza
stanza.download("grc")
PY

# 5) Launch the GUI application
python Talos_Text_Analyser.py
```

## Author

Prof. Christophe Roche — TALOS ERA Chair Holder — University of Crete

📧 roche.university@gmail.com

🌐 https://talos-ai4ssh.uoc.gr/

---

## Citation  

For general reference to the project:  
> Roche, C. (2025). TALOS Text File Analyser (Version 2.0).  
> TALOS AI4SSH Project, University of Crete.  
> https://talos-ai4ssh.uoc.gr/

---

## License

All the code is distributed under the **Creative Commons Attribution–NonCommercial (CC BY-NC 4.0)** license.  
You are free to **share and redistribute** the material under the following conditions:  
- **BY**: Credit must be given to the creator(s).  
- **NC**: Only non-commercial uses are permitted.

More info: https://creativecommons.org/licenses/by-nc/4.0/
 
---

## More Information

- TALOS Text File Analyser Website: [talos-ai4ssh.eu/Text_Analyser](http://talos-ai4ssh.eu/Text_Analyser/)
- TALOS Project Website: [talos-ai4ssh.uoc.gr](https://talos-ai4ssh.uoc.gr)  

---
