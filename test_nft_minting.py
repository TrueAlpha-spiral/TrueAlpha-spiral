#!/usr/bin/env python3
"""
NFT HAIKU MINTING TEST SCRIPT

This script tests the NFT minting functionality in the Quantum Echo Authenticator.
It connects to the quantum-entangled blockchain, mints a haiku as an NFT,
and verifies its authenticity.

Architect: Russell Nordland
"""

import sys
import time
from quantum_echo_authenticator import QuantumEchoAuthenticator

# ANSI colors for terminal output
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_header():
 """Print the header for the test script."""
 print(f"\n{BOLD}{CYAN}===================================================={RESET}")
 print(f"{BOLD}{CYAN} QUANTUM ECHO AUTHENTICATOR - NFT MINTING TEST {RESET}")
 print(f"{BOLD}{CYAN}===================================================={RESET}")
 print(f"{YELLOW}Connecting to the quantum-entangled blockchain...{RESET}")
 print(f"{YELLOW}Testing haiku verification and NFT minting...{RESET}")

def print_section(title):
 """Print a section header."""
 print(f"\n{BOLD}{CYAN}----------------------------------------------------{RESET}")
 print(f"{BOLD}{CYAN} {title} {RESET}")
 print(f"{BOLD}{CYAN}----------------------------------------------------{RESET}")

def main():
 """Run the NFT minting test."""
 print_header()

 # Create and initialize the authenticator
 print(f"\n{YELLOW}Initializing Quantum Echo Authenticator...{RESET}")
 authenticator = QuantumEchoAuthenticator()
 initialized = authenticator.initialize()

 if not initialized:
 print(f"{RED}Failed to initialize Quantum Echo Authenticator. Exiting.{RESET}")
 return 1

 print(f"{GREEN}Quantum Echo Authenticator initialized successfully.{RESET}")

 # Connect to the blockchain
 print_section("BLOCKCHAIN CONNECTION")
 connected = authenticator.connect_blockchain()

 if not connected:
 print(f"{RED}Failed to connect to blockchain. Exiting.{RESET}")
 return 1

 # Generate a verification haiku
 print_section("HAIKU GENERATION")
 haiku = authenticator.generate_verification_haiku()
 # Print the haiku with line breaks
 formatted_haiku = haiku.replace(" / ", "\n")
 print(f"{CYAN}{formatted_haiku}{RESET}")

 # Verify the haiku
 print_section("HAIKU VERIFICATION")
 verified = authenticator.verify_haiku(haiku)

 if not verified:
 print(f"{RED}Haiku verification failed. Cannot mint NFT.{RESET}")
 return 1

 print(f"{GREEN}Haiku verified successfully.{RESET}")

 # Check channel security
 secure = authenticator.check_channel_security()
 print(f"Channel security: {GREEN if secure else RED}{secure}{RESET}")

 if not secure:
 print(f"{RED}Channel not secure. Cannot mint NFT.{RESET}")
 return 1

 # Mint the haiku as an NFT
 print_section("NFT MINTING")
 print(f"{YELLOW}Minting haiku as NFT...{RESET}")

 # Use a test wallet address
 wallet_address = "0x71C7656EC7ab88b098defB751B7401B5f6d8976F"

 nft = authenticator.mint_haiku_nft(haiku, wallet_address)

 if not nft:
 print(f"{RED}Failed to mint NFT.{RESET}")
 return 1

 print(f"{GREEN}NFT minted successfully!{RESET}")
 print(f"Token ID: {CYAN}{nft['token_id']}{RESET}")
 print(f"Owner: {CYAN}{nft['owner_address']}{RESET}")
 print(f"Transaction: {CYAN}{nft['transaction_hash'][:16]}...{RESET}")
 print(f"Timestamp: {CYAN}{nft['timestamp']}{RESET}")

 # Verify NFT authenticity
 print_section("NFT AUTHENTICITY VERIFICATION")
 print(f"{YELLOW}Verifying NFT authenticity...{RESET}")

 verification = authenticator.verify_nft_authenticity(nft['token_id'])

 if not verification['authentic']:
 print(f"{RED}NFT authenticity verification failed!{RESET}")
 if not verification.get('syllable_check', False):
 print(f"Syllable check: {RED}Failed{RESET}")
 if not verification.get('signature_check', False):
 print(f"Signature check: {RED}Failed{RESET}")
 return 1

 print(f"{GREEN}NFT authenticity verified! ✓{RESET}")
 print(f"Syllable check: {GREEN}Passed{RESET}")
 print(f"Signature check: {GREEN}Passed{RESET}")

 # Retrieve all minted NFTs
 print_section("RETRIEVING ALL MINTED NFTS")
 all_nfts = authenticator.get_minted_nfts()
 print(f"Total NFTs minted: {CYAN}{len(all_nfts)}{RESET}")

 print_section("TEST COMPLETE")
 print(f"{GREEN}NFT minting test completed successfully.{RESET}")
 print(f"{BOLD}The haiku is now permanently recorded on the quantum-entangled blockchain{RESET}")
 print(f"{BOLD}as an NFT with cryptographic proof of authenticity.{RESET}")

 return 0

if __name__ == "__main__":
 sys.exit(main())