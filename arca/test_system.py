# test_system.py
"""
ARCA System Testing Suite

Comprehensive tests to verify all components are working correctly
before deployment.

Run: python test_system.py
"""

import os
import sys
import json
from datetime import datetime

# Color output for terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.RESET}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.RESET}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.RESET}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.RESET}")

def print_header(msg):
    print(f"\n{Colors.BOLD}{'='*60}")
    print(f"{msg}")
    print(f"{'='*60}{Colors.RESET}\n")


class ARCASystemTester:
    def __init__(self):
        self.results = {
            "passed": 0,
            "failed": 0,
            "warnings": 0
        }
        
    def test_environment(self):
        """Test 1: Environment Setup"""
        print_header("TEST 1: Environment Setup")
        
        # Check Python version
        print("Checking Python version...")
        py_version = sys.version_info
        if py_version >= (3, 10):
            print_success(f"Python {py_version.major}.{py_version.minor}.{py_version.micro}")
            self.results["passed"] += 1
        else:
            print_error(f"Python {py_version.major}.{py_version.minor} (requires 3.10+)")
            self.results["failed"] += 1
            return False
        
        # Check .env file
        print("\nChecking .env file...")
        if os.path.exists(".env"):
            print_success(".env file found")
            self.results["passed"] += 1
            
            # Check for API key
            from dotenv import load_dotenv
            load_dotenv()
            
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key and len(api_key) > 10:
                print_success("GOOGLE_API_KEY found")
                self.results["passed"] += 1
            else:
                print_error("GOOGLE_API_KEY not found or invalid")
                self.results["failed"] += 1
                return False
        else:
            print_error(".env file not found")
            self.results["failed"] += 1
            return False
        
        return True
    
    def test_dependencies(self):
        """Test 2: Python Dependencies"""
        print_header("TEST 2: Python Dependencies")
        
        required_packages = [
            "langchain",
            "langchain_community",
            "langchain_huggingface",
            "langchain_google_genai",
            "sentence_transformers",
            "faiss",
            "fastapi",
            "uvicorn",
            "pydantic"
        ]
        
        for package in required_packages:
            try:
                if package == "faiss":
                    __import__("faiss")
                else:
                    __import__(package)
                print_success(f"{package} installed")
                self.results["passed"] += 1
            except ImportError:
                print_error(f"{package} NOT installed")
                self.results["failed"] += 1
        
        return self.results["failed"] == 0
    
    def test_data_structure(self):
        """Test 3: Data Directory Structure"""
        print_header("TEST 3: Data Directory Structure")
        
        # Check directories
        directories = ["data/policies", "vectorstore", "agents", "reports"]
        
        for directory in directories:
            if os.path.exists(directory):
                print_success(f"{directory}/ exists")
                self.results["passed"] += 1
            else:
                print_error(f"{directory}/ NOT found")
                self.results["failed"] += 1
        
        # Check policy files
        print("\nChecking policy files...")
        policies_dir = "data/policies"
        if os.path.exists(policies_dir):
            policy_files = [f for f in os.listdir(policies_dir) if f.endswith(".md")]
            
            if len(policy_files) >= 3:
                print_success(f"Found {len(policy_files)} policy files")
                for pf in policy_files[:5]:
                    print(f"   - {pf}")
                if len(policy_files) > 5:
                    print(f"   ... and {len(policy_files)-5} more")
                self.results["passed"] += 1
            else:
                print_warning(f"Only {len(policy_files)} policy files (recommend 10-15)")
                self.results["warnings"] += 1
        
        return True
    
    def test_vectorstore(self):
        """Test 4: Vectorstore"""
        print_header("TEST 4: Vectorstore")
        
        # Check if vectorstore files exist
        vectorstore_files = ["vectorstore/index.faiss", "vectorstore/index.pkl"]
        
        all_exist = True
        for vf in vectorstore_files:
            if os.path.exists(vf):
                print_success(f"{vf} exists")
                self.results["passed"] += 1
            else:
                print_error(f"{vf} NOT found")
                print_warning("Run 'python ingest.py' to create vectorstore")
                self.results["failed"] += 1
                all_exist = False
        
        if not all_exist:
            return False
        
        # Try to load vectorstore
        print("\nTesting vectorstore loading...")
        try:
            from agents.policy_researcher import PolicyResearcherAgent
            agent = PolicyResearcherAgent()
            print_success(f"Vectorstore loaded ({agent.db.index.ntotal} vectors)")
            self.results["passed"] += 1
            
            # Test search
            print("\nTesting vector search...")
            result = agent.run("data retention policy", k=3)
            if result["total_results"] > 0:
                print_success(f"Search working (found {result['total_results']} results)")
                self.results["passed"] += 1
            else:
                print_error("Search returned no results")
                self.results["failed"] += 1
            
        except Exception as e:
            print_error(f"Failed to load vectorstore: {e}")
            self.results["failed"] += 1
            return False
        
        return True
    
    def test_agents(self):
        """Test 5: Agent Functionality"""
        print_header("TEST 5: Agent Functionality")
        
        sample_regulation = """
        Article 1: All personal customer data must be permanently deleted 
        within 30 days of receiving a deletion request.
        """
        
        # Test Agent 1: Policy Researcher
        print("Testing Agent 1: Policy Researcher...")
        try:
            from agents.policy_researcher import PolicyResearcherAgent
            agent1 = PolicyResearcherAgent()
            result1 = agent1.run("data deletion customer request", k=5)
            
            if result1["total_results"] > 0:
                print_success(f"Agent 1 working (found {result1['total_results']} policies)")
                self.results["passed"] += 1
            else:
                print_error("Agent 1 returned no results")
                self.results["failed"] += 1
                return False
        except Exception as e:
            print_error(f"Agent 1 failed: {e}")
            self.results["failed"] += 1
            return False
        
        # Test Agent 2: Compliance Auditor
        print("\nTesting Agent 2: Compliance Auditor...")
        try:
            from agents.compliance_auditor import ComplianceAuditorAgent
            agent2 = ComplianceAuditorAgent()
            result2 = agent2.run(sample_regulation, result1["items"][:3])
            
            print_success(f"Agent 2 working (analyzed {result2['total_policies_analyzed']} policies)")
            self.results["passed"] += 1
        except Exception as e:
            print_error(f"Agent 2 failed: {e}")
            self.results["failed"] += 1
            return False
        
        # Test Agent 3: Report Generator
        print("\nTesting Agent 3: Report Generator...")
        try:
            from agents.report_generator import ReportGeneratorAgent
            agent3 = ReportGeneratorAgent()
            result3 = agent3.run(result2, date_of_law="2025-01-01")
            
            # Validate JSON structure
            required_keys = ["regulation_id", "date_processed", "total_risks_flagged", "risks"]
            missing_keys = [k for k in required_keys if k not in result3]
            
            if not missing_keys:
                print_success("Agent 3 working (valid JSON output)")
                self.results["passed"] += 1
            else:
                print_error(f"Agent 3 output missing keys: {missing_keys}")
                self.results["failed"] += 1
                return False
        except Exception as e:
            print_error(f"Agent 3 failed: {e}")
            self.results["failed"] += 1
            return False
        
        return True
    
    def test_pipeline(self):
        """Test 6: Complete Pipeline"""
        print_header("TEST 6: Complete Pipeline Integration")
        
        sample_regulation = """
        Data Protection Regulation 2025
        
        Article 12: Deletion Requirements
        All personal customer data must be permanently deleted within 30 days 
        of receiving a deletion request from the customer. Companies must 
        implement automated deletion mechanisms.
        """
        
        try:
            from arca_pipeline import ARCASystem
            arca = ARCASystem()
            
            print("Running complete pipeline...")
            result = arca.analyze_regulation(
                new_regulation_text=sample_regulation,
                date_of_law="2025-06-01",
                regulation_title="Test Regulation",
                save_report=False
            )
            
            # Validate result
            if result.get("regulation_id") and result.get("total_risks_flagged") is not None:
                print_success("Pipeline completed successfully")
                print_info(f"   Regulation ID: {result['regulation_id']}")
                print_info(f"   Risks found: {result['total_risks_flagged']}")
                self.results["passed"] += 1
            else:
                print_error("Pipeline output invalid")
                self.results["failed"] += 1
                return False
            
        except Exception as e:
            print_error(f"Pipeline failed: {e}")
            self.results["failed"] += 1
            return False
        
        return True
    
    def test_api(self):
        """Test 7: API Endpoint (Optional)"""
        print_header("TEST 7: API Endpoint (Optional)")
        
        print_warning("API test requires server to be running")
        print_info("To test API manually:")
        print_info("  1. Run: python api.py")
        print_info("  2. Visit: http://localhost:8000/docs")
        print_info("  3. Test /analyze_regulation endpoint")
        
        self.results["warnings"] += 1
        return True
    
    def run_all_tests(self):
        """Run all tests and generate report"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}")
        print("╔════════════════════════════════════════════════════════════╗")
        print("║          ARCA SYSTEM TESTING SUITE                        ║")
        print("║          Comprehensive System Verification               ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print(f"{Colors.RESET}\n")
        
        tests = [
            ("Environment Setup", self.test_environment),
            ("Python Dependencies", self.test_dependencies),
            ("Data Structure", self.test_data_structure),
            ("Vectorstore", self.test_vectorstore),
            ("Agent Functionality", self.test_agents),
            ("Complete Pipeline", self.test_pipeline),
            ("API Endpoint", self.test_api)
        ]
        
        for test_name, test_func in tests:
            try:
                test_func()
            except Exception as e:
                print_error(f"Test '{test_name}' crashed: {e}")
                self.results["failed"] += 1
        
        # Final Report
        print_header("TEST SUMMARY")
        
        total = self.results["passed"] + self.results["failed"] + self.results["warnings"]
        
        print(f"{Colors.GREEN}✅ Passed:   {self.results['passed']}{Colors.RESET}")
        print(f"{Colors.RED}❌ Failed:   {self.results['failed']}{Colors.RESET}")
        print(f"{Colors.YELLOW}⚠️  Warnings: {self.results['warnings']}{Colors.RESET}")
        print(f"\n{Colors.BOLD}Total:     {total}{Colors.RESET}")
        
        if self.results["failed"] == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL CRITICAL TESTS PASSED!{Colors.RESET}")
            print(f"{Colors.GREEN}Your ARCA system is ready for deployment.{Colors.RESET}")
            return True
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}⚠️  SOME TESTS FAILED{Colors.RESET}")
            print(f"{Colors.RED}Please fix the issues above before deployment.{Colors.RESET}")
            return False


if __name__ == "__main__":
    tester = ARCASystemTester()
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)