# TALOS Αναλυτής Αρχείων Κειμένου

[![Python](https://img.shields.io/badge/Python-3.8%2B-informational.svg)](#-run)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-lightgrey.svg)](#-run)
[![spaCy](https://img.shields.io/badge/NLP-spaCy-lightgrey.svg)](#-run)
[![Stanza](https://img.shields.io/badge/NLP-Stanza-lightgrey.svg)](#-run)

Διαθέσιμες γλώσσες: [English](README.md) | [Ελληνικά](README.el.md)

---

Αυτό το αποθετήριο παρέχει μια ελαφριά **εφαρμογή γραφικού περιβάλλοντος (desktop GUI)** για ανάλυση, εξαγωγή και αποθήκευση γλωσσικών πληροφοριών από αρχεία απλού κειμένου.

---

## 📂 Περιεχόμενα

Το αποθετήριο περιλαμβάνει:

- `Talos_Text_Analyser.py` — ο πλήρης πηγαίος κώδικας (όλα-σε-ένα εφαρμογή Tkinter)
- `Talos_Text_Analyser_Documentation.pdf` — οδηγός εγκατάστασης & χρήσης (Έκδοση 2.0)

---

## Επισκόπηση

Ο **TALOS Αναλυτής Αρχείων Κειμένου** είναι ένα διαλειτουργικό **επιτραπέζιο** εργαλείο (Tkinter) για **διαδραστική ανάλυση κειμένου**. Μπορεί να:

- Υπολογίζει **συχνότητες λέξεων**  
- Εξάγει **ουσιαστικά** (βάσει POS)  
- Ανιχνεύει **ονόματα προσώπων** και **τοπωνύμια** (NER)  
- Εκτελεί **λεμματοποίηση**  
- Εντοπίζει **Λεξικο-συντακτικά πρότυπα** (προκαθορισμένα & προσαρμοσμένα έως 5 θέσεις)  
- **Εξάγει** αποτελέσματα σε **Excel (.xlsx)** και **CSV**  

Σχεδιασμένο για **ερευνητές, εκπαιδευτικούς και προγραμματιστές**, με ειδική υποστήριξη για **Αρχαία Ελληνικά** μέσω Stanza και **σύγχρονες γλώσσες** μέσω spaCy.

> **Είσοδος:** αρχεία απλού κειμένου (`.txt`). Για βέλτιστα αποτελέσματα, χρησιμοποιήστε κωδικοποίηση UTF-8.

---

## Χαρακτηριστικά

- **Αυτόματη ανίχνευση γλώσσας** με βελτιωμένες ευρετικές για Αγγλικά/Ελληνικά· υποστηρίζεται διάκριση **Αρχαίων** και **Νέων Ελληνικών**
- **Έξι τρόποι ανάλυσης:** Λέξεις, Ουσιαστικά, Ονόματα Προσώπων, Τοπωνύμια, Λήμματα, Εξαγωγή Προτύπων
- **Δόμηση προτύπων** (POS templates, wildcard, έως 5 θέσεις)
- **Export** σε Excel (πολλαπλά φύλλα) και CSV
- **Πολύγλωσσο NLP:** μοντέλα spaCy για σύγχρονες γλώσσες· Stanza για **Αρχαία Ελληνικά (grc)**
- **Σύγχρονο dark UI** με μπάρες προόδου και άμεση ανατροφοδότηση

---

## Εκτέλεση

```bash
# 1) Βεβαιωθείτε ότι έχετε Python 3.8+
python --version

# 2) Εγκατάσταση βασικών βιβλιοθηκών (one-liner)
pip install pandas openpyxl spacy langdetect stanza

# 3) Εγκατάσταση μοντέλων spaCy (απαραίτητο)
python -m spacy download en_core_web_sm
python -m spacy download el_core_news_sm   # Ελληνικά

# 4) Εγκατάσταση μοντέλου Stanza για Αρχαία Ελληνικά (μια φορά)
python - << 'PY'
import stanza
stanza.download("grc")
PY

# 5) Εκκίνηση εφαρμογής GUI
python Talos_Text_Analyser.py
```

---
## Συγγραφέας

Καθ. Christophe Roche — TALOS ERA Chair Holder — Πανεπιστήμιο Κρήτης

📧 roche.university@gmail.com

🌐 https://talos-ai4ssh.uoc.gr/

---

## Αναφορά

Για γενική αναφορά στο έργο:

> Roche, C. (2025). TALOS Text File Analyser (Έκδοση 2.0).
> TALOS AI4SSH Project, Πανεπιστήμιο Κρήτης.
> https://talos-ai4ssh.uoc.gr/

---

## Άδεια

Όλος ο κώδικας διανέμεται με άδεια Creative Commons Attribution–NonCommercial (CC BY-NC 4.0).
Μπορείτε να κοινοποιήσετε και να αναδιανείμετε το υλικό υπό τις ακόλουθες προϋποθέσεις:

> BY: Πρέπει να αποδίδεται αναφορά στον δημιουργό.

> NC: Επιτρέπεται μόνο μη-εμπορική χρήση.

Περισσότερες πληροφορίες: https://creativecommons.org/licenses/by-nc/4.0/

---

## Περισσότερες Πληροφορίες

Ιστότοπος TALOS Text File Analyser: [talos-ai4ssh.eu/Text_Analyser](http://talos-ai4ssh.eu/Text_Analyser/)

Ιστότοπος Έργου TALOS: [talos-ai4ssh.uoc.gr](https://talos-ai4ssh.uoc.gr)

---
