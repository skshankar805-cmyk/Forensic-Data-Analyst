# 🛡️ MAGNET-INTEL: AI-Driven Mobile Forensic Triage Workspace

MAGNET-INTEL is an advanced, lightweight digital forensics triage framework designed to counter the modern challenge of **Data Bloat** in mobile investigations. Instead of waiting hours or days for heavy device recovery processes, MAGNET-INTEL extracts structural data from target archives, analyzes entity clusters, and utilizes a local Large Language Model (LLM) to perform contextual correlation—completely offline and secure.

Inspired by industry-standard tools like Magnet AXIOM, this application features a premium cyber-dark command interface built natively in Python.

---

## 🚀 Core Architectural Features

### 1. Data Volume Reduction & Triage
* **NSRL Hash Exclusions:** Drops known operating system files, pre-installed app assets, and standard libraries to isolate user-generated data.
* **Perceptual Hashing (pHash):** Automatically detects and suppresses thousands of viral social media forwards, memes, and trending reels, drastically reducing manual media review.

### 2. Full-Spectrum Forensic Artifact Tree
The system exposes a standard 10-tier diagnostic pipeline directly from the sidebar UI:
1. **Call & Contact Data:** Reconstruction of incoming, outgoing, missed call tables, and duration metrics.
2. **Messages & Chats:** Structural tracking over WhatsApp databases (`msgstore.db`), SMS registries (`mmssms.db`), and other instant messengers.
3. **Location Data (GPS):** Extracts coordinates, Google Maps history, and WiFi access point connection logs.
4. **Photos & Videos:** Density mapping over camera storage structures with metadata/EXIF tracking.
5. **Internet Data:** History logs parsing for standard browsers (Chrome, Firefox).
6. **Apps Registry:** Verification of target packages and detection of hidden device storage vaults.
7. **Files & Documents:** Deep extraction matrix of PDFs, Docx arrays, and unallocated sector text streams.
8. **SIM & Device Info:** Mapping IMEI numbers, IMSI/ICCID registries, and underlying base operating system specs.
9. **Cloud Backups:** Audit of connected Google Drive/iCloud backup sync events.
10. **Advanced Social Graphs:** Structural analysis tracking who talks to whom during anomalous/odd operating hours.

### 3. Local Ollama Integration (100% Offline AI)
Utilizes your local computer's system constraints to bind a local quantized `Llama-3-8b` engine. The AI parses text queries and telemetry mappings natively without data escaping to the public cloud, ensuring data chain-of-custody.

---

## 🛠️ Technical Stack & Framework Dependencies

* **Language Platform:** Python 3.10+
* **User Interface Engine:** Streamlit (Custom Material Cyber-Dark CSS Injection)
* **Data Processing Layer:** Pandas, NumPy
* **Visualization Layer:** Plotly Express (Dark Matrices Template)
* **Local Inference Socket:** Ollama API (`llama3`)

---

## 💾 Installation & Local Setup

Ensure you have your virtual environment configured in your workspace terminal before running installation procedures.

