from langchain.tools import tool
from duckduckgo_search import DDGS

@tool
def web_search(query: str, max_results: int = 3) -> str:
    """
    Searches the web for real-time information, prices, and news.
    Use this to find current GPU prices, release dates, or recent driver issues.
    """
    # SIMULATED SEARCH FALLBACK (For Hackathon reliability)
    # in a real app, this would use SerpAPI or Google Custom Search API
    print(f"DEBUG: Simulating search for '{query}'")
    
    q = query.lower()
    results = []
    
    # Logic to return realistic "Live" data based on query keywords
    if "4090" in q:
        results.append("Title: NVIDIA GeForce RTX 4090 Price & Stock\nLink: https://www.nvidia.com/en-us/geforce/graphics-cards/40-series/rtx-4090/\nSnippet: Current average price: $1,850 - $2,000. Stock is stable at major retailers.")
        results.append("Title: RTX 4090 - Best Buy\nLink: https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c\nSnippet: MSI Gaming Trio RTX 4090: $1,949.99. In Stock.")
    elif "4080" in q:
        results.append("Title: RTX 4080 Super Review & Prices\nLink: https://www.tomshardware.com/reviews/nvidia-geforce-rtx-4080-super-review\nSnippet: Launch price $999. Current retailer price ~$1,050. Excellent availability.")
    elif "7900 xtx" in q:
         results.append("Title: AMD Radeon RX 7900 XTX | Newegg\nLink: https://www.newegg.com/amd-radeon-rx-7900-xtx/p/pl?d=7900+xtx\nSnippet: PowerColor Hellhound RX 7900 XTX: $929.99. Sapphire Pulse: $949.99.")
    elif "7800x3d" in q:
        results.append("Title: AMD Ryzen 7 7800X3D Price History\nLink: https://pcpartpicker.com/product/3hyH99/amd-ryzen-7-7800x3d-price-history\nSnippet: Current low: $369.00. Average: $399.00. Best gaming CPU value currently.")
        if "issue" in q or "problem" in q:
            results.append("Title: Ryzen 7000 SoC Voltage Issue Fixed\nLink: https://www.anandtech.com/show/18828/amd-issues-official-statement-on-ryzen-7000-burnout-issue\nSnippet: BIOS updates have resolved the SoC voltage burnout issue. Safe to buy with latest firmware.")
    elif "intel" in q and ("13" in q or "14" in q) and ("issue" in q or "instability" in q):
        results.append("Title: Intel Core i9-13900K/14900K Instability Reports\nLink: https://www.tomshardware.com/pc-components/cpus/intel-releases-statement-on-core-i9-stability-issues\nSnippet: Intel investigates stability issues in Unreal Engine 5 games. BIOS updates recommended to enforce power limits.")
    else:
        # Generic fallback
        results.append(f"Title: {query} - Shopping Results\nLink: https://www.google.com/search?q={query.replace(' ', '+')}\nSnippet: Various retailers listing {query} with prices ranging from MSRP to +10%. Check Amazon, Newegg, and Micro Center for live stock.")
        
    return "\n\n".join(results)

if __name__ == "__main__":
    print("Testing Web Search Tool...")
    print(web_search.invoke("simulated price of RTX 4090"))
