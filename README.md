# ProfMatch 🎓

Find your next research opportunity with AI-powered professor matching.

## Overview 🌟

ProfMatch simplifies the process of finding research opportunities by using AI to match students with active professors based on research interests. No more navigating outdated academic directories or spending hours searching through scattered information.

Try it now: [ProfMatch App](https://profmatch.up.railway.app/)

## Features ✨

- Natural language search for research interests
- Real-time professor matching using vector similarity
- Verified, up-to-date professor information
- Email contacts for reaching out
- Daily refreshed database of active researchers
- 5 free credits daily during open beta!

## Tech Stack 🛠️

### Frontend
- React
- TypeScript
- Tailwind CSS
- Vite

### Backend
- Python
- FastAPI
- Selenium (web scraping)
- Perplexity API (verification & description generation)

### Infrastructure
- Railway (deployment)
- Pinecone (vector database)
- Supabase (PostgreSQL)
- Docker

## Getting Started 🚀

### Prerequisites
- Node.js (v18+)
- Python 3.11+
- Docker & Docker Compose

### Environment Variables
```env
# Backend (.env)
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX=your_index_name

# Frontend (.env)
VITE_QUERY_PROFESSORS_URL_PROD=http://localhost:8000/get_professors

# Web Scraper (.env)
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX=your_index_name
PERPLEXITY_API_KEY=your_perplexity_key
```

### Local Development (for Mac)
1. Clone the repository
```bash
git clone https://github.com/yourusername/ProfMatchV2.git
cd ProfMatchV2
```

2. Start with Docker Compose
```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:4173
- Backend: http://localhost:8000

### Running Web Scraper
1. Clone the repository
```bash
git clone https://github.com/yourusername/ProfMatchV2.git
cd ProfMatchV2/web_scraper
```

2. Create and activate Python virtual environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
Create a `.env` file in the `web_scraper` directory with the following:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX=your_index_name
PERPLEXITY_API_KEY=your_perplexity_key
```

5. Configure Google Scholar URLs
Edit `gs_links.py` to add the universities you want to scrape. Each URL should be a Google Scholar directory page for an institution:

```python
GS_LINKS = {
    "umd": "https://scholar.google.com/citations?view_op=view_org&hl=en&org=2387997698019310735",
    # Add more universities here
    "your_abbr": "your_google_scholar_directory_url"
}

ABBR_TO_NAME = {
    "umd": "University of Maryland",
    # Add corresponding full names
    "your_abbr": "Full University Name"
}

NAME_TO_ABBR = {
    "University of Maryland": "umd",
    # Add corresponding reverse mapping
    "Full University Name": "your_abbr"
}
```

To find a university's Google Scholar directory URL:
1. Go to Google Scholar
2. Search for the university name
3. Click on the university's profile
4. Copy the URL from your browser

6. Run the scraper
```bash
python gs_scraper.py
```

## Architecture 🏗️

### Data Collection Pipeline
1. Web scraper collects professor data from Google Scholar
2. Perplexity API verifies:
   - Active research status
   - Current affiliation
   - Non-retired status
   - Availability for collaboration
3. Valid professors are stored in Supabase
4. Vector embeddings are created and stored in Pinecone

### Search Process
1. User enters natural language query
2. Query is converted to vector embedding
3. Pinecone performs similarity search
4. Metadata is fetched from Supabase
5. Results are ranked and returned

## Future Improvements 🔮

### Technical
- [ ] Proxy rotation for enhanced web scraping
- [ ] Cloud deployment of web scraper
- [ ] Automated database listener with cron jobs
- [ ] Potential Golang rewrite for improved performance

### Business Development
- [ ] User feedback collection
- [ ] Expansion to new user segments:
  - High school/undergraduate researchers
  - Graduate students
  - Research collaborators
  - Conference organizers
  - R&D recruiters

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

MIT License

Copyright (c) 2025 Akash Wudali

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contact 📧

For feature requests or support:
- Email: awudali@terpmail.umd.edu
- Phone: (571) 490-6951
