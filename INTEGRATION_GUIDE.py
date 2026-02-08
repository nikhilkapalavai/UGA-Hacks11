"""
INTEGRATION GUIDE: Multi-Agent Pipeline into app.py

This file shows EXACTLY how to refactor your existing FastAPI endpoint
to use the Build → Critique → Improve pipeline.
"""

# ============================================================================
# STEP 1: Add helper functions to extract meaning from user queries
# ============================================================================

HELPER_FUNCTIONS = """
def extract_budget(user_query: str) -> str:
    '''Extract budget amount from query like "$1200" or "1200 dollar"'''
    import re
    match = re.search(r'\$?(\d{3,5})', user_query)
    return match.group(1) if match else "1000"

def extract_usecase(user_query: str) -> str:
    '''Extract use case: gaming, streaming, workstation, etc.'''
    cases = ["gaming", "streaming", "workstation", "content creation", "office"]
    for case in cases:
        if case.lower() in user_query.lower():
            return case
    return "general"

def extract_goal(user_query: str) -> str:
    '''Generate a title from the query'''
    return user_query[:50].rstrip(".") + "..."
"""

# ============================================================================
# STEP 2: Refactor your main endpoint to use multi-agent pipeline
# ============================================================================

REFACTORED_ENDPOINT = """
from fastapi import FastAPI
from pydantic import BaseModel
import json
from gemini_agents import (
    BUILD_AGENT_PROMPT,
    CRITIQUE_AGENT_PROMPT,
    IMPROVE_AGENT_PROMPT,
    MASTER_ORCHESTRATOR_PROMPT
)

app = FastAPI()

class BuildRequest(BaseModel):
    query: str
    verbose: bool = False  # Include full reasoning output

class BuildResponse(BaseModel):
    build: dict
    reasoning: dict
    ui_data: dict
    status: str

@app.post("/api/build-pc")
async def build_pc_with_reasoning(request: BuildRequest) -> BuildResponse:
    '''
    Multi-agent reasoning pipeline: Build → Critique → Improve
    '''
    
    retriever = get_retriever()
    
    # ========== STAGE 1: BUILD AGENT ==========
    print("[Agent 1] Building initial PC configuration...")
    
    # Gather context
    retrieved_parts = retriever.invoke(request.query)
    web_search_results = search_web(
        f"PC gaming parts {extract_budget(request.query)} budget pricing 2025"
    )
    
    # Call Build Agent
    build_prompt = BUILD_AGENT_PROMPT.format(
        user_requirements=request.query,
        retrieved_parts=format_parts_for_prompt(retrieved_parts),
        web_search_results=format_web_results_for_prompt(web_search_results)
    )
    
    build_response = chat_vertex_ai.invoke(build_prompt)
    
    try:
        initial_build = json.loads(build_response.content)
    except json.JSONDecodeError:
        # Fallback if response isn't valid JSON
        initial_build = {
            "reasoning": {"parsed_requirements": request.query},
            "build": {"parts": [], "total_budget": 0}
        }
    
    if request.verbose:
        print(f"[Agent 1 Output] Tools used: {initial_build.get('reasoning', {}).get('tool_decisions', [])}")
    
    # ========== STAGE 2: CRITIQUE AGENT ==========
    print("[Agent 2] Critiquing initial build...")
    
    critique_prompt = CRITIQUE_AGENT_PROMPT.format(
        build_json=json.dumps(initial_build.get("build", {})),
        market_data=format_web_results_for_prompt(web_search_results),
        reddit_data=format_parts_for_prompt(retriever.invoke("reddit advice building PC")),
        original_requirements=request.query
    )
    
    critique_response = chat_vertex_ai.invoke(critique_prompt)
    
    try:
        critique = json.loads(critique_response.content)
    except json.JSONDecodeError:
        critique = {"critique": {"concerns": [], "overall_assessment": "No critique returned"}}
    
    if request.verbose:
        concerns = critique.get("critique", {}).get("concerns", [])
        print(f"[Agent 2 Output] Found {len(concerns)} concerns")
        for concern in concerns[:3]:
            print(f"  - {concern.get('issue', 'Unknown')}")
    
    # ========== STAGE 3: IMPROVE AGENT ==========
    print("[Agent 3] Improving build based on critique...")
    
    improve_prompt = IMPROVE_AGENT_PROMPT.format(
        original_build=json.dumps(initial_build.get("build", {})),
        critique_feedback=json.dumps(critique.get("critique", {})),
        market_data=format_web_results_for_prompt(web_search_results),
        original_requirements=request.query
    )
    
    improve_response = chat_vertex_ai.invoke(improve_prompt)
    
    try:
        revisions = json.loads(improve_response.content)
    except json.JSONDecodeError:
        revisions = {"revisions": {"changes_made": [], "revised_build": initial_build.get("build", {})}}
    
    if request.verbose:
        changes = revisions.get("revisions", {}).get("changes_made", [])
        print(f"[Agent 3 Output] Made {len(changes)} revisions")
        for change in changes[:3]:
            print(f"  - {change.get('original_part', '?')} → {change.get('revised_part', '?')}")
    
    # ========== STAGE 4: ORCHESTRATOR (Optional, for narrative polish) ==========
    print("[Orchestrator] Synthesizing narrative...")
    
    orchestrator_prompt = MASTER_ORCHESTRATOR_PROMPT.format(
        user_goal=extract_goal(request.query),
        user_request=request.query,
        agent1_output=json.dumps(initial_build),
        agent2_output=json.dumps(critique),
        agent3_output=json.dumps(revisions)
    )
    
    narrative_response = chat_vertex_ai.invoke(orchestrator_prompt)
    
    try:
        narrative = json.loads(narrative_response.content)
    except json.JSONDecodeError:
        narrative = {"narrative": {"core_story": "PC build generated through reasoning pipeline"}, "ui_data": {}}
    
    # ========== BUILD RESPONSE ==========
    final_build = revisions.get("revisions", {}).get("revised_build", initial_build.get("build", {}))
    
    response = BuildResponse(
        build=final_build,
        reasoning={
            "stage_1_initial_build": initial_build,
            "stage_2_critique": critique,
            "stage_3_improvements": revisions,
            "narrative": narrative.get("narrative", {})
        },
        ui_data=narrative.get("ui_data", {
            "comparison_table": "See full reasoning in reasoning.stage_1_initial_build vs stage_3_improvements",
            "concern_badges": [c.get("category", "Unknown") for c in critique.get("critique", {}).get("concerns", [])[:5]],
            "decision_tree": "User can view alternatives in improvements section"
        }),
        status="success"
    )
    
    print("[Pipeline Complete] Build ready for UI rendering")
    
    return response
"""

