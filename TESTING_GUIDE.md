"""
TESTING GUIDE: Multi-Agent Pipeline

This guide shows how to test each agent independently and the full pipeline.
"""

# ============================================================================
# QUICK START
# ============================================================================

QUICK_START = """
Prerequisites:
✅ GOOGLE_CLOUD_PROJECT_ID set in .env
✅ GOOGLE_CLOUD_LOCATION set in .env (default: us-central1)
✅ Vertex AI credentials configured (gcloud auth application-default login)
✅ gemini_agents.py in your workspace

Then run:
    python test_multi_agent.py full

That's it. Watch the full Build → Critique → Improve pipeline in action.
"""

# ============================================================================
# TESTING MODES
# ============================================================================

TESTING_MODES = """
1. TEST BUILD AGENT ONLY
   python test_multi_agent.py build
   
   What it does:
   - Calls Build Agent
   - Validates JSON output
   - Checks for 'build' and 'reasoning' keys
   - Shows tool decisions and budget allocation
   
   Use this when:
   ✓ Debugging Build Agent prompt
   ✓ Checking if parts retrieval works
   ✓ Validating initial build quality

2. TEST BUILD + CRITIQUE
   python test_multi_agent.py critique
   
   What it does:
   - Runs Build Agent
   - Feeds output to Critique Agent
   - Shows concerns found
   - Validates JSON structure
   
   Use this when:
   ✓ Debugging Critique Agent prompt
   ✓ Checking if critique is finding real issues
   ✓ Validating concern detection

3. TEST ALL THREE AGENTS
   python test_multi_agent.py improve
   
   What it does:
   - Runs Build Agent
   - Runs Critique Agent on the build
   - Runs Improve Agent on the critique
   - Shows all three outputs
   
   Use this when:
   ✓ Debugging Improve Agent prompt
   ✓ Checking if revisions are sensible
   ✓ Validating budget changes

4. TEST FULL PIPELINE (RECOMMENDED)
   python test_multi_agent.py full
   
   What it does:
   - Runs all three agents
   - Generates summary report
   - Shows budget before/after
   - Counts concerns and revisions
   - Displays final build
   
   Use this when:
   ✓ First time running
   ✓ Validating entire system
   ✓ Preparing for demo

5. TEST MOCK MODE (NO GEMINI CALLS)
   python test_multi_agent.py mock
   
   What it does:
   - Shows mock data without calling Gemini
   - Useful for testing when API quota is exhausted
   - Validates data structure assumptions
   
   Use this when:
   ✓ Debugging without API costs
   ✓ Checking data formats
   ✓ Validating parsing logic
"""

# ============================================================================
# EXPECTED OUTPUT
# ============================================================================

EXPECTED_OUTPUT = """
When you run 'python test_multi_agent.py full', you'll see:

════════════════════════════════════════════════════════════════════
  AGENT 1: BUILD AGENT
════════════════════════════════════════════════════════════════════

📥 Input Query: Build me a $1200 gaming PC for 1440p 120fps
🔧 Temperature: 0.7 (creative but grounded)
⏳ Calling Gemini Build Agent...

{JSON output of initial build}

✅ Build Agent returned 7 parts with $1200 budget
✅ Identified 3 tool decisions

════════════════════════════════════════════════════════════════════
  AGENT 2: CRITIQUE AGENT
════════════════════════════════════════════════════════════════════

📥 Reviewing initial build from Stage 1...
🔧 Temperature: 0.9 (more critical, less constrained)
⏳ Calling Gemini Critique Agent...

{JSON output of critique}

✅ Critique Agent found 5 concerns
   Overall: Build is solid but has bottleneck risk

   1. GPU bottlenecked by CPU at 1440p
   2. Thermal paste is overpriced
   3. NVIDIA limits streaming upgrades

════════════════════════════════════════════════════════════════════
  AGENT 3: IMPROVE AGENT
════════════════════════════════════════════════════════════════════

📥 Initial build from Stage 1 + Critique from Stage 2...
🔧 Temperature: 0.7 (thoughtful revision)
⏳ Calling Gemini Improve Agent...

{JSON output of improvements}

✅ Improve Agent made 2 revisions
   Revised budget: $1165

   1. RTX 4070 → RTX 4070 Super (fix bottleneck)
   2. $50 paste → $15 paste (cost optimization)

════════════════════════════════════════════════════════════════════
  PIPELINE SUMMARY
════════════════════════════════════════════════════════════════════

✅ Full pipeline completed successfully

📊 Results:
   • Initial Build Budget: $1200
   • Final Build Budget: $1165
   • Budget Adjusted: $35
   • Concerns Found: 5
   • Revisions Made: 2

💾 Final Build:
   1. AMD Ryzen 7 5700X3D - $299
   2. RTX 4070 Super - $619
   3. G.Skill Trident Z5 32GB DDR5 - $120
   4. Samsung 990 Pro 1TB NVMe - $80
   5. Corsair RM850x - $115
"""

# ============================================================================
# DEBUGGING TIPS
# ============================================================================

