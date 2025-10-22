🧠 String Analysis API

A RESTful Flask API that analyzes text strings, providing various metrics such as palindrome detection, word count, unique character count, and more.
The API supports filtering, retrieval, and deletion of stored string analyses.

🔍 Overview

This project is a simple but powerful Flask-based API that performs text analysis on user-provided strings.
It can:

. Detect palindromes

. Count words and characters

. Compute SHA-256 hashes

. Maintain an in-memory database for quick retrieval and filtering

. Support advanced query-based filtering on string properties

This kind of API can be useful for educational tools, text-processing systems, or as a component of larger NLP (Natural Language Processing) systems.

🚀 Features

✅ Analyze any string and extract properties:

. Length

. Palindrome check

. Word count

. Unique character count

. Character frequency map

. SHA-256 hash ID

✅ Store analyzed strings in-memory

✅ Retrieve and filter stored results using query parameters

✅ Delete individual records

✅ Structured JSON responses and proper HTTP status codes

🧰 Tech Stack

. Python 3.10+

. Flask — for the API framework

. hashlib — for secure string hashing

. collections.Counter — for frequency analysis

. datetime — for timestamps

📡 API Endpoints
1️⃣ POST /string

Analyze and store a new string.

🧾 Request Body
{
  "value": "madam"
}

✅ Response (201 Created)
{
  "id": "e49b1c8e9f9e53fbc7427c83...",
  "value": "madam",
  "properties": {
    "length": 5,
    "is_palindrome": true,
    "unique_characters": 3,
    "word_count": 1,
    "sha256_hash": "e49b1c8e9f9e53fbc7427c83...",
    "character_frequency_map": {
      "m": 2,
      "a": 2,
      "d": 1
    }
  },
  "created_at": "2025-10-21T12:15:30.123Z"
}

2️⃣ GET /strings

Retrieve all analyzed strings (optionally filtered).
Example
GET /strings?is_palindrome=true&min_length=3

✅ Response
{
  "data": [...],
  "count": 2,
  "filters_applied": {
    "is_palindrome": "true",
    "min_length": "3"
  }
}
3️⃣ GET /strings/<string_id>

Retrieve a specific string by its SHA-256 ID.

Example
GET /strings/e49b1c8e9f9e53fbc7427c83...

✅ Response
{
  "id": "e49b1c8e9f9e53fbc7427c83...",
  "value": "madam",
  "properties": {...},
  "created_at": "2025-10-21T12:15:30.123Z"
}
4️⃣ DELETE /strings/<string_id>

Delete a string record from the in-memory store.

✅ Response
204 No Content

⚙️ Installation

Clone the repository

git clone https://github.com/<abdullateef>/flask-string-analysis-api.git
cd flask-string-analysis-api


Create a virtual environment

python -m venv venv


Activate the environment

Windows: venv\Scripts\activate

macOS/Linux: source venv/bin/activate

Install dependencies

pip install flask

