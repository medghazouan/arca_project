# arca_pipeline.py
"""
ARCA System: Complete Sequential Pipeline Integration

Orchestrates the 3-agent crew in strict sequential order:
1. Policy Researcher → Retrieves Top 5 relevant policies
2. Compliance Auditor → Analyzes conflicts and assigns severity
3. Report Generator → Formats final JSON output

TSD Compliance: Sequential execution, no parallel processing
"""

import os
import sys
from typing import Dict, Any
from datetime import datetime

# Import all 3 agents
from agents.policy_researcher import PolicyResearcherAgent
from agents.compliance_auditor import ComplianceAuditorAgent
from agents.report_generator import ReportGeneratorAgent


class ARCASystem:
    def __init__(self):
        """
        Initialize the complete ARCA system with all 3 agents
        
        TSD Architecture: Sequential workflow (chaîne de montage)
        """
        print("=" * 60)
        print("🤖 INITIALIZING ARCA SYSTEM")
        print("=" * 60)
        
        try:
            # Initialize Agent 1: Policy Researcher
            print("\n[1/3] Initializing Policy Researcher Agent...")
            self.agent1 = PolicyResearcherAgent()
            print("      ✅ Policy Researcher ready")
            
            # Initialize Agent 2: Compliance Auditor
            print("\n[2/3] Initializing Compliance Auditor Agent...")
            self.agent2 = ComplianceAuditorAgent()
            print("      ✅ Compliance Auditor ready")
            
            # Initialize Agent 3: Report Generator
            print("\n[3/3] Initializing Report Generator Agent...")
            self.agent3 = ReportGeneratorAgent()
            print("      ✅ Report Generator ready")
            
            print("\n" + "=" * 60)
            print("✅ ARCA SYSTEM INITIALIZED")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ INITIALIZATION FAILED: {e}")
            raise

    def analyze_regulation(
        self,
        new_regulation_text: str,
        date_of_law: str = None,
        regulation_title: str = "Untitled Regulation",
        top_k: int = 5,
        save_report: bool = True,
        output_path: str = None
    ) -> Dict[str, Any]:
        """
        Main pipeline: Analyze a new regulation against internal policies
        
        TSD Sequential Flow:
        ┌─────────────────────────────────────────────────────────┐
        │ INPUT: new_regulation_text                              │
        └─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────────────────────────────────────────┐
        │ AGENT 1: Policy Researcher                              │
        │ → Searches vectorDB for Top 5 relevant policies        │
        │ → Output: List of policy excerpts + IDs                │
        └─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────────────────────────────────────────┐
        │ AGENT 2: Compliance Auditor                             │
        │ → Analyzes each policy vs regulation                   │
        │ → Output: Conflict analysis with severity              │
        └─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────────────────────────────────────────┐
        │ AGENT 3: Report Generator                               │
        │ → Formats analysis into structured JSON                │
        │ → Output: TSD-compliant JSON report                    │
        └─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────────────────────────────────────────┐
        │ OUTPUT: Final JSON Report                               │
        └─────────────────────────────────────────────────────────┘
        
        Args:
            new_regulation_text: The complete text of new regulation
            date_of_law: Date in YYYY-MM-DD format (optional)
            regulation_title: Title/name of regulation (optional)
            top_k: Number of policies to retrieve (default: 5)
            save_report: Whether to save JSON to file (default: True)
            output_path: Custom output path (default: auto-generated)
        
        Returns:
            Complete JSON report matching TSD schema
        """
        
        print("\n" + "=" * 80)
        print("🚀 STARTING ARCA ANALYSIS PIPELINE")
        print("=" * 80)
        print(f"Regulation: {regulation_title}")
        print(f"Date of Law: {date_of_law or 'Not specified'}")
        print(f"Text length: {len(new_regulation_text)} characters")
        print("=" * 80)
        
        start_time = datetime.now()
        
        # ─────────────────────────────────────────────────────────
        # STAGE 1: POLICY RESEARCH
        # ─────────────────────────────────────────────────────────
        print("\n" + "━" * 80)
        print("📚 STAGE 1/3: POLICY RESEARCH")
        print("━" * 80)
        print(f"Searching for Top {top_k} relevant internal policies...")
        
        try:
            research_results = self.agent1.run(
                query=new_regulation_text,
                k=top_k
            )
            
            print(f"✅ Found {research_results['total_results']} relevant policies")
            for i, item in enumerate(research_results['items'], 1):
                print(f"   [{i}] {item['policy_id']} (score: {item['score']:.4f})")
            
        except Exception as e:
            print(f"❌ STAGE 1 FAILED: {e}")
            raise
        
        # ─────────────────────────────────────────────────────────
        # STAGE 2: COMPLIANCE AUDIT
        # ─────────────────────────────────────────────────────────
        print("\n" + "━" * 80)
        print("⚖️  STAGE 2/3: COMPLIANCE AUDIT")
        print("━" * 80)
        print(f"Analyzing {len(research_results['items'])} policies for conflicts...")
        
        try:
            audit_results = self.agent2.run(
                new_regulation_text=new_regulation_text,
                policy_items=research_results['items']
            )
            
            print(f"\n✅ Audit complete:")
            print(f"   Total conflicts: {audit_results['total_conflicts_found']}")
            
            # Show severity breakdown
            severity_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
            for conflict in audit_results['conflicts']:
                severity_counts[conflict['severity']] += 1
            
            if severity_counts['HIGH'] > 0:
                print(f"   🔴 HIGH severity: {severity_counts['HIGH']}")
            if severity_counts['MEDIUM'] > 0:
                print(f"   🟡 MEDIUM severity: {severity_counts['MEDIUM']}")
            if severity_counts['LOW'] > 0:
                print(f"   🟢 LOW severity: {severity_counts['LOW']}")
            
        except Exception as e:
            print(f"❌ STAGE 2 FAILED: {e}")
            raise
        
        # ─────────────────────────────────────────────────────────
        # STAGE 3: REPORT GENERATION
        # ─────────────────────────────────────────────────────────
        print("\n" + "━" * 80)
        print("📊 STAGE 3/3: REPORT GENERATION")
        print("━" * 80)
        print("Formatting final JSON report...")
        
        try:
            final_report = self.agent3.run(
                audit_results=audit_results,
                date_of_law=date_of_law,
                regulation_title=regulation_title
            )
            
            print(f"✅ Report generated successfully")
            print(f"   Regulation ID: {final_report['regulation_id']}")
            
        except Exception as e:
            print(f"❌ STAGE 3 FAILED: {e}")
            raise
        
        # ─────────────────────────────────────────────────────────
        # SAVE REPORT (Optional)
        # ─────────────────────────────────────────────────────────
        if save_report:
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"reports/arca_report_{timestamp}.json"
            
            # Create reports directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path) or "reports", exist_ok=True)
            
            self.agent3.save_report(final_report, output_path)
        
        # ─────────────────────────────────────────────────────────
        # PIPELINE COMPLETE
        # ─────────────────────────────────────────────────────────
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print("\n" + "=" * 80)
        print("✅ ARCA PIPELINE COMPLETE")
        print("=" * 80)
        print(f"Total duration: {duration:.2f} seconds")
        print(f"Policies analyzed: {audit_results['total_policies_analyzed']}")
        print(f"Conflicts found: {final_report['total_risks_flagged']}")
        if save_report:
            print(f"Report saved: {output_path}")
        print("=" * 80)
        
        return final_report


