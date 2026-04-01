import os
import base64
import json
import uuid
import traceback
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.cloud import storage
from sqlalchemy import create_engine, text

load_dotenv()

app = Flask(__name__)

# --- Configuration ---
API_KEY = os.getenv("GEMINI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")

genai_client = None 
storage_client = None
engine = None 

try:
    genai_client = genai.Client(api_key=API_KEY)
    storage_client = storage.Client()
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set in environment variables.")
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
except Exception as e:
    print(f"Initialization Error: {traceback.format_exc()}")

@app.route('/')
def home():
    if engine is None:
        return jsonify({"error": "Database engine not initialized."}), 500
    try:
        with engine.connect() as conn:
            # UPDATED: Querying zoo_animals instead of items
            query = text("""
                SELECT common_name, scientific_name, diet_type, habitat, fun_fact, wiki_summary_preview 
                FROM zoo_animals 
                LIMIT 20
            """)
            result = conn.execute(query)
            
            items = []
            for row in result:
                items.append({
                    "title": row[0],
                    "subtitle": row[1],
                    "category": row[2],
                    "bio": f"{row[3]} | {row[4]}",
                    "image_url": f"https://loremflickr.com/500/500/{row[0].replace(' ', ',')},animal",
                    "description": row[5]
                })
            return render_template('app.html', items=items)
    except Exception as e:
        return jsonify({"error": "Failed to fetch items", "details": str(e)}), 500

@app.route('/api/search', methods=['GET'])
def search():
    if engine is None:
        return jsonify({"error": "Database engine not initialized."}), 500
    query_text = request.args.get('query')
    if not query_text:
        return jsonify([])

    try:
        with engine.connect() as conn:
            # UPDATED: Vector search for zoo_animals table
            search_sql = text("""
                SELECT common_name, scientific_name, diet_type, habitat, fun_fact,
                       1 - (animal_vector <=> embedding('text-embedding-005', :query)::vector) as score
                FROM zoo_animals
                WHERE animal_vector IS NOT NULL
                ORDER BY score DESC
                LIMIT 5
            """)
            result = conn.execute(search_sql, {"query": query_text})
            
            hits = []
            for row in result:
                hits.append({
                    "title": row[0],
                    "subtitle": row[1],
                    "category": row[2],
                    "habitat": row[3],
                    "bio": row[4],
                    "image_url": f"https://loremflickr.com/500/500/{row[0].replace(' ', ',')},animal",
                    "score": round(float(row[5]), 3)
                })
            return jsonify(hits)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/check-database', methods=['POST'])
def check_database():
    data = request.json
    filename = data.get('filename', '').lower()
    
    with engine.connect() as conn:
        # We check if the filename contains any common_name from our DB
        query = text("""
            SELECT common_name, scientific_name, diet_type, habitat, fun_fact 
            FROM zoo_animals 
            WHERE :filename LIKE '%' || LOWER(common_name) || '%'
            LIMIT 1
        """)
        result = conn.execute(query, {"filename": filename}).fetchone()
        
        if result:
            return jsonify({
                "found": True,
                "data": {
                    "title": result[0],
                    "subtitle": result[1],
                    "category": result[2],
                    "bio": f"{result[3]} | {result[4]}"
                }
            })
        
        return jsonify({"found": False})

@app.route('/api/smart-identify', methods=['POST'])
def smart_identify():
    if not genai_client:
        return jsonify({"error": "Gemini client not initialized"}), 500

    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files['image']
    image_bytes = file.read()

    try:
        # STEP 1: AI Agent identifies the creature's name visually
        name_prompt = "Identify the animal in this image. Respond with ONLY the common name (e.g., 'Meerkat')."
        
        response = genai_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=name_prompt),
                        types.Part.from_bytes(data=image_bytes, mime_type=file.mimetype)
                    ]
                )
            ]
        )
        
        identified_name = response.text.strip().split('\n')[0]
        print(f"DEBUG: Gemini identified: {identified_name}")

        # STEP 2: Check AlloyDB for that specific name using Vector Search
        with engine.connect() as conn:
            vector_query = text("""
                SELECT common_name, scientific_name, diet_type, habitat, fun_fact,
                       1 - (animal_vector <=> embedding('text-embedding-005', :name)::vector) as similarity
                FROM zoo_animals
                WHERE animal_vector IS NOT NULL
                ORDER BY similarity DESC
                LIMIT 1
            """)
            db_result = conn.execute(vector_query, {"name": identified_name}).fetchone()
        
        # STEP 3: Return result based on similarity threshold
        # We check if a result exists AND if the similarity is high enough (e.g., > 0.7)
        if db_result and db_result[5] > 0.5:
            return jsonify({
                "found": True,
                "data": {
                    "title": db_result[0],
                    "subtitle": db_result[1],
                    "category": db_result[2],
                    "bio": f"{db_result[3]} | {db_result[4]}"
                }
            })
        else:
            # If no match or match is too weak, return the "Not Found" state
            return jsonify({
                "found": False,
                "name": identified_name,
                "message": f"Identified as {identified_name}, but it's not in the Voya database yet."
            })

    except Exception as e:
        print(f"Smart Identify Error: {traceback.format_exc()}")
        return jsonify({"error": "Processing failed", "details": str(e)}), 500

# Keep your other routes (swipe, list-item) as they are, 
# but note they still point to the 'items' table if used.

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), threaded=True)