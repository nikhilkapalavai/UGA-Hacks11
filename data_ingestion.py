import json
import os
import glob
import hashlib

# Mapping filenames to component types
COMPONENT_MAP = {
    "cpu.json": "CPU",
    "video-card.json": "GPU",
    "motherboard.json": "Motherboard",
    "memory.json": "RAM",
    "internal-hard-drive.json": "Storage",
    "power-supply.json": "PSU",
    "case.json": "Case",
    "cpu-cooler.json": "CPU Cooler",
    "monitor.json": "Monitor",
    "mouse.json": "Mouse",
    "keyboard.json": "Keyboard",
    "headphones.json": "Headphones",
    "external-hard-drive.json": "External Storage",
    "fan-controller.json": "Fan Controller",
    "optical-drive.json": "Optical Drive",
    "sound-card.json": "Sound Card",
    "speakers.json": "Speakers",
    "thermal-paste.json": "Thermal Paste",
    "ups.json": "UPS",
    "webcam.json": "Webcam",
    "wired-network-card.json": "Wired Network Card",
    "wireless-network-card.json": "Wireless Network Card",
    "case-fan.json": "Case Fan",
    "case-accessory.json": "Case Accessory"
}

def generate_id(text):
    """Generates a stable ID based on text content."""
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def load_and_process_data(input_dir, output_file):
    master_data = []
    
    # Get all JSON files in the directory
    json_files = glob.glob(os.path.join(input_dir, "*.json"))
    
    print(f"Found {len(json_files)} JSON files.")

    for file_path in json_files:
        filename = os.path.basename(file_path)

        # --- PROCESS REDDIT DATA ---
        if "reddit" in filename.lower():
            print(f"Processing {filename} as Community Build Advice...")
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    items = json.load(f)
                
                for i, item in enumerate(items):
                    prompt = item.get("prompt", "")
                    completion = item.get("completion", "")
                    
                    if not prompt or not completion:
                        continue
                        
                    # formatted content for RAG
                    text_content = f"User Request: {prompt}\n\nExpert Recommendation: {completion}"
                    
                    # formatted content for RAG
                    text_content = f"User Request: {prompt}\n\nExpert Recommendation: {completion}"
                    
                    doc = {
                        "id": f"reddit_{generate_id(prompt)[:12]}",
                        "structData": {
                            "title": f"Community Build Advice: {prompt[:50]}...",
                            "description": text_content,
                            "url": f"https://reddit.com/advice/{i}", 
                            "type": "Community Advice",
                            "source": "Reddit",
                            "price": "N/A"
                        }
                    }
                    master_data.append(doc)
            except Exception as e:
                print(f"Error processing Reddit file {filename}: {e}")
            continue

        # --- PROCESS PC PART DATA ---
        component_type = COMPONENT_MAP.get(filename, filename.replace(".json", "").replace("-", " ").title())
        print(f"Processing {filename} as {component_type}...")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                items = json.load(f)
                
            if not isinstance(items, list):
                print(f"Warning: {filename} does not contain a list of items. Skipping.")
                continue

            for item in items:
                # 1. rich description
                description_parts = [f"Component Type: {component_type}"]
                for key, value in item.items():
                    if value is not None and value != "":
                        val_str = str(value)
                        formatted_key = key.replace("_", " ").title()
                        description_parts.append(f"{formatted_key}: {val_str}")
                
                text_content = ". ".join(description_parts)

                # 2. Consistent Schema
                # Remove complex nested objects from root to prevent schema drift
                # Put everything complex into structData
                
                name = item.get("name", "Unknown Component")
                price = item.get("price")
                
                # Sanitize ID
                item_id = f"{component_type}_{str(name).replace(' ', '_')}"
                # Ensure ID is safe characters only
                item_id = "".join([c if c.isalnum() or c in "-_" else "_" for c in item_id])[:128]

                doc = {
                    "id": item_id,
                    "structData": {
                        "title": name,
                        "description": text_content,
                        "content": text_content, # Explicit content field for search
                        "url": f"https://pcpartpicker.com/product/{item_id}",
                        "filepath": filename,
                        "type": component_type,
                        "price": str(price) if price else "N/A",
                        "specs": json.dumps(item) # Stringify specs to avoid schema issues
                    }
                }
                
                master_data.append(doc)

        except Exception as e:
            print(f"Error processing {filename}: {e}")

    # Save to JSONL
    with open(output_file, "w", encoding="utf-8") as f:
        for entry in master_data:
            json.dump(entry, f)
            f.write("\n")

    print(f"Successfully processed {len(master_data)} items into {output_file}")

if __name__ == "__main__":
    INPUT_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_FILE = os.path.join(INPUT_DIR, "master_parts.jsonl")
    
    load_and_process_data(INPUT_DIR, OUTPUT_FILE)
