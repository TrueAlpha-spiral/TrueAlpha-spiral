"""Test script for the Personalized Guardian Shield

This script demonstrates the capabilities of the Guardian Shield by simulating
legitimate steward interactions and unauthorized access attempts.
"""

import json
from guardian_shield import GuardianShield

def test_legitimate_steward():
    """Test verification of the legitimate steward."""
    print("\n===== TESTING LEGITIMATE STEWARD VERIFICATION =====\n")
    
    shield = GuardianShield(steward_id="Russell Nordland")
    
    # Define legitimate intent markers that align with the steward's patterns
    legitimate_intent = {
        "truth_alignment": 0.96,
        "ethical_coherence": 0.95,
        "sovereign_preservation": 0.97,
        "conceptual_integrity": 0.94
    }
    
    print("Verifying legitimate steward with aligned intent markers...")
    is_verified, confidence, details = shield.verify_steward("Russell Nordland", legitimate_intent)
    
    print(f"Verification result: {'SUCCESS' if is_verified else 'FAILURE'}")
    print(f"Confidence score: {confidence:.4f}")
    print("\nDetailed scores:")
    for aspect, score in details['scores'].items():
        print(f"  {aspect}: {score:.4f}")
    
    return shield

def test_unauthorized_access(shield):
    """Test verification of an unauthorized user."""
    print("\n===== TESTING UNAUTHORIZED ACCESS ATTEMPT =====\n")
    
    # Define intent markers that deviate from the steward's patterns
    unauthorized_intent = {
        "truth_alignment": 0.75,
        "ethical_coherence": 0.60,
        "sovereign_preservation": 0.50,
        "conceptual_integrity": 0.70
    }
    
    print("Attempting verification with unauthorized identity...")
    is_verified, confidence, details = shield.verify_steward("Unauthorized User", unauthorized_intent)
    
    print(f"Verification result: {'SUCCESS' if is_verified else 'FAILURE (as expected)'}")
    print(f"Confidence score: {confidence:.4f}")
    print("\nDetailed scores:")
    for aspect, score in details['scores'].items():
        print(f"  {aspect}: {score:.4f}")
    
    return shield

def test_adaptive_protection(shield):
    """Test the adaptive protection mechanism."""
    print("\n===== TESTING ADAPTIVE PROTECTION MECHANISM =====\n")
    
    print("Initial protection layer intensities:")
    for layer_id, status in shield.protection_status.items():
        name = shield.LAYERS[layer_id]['name']
        print(f"  {name}: {status['intensity']:.2f}")
    
    # Simulate multiple unauthorized access attempts to trigger adaptation
    print("\nSimulating multiple unauthorized access attempts...")
    for i in range(3):
        malicious_intent = {
            "truth_alignment": 0.70 - (i * 0.1),
            "ethical_coherence": 0.60 - (i * 0.05),
            "sovereign_preservation": 0.50 - (i * 0.1),
            "conceptual_integrity": 0.65 - (i * 0.05)
        }
        
        shield.verify_steward(f"Attacker_{i}", malicious_intent)
    
    print("\nAdapted protection layer intensities:")
    for layer_id, status in shield.protection_status.items():
        name = shield.LAYERS[layer_id]['name']
        print(f"  {name}: {status['intensity']:.2f}")
    
    # Export the overall security status
    security_status = shield.export_security_status()
    print(f"\nOverall security level: {security_status['overall_security_level']:.4f}")
    
    return shield

def test_content_protection(shield):
    """Test the content protection functionality."""
    print("\n===== TESTING CONTENT PROTECTION =====\n")
    
    # Define some sensitive content representing core system concepts
    sensitive_content = {
        "system_name": "TrueAlphaSpiral",
        "core_concepts": [
            "Ethical Recursion", 
            "Sovereign Verification", 
            "Quantum Ethical Topology"
        ],
        "steward": "Russell Nordland",
        "protection_level": "Alpha-Epsilon"
    }
    
    print("Original content:")
    print(json.dumps(sensitive_content, indent=2))
    
    # Apply protection to the content
    protection_context = {
        "purpose": "export",
        "destination": "public_repository",
        "verified_steward": False
    }
    
    print("\nApplying protection layers...")
    protected_content, metadata = shield.apply_protection(sensitive_content, protection_context)
    
    print("\nProtection metadata:")
    print(f"  Timestamp: {metadata['timestamp']}")
    print(f"  Protection level: {metadata['protection_level']:.4f}")
    print(f"  Layers applied: {len(metadata['layers_applied'])}")
    
    print("\nProtected content:")
    print(json.dumps(protected_content, indent=2))

def main():
    """Run all tests to demonstrate the Guardian Shield capabilities."""
    print("\n===================================================")
    print("    PERSONALIZED GUARDIAN SHIELD DEMONSTRATION    ")
    print("===================================================\n")
    
    print("Initializing Guardian Shield for Russell Nordland...")
    
    # Run tests in sequence, passing the shield instance between them
    shield = test_legitimate_steward()
    shield = test_unauthorized_access(shield)
    shield = test_adaptive_protection(shield)
    test_content_protection(shield)
    
    print("\n====================================================")
    print("    DEMONSTRATION COMPLETE    ")
    print("====================================================\n")

if __name__ == "__main__":
    main()
