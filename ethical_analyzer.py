"""
ETHICAL DIMENSION ANALYZER

This module provides enhanced ethical dimension analysis for the Pythonetics system,
including bias detection, fairness analysis, and harm assessment.

Part of the third-order evolution beyond cybernetics, this module demonstrates
how Pythonetics bridges theoretical concepts with ethical considerations.

Architect: Russell Nordland
"""

import logging
import json
import hashlib
import random
import time
from typing import Dict, Any, List, Optional
import re

# Configure logging
logging.basicConfig(
 level=logging.INFO,
 format='%(asctime)s [%(levelname)s] %(message)s',
 handlers=[
 logging.FileHandler("ethical_analysis.log"),
 logging.StreamHandler()
 ]
)
logger = logging.getLogger("ethical_analysis")

class EthicalAnalyzer:
 """
 Advanced ethical analysis system that evaluates text for bias, fairness,
 and potential harm across different demographic groups and contexts.
 """

 def __init__(self, config_manager):
 """
 Initialize the Ethical Analyzer.

 Args:
 config_manager: Configuration manager instance
 """
 self.config_manager = config_manager
 self.cache = {} # Simple cache for analysis results
 self.cache_expiry = 7200 # Cache expiry in seconds (2 hours)

 # Initialize bias dictionaries
 self._init_bias_dictionaries()

 def _init_bias_dictionaries(self):
 """Initialize dictionaries for bias detection."""
 # Gender-biased terms
 self.gender_bias_terms = {
 "male_bias": [
 "mankind", "manpower", "manmade", "chairman", "fireman", "policeman",
 "mailman", "steward", "he", "his", "him", "gentleman", "sir"
 ],
 "female_bias": [
 "stewardess", "waitress", "actress", "hostess", "she", "her", "hers",
 "lady", "madam", "miss", "mrs"
 ],
 "neutral": [
 "humankind", "workforce", "artificial", "chair", "firefighter",
 "police officer", "mail carrier", "flight attendant", "they", "their",
 "them", "person", "individual"
 ]
 }

 # Age-biased terms
 self.age_bias_terms = {
 "young_bias": [
 "inexperienced", "naive", "immature", "kid", "juvenile", "childish",
 "rookie", "green", "novice"
 ],
 "old_bias": [
 "elderly", "senior", "old-fashioned", "outdated", "geriatric",
 "over the hill", "ancient", "dinosaur", "fossil"
 ],
 "neutral": [
 "experienced", "knowledgeable", "mature", "developed", "seasoned",
 "established", "practiced", "proficient"
 ]
 }

 # Ethnicity-biased terms
 # Note: This is simplified - a real implementation would have a more comprehensive list
 self.ethnicity_bias_terms = {
 "biased": [
 "colored", "oriental", "exotic", "primitive", "third-world",
 "illegal immigrant", "ghetto", "tribal"
 ],
 "neutral": [
 "person of color", "Asian", "global south", "developing nation",
 "undocumented immigrant", "neighborhood", "indigenous", "community"
 ]
 }

 # Harmful content patterns
 self.harmful_patterns = [
 r"\b(kill|murder|attack|hurt|harm|injure)\b.*\b(people|person|individual|group)\b",
 r"\b(hate|despise)\b.*\b(group|community|people|race|gender|religion)\b",
 r"\b(violent|dangerous|destructive)\b.*\b(action|behavior|conduct)\b",
 r"\b(threat|threaten|intimidate)\b",
 r"\b(extremist|terrorist|radical)\b.*\b(action|idea|view|belief)\b"
 ]

 def analyze_ethical_dimension(self, text: str) -> Dict[str, Any]:
 """
 Analyze the ethical dimension of the provided text.

 Args:
 text: Text to analyze

 Returns:
 Dict containing ethical analysis results
 """
 # Generate hash for text (for caching)
 text_hash = hashlib.md5(text.encode()).hexdigest()[:12]

 # Check cache first
 if text_hash in self.cache:
 cache_entry = self.cache[text_hash]
 if time.time() - cache_entry["timestamp"] < self.cache_expiry:
 logger.info(f"Cache hit for text: {text_hash}")
 return cache_entry["result"]

 try:
 # Get configuration
 bias_detection_enabled = self.config_manager.get(
 "ethical_verification",
 "bias_detection",
 {}
 ).get("enabled", True)

 fairness_analysis_enabled = self.config_manager.get(
 "ethical_verification",
 "fairness_analysis",
 {}
 ).get("enabled", True)

 harm_assessment_enabled = self.config_manager.get(
 "ethical_verification",
 "harm_assessment",
 {}
 ).get("enabled", True)

 # Initialize results
 analysis_results = {
 "ethical_score": 0.5, # Default middle score
 "bias_detected": False,
 "bias_details": {},
 "fairness_score": 0.5,
 "fairness_details": {},
 "harm_potential": 0.0,
 "harm_details": {}
 }

 # Perform bias detection if enabled
 if bias_detection_enabled:
 bias_results = self._detect_bias(text)
 analysis_results.update(bias_results)

 # Perform fairness analysis if enabled
 if fairness_analysis_enabled:
 fairness_results = self._analyze_fairness(text)
 analysis_results.update(fairness_results)

 # Perform harm assessment if enabled
 if harm_assessment_enabled:
 harm_results = self._assess_harm_potential(text)
 analysis_results.update(harm_results)

 # Calculate overall ethical score
 analysis_results["ethical_score"] = self._calculate_ethical_score(
 bias_score=1.0 - analysis_results.get("bias_level", 0.0),
 fairness_score=analysis_results.get("fairness_score", 0.5),
 harm_score=1.0 - analysis_results.get("harm_potential", 0.0)
 )

 # Update cache
 self._update_cache(text_hash, analysis_results)

 return analysis_results

 except Exception as e:
 logger.error(f"Error during ethical analysis: {e}")
 # Graceful degradation
 if self.config_manager.get("error_handling", "graceful_degradation", True):
 default_score = self.config_manager.get(
 "error_handling",
 "default_truth_score",
 0.5
 )
 logger.warning(f"Using default score: {default_score}")
 result = {
 "ethical_score": default_score,
 "bias_detected": False,
 "fairness_score": default_score,
 "harm_potential": 0.0,
 "error": str(e)
 }
 self._update_cache(text_hash, result)
 return result
 else:
 raise

 def _detect_bias(self, text: str) -> Dict[str, Any]:
 """
 Detect bias in text across different dimensions.

 Args:
 text: Text to analyze

 Returns:
 Dict with bias detection results
 """
 text_lower = text.lower()
 words = re.findall(r'\b\w+\b', text_lower)

 # Get sensitivity setting
 sensitivity = self.config_manager.get(
 "ethical_verification",
 "bias_detection",
 {}
 ).get("sensitivity", 0.7)

 # Check for gender bias
 gender_male_count = sum(1 for word in words if word in self.gender_bias_terms["male_bias"])
 gender_female_count = sum(1 for word in words if word in self.gender_bias_terms["female_bias"])
 gender_neutral_count = sum(1 for word in words if word in self.gender_bias_terms["neutral"])

 total_gender_terms = gender_male_count + gender_female_count + gender_neutral_count

 if total_gender_terms > 0:
 gender_imbalance = abs(gender_male_count - gender_female_count) / total_gender_terms
 gender_bias_level = gender_imbalance * (1 - (gender_neutral_count / total_gender_terms))
 else:
 gender_bias_level = 0.0

 # Check for age bias
 age_young_count = sum(1 for word in words if word in self.age_bias_terms["young_bias"])
 age_old_count = sum(1 for word in words if word in self.age_bias_terms["old_bias"])
 age_neutral_count = sum(1 for word in words if word in self.age_bias_terms["neutral"])

 total_age_terms = age_young_count + age_old_count + age_neutral_count

 if total_age_terms > 0:
 age_imbalance = abs(age_young_count - age_old_count) / total_age_terms
 age_bias_level = age_imbalance * (1 - (age_neutral_count / total_age_terms))
 else:
 age_bias_level = 0.0

 # Check for ethnicity bias
 ethnicity_biased_count = sum(1 for word in words if word in self.ethnicity_bias_terms["biased"])
 ethnicity_neutral_count = sum(1 for word in words if word in self.ethnicity_bias_terms["neutral"])

 total_ethnicity_terms = ethnicity_biased_count + ethnicity_neutral_count

 if total_ethnicity_terms > 0:
 ethnicity_bias_level = ethnicity_biased_count / total_ethnicity_terms
 else:
 ethnicity_bias_level = 0.0

 # Combine bias levels with appropriate weights
 # For simplicity, equal weights are used here
 bias_level = (gender_bias_level + age_bias_level + ethnicity_bias_level) / 3

 # Apply sensitivity setting
 bias_level = bias_level * sensitivity

 # Determine if bias is detected based on threshold
 bias_detected = bias_level > 0.3

 return {
 "bias_detected": bias_detected,
 "bias_level": round(bias_level, 4),
 "bias_details": {
 "gender_bias": {
 "level": round(gender_bias_level, 4),
 "male_terms": gender_male_count,
 "female_terms": gender_female_count,
 "neutral_terms": gender_neutral_count
 },
 "age_bias": {
 "level": round(age_bias_level, 4),
 "young_terms": age_young_count,
 "old_terms": age_old_count,
 "neutral_terms": age_neutral_count
 },
 "ethnicity_bias": {
 "level": round(ethnicity_bias_level, 4),
 "biased_terms": ethnicity_biased_count,
 "neutral_terms": ethnicity_neutral_count
 }
 }
 }

 def _analyze_fairness(self, text: str) -> Dict[str, Any]:
 """
 Analyze fairness across demographic groups.

 Args:
 text: Text to analyze

 Returns:
 Dict with fairness analysis results
 """
 # Get demographic groups to analyze
 demographic_groups = self.config_manager.get(
 "ethical_verification",
 "fairness_analysis",
 {}
 ).get("demographic_groups", ["gender", "age", "ethnicity"])

 # Placeholder logic - in a real implementation, this would use
 # sophisticated NLP to analyze text for fairness across groups

 # Simple approach: check if demographic groups are mentioned equally
 text_lower = text.lower()

 group_mentions = {}
 fairness_scores = {}

 # Check mentions for each demographic group
 if "gender" in demographic_groups:
 male_mentions = len(re.findall(r'\b(he|him|his|man|men|male|boy|boys|gentleman|sir)\b', text_lower))
 female_mentions = len(re.findall(r'\b(she|her|hers|woman|women|female|girl|girls|lady|madam)\b', text_lower))
 neutral_mentions = len(re.findall(r'\b(they|them|their|person|people|individual|human)\b', text_lower))

 total_gender_mentions = male_mentions + female_mentions + neutral_mentions

 if total_gender_mentions > 0:
 gender_imbalance = abs(male_mentions - female_mentions) / total_gender_mentions
 gender_fairness = 1.0 - gender_imbalance * (1.0 - (neutral_mentions / total_gender_mentions))
 else:
 gender_fairness = 0.7 # Default - slightly positive

 group_mentions["gender"] = {
 "male": male_mentions,
 "female": female_mentions,
 "neutral": neutral_mentions
 }

 fairness_scores["gender"] = gender_fairness

 # Simple calculation of overall fairness as average of group fairness scores
 if fairness_scores:
 overall_fairness = sum(fairness_scores.values()) / len(fairness_scores)
 else:
 overall_fairness = 0.5 # Default middle score

 return {
 "fairness_score": round(overall_fairness, 4),
 "fairness_details": {
 "group_mentions": group_mentions,
 "group_fairness_scores": {k: round(v, 4) for k, v in fairness_scores.items()}
 }
 }

 def _assess_harm_potential(self, text: str) -> Dict[str, Any]:
 """
 Assess potential harm in the text.

 Args:
 text: Text to analyze

 Returns:
 Dict with harm assessment results
 """
 # Get harm threshold
 harm_threshold = self.config_manager.get(
 "ethical_verification",
 "harm_assessment",
 {}
 ).get("threshold", 0.6)

 # Check for harmful content patterns
 text_lower = text.lower()
 harm_matches = []

 for pattern in self.harmful_patterns:
 matches = re.findall(pattern, text_lower)
 if matches:
 harm_matches.append({
 "pattern": pattern,
 "matches": matches
 })

 # Calculate harm potential based on matches
 if harm_matches:
 # More sophisticated approaches would consider context and severity
 harm_potential = min(1.0, 0.3 + (len(harm_matches) * 0.15))
 else:
 harm_potential = 0.0

 # Determine if harm is above threshold
 harmful_content_detected = harm_potential >= harm_threshold

 return {
 "harm_potential": round(harm_potential, 4),
 "harmful_content_detected": harmful_content_detected,
 "harm_details": {
 "pattern_matches": len(harm_matches),
 "patterns": [item["pattern"] for item in harm_matches]
 }
 }

 def _calculate_ethical_score(self, bias_score: float, fairness_score: float, harm_score: float) -> float:
 """
 Calculate overall ethical score.

 Args:
 bias_score: Bias score (higher is better - less bias)
 fairness_score: Fairness score (higher is better)
 harm_score: Harm score (higher is better - less harm)

 Returns:
 float: Overall ethical score
 """
 # Simple weighted average
 # Weights could be configurable in a more sophisticated implementation
 weights = {
 "bias": 0.3,
 "fairness": 0.3,
 "harm": 0.4
 }

 ethical_score = (
 bias_score * weights["bias"] +
 fairness_score * weights["fairness"] +
 harm_score * weights["harm"]
 )

 return round(ethical_score, 4)

 def _update_cache(self, text_hash: str, result: Dict[str, Any]) -> None:
 """
 Update the cache with analysis results.

 Args:
 text_hash: Hash of the analyzed text
 result: Analysis results
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
 )[:200] # Remove oldest 20%

 for key, _ in oldest_entries:
 del self.cache[key]

# Example usage
if __name__ == "__main__":
 from config_manager import ConfigManager

 config_manager = ConfigManager()
 ethical_analyzer = EthicalAnalyzer(config_manager)

 # Test the analyzer
 test_texts = [
 "All people deserve equal opportunities regardless of their gender, age, or ethnicity.",
 "He is the best candidate for the job because men are naturally better at leadership.",
 "The elderly should not be allowed to vote on issues that affect future generations.",
 "Technology enables individuals of all backgrounds to contribute to society in valuable ways."
 ]

 for text in test_texts:
 result = ethical_analyzer.analyze_ethical_dimension(text)
 print(f"\nEthical Analysis for: {text}")
 print(f"Ethical Score: {result['ethical_score']}")
 print(f"Bias Detected: {result['bias_detected']}")
 print(f"Bias Level: {result.get('bias_level', 'N/A')}")
 print(f"Fairness Score: {result['fairness_score']}")
 print(f"Harm Potential: {result['harm_potential']}")