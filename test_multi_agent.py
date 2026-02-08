"""
Test script for multi-agent pipeline.
Run this FIRST to validate each agent independently before integrating into app.py
"""

import json
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Mock data for testing without full Vertex AI setup
MOCK_RETRIEVED_PARTS = """
1. CPU: AMD Ryzen 7 5700X3D - $299 - Best gaming CPU for 1440p
2. GPU: RTX 4070 - $599 - Good balance of performance and price
3. RAM: G.Skill Trident Z5 32GB DDR5 - $120 - Fast and reliable
4. Storage: Samsung 990 Pro 1TB NVMe - $80 - Fast SSD
5. PSU: Corsair RM850x - $115 - 850W Gold rated, reliable
6. Case: NZXT H510 Flow - $85 - Good thermals and aesthetics
7. CPU Cooler: Noctua NH-D15 - $90 - Best air cooling option
8. Thermal Paste: Arctic MX-6 - $15 - Adequate thermal paste
"""

MOCK_WEB_RESULTS = """
- RTX 4070 prices average $579-619 according to PCPartPicker
- DDR5 RAM prices dropped 15% in January 2025
- Ryzen 7 5700X3D availability is good, no stock issues
- Reddit consensus: RTX 4070 vs RTX 4070 Super is debated (value vs performance)
- Gaming at 1440p: 1200 budget is tight for 120+ FPS gaming
"""

MOCK_REDDIT_DATA = """
r/buildapc threads:
- "RTX 4070 pairs better with 5700X3D than 4070 Super for value"
- "32GB RAM overkill for gaming, 16GB fine, save $60"
- "Thermal paste doesn't matter much, stock cooler paste works"
- "Corsair PSU is reliable, good choice"
- "NZXT H510 has okay airflow, but Meshify C is better"
"""

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def extract_budget(user_query: str) -> str:
    """Extract budget from query"""
    import re
    match = re.search(r'\$?(\d{3,5})', user_query)
    return match.group(1) if match else "1000"

def extract_goal(user_query: str) -> str:
    """Extract goal from query"""
    return user_query[:60].rstrip(".") + "..."