# ============================================================================
# STEP 3: Add formatting helpers for cleaner prompts
# ============================================================================

FORMATTING_HELPERS = """
def format_parts_for_prompt(retrieved_docs) -> str:
    '''Convert LangChain retriever output to clean text for prompts'''
    if not retrieved_docs:
        return "No parts data available"
    
    formatted = []
    for doc in retrieved_docs[:10]:  # Top 10 results
        content = doc.page_content if hasattr(doc, 'page_content') else str(doc)
        formatted.append(content)
    
    return "\\n".join(formatted)

def format_web_results_for_prompt(web_results) -> str:
    '''Convert web search results to clean text'''
    if not web_results:
        return "No web data available"
    
    # Assuming web search returns list of dicts with 'title' and 'snippet'
    formatted = []
    for result in web_results[:5]:  # Top 5 results
        if isinstance(result, dict):
            formatted.append(f"- {result.get('title', 'Untitled')}: {result.get('snippet', '')}")
        else:
            formatted.append(f"- {str(result)}")
    
    return "\\n".join(formatted)
"""

# ============================================================================
# STEP 4: Update your FastAPI response to expose reasoning in UI
# ============================================================================

FRONTEND_INTEGRATION = """
// In your Next.js frontend, update ChatInterface.tsx or similar:

// After calling /api/build-pc endpoint:
const response = await fetch('/api/build-pc', {
    method: 'POST',
    body: JSON.stringify({ query: userInput, verbose: true })
});

const data = await response.json();

// Render the pipeline visually:
<ReasoningPipeline>
    <Stage 
        name="Build"
        output={data.reasoning.stage_1_initial_build}
        hide_details={true}
        summary="Initial build created with {num_tools} tools"
    />
    <Stage
        name="Critique"
        output={data.reasoning.stage_2_critique}
        concerns={data.ui_data.concern_badges}
        summary="Found {num_concerns} potential issues"
    />
    <Stage
        name="Improve"
        output={data.reasoning.stage_3_improvements}
        changes={data.ui_data.changes_count}
        summary="{num_changes} revisions made to fix concerns"
    />
</ReasoningPipeline>

<FinalBuild parts={data.build} />
"""

