# Langflow RAG Project: Citizen Advice Benefits Assistant

This project implements a Retrieval-Augmented Generation (RAG) system using Langflow to create an AI assistant that can answer questions about UK benefits using information from the Citizens Advice website.

## 🎯 Project Overview

The system scrapes content from [Citizens Advice Benefits pages](https://www.citizensadvice.org.uk/benefits/), processes it into embeddings, stores it in a Chroma vector database, and uses Mistral AI to generate contextual responses to user queries about UK benefits.

## 📋 Prerequisites

Before setting up this project, you'll need:

1. **API Keys:**
   - [OpenAI API Key](https://platform.openai.com/api-keys) (for embeddings)
   - [Mistral AI API Key](https://console.mistral.ai/) (for text generation)

2. **System Requirements:**
   - macOS, Windows, or Linux
   - At least 4GB RAM (recommended)
   - Stable internet connection

## 🚀 Installation Steps

### Step 1: Install Langflow Desktop (Recommended)

The easiest way to get started is using Langflow Desktop:

1. **Download Langflow Desktop:**
   - Visit [Langflow Desktop](https://docs.langflow.org/get-started-installation)
   - Click "Download Langflow"
   - Enter your contact information
   - Download the appropriate version for your OS

2. **Install the Application:**
   - **macOS:** Mount and install the downloaded `.dmg` file
   - **Windows:** Double-click the downloaded `.msi` file and follow the installation wizard
   - **Linux:** Follow the platform-specific installation instructions

3. **Launch Langflow:**
   - Open the Langflow application
   - The interface should be available at `http://127.0.0.1:7860`

### Alternative: Install Langflow OSS (Python Package)

If you prefer the Python package version:

1. **Install Python 3.10-3.13** (3.10-3.12 for Windows)

2. **Install uv package manager:**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Create a virtual environment:**
   ```bash
   uv venv langflow-env
   source langflow-env/bin/activate  # On Windows: langflow-env\Scripts\activate
   ```

4. **Install Langflow:**
   ```bash
   uv pip install langflow
   ```

5. **Run Langflow:**
   ```bash
   uv run langflow run
   ```

## 🔧 Project Setup

### Step 2: Import the Flow

1. **Open Langflow Interface:**
   - Navigate to `http://127.0.0.1:7860` in your browser
   - You should see the Langflow dashboard

2. **Import the Flow:**
   - Click on "My Projects" in the sidebar
   - Click the "Add Flow" button
   - Drag and drop the `Citizen Advice RAG.json` file from the `langflow_json/` folder
   - The flow will be imported and appear in your projects list

### Step 3: Configure API Keys

1. **Access Global Variables:**
   - In the Langflow interface, click on the settings icon (gear) in the top right
   - Select "Global Variables" or "Environment Variables"

2. **Add Required API Keys:**
   - **OpenAI API Key:**
     - Variable Name: `OPENAI_API_KEY`
     - Value: Your OpenAI API key from [platform.openai.com](https://platform.openai.com/api-keys)
   
   - **Mistral API Key:**
     - Variable Name: `MISTRAL_API_KEY`
     - Value: Your Mistral AI API key from [console.mistral.ai](https://console.mistral.ai/)

3. **Save Configuration:**
   - Click "Save" to store your API keys
   - The keys will be securely stored and used by the flow components

## 🎮 Using the RAG System

### Step 4: Run the Flow

1. **Open the Flow:**
   - Click on the "Citizen Advice RAG" project in your projects list
   - The flow canvas will open showing the complete RAG pipeline

2. **Initialize the System:**
   - The flow includes components for:
     - **URL Component:** Scrapes content from Citizens Advice benefits pages
     - **Text Splitting:** Breaks content into manageable chunks
     - **Embeddings:** Converts text to vector representations using Mistral AI
     - **Chroma Database:** Stores and retrieves relevant information
     - **Mistral Model:** Generates responses based on retrieved context

3. **Start the Playground:**
   - Click on the "Playground" tab in the interface
   - This opens the chat interface where you can interact with the system

### Step 5: Ask Questions

You can now ask questions about UK benefits, such as:

- "What is Universal Credit and how do I apply?"
- "Am I eligible for Housing Benefit?"
- "How does volunteering affect my benefits?"
- "What benefits are available for disabled people?"
- "How do I claim Child Benefit?"
- "What is Personal Independence Payment?"

The system will:
1. Search the Citizens Advice knowledge base
2. Retrieve relevant information
3. Generate contextual, accurate responses
4. Provide source information when available

## 🔍 Flow Architecture

The RAG system consists of several key components:

```
User Query → Chat Input → Chroma Search → Context Retrieval → Prompt Template → Mistral Model → Response
```

**Key Components:**
- **URL Component:** Scrapes [Citizens Advice benefits pages](https://www.citizensadvice.org.uk/benefits/)
- **SplitText:** Breaks content into semantic chunks for better retrieval
- **Mistral AI Embeddings:** Creates vector representations of text
- **Chroma Database:** Stores embeddings and enables similarity search
- **Prompt Template:** Structures the context and question for the LLM
- **Mistral Model:** Generates human-like responses based on retrieved context

## 🛠️ Troubleshooting

### Common Issues:

1. **"No module named 'langflow.__main__'" Error:**
   - Use `uv run langflow run` instead of `langflow run`
   - Reinstall with: `uv pip install langflow -U --force-reinstall`

2. **API Key Errors:**
   - Ensure API keys are correctly set in Global Variables
   - Verify keys are valid and have sufficient credits
   - Check for typos in variable names

3. **Chroma Database Issues:**
   - Clear cache if needed: Delete contents of `~/.cache/langflow/`
   - Restart Langflow after clearing cache

4. **Performance Issues:**
   - Ensure you have at least 4GB RAM available
   - Close other resource-intensive applications
   - Consider using Langflow Desktop for better performance

## 💰 Costing

Understanding the costs involved in running this RAG system:

### **Langflow OSS (Local Setup)**
- **Cost: FREE** 🎉
- Langflow open-source version has no licensing fees
- Runs entirely on your local machine
- No cloud hosting costs

### **Mistral AI API**
- **Free Tier:** Very generous
- **Embeddings:** Free tier includes substantial usage
- **Text Generation:** Free tier available with reasonable limits
- **Paid Tier:** Pay-as-you-go pricing when you exceed free limits
- **Recommendation:** Start with free tier - it's sufficient for testing and moderate usage

### **OpenAI API**
- **Cost:** Approximately $0.005 per query run
- **Usage:** Used for text embeddings in this flow
- **Pricing:** Based on token usage (very cost-effective for embeddings)
- **Alternative:** You can replace OpenAI embeddings with Mistral AI embeddings to reduce costs

### **Total Cost Estimate**
- **Setup:** $0 (Langflow OSS is free)
- **Per Query:** ~$0.005 (mainly OpenAI embeddings)
- **Monthly (100 queries):** ~$0.50
- **Monthly (1000 queries):** ~$5.00

### **Cost Optimization Tips**
1. **Use Mistral AI for both embeddings and generation** to eliminate OpenAI costs
2. **Batch process queries** when possible to reduce API calls
3. **Monitor usage** through your API provider dashboards
4. **Set up usage alerts** to avoid unexpected charges
5. **Consider caching** frequently asked questions to reduce API calls

## 📚 Additional Resources

- [Langflow Documentation](https://docs.langflow.org/)
- [Citizens Advice Benefits](https://www.citizensadvice.org.uk/benefits/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Mistral AI Documentation](https://docs.mistral.ai/)
- **[Technical RAG Documentation](DOC.md)** - Detailed explanation of how the RAG system works and how to build similar flows

## 🤝 Contributing

This project demonstrates how to build a RAG system using Langflow in low code and now code environments which we think would be great for the charity sector to prototype and test new ideas. Feel free to:
- Modify the flow for different use cases
- Add new data sources
- Improve the prompt templates
- Share your improvements

## 📄 License

This project is open source and available under the MIT License.

---

**Note:** This system is for educational and demonstration purposes. For official benefits advice, always consult with Citizens Advice or relevant government agencies.