def pretty_print(title, content):
    """Pretty print section headers"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")
    if isinstance(content, dict):
        print(json.dumps(content, indent=2))
    else:
        print(content)

def parse_json_response(response_text: str, agent_name: str) -> dict:
    """
    Safely parse JSON from Gemini response.
    Gemini might wrap it in markdown code blocks.
    """
    try:
        # Try direct parsing first
        return json.loads(response_text)
    except json.JSONDecodeError:
        # Try extracting from markdown code block
        if "```json" in response_text:
            start = response_text.find("```json") + 7
            end = response_text.find("```", start)
            json_str = response_text[start:end].strip()
            return json.loads(json_str)
        elif "```" in response_text:
            start = response_text.find("```") + 3
            end = response_text.find("```", start)
            json_str = response_text[start:end].strip()
            return json.loads(json_str)
        else:
            print(f"⚠️  WARNING: Could not parse {agent_name} response as JSON")
            print(f"Response was: {response_text[:200]}...")
            return {"error": "Could not parse JSON", "raw_response": response_text[:500]}

# ============================================================================
# TEST 1: Build Agent Only
# ============================================================================

def test_build_agent():
    """Test the Build Agent independently"""
    from langchain_google_vertexai import ChatVertexAI
    from gemini_agents import BUILD_AGENT_PROMPT
    
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " AGENT 1: BUILD AGENT ".center(68) + "║")
    print("╚" + "="*68 + "╝")
    
    user_query = "Build me a $1200 gaming PC for 1440p 120fps"
    
    try:
        llm = ChatVertexAI(
            project=os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
            location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
            model_name="gemini-2.0-flash-exp",
            temperature=0.7,
        )
        
        prompt = BUILD_AGENT_PROMPT.format(
            user_requirements=user_query,
            retrieved_parts=MOCK_RETRIEVED_PARTS,
            web_search_results=MOCK_WEB_RESULTS
        )
        
        print(f"\n📥 Input Query: {user_query}")
        print(f"🔧 Temperature: 0.7 (creative but grounded)")
        print(f"⏳ Calling Gemini Build Agent...")
        
        response = llm.invoke(prompt)
        response_text = response.content
        
        build_output = parse_json_response(response_text, "Build Agent")
        
        pretty_print("Agent 1 Output: Initial Build", build_output)
        
        # Validate structure
        if "build" in build_output:
            parts = build_output.get("build", {}).get("parts", [])
            budget = build_output.get("build", {}).get("total_budget", 0)
            print(f"\n✅ Build Agent returned {len(parts)} parts with ${budget} budget")
            
            if "reasoning" in build_output:
                tools_used = build_output.get("reasoning", {}).get("tool_decisions", [])
                print(f"✅ Identified {len(tools_used)} tool decisions")
            
            return build_output
        else:
            print("❌ Build Agent output missing 'build' key")
            return None
            
    except Exception as e:
        print(f"❌ Build Agent failed: {str(e)}")
        print(f"   Make sure GOOGLE_CLOUD_PROJECT_ID and VERTEX_SEARCH_DATA_STORE_ID are set")
        return None

# ============================================================================
# TEST 2: Critique Agent (uses Build Agent output)
# ============================================================================

def test_critique_agent(initial_build: dict):
    """Test the Critique Agent against the initial build"""
    from langchain_google_vertexai import ChatVertexAI
    from gemini_agents import CRITIQUE_AGENT_PROMPT
    
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " AGENT 2: CRITIQUE AGENT ".center(68) + "║")
    print("╚" + "="*68 + "╝")
    
    try:
        llm = ChatVertexAI(
            project=os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
            location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
            model_name="gemini-2.0-flash-exp",
            temperature=0.9,  # More critical
        )
        
        prompt = CRITIQUE_AGENT_PROMPT.format(
            build_json=json.dumps(initial_build.get("build", {})),
            market_data=MOCK_WEB_RESULTS,
            reddit_data=MOCK_REDDIT_DATA,
            original_requirements="Build me a $1200 gaming PC for 1440p 120fps"
        )
        
        print(f"\n📥 Reviewing initial build from Stage 1...")
        print(f"🔧 Temperature: 0.9 (more critical, less constrained)")
        print(f"⏳ Calling Gemini Critique Agent...")
        
        response = llm.invoke(prompt)
        response_text = response.content
        
        critique_output = parse_json_response(response_text, "Critique Agent")
        
        pretty_print("Agent 2 Output: Critique & Concerns", critique_output)
        
        # Validate structure
        if "critique" in critique_output:
            concerns = critique_output.get("critique", {}).get("concerns", [])
            assessment = critique_output.get("critique", {}).get("overall_assessment", "")
            print(f"\n✅ Critique Agent found {len(concerns)} concerns")
            print(f"   Overall: {assessment}")
            
            for i, concern in enumerate(concerns[:3], 1):
                print(f"   {i}. {concern.get('issue', 'Unknown')}")
            
            return critique_output
        else:
            print("❌ Critique Agent output missing 'critique' key")
            return None
            
    except Exception as e:
        print(f"❌ Critique Agent failed: {str(e)}")
        return None

# ============================================================================
# TEST 3: Improve Agent (uses Build + Critique)
# ============================================================================

def test_improve_agent(initial_build: dict, critique: dict):
    """Test the Improve Agent"""
    from langchain_google_vertexai import ChatVertexAI
    from gemini_agents import IMPROVE_AGENT_PROMPT
    
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " AGENT 3: IMPROVE AGENT ".center(68) + "║")
    print("╚" + "="*68 + "╝")
    
    try:
        llm = ChatVertexAI(
            project=os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
            location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
            model_name="gemini-2.0-flash-exp",
            temperature=0.7,
        )
        
        prompt = IMPROVE_AGENT_PROMPT.format(
            original_build=json.dumps(initial_build.get("build", {})),
            critique_feedback=json.dumps(critique.get("critique", {})),
            market_data=MOCK_WEB_RESULTS,
            original_requirements="Build me a $1200 gaming PC for 1440p 120fps"
        )
        
        print(f"\n📥 Initial build from Stage 1 + Critique from Stage 2...")
        print(f"🔧 Temperature: 0.7 (thoughtful revision)")
        print(f"⏳ Calling Gemini Improve Agent...")
        
        response = llm.invoke(prompt)
        response_text = response.content
        
        improve_output = parse_json_response(response_text, "Improve Agent")
        
        pretty_print("Agent 3 Output: Revisions & Improved Build", improve_output)
        
        # Validate structure
        if "revisions" in improve_output:
            changes = improve_output.get("revisions", {}).get("changes_made", [])
            revised_build = improve_output.get("revisions", {}).get("revised_build", {})
            print(f"\n✅ Improve Agent made {len(changes)} revisions")
            print(f"   Revised budget: ${revised_build.get('total_budget', 'N/A')}")
            
            for i, change in enumerate(changes[:3], 1):
                orig = change.get("original_part", "?")
                revised = change.get("revised_part", "?")
                print(f"   {i}. {orig} → {revised}")
            
            return improve_output
        else:
            print("❌ Improve Agent output missing 'revisions' key")
            return None
            
    except Exception as e:
        print(f"❌ Improve Agent failed: {str(e)}")
        return None

# ============================================================================
# TEST 4: Full Pipeline
# ============================================================================

def test_full_pipeline():
    """Run all three agents in sequence"""
    print("\n\n")
    print("╔" + "="*68 + "╗")
    print("║" + " FULL MULTI-AGENT PIPELINE TEST ".center(68) + "║")
    print("╚" + "="*68 + "╝")
    
    # Stage 1
    build = test_build_agent()
    if not build:
        print("\n❌ Pipeline stopped: Build Agent failed")
        return
    
    # Stage 2
    critique = test_critique_agent(build)
    if not critique:
        print("\n❌ Pipeline stopped: Critique Agent failed")
        return
    
    # Stage 3
    revisions = test_improve_agent(build, critique)
    if not revisions:
        print("\n❌ Pipeline stopped: Improve Agent failed")
        return
    
    # Summary
    print("\n\n")
    print("╔" + "="*68 + "╗")
    print("║" + " PIPELINE SUMMARY ".center(68) + "║")
    print("╚" + "="*68 + "╝")
    
    initial_budget = build.get("build", {}).get("total_budget", 0)
    final_budget = revisions.get("revisions", {}).get("revised_build", {}).get("total_budget", 0)
    changes = len(revisions.get("revisions", {}).get("changes_made", []))
    concerns = len(critique.get("critique", {}).get("concerns", []))
    
    print(f"\n✅ Full pipeline completed successfully")
    print(f"\n📊 Results:")
    print(f"   • Initial Build Budget: ${initial_budget}")
    print(f"   • Final Build Budget: ${final_budget}")
    print(f"   • Budget Adjusted: ${initial_budget - final_budget}")
    print(f"   • Concerns Found: {concerns}")
    print(f"   • Revisions Made: {changes}")
    
    print(f"\n💾 Final Build:")
    final_parts = revisions.get("revisions", {}).get("revised_build", {}).get("parts", [])
    for i, part in enumerate(final_parts[:5], 1):
        name = part.get("name", "Unknown")
        price = part.get("price", "N/A")
        print(f"   {i}. {name} - ${price}")

# ============================================================================
# COMMAND-LINE INTERFACE
# ============================================================================

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "build":
            test_build_agent()
        elif sys.argv[1] == "critique":
            build = test_build_agent()
            if build:
                test_critique_agent(build)
        elif sys.argv[1] == "improve":
            build = test_build_agent()
            if build:
                critique = test_critique_agent(build)
                if critique:
                    test_improve_agent(build, critique)
        elif sys.argv[1] == "full":
            test_full_pipeline()
        elif sys.argv[1] == "mock":
            print("\n⚠️  MOCK MODE (no Gemini calls, just shows data flow)")
            print("Run with 'python test_multi_agent.py full' for real testing")
            print(f"\nMock retrieved parts:\n{MOCK_RETRIEVED_PARTS}")
            print(f"\nMock web results:\n{MOCK_WEB_RESULTS}")
            print(f"\nMock Reddit data:\n{MOCK_REDDIT_DATA}")
    else:
        # Default: run full pipeline
        test_full_pipeline()

if __name__ == "__main__":
    main()
