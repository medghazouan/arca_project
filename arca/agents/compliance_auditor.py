# agents/compliance_auditor.py
"""
Agent 2: Compliance Auditor (ARCA System)

TSD Role: "Analyste juridique senior, spécialiste de l'analyse des divergences"
TSD Objective: Analyze each policy excerpt and determine conflict risk level

Input: 
- new_regulation_text (str): The new regulation text
- policy_excerpts (list): Top 5 excerpts from Agent 1

Output:
- List of conflict analyses with severity (HIGH/MEDIUM/LOW)

Tools: None (pure LLM reasoning)
"""

import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI

load_dotenv()

# LLM Configuration
llm = GoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)


class ComplianceAuditorAgent:
    def __init__(self):
        """
        Initialize the Compliance Auditor Agent
        
        TSD Requirements:
        - No external tools
        - Pure logical reasoning
        - Classify conflicts as HIGH, MEDIUM, or LOW
        """
        self.llm = llm

    def analyze_single_policy(
        self, 
        new_regulation_text: str, 
        policy_excerpt: str,
        policy_id: str
    ) -> Dict[str, Any]:
        """
        Analyze a single policy excerpt against the new regulation
        
        Returns:
        - severity: HIGH, MEDIUM, or LOW
        - divergence_summary: Brief explanation of conflict
        - conflicting_policy_excerpt: The problematic part
        - new_rule_excerpt: The conflicting regulation part
        - recommendation: Actionable next step
        """
        
        prompt = f"""You are a senior legal compliance analyst specialized in regulatory gap analysis.

Your task: Compare the internal company policy excerpt below with a new regulation and determine if there is a conflict.

NEW REGULATION:
{new_regulation_text}

INTERNAL POLICY EXCERPT:
{policy_excerpt}

ANALYSIS INSTRUCTIONS:
1. Identify if there is ANY conflict, divergence, or gap between the policy and the regulation
2. Classify the severity as:
   - HIGH: Direct contradiction, legal risk, immediate action required
   - MEDIUM: Partial conflict, ambiguity, or missing requirement
   - LOW: Minor gap, best practice improvement, or no real conflict

3. Return your analysis in this EXACT JSON format (no other text):
{{
  "severity": "HIGH" | "MEDIUM" | "LOW",
  "has_conflict": true | false,
  "divergence_summary": "One sentence explaining the conflict",
  "conflicting_policy_excerpt": "Quote the specific problematic part from the policy (max 200 chars)",
  "new_rule_excerpt": "Quote the specific conflicting part from the regulation (max 200 chars)",
  "recommendation": "One clear action item for legal team"
}}

If there is NO conflict, set has_conflict to false and use severity "LOW".
"""

        try:
            response = self.llm.invoke(prompt)
            
            # Parse JSON from response
            import json
            import re
            
            # Extract JSON from response (handle markdown code blocks)
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
            else:
                raise ValueError("No valid JSON found in LLM response")
            
            # Add policy_id to result
            analysis["policy_id"] = policy_id
            
            return analysis
            
        except Exception as e:
            # Fallback structure if parsing fails
            return {
                "policy_id": policy_id,
                "severity": "LOW",
                "has_conflict": False,
                "divergence_summary": f"Analysis failed: {str(e)}",
                "conflicting_policy_excerpt": policy_excerpt[:200],
                "new_rule_excerpt": new_regulation_text[:200],
                "recommendation": "Manual review required due to analysis error"
            }

    def run(
        self, 
        new_regulation_text: str, 
        policy_items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Main execution: Analyze all policy excerpts against the new regulation
        
        TSD Flow:
        1. Receive Top 5 excerpts from Agent 1 (Policy Researcher)
        2. Analyze each one individually
        3. Return structured analysis for Agent 3 (Report Generator)
        
        Args:
            new_regulation_text: The complete new regulation text
            policy_items: List of dicts from Agent 1, each with:
                - policy_id
                - excerpt
                - score
        
        Returns:
            Dict with:
            - regulation_text: Original regulation
            - total_policies_analyzed: Count
            - conflicts: List of analysis results
        """
        
        print("=" * 60)
        print("⚖️  COMPLIANCE AUDITOR: Starting Analysis")
        print("=" * 60)
        
        conflicts = []
        
        for i, item in enumerate(policy_items, 1):
            print(f"\n[{i}/{len(policy_items)}] Analyzing Policy: {item['policy_id']}")
            
            analysis = self.analyze_single_policy(
                new_regulation_text=new_regulation_text,
                policy_excerpt=item['excerpt'],
                policy_id=item['policy_id']
            )
            
            # Only keep actual conflicts (or log all for transparency)
            if analysis.get("has_conflict", False):
                conflicts.append(analysis)
                print(f"   ⚠️  {analysis['severity']} risk detected")
            else:
                print(f"   ✅ No conflict detected")
        
        result = {
            "regulation_text": new_regulation_text,
            "total_policies_analyzed": len(policy_items),
            "total_conflicts_found": len(conflicts),
            "conflicts": conflicts
        }
        
        print("\n" + "=" * 60)
        print(f"✅ Analysis Complete: {len(conflicts)} conflicts found")
        print("=" * 60)
        
        return result


def quick_test():
    """Test the Compliance Auditor with sample data"""
    from policy_researcher import PolicyResearcherAgent
    
    # Sample regulation
    new_regulation = """
    Article 12: All personal data must be deleted within 30 days of a customer's 
    deletion request. Companies must provide automated deletion mechanisms and 
    maintain deletion logs for 5 years.
    """
    
    # Get relevant policies using Agent 1
    print("🔍 Step 1: Retrieving relevant policies...")
    researcher = PolicyResearcherAgent()
    policy_results = researcher.run("data deletion customer request retention period", k=5)
    
    # Analyze with Agent 2
    print("\n⚖️  Step 2: Analyzing conflicts...")
    auditor = ComplianceAuditorAgent()
    audit_results = auditor.run(
        new_regulation_text=new_regulation,
        policy_items=policy_results['items']
    )
    
    # Display results
    print("\n" + "=" * 60)
    print("AUDIT RESULTS")
    print("=" * 60)
    print(f"Policies analyzed: {audit_results['total_policies_analyzed']}")
    print(f"Conflicts found: {audit_results['total_conflicts_found']}")
    
    for i, conflict in enumerate(audit_results['conflicts'], 1):
        print(f"\n[Conflict {i}]")
        print(f"  Policy ID: {conflict['policy_id']}")
        print(f"  Severity: {conflict['severity']}")
        print(f"  Summary: {conflict['divergence_summary']}")
        print(f"  Recommendation: {conflict['recommendation']}")


if __name__ == "__main__":
    quick_test()