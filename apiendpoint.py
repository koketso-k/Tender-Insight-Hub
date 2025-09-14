
from flask import Flask, request, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# In-memory "database"
TENDERS_DB = [
    {"id": 1, "title": "Supply of Laptops", "status": "open", "category": "IT", "description": "Supply of 100 high-end laptops for government officials."},
    {"id": 2, "title": "Construction of Road", "status": "closed", "category": "Infrastructure", "description": "Construction of a 5km highway section."},
    {"id": 3, "title": "Office Furniture", "status": "open", "category": "Supplies", "description": "Procurement of chairs and desks for the new office."},
    {"id": 4, "title": "Catering Services", "status": "draft", "category": "Services", "description": "Catering for annual conference for 500 people."},
    {"id": 5, "title": "Security System Upgrade", "status": "open", "category": "IT", "description": "Installation of new CCTV and access control systems."},
]

class PublicTenders(Resource):
    def get(self):
        status_filter = request.args.get('status')
        category_filter = request.args.get('category')
        
        filtered_tenders = TENDERS_DB
        if status_filter:
            filtered_tenders = [t for t in filtered_tenders if t['status'] == status_filter.lower()]
        if category_filter:
            filtered_tenders = [t for t in filtered_tenders if t['category'] == category_filter.lower()]
            
        # Pagination
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 5))
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_tenders = filtered_tenders[start_idx:end_idx]
        
        response = {
            "page": page,
            "per_page": per_page,
            "total_tenders": len(filtered_tenders),
            "total_pages": (len(filtered_tenders) + per_page - 1) // per_page,
            "tenders": paginated_tenders
        }
        return jsonify(response)

api.add_resource(PublicTenders, '/public/tenders')

if __name__ == '__main__':
    # Run the server. The use_reloader=False is CRUCIAL in Jupyter.
    app.run(debug=True, use_reloader=False).
    import requests
import json

base_url = "http://127.0.0.1:5000/public/tenders"

print("1. Testing all tenders:")
response = requests.get(base_url)
print(f"Status Code: {response.status_code}")
print(json.dumps(response.json(), indent=4))
print("\n" + "-"*50 + "\n")

print("2. Testing filtering for 'open' tenders:")
response = requests.get(base_url, params={'status': 'open'})
print(f"Status Code: {response.status_code}")
print(json.dumps(response.json(), indent=4))
print("\n" + "-"*50 + "\n")

print("3. Testing pagination (page 2, 2 items per page):")
response = requests.get(base_url, params={'page': 2, 'per_page': 2})
print(f"Status Code: {response.status_code}")
print(json.dumps(response.json(), indent=4))
print("\n" + "-"*50 + "\n")

print("4. Testing combined filter (open IT tenders):")
response = requests.get(base_url, params={'status': 'open', 'category': 'it'})
print(f"Status Code: {response.status_code}")
print(json.dumps(response.json(), indent=4))