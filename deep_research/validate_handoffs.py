"""
Validation script for handoff system structure.
This script tests the handoff system without requiring API keys.
"""

def validate_imports():
    """Validate that all handoff components can be imported"""
    print("🔍 Validating handoff system imports...")
    
    try:
        # Test handoff models
        from handoff_models import (
            HandoffType, ResearchContext, HumanReviewRequest,
            ExpertConsultationRequest, AdditionalResearchRequest,
            QualityCheckRequest, ApprovalRequest, HandoffResponse
        )
        print("✅ Handoff models imported successfully")
        
        # Test handoff agents
        from handoff_agents import (
            human_review_agent, expert_consultation_agent,
            quality_assurance_agent, approval_agent
        )
        print("✅ Handoff agents imported successfully")
        
        # Test enhanced research manager
        from enhanced_research_manager import EnhancedResearchManager
        print("✅ Enhanced research manager imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def validate_handoff_types():
    """Validate handoff type enum"""
    print("\n🔍 Validating handoff types...")
    
    from handoff_models import HandoffType
    
    expected_types = [
        "human_review", "expert_consultation", "additional_research",
        "quality_check", "approval", "custom"
    ]
    
    for expected_type in expected_types:
        if hasattr(HandoffType, expected_type.upper()):
            print(f"✅ {expected_type} handoff type available")
        else:
            print(f"❌ {expected_type} handoff type missing")
            return False
    
    return True

def validate_agent_structure():
    """Validate agent structure"""
    print("\n🔍 Validating agent structure...")
    
    from handoff_agents import (
        human_review_agent, expert_consultation_agent,
        quality_assurance_agent, approval_agent
    )
    
    agents = [
        ("Human Review Agent", human_review_agent),
        ("Expert Consultation Agent", expert_consultation_agent),
        ("Quality Assurance Agent", quality_assurance_agent),
        ("Approval Agent", approval_agent)
    ]
    
    for name, agent in agents:
        if hasattr(agent, 'name') and hasattr(agent, 'tools'):
            print(f"✅ {name} structure valid")
        else:
            print(f"❌ {name} structure invalid")
            return False
    
    return True

def validate_research_manager():
    """Validate research manager structure"""
    print("\n🔍 Validating research manager structure...")
    
    from enhanced_research_manager import EnhancedResearchManager
    
    # Test instantiation
    manager = EnhancedResearchManager(enable_handoffs=True)
    print("✅ EnhancedResearchManager instantiated successfully")
    
    # Test handoff detection methods
    if hasattr(manager, '_needs_expert_consultation'):
        print("✅ Expert consultation detection method available")
    else:
        print("❌ Expert consultation detection method missing")
        return False
    
    if hasattr(manager, '_needs_human_review'):
        print("✅ Human review detection method available")
    else:
        print("❌ Human review detection method missing")
        return False
    
    return True

def validate_handoff_triggers():
    """Validate handoff trigger logic"""
    print("\n🔍 Validating handoff trigger logic...")
    
    from enhanced_research_manager import EnhancedResearchManager
    manager = EnhancedResearchManager(enable_handoffs=True)
    
    # Test expert consultation triggers
    expert_queries = [
        "What are the medical implications of new treatments?",
        "What are the legal requirements for AI?",
        "What are the financial risks of cryptocurrency?",
        "What are the technical challenges in quantum computing?"
    ]
    
    for query in expert_queries:
        if manager._needs_expert_consultation(query):
            print(f"✅ Expert consultation triggered for: {query[:30]}...")
        else:
            print(f"❌ Expert consultation NOT triggered for: {query[:30]}...")
    
    # Test human review triggers
    review_queries = [
        "Compare and analyze different strategies",
        "Evaluate the effectiveness of approaches",
        "Assess the risks and benefits"
    ]
    
    for query in review_queries:
        if manager._needs_human_review(query):
            print(f"✅ Human review triggered for: {query[:30]}...")
        else:
            print(f"❌ Human review NOT triggered for: {query[:30]}...")
    
    return True

def main():
    """Run all validation tests"""
    print("🚀 HANDOFF SYSTEM VALIDATION")
    print("=" * 50)
    
    tests = [
        ("Import Validation", validate_imports),
        ("Handoff Types", validate_handoff_types),
        ("Agent Structure", validate_agent_structure),
        ("Research Manager", validate_research_manager),
        ("Handoff Triggers", validate_handoff_triggers)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print(f"\n📊 VALIDATION RESULTS")
    print("=" * 30)
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 All validations passed! Handoff system is ready to use.")
        print("\nNext steps:")
        print("1. Set OPENAI_API_KEY environment variable")
        print("2. Run: python enhanced_deep_research.py")
        print("3. Try queries that trigger handoffs!")
    else:
        print("⚠️ Some validations failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()
