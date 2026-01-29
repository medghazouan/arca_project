# test_file_upload_api.py
"""
Test script for the file upload API endpoint
"""

import requests
import os

# Create a simple test regulation file
test_content = """
Article 1: All customer personal data must be deleted within 30 days 
of receiving a deletion request. Automated deletion systems are mandatory.
"""

# Save test file
test_file = "test_regulation.txt"
with open(test_file, 'w', encoding='utf-8') as f:
    f.write(test_content)

print("Testing /analyze_regulation_file endpoint...")
print("=" * 60)

try:
    # Test 1: Upload file with all parameters
    print("\nTest 1: Upload with all parameters")
    with open(test_file, 'rb') as f:
        files = {'file': (test_file, f, 'text/plain')}
        data = {
            'date_of_law': '2025-06-01',
            'regulation_title': 'Test Regulation',
            'summarize': 'true'
        }
        
        response = requests.post(
            'http://localhost:8000/analyze_regulation_file',
            files=files,
            data=data
        )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Success! Found {result['total_risks_flagged']} risks")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text}")
    
    # Test 2: Upload file with minimal parameters
    print("\n\nTest 2: Upload with minimal parameters (file only)")
    with open(test_file, 'rb') as f:
        files = {'file': (test_file, f, 'text/plain')}
        
        response = requests.post(
            'http://localhost:8000/analyze_regulation_file',
            files=files
        )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Success! Found {result['total_risks_flagged']} risks")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text}")

except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to API server!")
    print("   Make sure the server is running: python api.py")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"\n🧹 Cleaned up {test_file}")

print("\n" + "=" * 60)
print("\nCommon issues:")
print("1. Make sure API server is running: python api.py")
print("2. Check file format (.pdf or .txt)")
print("3. Verify date format (YYYY-MM-DD)")
print("4. Check Swagger UI for details: http://localhost:8000/docs")
