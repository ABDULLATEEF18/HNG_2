import json
import hashlib 
from datetime import datetime
from collections import Counter
from flask import Flask, request, jsonify, abort
import os
# --- Configuration and In-Memory Storage ---
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# In-memory storage: Keyed by SHA-256 hash
DATA_STORE = {}

#@app.route("/string", methods=["POST"])
def analyse_string(value):
    # get the hash value
    hash_value = hashlib.sha256(value.encode()).hexdigest()
    # get string length
    length = len(value)
    # check if palindrome
    
    # Case-insensitive palindrome check base
    normalized_value = ''.join(char for char in value if char.isalnum()).lower()

    # 2. Palindrome check
    is_palindrome = normalized_value == normalized_value[::-1]

    # check word count
    word_count = len(value.split())
    # check unique characters
    character_frequency_map = dict(Counter(value))
    unique_characters = len(character_frequency_map) 
    
    return {
              "id": hash_value,
              "value": value,
              "properties": {
                               "length": length,
                               "is_palindrome": is_palindrome,
                               "unique_characters": unique_characters,
                               "word_count": word_count,
                                "sha256_hash": hash_value,
                                "character_frequency_map": character_frequency_map
                             },
             "created_at": datetime.utcnow().isoformat() + "Z"
           }
# function to get filtered data.

def apply_filters(data_list, filters):
    """
    Applies a dictionary of filters (from query parameters or NL parser) to a list of string records.
    """
    filtered_data = []
    
    # Cast parameters to correct types
    try:
        f_is_palindrome = filters.get('is_palindrome')
        f_min_length = int(filters['min_length']) if filters.get('min_length') else None
        f_max_length = int(filters['max_length']) if filters.get('max_length') else None
        f_word_count = int(filters['word_count']) if filters.get('word_count') else None
        f_contains_char = filters.get('contains_character')
    except ValueError:
        # Re-raise a 400 error if casting fails
        abort(400, description="Invalid filter value type (min_length, max_length, word_count must be integers).")


    # Convert boolean string 'true'/'false' to actual boolean if present
    if f_is_palindrome is not None:
        if isinstance(f_is_palindrome, str):
            f_is_palindrome = f_is_palindrome.lower() == 'true'
        # If it's already a bool (e.g., from NL parser), keep it.

    for record in data_list:
        p = record['properties']
        
        # 1. is_palindrome filter
        if f_is_palindrome is not None and p['is_palindrome'] != f_is_palindrome:
            continue
        
        # 2. min_length filter
        if f_min_length is not None and p['length'] < f_min_length:
            continue
            
        # 3. max_length filter
        if f_max_length is not None and p['length'] > f_max_length:
            continue
            
        # 4. word_count filter
        if f_word_count is not None and p['word_count'] != f_word_count:
            continue

        # 5. contains_character filter (case-sensitive as per standard practice unless specified otherwise)
        if f_contains_char and f_contains_char not in record['value']:
            continue
            
        filtered_data.append(record)

    return filtered_data
   
# endpoint_1: create/ analyze string

@app.route("/string", methods=["POST"])
def create_string():
    
    data = request.get_json(silent=True)
    #409 Conflict: String already exists in the system
    #400 Bad Request: Invalid request body or missing "value" field
    if not data or "value" not in data:
          return jsonify({"error": "Invalid JSON or missing 'value' field"}), 400
    string_value = data['value']
    # 422 Unprocessable Entity: Invalid data type for "value" (must be string)
    if not isinstance(string_value, str):
        return jsonify({"error": "The 'value' field must be a string."}), 422
    # analyze string
    string_analysis = analyse_string(string_value)
    string_id = string_analysis["id"]
    
    if string_id in DATA_STORE:
        return jsonify({"error": "String already exists in the system.", "id": string_id}), 409

    # Store the result
    DATA_STORE[string_id] = string_analysis

    # 201 Created
    return jsonify(string_analysis), 201

# endpoint_2: get specific string
@app.route("/strings/<string_id>", methods=["GET"])
def get_string(string_id):
    
    record = DATA_STORE.get(string_id)

    # 404 Not Found: String does not exist in the system
    if record is None:
        return jsonify({"error": f"String with ID '{string_id}' not found."}), 404

    # 200 OK
    return jsonify(record), 200



@app.route('/strings', methods=['GET'])
def get_all_strings_with_filtering():
    # Collect filters from URL query parameters
    filters = request.args.to_dict()
    
    # Check for invalid filter keys to help with 400 response
    valid_filters = {'is_palindrome', 'min_length', 'max_length', 'word_count', 'contains_character'}
    if not valid_filters.issuperset(filters.keys()):
        return jsonify({"error": "Invalid query parameter used. Valid parameters are: " + ', '.join(valid_filters)}), 400

    data_list = list(DATA_STORE.values())

    try:
        filtered_data = apply_filters(data_list, filters)
    except Exception as e:
        # Catch exceptions thrown by apply_filters (like 400 Bad Request on casting)
        if hasattr(e, 'code') and e.code == 400:
             return jsonify({"error": e.description}), 400
        # If it's another error, return a generic 500 or re-raise
        raise e


    # 200 OK
    response = {
        "data": filtered_data,
        "count": len(filtered_data),
        "filters_applied": filters
    }
    return jsonify(response), 200


@app.route('/strings/<string_id>', methods=['DELETE'])
def delete_string(string_id):
    """
    5. Delete String: DELETE /strings/{string_id}
    """
    if string_id not in DATA_STORE:
        # 404 Not Found: String does not exist in the system
        return jsonify({"error": f"String with ID '{string_id}' not found."}), 404

    del DATA_STORE[string_id]

    # 204 No Content
    return '', 204

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
