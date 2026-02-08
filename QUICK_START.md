# BuildBuddy AI - Quick Start Guide

## One-Command Startup

### Windows
```bash
START.bat
```

### Mac/Linux
```bash
bash start.sh
```

Both commands will:
1. ✅ Start FastAPI backend on `http://localhost:8000`
2. ✅ Start Next.js frontend on `http://localhost:3000`
3. ✅ Open your browser (if in WSL/remote, navigate manually)

---

## First Time Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- Google Cloud credentials configured (`gcloud auth application-default login`)

### Environment Variables (.env file)
Create a `.env` file in the project root:

```
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
VERTEX_SEARCH_DATA_STORE_ID=your-data-store-id
GEMINI_MODEL=gemini-2.0-flash-exp
```

### Install Dependencies

**Backend:**
```bash
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

---

## Using the Interface

### Access the UI
Open your browser: **http://localhost:3000**

### Two Modes

#### 1. **Reasoning Mode** (Recommended for Competition)
Shows the full Build → Critique → Improve pipeline with visible reasoning.

**Try this:**
```
Build me a $1200 gaming PC for 1440p 120fps
```

**What you'll see:**
- **Stage 1 (Build)**: Initial PC configuration + tools used + budget allocation
- **Stage 2 (Critique)**: Problems found (bottlenecks, price risks, Reddit consensus)
- **Stage 3 (Improve)**: Changes made to fix concerns + revised budget
- **Final Build**: Complete parts list with pricing

#### 2. **Chat Mode**
Simple question/answer about PC components (traditional RAG).

**Try this:**
```
What's a good GPU for $500?
```

---

## API Endpoints

### Build PC with Reasoning (Multi-Agent Pipeline)
```bash
curl -X POST http://localhost:8000/build-pc \
  -H "Content-Type: application/json" \
  -d '{"query": "Build me a $1200 gaming PC", "verbose": true}'
```

**Response includes:**
- `build`: Final PC configuration
- `reasoning.stage_1_build`: Initial build + tool decisions
- `reasoning.stage_2_critique`: Problems found
- `reasoning.stage_3_improvements`: Revisions made

### Simple Chat
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What CPU should I get for gaming?"}'
```

### API Documentation
Visit: **http://localhost:8000/docs** (Swagger UI)

---

## Testing the System

### Option 1: Use the Web UI
1. Navigate to http://localhost:3000
2. Switch to "Reasoning Mode"
3. Type: `"Build me a $1200 gaming PC for 1440p 120fps"`
4. Watch the three agents work

### Option 2: Run Test Script
```bash
python test_multi_agent.py full
```

This tests the agents directly without the UI (faster, no latency).

### Option 3: Test Individual Agents
```bash
python test_multi_agent.py build      # Build Agent only
python test_multi_agent.py critique   # Build + Critique
python test_multi_agent.py improve    # Build + Critique + Improve
python test_multi_agent.py mock       # No API calls, just data flow
```

---

## Troubleshooting

### Backend fails to start
**Error**: `ModuleNotFoundError: No module named 'langchain_google_vertexai'`

**Solution**:
```bash
pip install -r requirements.txt
```

### "Backend is running" message but no response
**Error**: Connection refused at `localhost:8000`

**Solution**:
- Check if backend is actually running in its terminal
- Try: `curl http://localhost:8000/` to test
- Verify no other app is using port 8000

### Frontend shows "Cannot connect to backend"
**Error**: CORS error or connection timeout

**Solution**:
- Make sure backend is running: `http://localhost:8000/docs`
- Check that CORS is enabled (it is, in app.py)
- Try refreshing the frontend page

### Google Cloud authentication fails
**Error**: `403 Forbidden` or `unauthenticated`

**Solution**:
```bash
gcloud auth application-default login
```

### Vertex AI search not working
**Error**: Pipeline runs but returns mock data

**Solution**:
- Check VERTEX_SEARCH_DATA_STORE_ID in .env
- Verify data store exists in Google Cloud console
- Try test_multi_agent.py test first:
  ```bash
  python test_multi_agent.py full
  ```

---

## Performance Notes

- **Full pipeline latency**: ~80 seconds (4 Gemini calls × ~20 sec each)
- **Breakdown**:
  - Build Agent: ~25 seconds
  - Critique Agent: ~20 seconds
  - Improve Agent: ~20 seconds
  - Total: ~80 seconds

This is **intentional** and shows reasoning. Judges expect AI to "think."

---

## Demo Script (for Competition)

When presenting to judges:

1. **Start the app**: `START.bat` (or `bash start.sh`)
2. **Wait for startup** (takes ~30 seconds)
3. **Navigate to**: http://localhost:3000
4. **Say**: "I'm going to have BuildBuddy create a custom PC build using multi-step reasoning."
5. **Switch to Reasoning Mode** ⚡
6. **Type**: `"Build me a $1200 gaming PC for 1440p 120fps"`
7. **Watch it run through Build → Critique → Improve**
8. **Point out**:
   - "See how it identifies problems in its own build?"
   - "It's critiquing itself independently"
   - "Then it patches those issues with clear reasoning"
   - "That's genuine AI reasoning, not just retrieval"

This is your **"holy sh*t" moment** for judges.

---

## Customization

### Adjust reasoning temperatures (in app.py)
- **Build Agent**: `temperature=0.7` (creative but grounded)
- **Critique Agent**: `temperature=0.9` (more critical)
- **Improve Agent**: `temperature=0.7` (thoughtful)

Lower = more consistent, Higher = more creative

### Add more prompts
Edit the `*_PROMPT` variables in `app.py` to customize reasoning

### Change Gemini model
Update `GEMINI_MODEL` in `.env` or app.py

---

## Next Steps

1. ✅ **Test locally** using the startup script
2. ✅ **Try the Reasoning Mode** with sample queries
3. ✅ **Read the reasoning output** to understand the pipeline
4. ✅ **Adjust prompts** if needed for your use case
5. ✅ **Deploy to cloud** when ready (GCP Cloud Run, Vercel, etc.)

---

For detailed prompting documentation, see: `gemini_agents.py`
For integration details, see: `INTEGRATION_GUIDE.py`
For testing scripts, see: `test_multi_agent.py` and `TESTING_GUIDE.md`
