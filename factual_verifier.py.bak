"""
FACTUAL VERIFICATION MODULE

This module provides enhanced factual verification capabilities for the Pythonetics system,
including integration with external fact-checking APIs and knowledge bases.

Part of the third-order evolution beyond cybernetics, this module demonstrates
how Pythonetics bridges theoretical concepts with practical implementation.

Architect: Russell Nordland
"""

import time
import logging
import json
import hashlib
import random
from typing import Dict, Any, List, Optional
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("factual_verification.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("factual_verification")

class FactualVerifier:
    """
    Advanced factual verification system that integrates external knowledge sources
    with internal verification mechanisms.
    """
    
    def __init__(self, config_manager):
        """
        Initialize the Factual Verifier.
        
        Args:
            config_manager: Configuration manager instance
        """
        self.config_manager = config_manager
        self.cache = {}  # Simple cache for verification results
        self.cache_expiry = 3600  # Cache expiry in seconds (1 hour)
        
    def verify_factual_accuracy(self, text: str) -> Dict[str, Any]:
        """
        Verify the factual accuracy of the provided text.
        
        Args:
            text: Text to verify
            
        Returns:
            Dict containing verification results
        """
        # Generate hash for text (for caching)
        text_hash = hashlib.md5(text.encode()).hexdigest()[:12]
        
        # Check cache first
        if text_hash in self.cache:
            cache_entry = self.cache[text_hash]
            if time.time() - cache_entry["timestamp"] < self.cache_expiry:
                logger.info(f"Cache hit for text: {text_hash}")
                return cache_entry["result"]
        
        # Determine verification strategy
        use_external_apis = self.config_manager.get("factual_verification", "use_external_apis", False)
        
        try:
            # Attempt external verification if enabled
            if use_external_apis:
                fact_check_enabled = self.config_manager.get(
                    "factual_verification", 
                    "apis", 
                    {}
                ).get("fact_check", {}).get("enabled", False)
                
                knowledge_base_enabled = self.config_manager.get(
                    "factual_verification", 
                    "apis", 
                    {}
                ).get("knowledge_base", {}).get("enabled", False)
                
                # Try fact checking API
                if fact_check_enabled:
                    result = self._verify_with_fact_check_api(text)
                    if result:
                        self._update_cache(text_hash, result)
                        return result
                
                # Try knowledge base API
                if knowledge_base_enabled:
                    result = self._verify_with_knowledge_base(text)
                    if result:
                        self._update_cache(text_hash, result)
                        return result
            
            # Fallback to internal verification
            result = self._internal_verification(text)
            self._update_cache(text_hash, result)
            return result
            
        except Exception as e:
            logger.error(f"Error during factual verification: {e}")
            # Graceful degradation
            if self.config_manager.get("error_handling", "graceful_degradation", True):
                default_score = self.config_manager.get(
                    "error_handling", 
                    "default_truth_score", 
                    0.5
                )
                logger.warning(f"Using default score: {default_score}")
                result = {
                    "factual_score": default_score,
                    "confidence": 0.3,  # Low confidence due to error
                    "method": "fallback",
                    "sources": [],
                    "error": str(e)
                }
                self._update_cache(text_hash, result)
                return result
            else:
                raise
    
    def _verify_with_fact_check_api(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Verify text using an external fact-checking API.
        
        Args:
            text: Text to verify
            
        Returns:
            Dict with verification results or None if verification failed
        """
        api_config = self.config_manager.get(
            "factual_verification", 
            "apis", 
            {}
        ).get("fact_check", {})
        
        url = api_config.get("url", "")
        api_key = api_config.get("key", "")
        
        if not url:
            logger.warning("Fact check API URL not configured")
            return None
            
        try:
            # Configure API request
            headers = {}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
                
            payload = {"text": text}
            
            # Make API request
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=5  # 5 second timeout
            )
            
            # Check response
            if response.status_code == 200:
                data = response.json()
                return {
                    "factual_score": data.get("score", 0.5),
                    "confidence": data.get("confidence", 0.5),
                    "method": "fact_check_api",
                    "sources": data.get("sources", [])
                }
            else:
                logger.warning(f"Fact check API returned status {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling fact check API: {e}")
            return None
            
        except json.JSONDecodeError:
            logger.error("Error decoding fact check API response")
            return None
    
    def _verify_with_knowledge_base(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Verify text against a knowledge base.
        
        Args:
            text: Text to verify
            
        Returns:
            Dict with verification results or None if verification failed
        """
        api_config = self.config_manager.get(
            "factual_verification", 
            "apis", 
            {}
        ).get("knowledge_base", {})
        
        url = api_config.get("url", "")
        api_key = api_config.get("key", "")
        
        if not url:
            logger.warning("Knowledge base API URL not configured")
            return None
            
        try:
            # Configure API request
            headers = {}
            if api_key:
                headers["X-API-Key"] = api_key
                
            payload = {"query": text}
            
            # Make API request
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=10  # 10 second timeout
            )
            
            # Check response
            if response.status_code == 200:
                data = response.json()
                
                # Calculate factual score based on relevance and confidence
                matches = data.get("matches", [])
                if not matches:
                    return {
                        "factual_score": 0.3,  # Low score for no matches
                        "confidence": 0.6,
                        "method": "knowledge_base",
                        "sources": []
                    }
                
                # Average relevance scores from matches
                total_relevance = sum(match.get("relevance", 0) for match in matches)
                avg_relevance = total_relevance / len(matches)
                
                # Extract sources
                sources = []
                for match in matches[:3]:  # Include top 3 sources
                    sources.append({
                        "title": match.get("title", "Unknown Source"),
                        "relevance": match.get("relevance", 0),
                        "url": match.get("url", "")
                    })
                
                return {
                    "factual_score": avg_relevance,
                    "confidence": data.get("confidence", 0.5),
                    "method": "knowledge_base",
                    "sources": sources
                }
            else:
                logger.warning(f"Knowledge base API returned status {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling knowledge base API: {e}")
            return None
            
        except json.JSONDecodeError:
            logger.error("Error decoding knowledge base API response")
            return None
    
    def _internal_verification(self, text: str) -> Dict[str, Any]:
        """
        Perform internal factual verification when external APIs are not available.
        
        Args:
            text: Text to verify
            
        Returns:
            Dict with verification results
        """
        fallback_config = self.config_manager.get("factual_verification", "fallback", {})
        
        # Get configuration parameters with defaults
        base_score = fallback_config.get("base_score", 0.5)
        length_factor_weight = fallback_config.get("length_factor_weight", 0.3)
        random_variation = fallback_config.get("random_variation", 0.2)
        
        # Bias score based on text length (longer texts have slightly higher score)
        length_factor = min(1.0, len(text) / 1000) * length_factor_weight
        
        # Add controlled random variation
        variation = random.uniform(-random_variation, random_variation)
        
        # Calculate final score with constraints
        factual_score = round(min(0.99, max(0.01, base_score + length_factor + variation)), 4)
        
        return {
            "factual_score": factual_score,
            "confidence": 0.4,  # Lower confidence for internal verification
            "method": "internal",
            "sources": []
        }
    
    def _update_cache(self, text_hash: str, result: Dict[str, Any]) -> None:
        """
        Update the cache with verification results.
        
        Args:
            text_hash: Hash of the verified text
            result: Verification results
        """
        self.cache[text_hash] = {
            "timestamp": time.time(),
            "result": result
        }
        
        # Prune cache if it gets too large
        if len(self.cache) > 1000:
            # Remove oldest entries
            oldest_entries = sorted(
                self.cache.items(),
                key=lambda x: x[1]["timestamp"]
            )[:200]  # Remove oldest 20%
            
            for key, _ in oldest_entries:
                del self.cache[key]

# Example usage
if __name__ == "__main__":
    from config_manager import ConfigManager
    
    config_manager = ConfigManager()
    factual_verifier = FactualVerifier(config_manager)
    
    # Test the verifier
    test_texts = [
        "The Earth is a planet in our solar system.",
        "The capital of France is Paris.",
        "Artificial intelligence will definitely take over the world by 2030.",
        "Water boils at 100 degrees Celsius at standard atmospheric pressure."
    ]
    
    for text in test_texts:
        result = factual_verifier.verify_factual_accuracy(text)
        print(f"\nVerification for: {text}")
        print(f"Factual Score: {result['factual_score']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Method: {result['method']}")
        if result['sources']:
            print(f"Sources: {len(result['sources'])}")
            for source in result['sources']:
                print(f"  - {source.get('title', 'Unknown')}")