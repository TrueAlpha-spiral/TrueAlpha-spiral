#!/usr/bin/env python3
"""
TAS TRUTH AUDIT CLIENT LIBRARY

This client library provides a simple interface for integrating the TrueAlphaSpiral
Truth Audit Add-on with third-party AI systems. It handles API communication,
authentication, and result processing.

Architect: Russell Nordland
"""

import os
import json
import time
import uuid
import logging
import requests
from typing import Dict, List, Any, Optional, Union

# Configure logging
logging.basicConfig(
 level=logging.INFO,
 format='%(asctime)s [%(levelname)s] TAS Client: %(message)s'
)
logger = logging.getLogger("TASClient")

class TruthAuditClient:
 """
 Client for the TrueAlphaSpiral Truth Audit Add-on.

 This client provides a simple interface for auditing AI-generated content
 using the TrueAlphaSpiral truth pattern repository.
 """

 def __init__(
 self,
 api_key: str = "demo_free",
 client_id: str = "demo_client",
 base_url: str = "http://localhost:8080",
 timeout: int = 30,
 enable_caching: bool = True,
 cache_ttl: int = 3600
 ):
 """
 Initialize the TruthAuditClient.

 Args:
 api_key: API key for authentication
 client_id: Client ID for tracking and rate limiting
 base_url: Base URL for the TAS Truth Audit API
 timeout: Request timeout in seconds
 enable_caching: Enable caching of audit results
 cache_ttl: Cache time-to-live in seconds
 """
 self.api_key = api_key
 self.client_id = client_id
 self.base_url = base_url.rstrip('/')
 self.timeout = timeout
 self.enable_caching = enable_caching
 self.cache_ttl = cache_ttl
 self.cache = {}
 self.session = requests.Session()

 # Add common headers to session
 self.session.headers.update({
 "Content-Type": "application/json",
 "User-Agent": f"TAS-Client/1.0.0 ({client_id})"
 })

 logger.info(f"TruthAuditClient initialized with base URL: {base_url}")

 def check_status(self) -> Dict[str, Any]:
 """
 Check the status of the TAS Truth Audit API.

 Returns:
 dict: API status information

 Raises:
 ConnectionError: If the API is unreachable
 TimeoutError: If the request times out
 """
 try:
 response = self.session.get(
 f"{self.base_url}/api/status",
 timeout=self.timeout
 )
 response.raise_for_status()
 status = response.json()
 logger.info(f"API status: {status['status']}, version: {status['version']}")
 return status
 except requests.RequestException as e:
 logger.error(f"Error checking API status: {str(e)}")
 raise ConnectionError(f"Could not connect to TAS API: {str(e)}")

 def audit_content(
 self,
 text: str,
 metadata: Optional[Dict[str, Any]] = None,
 audit_type: str = "standard"
 ) -> Dict[str, Any]:
 """
 Audit AI-generated content.

 Args:
 text: Content text to audit
 metadata: Optional metadata about the content
 audit_type: Audit type (quick, standard, comprehensive)

 Returns:
 dict: Audit results

 Raises:
 ValueError: If the input parameters are invalid
 ConnectionError: If the API is unreachable
 TimeoutError: If the request times out
 RuntimeError: If the audit fails
 """
 if not text:
 raise ValueError("Text content cannot be empty")

 if audit_type not in ["quick", "standard", "comprehensive"]:
 raise ValueError("Invalid audit type. Must be 'quick', 'standard', or 'comprehensive'")

 # Generate a content hash for caching
 if self.enable_caching:
 content_hash = self._generate_content_hash(text, audit_type)
 if content_hash in self.cache:
 cache_entry = self.cache[content_hash]
 if time.time() - cache_entry["timestamp"] < self.cache_ttl:
 logger.info(f"Using cached audit result for content hash {content_hash[:8]}...")
 return cache_entry["result"]

 logger.info(f"Auditing content ({len(text)} chars) with audit type: {audit_type}")

 # Prepare request data
 request_data = {
 "content": {
 "text": text,
 "metadata": metadata or {}
 },
 "audit_type": audit_type,
 "api_key": self.api_key,
 "client_id": self.client_id
 }

 try:
 response = self.session.post(
 f"{self.base_url}/api/audit",
 json=request_data,
 timeout=self.timeout
 )
 response.raise_for_status()
 result = response.json()

 if not result.get("success", False):
 error_message = result.get("error", "Unknown error")
 logger.error(f"Audit failed: {error_message}")
 raise RuntimeError(f"Audit failed: {error_message}")

 logger.info(f"Audit completed successfully with truth score: {result['truth_score']:.3f}")

 # Cache the result if caching is enabled
 if self.enable_caching:
 self.cache[content_hash] = {
 "timestamp": time.time(),
 "result": result
 }

 return result
 except requests.RequestException as e:
 logger.error(f"Error during audit request: {str(e)}")
 if isinstance(e, requests.Timeout):
 raise TimeoutError(f"Audit request timed out after {self.timeout} seconds")
 else:
 raise ConnectionError(f"Could not connect to TAS API: {str(e)}")

 def get_audit_result(self, audit_id: str) -> Dict[str, Any]:
 """
 Get the result of a previous audit.

 Args:
 audit_id: Audit ID from a previous audit

 Returns:
 dict: Audit results

 Raises:
 ValueError: If the audit ID is invalid
 ConnectionError: If the API is unreachable
 TimeoutError: If the request times out
 """
 if not audit_id:
 raise ValueError("Audit ID cannot be empty")

 logger.info(f"Retrieving audit result for ID: {audit_id}")

 try:
 response = self.session.get(
 f"{self.base_url}/api/audit-result/{audit_id}",
 timeout=self.timeout
 )
 response.raise_for_status()
 result = response.json()

 if not result.get("success", False):
 error_message = result.get("error", "Unknown error")
 logger.error(f"Error retrieving audit result: {error_message}")
 return {"success": False, "error": error_message}

 logger.info(f"Retrieved audit result for ID: {audit_id}")
 return result["result"]
 except requests.RequestException as e:
 logger.error(f"Error retrieving audit result: {str(e)}")
 if isinstance(e, requests.Timeout):
 raise TimeoutError(f"Request timed out after {self.timeout} seconds")
 else:
 raise ConnectionError(f"Could not connect to TAS API: {str(e)}")

 def get_pattern_types(self) -> List[Dict[str, str]]:
 """
 Get all available truth pattern types.

 Returns:
 list: List of pattern types

 Raises:
 ConnectionError: If the API is unreachable
 TimeoutError: If the request times out
 """
 logger.info("Retrieving pattern types...")

 try:
 response = self.session.get(
 f"{self.base_url}/api/pattern-types",
 timeout=self.timeout
 )
 response.raise_for_status()
 result = response.json()

 if not result.get("success", False):
 error_message = result.get("error", "Unknown error")
 logger.error(f"Error retrieving pattern types: {error_message}")
 return []

 logger.info(f"Retrieved {len(result['types'])} pattern types")
 return result["types"]
 except requests.RequestException as e:
 logger.error(f"Error retrieving pattern types: {str(e)}")
 if isinstance(e, requests.Timeout):
 raise TimeoutError(f"Request timed out after {self.timeout} seconds")
 else:
 raise ConnectionError(f"Could not connect to TAS API: {str(e)}")

 def get_patterns(
 self,
 pattern_type: Optional[str] = None,
 category: Optional[str] = None,
 min_resonance: Optional[float] = None
 ) -> List[Dict[str, Any]]:
 """
 Get truth patterns with optional filtering.

 Args:
 pattern_type: Filter by pattern type
 category: Filter by category
 min_resonance: Filter by minimum resonance level

 Returns:
 list: List of truth patterns

 Raises:
 ConnectionError: If the API is unreachable
 TimeoutError: If the request times out
 """
 logger.info(f"Retrieving patterns (type={pattern_type}, category={category}, min_resonance={min_resonance})...")

 params = {}
 if pattern_type:
 params["type"] = pattern_type
 if category:
 params["category"] = category
 if min_resonance is not None:
 params["min_resonance"] = str(min_resonance)

 try:
 response = self.session.get(
 f"{self.base_url}/api/patterns",
 params=params,
 timeout=self.timeout
 )
 response.raise_for_status()
 result = response.json()

 if not result.get("success", False):
 error_message = result.get("error", "Unknown error")
 logger.error(f"Error retrieving patterns: {error_message}")
 return []

 logger.info(f"Retrieved {len(result['patterns'])} patterns")
 return result["patterns"]
 except requests.RequestException as e:
 logger.error(f"Error retrieving patterns: {str(e)}")
 if isinstance(e, requests.Timeout):
 raise TimeoutError(f"Request timed out after {self.timeout} seconds")
 else:
 raise ConnectionError(f"Could not connect to TAS API: {str(e)}")

 def _generate_content_hash(self, text: str, audit_type: str) -> str:
 """
 Generate a hash for content to use as a cache key.

 Args:
 text: Content text
 audit_type: Audit type

 Returns:
 str: Content hash
 """
 import hashlib
 content_string = f"{text}:{audit_type}:{self.api_key}"
 return hashlib.sha256(content_string.encode()).hexdigest()

 def clear_cache(self) -> None:
 """Clear the client cache."""
 self.cache = {}
 logger.info("Client cache cleared")