# ============================================================================
# STEP 5: Testing script to validate pipeline
# ============================================================================

TEST_SCRIPT = """
import asyncio
import json
from app import build_pc_with_reasoning, BuildRequest

async def test_pipeline():
    '''Test the full multi-agent pipeline'''
    
    test_queries = [
        "Build me a $1200 gaming PC for 1440p 144fps",
        "I want a streaming setup for Twitch, $2000 budget",
        "Need a workstation for 3D rendering, $3000"
    ]
    
    for query in test_queries:
        print(f"\\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")
        
        request = BuildRequest(query=query, verbose=True)
        response = await build_pc_with_reasoning(request)
        
        print(f"\\nFinal Build:")
        print(f"  Total Budget: ${response.build.get('total_budget', 0)}")
        print(f"  Parts Count: {len(response.build.get('parts', []))}")
        
        print(f"\\nCritiques Found: {len(response.reasoning['stage_2_critique'].get('critique', {}).get('concerns', []))}")
        print(f"Revisions Made: {len(response.reasoning['stage_3_improvements'].get('revisions', {}).get('changes_made', []))}")
        
        print(f"\\nUI Badges: {response.ui_data.get('concern_badges', [])}")

if __name__ == "__main__":
    asyncio.run(test_pipeline())
"""

# ============================================================================
# STEP 6: Key integration checklist
# ============================================================================

INTEGRATION_CHECKLIST = """
✅ Action Items to Integrate Multi-Agent Pipeline:

1. [ ] Copy gemini_agents.py to your project
2. [ ] Add helper functions (extract_budget, extract_goal, etc.) to app.py
3. [ ] Add formatting helpers (format_parts_for_prompt, etc.)
4. [ ] Replace your current @app.post("/api/build-pc") with refactored version
5. [ ] Test with test_script.py (included above)
6. [ ] Update BuildResponse model if needed
7. [ ] Ensure chat_vertex_ai is initialized (from your existing code)
8. [ ] Update get_retriever() call (from your existing code)
9. [ ] Add web search function if not already present
10. [ ] Test end-to-end in frontend

Critical Notes:
- The pipeline makes 4 Gemini calls per request (Build, Critique, Improve, Orchestrate)
- This is more expensive than single call, but shows reasoning = judges love it
- Consider caching/memoization if you expect high load
- JSON parsing can fail; include fallback logic (shown above)
- Use verbose=false in production to skip logging, verbose=true to debug

Timeline:
- 30 min: Copy files and update endpoint
- 30 min: Test with script
- 15 min: Integrate with frontend
- Total: ~1 hour to full multi-agent system
"""

if __name__ == "__main__":
    print(__doc__)
    print(INTEGRATION_CHECKLIST)
