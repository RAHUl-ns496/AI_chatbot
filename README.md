# AI_chatbot
public policy navigation using AI

## 🚀 Deploy to Streamlit Cloud

This app is ready to deploy on Streamlit Community Cloud! Follow these steps:

### Prerequisites
1. A GitHub account with this repository
2. A Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))
3. An OpenAI API key (get one at [platform.openai.com](https://platform.openai.com/api-keys))

### Deployment Steps

1. **Go to Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Create New App**
   - Click "New app" button
   - Select this repository: `RAHUl-ns496/AI_chatbot`
   - Select branch: `copilot/prepare-streamlit-deployment` (or `main` after merging)
   - Main file path: `OCR chatbot.py`
   - Click "Deploy"

3. **Configure Secrets**
   - Before or after deploying, click "Advanced settings"
   - In the "Secrets" section, add your OpenAI API key:
   ```toml
   OPENAI_API_KEY = "sk-your-api-key-here"
   ```
   - Click "Save"

4. **Wait for Deployment**
   - Streamlit Cloud will automatically install dependencies from `requirement.txt`
   - System packages (tesseract-ocr) will be installed from `apt.txt`
   - The app will be live at `https://[your-app-name].streamlit.app`

### Local Development

To run locally with Ollama (no API key needed):
```bash
streamlit run "OCR chatbot.py"
```

The app will automatically use Ollama if `OPENAI_API_KEY` is not set.

### Environment Variables
- `OPENAI_API_KEY`: Set this to use OpenAI models (required for Streamlit Cloud)
- `OLLAMA_HOST`: Set this to use a custom Ollama endpoint (default: `http://localhost:11434`)

## Features
- 📄 PDF text extraction
- 🖼️ OCR for images
- 💬 AI-powered document Q&A
- 😊 Sentiment analysis
- 📊 Full report generation
