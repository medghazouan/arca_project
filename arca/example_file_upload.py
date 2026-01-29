# example_file_upload.py
"""
ARCA System: Example Usage with File Upload

Demonstrates how to use the new document preprocessing features:
- Process PDF/TXT files
- Extract and clean text
- Summarize long documents
- Analyze with ARCA pipeline
"""

from arca_pipeline import analyze_regulation_from_file_smart
import os


def example_1_pdf_file():
    """
    Example 1: Analyze a PDF regulation file
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Analyze PDF File")
    print("=" * 80)
    
    # Path to your PDF file
    pdf_path = "regulations/gdpr_amendment_2025.pdf"
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"⚠️  File not found: {pdf_path}")
        print("   Please place a PDF file at this location or update the path")
        return
    
    try:
        result = analyze_regulation_from_file_smart(
            file_path=pdf_path,
            date_of_law="2025-06-01",
            regulation_title="GDPR Amendment 2025",
            summarize=True  # Auto-summarize if > 2000 words
        )
        
        # Display results
        print("\n" + "=" * 80)
        print("ANALYSIS RESULTS")
        print("=" * 80)
        print(f"Regulation ID: {result['regulation_id']}")
        print(f"Date Processed: {result['date_processed']}")
        print(f"Total Risks Found: {result['total_risks_flagged']}")
        
        # Document processing metadata
        if 'document_metadata' in result:
            meta = result['document_metadata']
            print(f"\nDocument Processing:")
            print(f"  Source File: {meta['source_file']}")
            print(f"  File Type: {meta['file_type']}")
            print(f"  Original Words: {meta['original_word_count']}")
            print(f"  Processed Words: {meta['processed_word_count']}")
            print(f"  Was Summarized: {meta['was_summarized']}")
        
        # Display risks
        if result['risks']:
            print(f"\nIdentified Risks:")
            for i, risk in enumerate(result['risks'], 1):
                print(f"\n[{i}] {risk['severity']} - {risk['policy_id']}")
                print(f"    {risk['divergence_summary']}")
                print(f"    → {risk['recommendation']}")
        
        print("\n✅ Analysis complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def example_2_txt_file():
    """
    Example 2: Analyze a TXT regulation file
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Analyze TXT File")
    print("=" * 80)
    
    # Create a sample TXT file
    sample_regulation = """
    New Labor Law Amendment 2025
    
    Article 1: Remote Work Requirements
    
    All companies with more than 50 employees must allow employees to work 
    remotely at least 3 days per week. Employers cannot require full-time 
    office attendance unless the role specifically requires physical presence.
    
    Article 2: Right to Disconnect
    
    Employees have the right to disconnect from work communications outside 
    of their contracted working hours. Employers must not contact employees 
    via email, phone, or messaging apps between 7 PM and 7 AM.
    
    Article 3: Compliance Timeline
    
    This regulation takes effect on July 1, 2025. Companies have 3 months 
    from the effective date to update their policies and procedures.
    
    Article 4: Penalties
    
    Non-compliance may result in fines of up to 50,000 EUR per violation.
    """
    
    # Save to file
    txt_path = "temp_regulation.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(sample_regulation)
    
    try:
        result = analyze_regulation_from_file_smart(
            file_path=txt_path,
            date_of_law="2025-07-01",
            regulation_title="Labor Law Amendment 2025",
            summarize=True
        )
        
        # Display results
        print("\n" + "=" * 80)
        print("ANALYSIS RESULTS")
        print("=" * 80)
        print(f"Regulation ID: {result['regulation_id']}")
        print(f"Total Risks Found: {result['total_risks_flagged']}")
        
        # Display conflicts
        for i, risk in enumerate(result['risks'], 1):
            print(f"\n[{i}] {risk['severity']}: {risk['policy_id']}")
            print(f"    {risk['divergence_summary']}")
        
        print("\n✅ Analysis complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        # Cleanup
        if os.path.exists(txt_path):
            os.remove(txt_path)


def example_3_api_upload():
    """
    Example 3: API file upload using curl
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 3: API File Upload")
    print("=" * 80)
    
    print("\nTo upload a file via the REST API, use this curl command:\n")
    
    curl_command = """curl -X POST "http://localhost:8000/analyze_regulation_file" \\
  -F "file=@regulations/regulation.pdf" \\
  -F "date_of_law=2025-06-01" \\
  -F "regulation_title=GDPR Amendment 2025" \\
  -F "summarize=true"
"""
    
    print(curl_command)
    
    print("\nOr using Python requests library:\n")
    
    python_code = """import requests

# Upload file and analyze
with open("regulations/regulation.pdf", "rb") as f:
    files = {"file": f}
    data = {
        "date_of_law": "2025-06-01",
        "regulation_title": "GDPR Amendment 2025",
        "summarize": "true"
    }
    
    response = requests.post(
        "http://localhost:8000/analyze_regulation_file",
        files=files,
        data=data
    )
    
    result = response.json()
    print(f"Found {result['total_risks_flagged']} conflicts")
"""
    
    print(python_code)
    
    print("\n📝 Note: Make sure the API server is running (python api.py)")


def example_4_direct_processing():
    """
    Example 4: Use DocumentProcessor directly (without ARCA analysis)
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Direct Document Processing")
    print("=" * 80)
    
    from document_processor import DocumentProcessor
    
    # Create sample file
    sample_text = """
    Page 1
    
    Data Protection Regulation 2025
    
    Article 1: Customer data must be deleted within 30 days of deletion request.
    
    Page 2
    
    Article 2: Automated deletion systems are mandatory.
    
    Page 3
    """
    
    # Save to file
    test_file = "test_doc.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(sample_text)
    
    try:
        # Process document
        processor = DocumentProcessor()
        result = processor.process_document(
            file_path=test_file,
            summarize=False  # Don't summarize (already short)
        )
        
        print("\nProcessing Results:")
        print(f"File Type: {result['file_type']}")
        print(f"Word Count: {result['word_count']}")
        print(f"Was Summarized: {result['was_summarized']}")
        
        print("\nCleaned Text:")
        print("-" * 80)
        print(result['processed_text'])
        print("-" * 80)
        
        print("\n✅ Text cleaned and ready for analysis!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)


if __name__ == "__main__":
    print("\n" + "╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "ARCA FILE UPLOAD EXAMPLES" + " " * 33 + "║")
    print("╚" + "═" * 78 + "╝")
    
    # Run examples
    # example_1_pdf_file()  # Uncomment if you have a PDF file
    example_2_txt_file()
    example_3_api_upload()
    example_4_direct_processing()
    
    print("\n" + "=" * 80)
    print("✅ ALL EXAMPLES COMPLETED")
    print("=" * 80)
    print("\nNext Steps:")
    print("1. Try uploading your own PDF or TXT files")
    print("2. Start the API server: python api.py")
    print("3. Test file upload via Swagger UI: http://localhost:8000/docs")
    print("=" * 80)