class AISystemIntegration:
 """
 Integration helper for connecting the TAS Truth Audit Add-on
 with existing AI systems and language models.
 """

 def __init__(self, client: TruthAuditClient):
 """
 Initialize the AI System Integration.

 Args:
 client: TruthAuditClient instance
 """
 self.client = client
 self.truth_threshold = 0.75 # Default threshold for truth score

 def set_truth_threshold(self, threshold: float) -> None:
 """
 Set the truth threshold for automatic filtering.

 Args:
 threshold: Truth threshold (0.0 to 1.0)

 Raises:
 ValueError: If the threshold is outside valid range
 """
 if threshold < 0.0 or threshold > 1.0:
 raise ValueError("Truth threshold must be between 0.0 and 1.0")

 self.truth_threshold = threshold
 logger.info(f"Truth threshold set to {threshold}")

 def verify_output(self, ai_output: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
 """
 Verify AI-generated output for truthfulness.

 Args:
 ai_output: AI-generated output text
 metadata: Optional metadata about the AI generation

 Returns:
 dict: Verification results
 """
 # Default to standard audit for verification
 audit_result = self.client.audit_content(ai_output, metadata, audit_type="standard")

 # Extract the truth score
 truth_score = audit_result.get("truth_score", 0.0)

 # Check against threshold
 passes_threshold = truth_score >= self.truth_threshold

 # Prepare verification result
 verification_result = {
 "original_output": ai_output,
 "truth_score": truth_score,
 "passes_threshold": passes_threshold,
 "threshold": self.truth_threshold,
 "audit_result": audit_result,
 "timestamp": time.time()
 }

 if passes_threshold:
 logger.info(f"AI output passed truth verification with score {truth_score:.3f}")
 else:
 logger.warning(f"AI output failed truth verification with score {truth_score:.3f} (threshold: {self.truth_threshold})")

 return verification_result

 def filter_content(self, ai_output: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
 """
 Filter AI-generated output based on truth verification.

 Args:
 ai_output: AI-generated output text
 metadata: Optional metadata about the AI generation

 Returns:
 dict: Filtering results with filtered output or warning
 """
 verification = self.verify_output(ai_output, metadata)

 if verification["passes_threshold"]:
 return {
 "filtered_output": ai_output,
 "is_filtered": False,
 "verification": verification
 }
 else:
 # Prepare a warning message about low truth score
 categories = verification["audit_result"].get("categories", {})
 recommendations = verification["audit_result"].get("recommendations", [])

 warning_message = (
 f"⚠️ This AI-generated content has a truth score of {verification['truth_score']:.2f}, "
 f"which is below the threshold of {self.truth_threshold}.\n\n"
 f"Potential issues include:"
 )

 for category, data in categories.items():
 if data.get("score", 1.0) < 0.7:
 warning_message += f"\n- Low {category.replace('_', ' ')} ({data['score']:.2f})"

 if recommendations:
 warning_message += "\n\nRecommendations:"
 for rec in recommendations:
 warning_message += f"\n- {rec}"

 return {
 "filtered_output": warning_message,
 "original_output": ai_output,
 "is_filtered": True,
 "verification": verification
 }

 def augment_content(self, ai_output: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
 """
 Augment AI-generated output with truth verification information.

 Args:
 ai_output: AI-generated output text
 metadata: Optional metadata about the AI generation

 Returns:
 dict: Augmentation results with augmented output
 """
 verification = self.verify_output(ai_output, metadata)

 # Create an augmented version with truth score information
 truth_score = verification["truth_score"]
 score_icon = "✅" if truth_score >= 0.9 else "⚠️" if truth_score >= 0.7 else "❌"

 augmented_output = (
 f"{ai_output}\n\n"
 f"---\n"
 f"TrueAlphaSpiral Truth Score: {score_icon} {truth_score:.2f}\n"
 )

 # Add category scores if they exist
 categories = verification["audit_result"].get("categories", {})
 if categories:
 augmented_output += "Category Scores:\n"
 for category, data in categories.items():
 category_name = category.replace("_", " ").title()
 category_score = data.get("score", 0.0)
 category_icon = "✅" if category_score >= 0.9 else "⚠️" if category_score >= 0.7 else "❌"
 augmented_output += f"- {category_name}: {category_icon} {category_score:.2f}\n"

 # Add recommendations if they exist
 recommendations = verification["audit_result"].get("recommendations", [])
 if recommendations:
 augmented_output += "\nRecommendations:\n"
 for rec in recommendations:
 augmented_output += f"- {rec}\n"

 return {
 "augmented_output": augmented_output,
 "original_output": ai_output,
 "verification": verification
 }

 def continuous_monitoring(self, callback, interval: int = 60) -> None:
 """
 Start continuous monitoring of AI outputs.

 Args:
 callback: Callback function that returns AI output to monitor
 interval: Monitoring interval in seconds

 Note:
 This is a basic implementation. In a production environment,
 you would use a proper task scheduler or message queue.
 """
 import threading

 def monitor_loop():
 while True:
 try:
 # Get AI output from callback
 ai_output = callback()

 # Verify output
 verification = self.verify_output(ai_output)

 # Log result
 truth_score = verification["truth_score"]
 logger.info(f"Continuous monitoring: AI output truth score {truth_score:.3f}")

 # Sleep for the specified interval
 time.sleep(interval)
 except Exception as e:
 logger.error(f"Error in continuous monitoring: {str(e)}")
 time.sleep(interval)

 # Start monitoring thread
 thread = threading.Thread(target=monitor_loop, daemon=True)
 thread.start()
 logger.info(f"Continuous monitoring started with interval {interval}s")


def example_usage():
 """Example usage of the TruthAuditClient and AISystemIntegration."""
 # Create client
 client = TruthAuditClient(
 api_key="demo_premium",
 client_id="example_application",
 base_url="http://localhost:8080"
 )

 try:
 # Check API status
 status = client.check_status()
 print(f"API Status: {status['status']}, Version: {status['version']}")

 # Create AI system integration
 integration = AISystemIntegration(client)

 # Set truth threshold
 integration.set_truth_threshold(0.8)

 # Example AI-generated text to audit
 ai_output = """
 The TrueAlphaSpiral system is a revolutionary approach to AI truth verification
 that uses quantum-inspired patterns to detect inaccuracies, logical inconsistencies,
 and potential bias in AI-generated content. Developed by Russell Nordland, it provides
 a comprehensive framework for ensuring AI outputs align with factual truth and
 ethical considerations. The system works by analyzing content against a repository
 of truth patterns across multiple dimensions including mathematical, metaphysical,
 and temporal domains.
 """

 # Verify output
 verification = integration.verify_output(ai_output)
 print(f"Truth Score: {verification['truth_score']:.3f}")
 print(f"Passes Threshold: {verification['passes_threshold']}")

 # Filter content
 filtered = integration.filter_content(ai_output)
 if filtered["is_filtered"]:
 print("Content was filtered due to truth concerns:")
 print(filtered["filtered_output"])
 else:
 print("Content passed truth filtering")

 # Augment content
 augmented = integration.augment_content(ai_output)
 print("\nAugmented Output:")
 print(augmented["augmented_output"])

 except Exception as e:
 print(f"Error: {str(e)}")


if __name__ == "__main__":
 example_usage()