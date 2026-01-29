# agents/report_generator.py
"""
Agent 3: Report Generator (ARCA System)

TSD Role: "Spécialiste des données et rédacteur technique"
TSD Objective: Transform raw analysis into structured JSON output

Input: Raw analysis from Agent 2 (Compliance Auditor)
Output: Perfectly structured JSON matching TSD schema (Section 4)

Tools: None (LLM formatting only)
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, Any, List


class ReportGeneratorAgent:
    def __init__(self):
        """
        Initialize the Report Generator Agent
        
        TSD Requirements:
        - No external tools
        - Strict JSON schema compliance
        - Machine-readable output
        """
        pass

    def generate_regulation_id(self, regulation_text: str, date_of_law: str = None) -> str:
        """
        Generate unique regulation_id from hash of text and date
        
        TSD Requirement: "généré à partir d'un hash de la date et du texte"
        """
        content = f"{date_of_law or ''}{regulation_text}"
        hash_obj = hashlib.md5(content.encode('utf-8'))
        return f"REG_{hash_obj.hexdigest()[:12].upper()}"

    def format_risk_object(self, conflict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format a single conflict into the TSD risk object schema
        
        TSD Section 4 Required Fields:
        - policy_id: str
        - severity: HIGH | MEDIUM | LOW
        - divergence_summary: str
        - conflicting_policy_excerpt: str
        - new_rule_excerpt: str
        - recommendation: str
        """
        return {
            "policy_id": conflict.get("policy_id", "UNKNOWN"),
            "severity": conflict.get("severity", "LOW"),
            "divergence_summary": conflict.get("divergence_summary", "No summary available"),
            "conflicting_policy_excerpt": conflict.get("conflicting_policy_excerpt", "")[:500],  # Limit length
            "new_rule_excerpt": conflict.get("new_rule_excerpt", "")[:500],  # Limit length
            "recommendation": conflict.get("recommendation", "Manual review required")
        }

    def run(
        self, 
        audit_results: Dict[str, Any],
        date_of_law: str = None,
        regulation_title: str = "Untitled Regulation"
    ) -> Dict[str, Any]:
        """
        Main execution: Transform audit results into final JSON report
        
        TSD Flow:
        1. Receive raw analysis from Agent 2
        2. Structure data according to JSON schema
        3. Validate all required fields
        4. Return machine-readable report
        
        Args:
            audit_results: Output from ComplianceAuditorAgent.run()
            date_of_law: Optional date in YYYY-MM-DD format
            regulation_title: Optional regulation title
        
        Returns:
            Dict matching TSD Section 4 JSON schema
        """
        
        print("=" * 60)
        print("📊 REPORT GENERATOR: Creating JSON Report")
        print("=" * 60)
        
        regulation_text = audit_results.get("regulation_text", "")
        conflicts = audit_results.get("conflicts", [])
        
        # Generate regulation_id (TSD requirement)
        regulation_id = self.generate_regulation_id(regulation_text, date_of_law)
        
        # Format risks array (TSD Section 4: "risks")
        risks = []
        for conflict in conflicts:
            risk_obj = self.format_risk_object(conflict)
            risks.append(risk_obj)
        
        # Build final report (TSD compliant)
        report = {
            "regulation_id": regulation_id,
            "regulation_title": regulation_title,
            "date_of_law": date_of_law or "N/A",
            "date_processed": datetime.now().strftime("%Y-%m-%d"),
            "total_risks_flagged": len(risks),
            "risks": risks,
            "metadata": {
                "total_policies_analyzed": audit_results.get("total_policies_analyzed", 0),
                "analysis_engine": "ARCA v1.0",
                "agents_used": ["PolicyResearcher", "ComplianceAuditor", "ReportGenerator"]
            }
        }
        
        # Validation check
        self._validate_report(report)
        
        print(f"\n✅ Report generated successfully")
        print(f"   Regulation ID: {regulation_id}")
        print(f"   Total risks: {len(risks)}")
        print(f"   Date processed: {report['date_processed']}")
        print("=" * 60)
        
        return report

    def _validate_report(self, report: Dict[str, Any]) -> None:
        """
        Validate that the report matches TSD schema requirements
        
        TSD Section 3.2: Conformité Stricte avec le Schéma de Sortie JSON
        """
        # Check main keys
        required_main_keys = [
            "regulation_id", 
            "date_processed", 
            "total_risks_flagged", 
            "risks"
        ]
        
        for key in required_main_keys:
            if key not in report:
                raise ValueError(f"Missing required key: {key}")
        
        # Check each risk object
        required_risk_keys = [
            "policy_id",
            "severity", 
            "divergence_summary",
            "conflicting_policy_excerpt",
            "new_rule_excerpt",
            "recommendation"
        ]
        
        for i, risk in enumerate(report["risks"]):
            for key in required_risk_keys:
                if key not in risk:
                    raise ValueError(f"Risk {i} missing required key: {key}")
            
            # Validate severity values
            if risk["severity"] not in ["HIGH", "MEDIUM", "LOW"]:
                raise ValueError(f"Invalid severity value: {risk['severity']}")
        
        # Check count consistency
        if report["total_risks_flagged"] != len(report["risks"]):
            raise ValueError("total_risks_flagged does not match risks array length")

    def save_report(self, report: Dict[str, Any], output_path: str = "report.json") -> str:
        """
        Save report to JSON file
        
        Args:
            report: The generated report dict
            output_path: File path to save to
        
        Returns:
            Path to saved file
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Report saved to: {output_path}")
        return output_path


def quick_test():
    """
    Test the Report Generator with sample audit results
    """
    # Sample audit results (from Agent 2)
    sample_audit = {
        "regulation_text": "All customer data must be deleted within 30 days of request.",
        "total_policies_analyzed": 5,
        "total_conflicts_found": 2,
        "conflicts": [
            {
                "policy_id": "data_retention_policy",
                "severity": "HIGH",
                "has_conflict": True,
                "divergence_summary": "Company policy allows 90 days vs regulation requires 30 days",
                "conflicting_policy_excerpt": "Customer data will be retained for 90 days after deletion request",
                "new_rule_excerpt": "All customer data must be deleted within 30 days of request",
                "recommendation": "Update data retention policy to comply with 30-day requirement"
            },
            {
                "policy_id": "privacy_policy",
                "severity": "MEDIUM",
                "has_conflict": True,
                "divergence_summary": "Missing automated deletion mechanism requirement",
                "conflicting_policy_excerpt": "Manual review required for all deletion requests",
                "new_rule_excerpt": "Companies must provide automated deletion mechanisms",
                "recommendation": "Implement automated deletion system for customer requests"
            }
        ]
    }
    
    # Generate report
    generator = ReportGeneratorAgent()
    report = generator.run(
        audit_results=sample_audit,
        date_of_law="2025-01-15",
        regulation_title="GDPR Amendment 2025"
    )
    
    # Display report
    print("\n" + "=" * 60)
    print("FINAL JSON REPORT")
    print("=" * 60)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    
    # Save to file
    generator.save_report(report, "sample_report.json")


if __name__ == "__main__":
    quick_test()