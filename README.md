****JobShield AI**

A Universal Chrome Extension for Intelligent Resume-to-Job Alignment.

JobShield AI uses Natural Language Processing (NLP) and Semantic Analysis to bridge the gap between job seekers and Applicant Tracking Systems (ATS). Unlike static scanners, it dynamically extracts skill requirements from any career page and compares them against a PDF resume in real-time.

🚀 Key Features
Universal Auto-Scraper: Automatically detects job descriptions on LinkedIn, Indeed, and many others using targeted CSS selectors.

Semantic Matching: Uses Sentence-BERT (all-MiniLM-L6-v2) to calculate a "Match Strength" based on meaning, not just exact word counts.

AI & Genericity Check: Analyzes resume "predictability" using GPT-2 perplexity scores to ensure your content feels human-written.

ATS Compliance Scanner: Identifies structural red flags like complex layouts or missing contact information that cause parsing failures.

Dynamic Keyword Gap: Employs the RAKE algorithm to extract top 15 skill requirements from the job post and highlights what is missing in your resume.

🛠️ Tech Stack
Frontend: JavaScript (Chrome Extension API), HTML5, CSS3.

Backend: Python (FastAPI), Uvicorn.

AI/NLP: PyTorch, Transformers (GPT-2), Sentence-Transformers, RAKE-NLTK.

PDF Processing: PyMuPDF (Fitz).

💻 Installation & Setup
1. Local Backend Setup

Ensure you have Conda or Python 3.10+ installed.

**Bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/JobShield-AI.git
cd JobShield-AI/backend

# Create and activate environment
conda create -n jobshield python=3.10
conda activate jobshield

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('punkt_tab')"

# Start the server
uvicorn main:app --host 127.0.0.1 --port 8000 --reload**


2. Chrome Extension Setup

Open Chrome and navigate to chrome://extensions/.

Enable Developer Mode (top-right toggle).

Click Load unpacked.

Select the extension folder from this repository.

📖 How to Use

**Navigate to any job description page (e.g., LinkedIn).

Click the JobShield AI icon in your browser toolbar.

Verify the status says: ✅ Job details detected automatically.

Upload your PDF Resume.**

Click Analyze Match Strength to see your score and missing keywords.

🏗️ Architecture

The project follows a "Brain and Body" architecture:

The Body (Chrome Extension): Handles UI, web scraping, and file handling.

The Brain (FastAPI Server): Processes PDF text and runs multiple AI inference models to provide feedback.

📝 License
Distributed under the MIT License.
**