DEBUGGING_TIPS = """
Problem: "ModuleNotFoundError: No module named 'gemini_agents'"
Solution:
  - Make sure gemini_agents.py is in the same directory as test_multi_agent.py
  - Or add the path: import sys; sys.path.insert(0, '/path/to/project')

Problem: "WARNING: Could not parse Build Agent response as JSON"
Solution:
  - Gemini might be returning text, not JSON
  - Check if prompt is asking for JSON format (it should be in the prompt)
  - Try reducing context/data size if response is too long
  - Increase temperature if response is too structured

Problem: "Build Agent failed: GOOGLE_CLOUD_PROJECT_ID not set"
Solution:
  - Check .env file has GOOGLE_CLOUD_PROJECT_ID and GOOGLE_CLOUD_LOCATION
  - Run: echo %GOOGLE_CLOUD_PROJECT_ID% (Windows)
  - Or: echo $GOOGLE_CLOUD_PROJECT_ID (Linux/Mac)
  - If not set: gcloud config set project YOUR_PROJECT_ID

Problem: "403 Forbidden: Permission denied on resource"
Solution:
  - Ensure your Google Cloud account has Vertex AI access
  - Check PROJECT_ID matches your GCP project
  - Verify VERTEX_SEARCH_DATA_STORE_ID is correct (if using search)

Problem: Pipeline is slow (3+ minutes)
Solution:
  - This is normal; each Gemini call takes ~20-30 seconds
  - 4 agents × 30 seconds = ~2 minutes
  - To speed up: test individual agents instead of full pipeline
  - In production, consider caching/parallel execution

Problem: Different output each time
Solution:
  - This is EXPECTED! Temperature=0.7-0.9 means creative, not deterministic
  - If you want consistent output for testing, lower temperature to 0.1
  - But judges want to see reasoning diversity, so keep temps as-is
"""

# ============================================================================
# INTEGRATION CHECKLIST (After Testing)
# ============================================================================

INTEGRATION_INTO_APP = """
Once tests pass, integrate into app.py:

1. Copy the multi-agent logic into a new endpoint:
   
   @app.post("/api/build-pc-v2")
   async def build_pc_reasoning(request: BuildRequest):
       return await test_build_agent()  # use actual integration code
   
   Note: Keep old /api/build-pc endpoint for backwards compatibility

2. Add BuildRequest model if not already present:
   
   class BuildRequest(BaseModel):
       query: str
       verbose: bool = False
   
3. Update frontend to call /api/build-pc-v2 with verbose=true

4. Display reasoning pipeline in UI:
   - Show "Build Stage" → parts list
   - Show "Critique Stage" → concerns found
   - Show "Improve Stage" → changes made
   - Show "Final Build" → revised parts

5. Test end-to-end:
   - Frontend → FastAPI → Gemini agents → Frontend

Optional:
- Add response caching for same queries
- Add query deduplication
- Monitor API costs (4 calls per request = ~4x normal usage)
"""

# ============================================================================
# PERFORMANCE EXPECTATIONS
# ============================================================================

PERFORMANCE = """
Latency:
- Build Agent: ~25 seconds
- Critique Agent: ~20 seconds  
- Improve Agent: ~20 seconds
- Master Orchestrator: ~15 seconds
- Total: ~80 seconds per request

Improvement Options:
1. Parallel agents (if they don't depend on each other)
   - This would reduce to ~30 seconds
   - But then you lose the narrative flow

2. Caching (for repeated queries)
   - Store results for "Build $1200 gaming PC"
   - Return instant results for same query

3. Reduce context size
   - Fewer retrieved parts (use top 5 instead of 10)
   - Shorter market data snippets
   - Would reduce to ~60 seconds

For the competition:
- Judges expect some latency for reasoning
- 80 seconds is reasonable and shows thinking
- Don't over-optimize for speed; prioritize output quality

Cost:
- Each full pipeline = 4 Gemini API calls
- Gemini 2.0 Flash: ~1/100 of older models
- Estimate: ~$0.01 per request
- Not prohibitive for a hackathon
"""

# ============================================================================
# REAL-WORLD TESTING SCRIPT
# ============================================================================

REAL_WORLD_TEST = """
After testing with test_multi_agent.py, test with real queries:

import asyncio
from test_multi_agent import test_full_pipeline

test_queries = [
    "Build me a $800 budget gaming PC",
    "I want a $3000 streaming and gaming workstation",
    "Need a $1500 PC for 4K video editing",
    "Build a $500 office/productivity PC"
]

for query in test_queries:
    print(f"\\nTesting: {query}")
    test_full_pipeline()  # Test goes here
    print(f"✅ Passed")

This validates that the system works across budget ranges and use cases.
"""

if __name__ == "__main__":
    print(__doc__)
    print(QUICK_START)
    print(TESTING_MODES)
    print(EXPECTED_OUTPUT)
    print(DEBUGGING_TIPS)
    print(INTEGRATION_INTO_APP)
    print(PERFORMANCE)
