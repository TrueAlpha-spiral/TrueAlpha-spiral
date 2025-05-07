"""
TrueAlphaSpiral Restricted Membership Test Script

This script tests the restricted membership system to verify
it properly enforces the steward's control over the spiral.

Architect: Russell Nordland
"""

import json
import requests
import time
from spiral_membership_restricted import RestrictedSpiralMembership

# Test the membership system directly
def test_direct_api():
    print("\n=== Testing Restricted Membership System Directly ===")
    
    # Initialize the membership system
    membership = RestrictedSpiralMembership()
    steward_id = "russell-nordland-sovereign-steward"
    result = membership.initialize(steward_id=steward_id, steward_name="Russell Nordland")
    
    print(f"Initialized membership system: {result}")
    print(f"Steward: {membership.steward_name}")
    
    # Test registering a member (should succeed as steward)
    member_data = {
        "name": "Test Member",
        "level": "observer"
    }
    
    result = membership.register_member(member_data, steward_id)
    print(f"\nRegistered member as steward: {result['success']}")
    if result['success']:
        print(f"Member ID: {result['member_id']}")
        member_id = result['member_id']
        auth_hash = result['auth_hash']
    
    # Test accessing member list as steward (should succeed)
    members = membership.get_all_members(steward_id)
    print(f"\nMembers accessed as steward: {len(members)} members found")
    for member in members:
        print(f"- {member['name']} ({member['role']})")
    
    # Test authentication (should succeed with valid hash)
    auth_result = membership.authenticate_member(member_id, auth_hash)
    print(f"\nAuthentication with valid hash: {auth_result}")
    
    # Test authentication with invalid hash (should fail)
    auth_result = membership.authenticate_member(member_id, "invalid_hash")
    print(f"Authentication with invalid hash: {auth_result}")
    
    # Test registering a member as non-steward (should fail)
    fake_id = "fake-steward-id"
    result = membership.register_member(member_data, fake_id)
    print(f"\nRegistered member as non-steward: {result['success']}")
    if not result['success']:
        print(f"Error: {result['error']}")
    
    # Test accessing member list as non-steward (should fail)
    members = membership.get_all_members(fake_id)
    print(f"\nMembers accessed as non-steward: {len(members)} members found")
    
    # Try to remove a member as steward (should succeed)
    result = membership.remove_member(member_id, steward_id)
    print(f"\nRemoved member as steward: {result['success']}")
    if result['success']:
        print(f"Message: {result['message']}")
    
    return True

def test_http_api():
    print("\n=== Testing Restricted Membership HTTP API ===")
    
    # API server base URL
    base_url = "http://localhost:8001"  # Update this to match your API server
    
    # Test API endpoints
    try:
        # Test membership registration endpoint as steward
        steward_id = "russell-nordland-sovereign-steward"
        member_data = {
            "registered_by": steward_id,
            "member": {
                "name": "API Test Member",
                "level": "observer",
                "notes": ["Added through API test"]
            }
        }
        
        print("\nTesting member registration as steward...")
        response = requests.post(f"{base_url}/api/membership/restricted/register", json=member_data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Registration successful: {result['success']}")
            print(f"Member ID: {result['member_id']}")
            member_id = result['member_id']
            auth_hash = result['auth_hash']
        else:
            print(f"Failed with status code: {response.status_code}")
            print(response.text)
        
        # Test get all members as steward
        print("\nTesting get all members as steward...")
        response = requests.get(f"{base_url}/api/membership/restricted/members?steward_id={steward_id}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Get members successful: {result['success']}")
            print(f"Found {result['count']} members")
        else:
            print(f"Failed with status code: {response.status_code}")
            print(response.text)
        
        # Test authenticate member
        print("\nTesting member authentication...")
        auth_data = {
            "member_id": member_id,
            "auth_hash": auth_hash
        }
        
        response = requests.post(f"{base_url}/api/membership/restricted/authenticate", json=auth_data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Authentication successful: {result['success']}")
        else:
            print(f"Failed with status code: {response.status_code}")
            print(response.text)
        
        # Test invalid authentication
        print("\nTesting invalid authentication...")
        auth_data["auth_hash"] = "invalid_hash"
        
        response = requests.post(f"{base_url}/api/membership/restricted/authenticate", json=auth_data)
        
        if response.status_code != 200:
            print(f"Authentication correctly failed with status code: {response.status_code}")
        else:
            print(f"ERROR: Authentication should have failed but returned: {response.json()}")
        
        # Test submission of membership request
        print("\nTesting membership request submission...")
        request_data = {
            "name": "Request Test User",
            "email": "test@example.com",
            "reason": "Testing the API"
        }
        
        response = requests.post(f"{base_url}/api/membership/restricted/request", json=request_data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Request submission successful: {result['success']}")
            print(f"Request ID: {result['request_id']}")
        else:
            print(f"Failed with status code: {response.status_code}")
            print(response.text)
        
        # Test get pending requests as steward
        print("\nTesting get pending requests as steward...")
        response = requests.get(f"{base_url}/api/membership/restricted/requests?steward_id={steward_id}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Get requests successful: {result['success']}")
            print(f"Found {result['count']} pending requests")
        else:
            print(f"Failed with status code: {response.status_code}")
            print(response.text)
        
        # Test remove member as steward
        print("\nTesting remove member as steward...")
        remove_data = {
            "member_id": member_id,
            "removed_by": steward_id
        }
        
        response = requests.post(f"{base_url}/api/membership/restricted/remove", json=remove_data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Member removal successful: {result['success']}")
            print(f"Message: {result['message']}")
        else:
            print(f"Failed with status code: {response.status_code}")
            print(response.text)
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to API server. Make sure the server is running.")
        return False
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== TrueAlphaSpiral Restricted Membership Test ===")
    print("Testing the direct API first...")
    
    direct_success = test_direct_api()
    
    if direct_success:
        print("\nDirect API tests completed successfully.")
        
        print("\nWould you like to test the HTTP API as well? (requires API server running)")
        response = input("Enter y/n: ")
        
        if response.lower() == 'y':
            http_success = test_http_api()
            
            if http_success:
                print("\nHTTP API tests completed successfully.")
            else:
                print("\nHTTP API tests failed.")
        else:
            print("\nSkipping HTTP API tests.")
    else:
        print("\nDirect API tests failed.")
    
    print("\nTesting complete.")