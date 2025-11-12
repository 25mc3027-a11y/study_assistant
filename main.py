import argparse
import json
import os
import sys
import google.generativeai as genai

# Add parent directory to path to find modules
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    from utils.pdf_utils import extract_text_from_pdf
    from agents.generation_agent import get_study_aids
    from agents.planner import create_revision_plan
except ImportError as e:
    print(f"Error importing modules: {e}. Make sure you are in the 'study_agent' directory.")
    sys.exit(1)

def main():
    """
    Main function to run the study agent from the command line.
    """
    parser = argparse.ArgumentParser(description="Autonomous Study Workflow Agent")
    parser.add_argument("pdf_file", help="Path to the PDF notes file.")
    args = parser.parse_args()

    # --- API Key Configuration ---
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        sys.exit(1)
    genai.configure(api_key=api_key)

    # --- Create output directory ---
    os.makedirs("outputs", exist_ok=True)
    
    try:
        # --- 1. Read PDF ---
        print(f"Reading PDF: {args.pdf_file}...")
        # Read as bytes
        with open(args.pdf_file, "rb") as f:
            pdf_bytes = f.read()
        pdf_text = extract_text_from_pdf(pdf_bytes)
        print("Successfully extracted text from PDF.")

        # --- 2. Generate Study Aids ---
        print("Calling Gemini API to generate study aids...")
        study_aids = get_study_aids(pdf_text)
        print("Successfully received study aids from Gemini.")
        
        # --- 3. Generate Plan ---
        topics = study_aids.get("topics", [])
        plan = create_revision_plan(topics)
        
        # --- 4. Save Outputs ---
        output_files = {
            "flashcards": study_aids.get("flashcards", []),
            "quizzes": study_aids.get("quiz", []),
            "planner": plan
        }

        for name, data in output_files.items():
            file_path = f"outputs/{name}.json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"Successfully saved {name} to {file_path}")

        print("\n--- Generation Complete! ---")
        print(f"Topics: {', '.join(topics)}")
        print(f"Generated {len(output_files['flashcards'])} flashcards.")
        print(f"Generated {len(output_files['quizzes'])} quiz questions.")
        print("Check the 'outputs' folder for your JSON files.")

    except Exception as e:
        print(f"\n--- An Error Occurred ---")
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()