#!/usr/bin/env python3
"""
Test script to generate research specifically for NVIDIA.
"""
import json
from sdr_assistant.core.research import research_manager

def test_nvidia_research():
    """Test generating research for NVIDIA"""
    print("\n===== TESTING RESEARCH GENERATION FOR NVIDIA =====")
    
    # Try to generate research for NVIDIA
    print("Generating research for NVIDIA...\n")
    
    result = research_manager.generate_research("NVIDIA")
    
    # Print the full result for debugging
    print(f"Success: {result.get('success', False)}")
    print(f"Message: {result.get('message', 'No message')}")
    
    # If research was generated successfully, print a sample
    if result.get('success', False):
        print("\n--- INDUSTRY INSIGHTS (SAMPLE) ---")
        industry = result.get('industryInsights', '')
        print(industry[:300] + "..." if len(industry) > 300 else industry)
        
        print("\n--- COMPANY INSIGHTS (SAMPLE) ---")
        company = result.get('companyInsights', '')
        print(company[:300] + "..." if len(company) > 300 else company)
        
        print("\n--- TALK TRACK (SAMPLE) ---")
        talk_track = result.get('recommendedTalkTrack', '')
        print(talk_track[:300] + "..." if len(talk_track) > 300 else talk_track)
    else:
        print("\nResearch generation failed. Let's debug why:")
        
        # Check if we need to add NVIDIA to the database first
        from sdr_assistant.core.accounts import account_manager
        accounts = account_manager.get_all_accounts()
        
        print(f"\nFound {len(accounts)} accounts in the database")
        print("Account names in database:", [a.name for a in accounts])
        
        if not any(a.name.lower() == "nvidia" for a in accounts):
            print("\nNVIDIA not found in the database. Adding it now...")
            new_account = {
                "name": "NVIDIA",
                "website": "nvidia.com",
                "industry": "Technology",
                "employees": "10000+",
                "description": "Leader in GPU technology and AI computing"
            }
            
            result = account_manager.add_account(new_account)
            print(f"Account creation result: {result}")
            
            if result.get('success', False):
                print("\nNow trying research generation again...")
                result = research_manager.generate_research("NVIDIA")
                print(f"Second attempt success: {result.get('success', False)}")
                if result.get('success', False):
                    print("\n--- INDUSTRY INSIGHTS (SAMPLE) ---")
                    industry = result.get('industryInsights', '')
                    print(industry[:300] + "..." if len(industry) > 300 else industry)

if __name__ == "__main__":
    test_nvidia_research()