# ─────────────────────────────────────────────────────────
# CONVENIENCE FUNCTIONS
# ─────────────────────────────────────────────────────────

def analyze_regulation_from_text(
    regulation_text: str,
    date_of_law: str = None,
    regulation_title: str = "Untitled Regulation"
) -> Dict[str, Any]:
    """
    Quick function to analyze a regulation from text string
    
    Usage:
        result = analyze_regulation_from_text(
            regulation_text="All customer data must be deleted within 30 days...",
            date_of_law="2025-01-15",
            regulation_title="GDPR Amendment 2025"
        )
    """
    arca = ARCASystem()
    return arca.analyze_regulation(
        new_regulation_text=regulation_text,
        date_of_law=date_of_law,
        regulation_title=regulation_title
    )


def analyze_regulation_from_file(
    file_path: str,
    date_of_law: str = None,
    regulation_title: str = None
) -> Dict[str, Any]:
    """
    Analyze a regulation from a text or markdown file
    
    Usage:
        result = analyze_regulation_from_file(
            file_path="regulations/new_law.txt",
            date_of_law="2025-01-15"
        )
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        regulation_text = f.read()
    
    # Use filename as title if not provided
    if regulation_title is None:
        regulation_title = os.path.basename(file_path)
    
    arca = ARCASystem()
    return arca.analyze_regulation(
        new_regulation_text=regulation_text,
        date_of_law=date_of_law,
        regulation_title=regulation_title
    )


# ─────────────────────────────────────────────────────────
# EXAMPLE USAGE & TESTING
# ─────────────────────────────────────────────────────────

def example_usage():
    """
    Example showing how to use the ARCA system
    """
    
    # Example 1: Analyze from text string
    print("\n" + "🎯 EXAMPLE 1: Analyze from text string")
    print("─" * 60)
    
    sample_regulation = """
    Article 12: Data Retention and Deletion Requirements
    
    1. All personal customer data must be permanently deleted within 30 days 
       of receiving a deletion request from the customer.
    
    2. Companies must implement automated deletion mechanisms that do not 
       require manual review for standard deletion requests.
    
    3. Deletion logs must be maintained for audit purposes for a minimum 
       period of 5 years.
    
    4. Customers must receive confirmation of deletion within 48 hours of 
       the deletion being completed.
    
    5. Any third-party processors holding customer data must also delete 
       the data within the same 30-day period.
    """
    
    try:
        result = analyze_regulation_from_text(
            regulation_text=sample_regulation,
            date_of_law="2025-06-01",
            regulation_title="Data Protection Amendment Act 2025"
        )
        
        print("\n✅ Analysis successful!")
        print(f"Regulation ID: {result['regulation_id']}")
        print(f"Total risks: {result['total_risks_flagged']}")
        
        # Display risks
        if result['risks']:
            print("\n📋 Identified Risks:")
            for i, risk in enumerate(result['risks'], 1):
                print(f"\n[{i}] {risk['severity']} - {risk['policy_id']}")
                print(f"    {risk['divergence_summary']}")
                print(f"    → {risk['recommendation']}")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")


def quick_test():
    """
    Quick test with minimal regulation text
    """
    print("\n" + "🧪 RUNNING QUICK TEST")
    print("=" * 60)
    
    test_regulation = """
    All customer personal data must be deleted within 30 days of a deletion 
    request. Automated deletion systems are mandatory.
    """
    
    result = analyze_regulation_from_text(
        regulation_text=test_regulation,
        date_of_law="2025-01-15",
        regulation_title="Test Regulation"
    )
    
    import json
    print("\n📄 Final Report:")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    # Run example usage
    example_usage()
    
    # Uncomment to run quick test:
    # quick_test()