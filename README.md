# 📄 README and Documentation Generator

An intelligent tool that automatically generates professional README files and comprehensive technical documentation for your projects using AI-powered analysis.

## ✨ Features

- **Automatic Code Analysis**: Upload your project files and get instant AI-powered analysis
- **README Generation**: Creates well-structured README.md files with proper sections
- **Professional Documentation**: Generates comprehensive technical documentation (DOCUMENTATION.md)
- **AI-Powered**: Uses Groq's `llama-3.3-70b-versatile` model for intelligent content generation
- **User-Friendly Interface**: Clean web interface for easy file upload and generation
- **Secure**: API keys stored in environment variables

## 🚀 Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript
- **AI Model**: Groq API with llama-3.3-70b-versatile
- **Text Processing**: langchain-text-splitters for handling large files
- **Server**: Uvicorn (ASGI server)

## 📋 Prerequisites

- Python 3.11+
- Groq API key ([Get one here](https://console.groq.com))

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/HassanCodesIt/README-and-Documentation-generator.git
cd README-and-Documentation-generator
```

2. **Create a virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
# or
source .venv/bin/activate  # On macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```

## 🎯 Usage

1. **Start the server**
```bash
uvicorn main:app --reload
```

2. **Open your browser**

Navigate to `http://127.0.0.1:8000`

3. **Upload your project**
   - Click "Choose Files" and select your project folder
   - Click "Upload Files" to analyze your code
   - Wait for the AI analysis to complete

4. **Generate documentation**
   - Click "Generate README" for a standard README.md file
   - Click "Generate Documentation" for comprehensive technical docs

## 📁 Project Structure

```
README-and-Documentation-generator/
├── main.py              # FastAPI backend with all endpoints
├── index.html           # Frontend interface
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not tracked)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🔧 Configuration

The application uses the following configuration:

- **Upload Directory**: `C:\Users\hassa\Desktop\readme_uploads`
- **Supported File Types**: `.py`, `.js`, `.ts`, `.html`, `.css`, `.json`, `.md`, `.txt`, `.yml`, `.yaml`
- **AI Model**: `llama-3.3-70b-versatile`
- **Chunk Size**: 2500 characters (for large files)

## 🌐 API Endpoints

- `GET /` - Serve the web interface
- `POST /save` - Upload and save project files
- `POST /llm` - Analyze files with AI
- `POST /generate_readme` - Generate README.md
- `POST /generate_docs` - Generate DOCUMENTATION.md

## 🔒 Security

- API keys are stored in `.env` file (not committed to Git)
- `.gitignore` configured to exclude sensitive files
- Only whitelisted file types are processed

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

**Hassan**
- GitHub: [@HassanCodesIt](https://github.com/HassanCodesIt)

## 🙏 Acknowledgments

- [Groq](https://groq.com) for providing the AI API
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [LangChain](https://www.langchain.com/) for text splitting utilities

---

Made with ❤️ by Hassan