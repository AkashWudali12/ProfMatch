# ProfMatch 🎓

Find your next research opportunity with AI-powered professor matching.

## Overview 🌟

ProfMatch simplifies the process of finding research opportunities by using AI to match students with active professors based on research interests. No more navigating outdated academic directories or spending hours searching through scattered information.

## Features ✨

- Natural language search for research interests
- Real-time professor matching using vector similarity
- Verified, up-to-date professor information
- Email contacts for reaching out
- Daily refreshed database of active researchers

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
PERPLEXITY_API_KEY=your_perplexity_key

# Frontend (.env)
VITE_BACKEND_URL=http://localhost:8000
VITE_QUERY_PROFESSORS_URL=http://localhost:8000/get_professors
```

### Local Development
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

[Add your license here]

## Contact 📧

For feature requests or support:
- Email: awudali@terpmail.umd.edu
- Phone: (571) 490-6951
