# ResearchMind AI

ResearchMind AI is a multi-agent research assistant built with Python and Streamlit. It searches the web, extracts content from relevant pages, drafts a structured research report, and critiques the final output using LLM-powered agents.

## Features

- Web search using Tavily API
- URL content scraping with BeautifulSoup
- Multi-agent workflow with LangChain
- Mistral AI integration for reasoning and generation
- Streamlit-based user interface
- Structured research report generation and review loop

## Project Structure

```bash
.
├── .gitignore
├── .env.example
├── agents.py
├── app.py
├── pipeline.py
├── tools.py
├── requirements.txt
├── README.md
```

## Tech Stack

- Python
- Streamlit
- LangChain
- Mistral AI
- Tavily API
- BeautifulSoup
- Requests
- Python-dotenv
- Rich

## Setup

1. Clone the repository
2. Create a virtual environment
3. Install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

5. Run the app:

```bash
streamlit run app.py
```

## Usage

- Open the local Streamlit app in your browser.
- Enter a research topic.
- The system will:
  - search the web,
  - identify top sources,
  - scrape relevant information,
  - generate a research report,
  - provide a critique and improvement feedback.

## Notes

- Keep your API keys in `.env` and do not commit them to version control.
- The project is designed for research and experimentation and can be extended with more agents, tools, or storage.

## License

This project is for educational and prototype use.
