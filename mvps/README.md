
# 📝 NeoGlass Summarizer & Paraphraser

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/) 
[![Streamlit](https://img.shields.io/badge/streamlit-1.30-orange)](https://streamlit.io/) 
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-facebook%2Fbart--large--cnn-yellow)](https://huggingface.co/facebook/bart-large-cnn) 
[![Groq](https://img.shields.io/badge/Groq-LLaMA3.1-purple)](https://www.groq.com/) 
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](https://opensource.org/licenses/Apache-2.0)

**NeoGlass** is a sleek, glassmorphic web application leveraging **state-of-the-art AI models** for high-quality text summarization and paraphrasing. Built with **Streamlit**, it combines **Hugging Face summarization models** and **Groq LLaMA 3.1** paraphrasing to provide an interactive, modern UI for text processing.  

🌐 **Try it online:** [Launch NeoGlass](https://share.streamlit.io/your-username/neoglass-summarizer/main/app.py)  

---

## ✨ Features

| Feature | Description | Icon |
|---------|-------------|------|
| **Abstractive Summarization** | Generates concise sentences capturing the text’s core meaning | ✍️ |
| **Extractive Summarization** | Extracts important sentences directly from the source text | ✂️ |
| **High-Speed Paraphrasing** | Instant paraphrasing with multiple variations using Groq API | 🚀 |
| **Modern Glassmorphic UI** | Beautiful and responsive interface with dynamic glowing effects | 🎨 |
| **Configurable Output Length** | Choose Short, Medium, or Long summaries | 🔧 |
| **Modular Pipeline** | Clean backend pipeline integrating all AI services | 🛠️ |

---
## 📂 File Structure
<pre>
mvps/
│
├── 📂 mvp/                    # Core application modules
│   ├── __init__.py            # Package initializer
│   ├── abstractive.py         # Abstractive summarization
│   ├── extractive.py          # Extractive summarization
│   ├── mvp_pipeline.py        # Main processing pipeline
│   ├── paraphraser.py         # Paraphrasing module
│   └── test_run.py            # Test running pipeline
│
├── .env                       # Environment variables for API keys
├── .gitignore                 # Git ignore file
├── app.py                     # Main app script
├── config.yaml                # Main YAML configuration
├── pyproject.toml             # Project configuration for Python
└── README.md                  # Project README
</pre>
---

<summary>⚙️ Setup & Installation</summary>

### Prerequisites
- Python 3.8+  
- Hugging Face API Key  
- Groq Cloud API Key

### Clone Repository

git clone https://github.com/RITHIKKUMARAN/Infosys_Data_Preprocessing.git
cd mvps

### Setup Virtual Environment

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

### Install Dependencies

pip install -r requirements.txt

### Create a .env file in the root directory:

HF_API_KEY="your_hugging_face_api_key_here"
GROQ_API_KEY="your_groq_api_key_here"
</details> <details> <summary>🚀 Running the Application</summary>
streamlit run app.py
Open your browser at: http://localhost:8501

</details> <details> <summary>🧪 Running Tests</summary>
python test_run.py
This validates all backend modules and prints results in the console.

</details> <details> <summary>🤝 Contributing</summary>
We welcome contributions!

Fork the repo

Create a branch:
git checkout -b feature/AmazingFeature

Commit changes:
git commit -m "Add some AmazingFeature"

Push branch:
git push origin feature/AmazingFeature

Open a Pull Request

</details> <details> <summary>📄 License</summary>
Licensed under Apache-2.0. See LICENSE

Built with ❤️ and modern AI.

</details>
