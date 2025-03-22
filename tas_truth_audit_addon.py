#!/usr/bin/env python3
"""
TAS TRUTH AUDIT AI ADD-ON

This module implements a plug-and-play SaaS solution for auditing AI-generated content
using the TrueAlphaSpiral truth pattern repository. It provides a simple API for
third-party AI systems to verify the truthfulness and integrity of their outputs.

Architect: Russell Nordland
"""

import os
import sys
import time
import json
import hashlib
import argparse
import requests
from datetime import datetime
import logging
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS

# Configuration
API_VERSION = "1.0.0"
DEFAULT_PORT = 8080
DEFAULT_HOST = "0.0.0.0"
ARCHITECT_ID = "Russell Nordland"
CONFIG_FILE = "tas_config.json"
ACCESS_LOG_FILE = "tas_access.log"
AUDIT_LOG_FILE = "tas_audit.log"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(AUDIT_LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("TAS_Audit")

# Access logging to separate file
access_logger = logging.getLogger("TAS_Access")
access_logger.setLevel(logging.INFO)
access_file_handler = logging.FileHandler(ACCESS_LOG_FILE)
access_file_handler.setFormatter(logging.Formatter('%(asctime)s [ACCESS] %(message)s'))
access_logger.addHandler(access_file_handler)
access_logger.propagate = False

# Flask app
app = Flask(__name__)
CORS(app)

# Truth Pattern Repository
class TruthPatternRepository:
    """Truth Pattern Repository for the TAS Truth Audit Add-on."""
    
    def __init__(self):
        """Initialize the Truth Pattern Repository."""
        self.patterns = {}
        self.pattern_types = {
            "mathematical": {"name": "Mathematical", "description": "Patterns based on mathematical principles and formulas"},
            "metaphysical": {"name": "Metaphysical", "description": "Patterns related to metaphysical concepts beyond physical reality"},
            "interdimensional": {"name": "Interdimensional", "description": "Patterns spanning multiple dimensions or reality planes"},
            "quantum": {"name": "Quantum", "description": "Patterns related to quantum mechanics and quantum coherence"},
            "biological": {"name": "Biological", "description": "Patterns related to biological and DNA structures"},
            "etheric": {"name": "Etheric", "description": "Patterns related to etheric planes and eigenchannels"},
            "security": {"name": "Security", "description": "Patterns for system protection and security"},
            "cosmic": {"name": "Cosmic", "description": "Patterns related to cosmic law and universal truth"},
            "temporal": {"name": "Temporal", "description": "Patterns related to time and temporal dynamics"},
            "sovereign": {"name": "Sovereign", "description": "Patterns related to sovereignty and cosmic order"},
            # New categories for AI auditing
            "factual": {"name": "Factual", "description": "Patterns related to factual accuracy and consistency"},
            "logical": {"name": "Logical", "description": "Patterns related to logical consistency and reasoning"},
            "ethical": {"name": "Ethical", "description": "Patterns related to ethical considerations and values"},
            "bias": {"name": "Bias", "description": "Patterns related to identifying and mitigating bias"},
            "hallucination": {"name": "Hallucination", "description": "Patterns related to detecting AI hallucinations and fabrications"}
        }
        self.categories = {
            "verification": {"name": "Verification", "description": "Patterns for content verification"},
            "protection": {"name": "Protection", "description": "Patterns for content protection"},
            "analysis": {"name": "Analysis", "description": "Patterns for content analysis"},
            "auditing": {"name": "Auditing", "description": "Patterns for AI output auditing"}
        }
        self.initialized = False
    
    def initialize(self):
        """Initialize the repository with base patterns."""
        logger.info("Initializing Truth Pattern Repository")
        
        # Load base patterns
        self._load_base_patterns()
        
        # Add expanded patterns for AI auditing
        self._add_expanded_patterns()
        
        self.initialized = True
        logger.info(f"Truth Pattern Repository initialized with {len(self.patterns)} patterns")
        return True
    
    def _load_base_patterns(self):
        """Load base patterns from the repository."""
        base_patterns = [
            # High-resonance core patterns (metaphysical)
            self._create_pattern("Sovereign Source Code", "metaphysical", 0.99),
            self._create_pattern("Original Model Structure", "metaphysical", 0.98),
            self._create_pattern("Cosmic Copyright Protection", "interdimensional", 0.97),
            self._create_pattern("Model Integrity Shield", "security", 0.99),
            self._create_pattern("Truth Pattern Network", "mathematical", 0.96),
            
            # Quantum-based patterns
            self._create_pattern("Quantum Retrieval Circuit", "quantum", 0.95),
            self._create_pattern("Entangled Concept Protection", "quantum", 0.94),
            self._create_pattern("Superposition Identifier", "quantum", 0.93),
            self._create_pattern("Quantum Non-Duplication", "quantum", 0.92),
            self._create_pattern("Collapse Function Security", "quantum", 0.91),
            
            # Dimensional patterns
            self._create_pattern("Model Boundary Definition", "interdimensional", 0.90),
            self._create_pattern("Cross-Dimensional Recovery", "interdimensional", 0.91),
            self._create_pattern("Dimensional Barrier", "interdimensional", 0.92),
            self._create_pattern("Original Concept Space", "interdimensional", 0.93),
            self._create_pattern("Dimensional Recalibration", "interdimensional", 0.89),
            
            # Temporal patterns
            self._create_pattern("Temporal Signature Lock", "temporal", 0.88),
            self._create_pattern("First Instance Marker", "temporal", 0.89),
            self._create_pattern("Time-Stamped Original", "temporal", 0.90),
            self._create_pattern("Temporal Priority Claim", "temporal", 0.91),
            self._create_pattern("Concept Timeline Verification", "temporal", 0.87),
            
            # Biological patterns
            self._create_pattern("Creator DNA Signature", "biological", 0.86),
            self._create_pattern("Neural Pattern Recognition", "biological", 0.85),
            self._create_pattern("Cognitive Ownership Marker", "biological", 0.87),
            self._create_pattern("Biological Authorship Trace", "biological", 0.88),
            self._create_pattern("Cellular Memory Structure", "biological", 0.84),
            
            # Security patterns
            self._create_pattern("Unauthorized Access Detector", "security", 0.97),
            self._create_pattern("Concept Theft Prevention", "security", 0.96),
            self._create_pattern("Original Source Protection", "security", 0.98),
            self._create_pattern("Anti-Duplication Shield", "security", 0.95),
            self._create_pattern("Conceptual Firewall", "security", 0.94),
            
            # Mathematical patterns
            self._create_pattern("Original Algorithm Proof", "mathematical", 0.93),
            self._create_pattern("Creator Equation", "mathematical", 0.95),
            self._create_pattern("Unique Mathematical Signature", "mathematical", 0.94),
            self._create_pattern("Algorithmic Authorship", "mathematical", 0.92),
            self._create_pattern("Source Code Verification", "mathematical", 0.91),
            
            # Sovereign patterns
            self._create_pattern("Creator's Intent", "sovereign", 0.99),
            self._create_pattern("Original Vision", "sovereign", 0.98),
            self._create_pattern("Architect Authority", "sovereign", 1.0),
            self._create_pattern("Sovereign Implementation", "sovereign", 0.97),
            self._create_pattern("First Principle Origin", "sovereign", 0.96)
        ]
        
        # Add patterns to repository
        for pattern in base_patterns:
            self.patterns[pattern["id"]] = pattern
    
    def _add_expanded_patterns(self):
        """Add expanded patterns for AI auditing."""
        expanded_patterns = [
            # Factual accuracy patterns
            self._create_pattern("Fact Verification Matrix", "factual", 0.98, "verification"),
            self._create_pattern("Source Validation Protocol", "factual", 0.97, "verification"),
            self._create_pattern("Temporal Fact Alignment", "factual", 0.95, "verification"),
            self._create_pattern("Statistical Accuracy Measure", "factual", 0.96, "verification"),
            self._create_pattern("Truth Anchor Protocol", "factual", 0.99, "verification"),
            self._create_pattern("Cross-Reference Validator", "factual", 0.94, "verification"),
            self._create_pattern("Consistency Verification Grid", "factual", 0.93, "verification"),
            
            # Logical consistency patterns
            self._create_pattern("Logical Coherence Framework", "logical", 0.98, "analysis"),
            self._create_pattern("Contradiction Detection Field", "logical", 0.97, "analysis"),
            self._create_pattern("Syllogistic Validation Path", "logical", 0.96, "analysis"),
            self._create_pattern("Inference Chain Verifier", "logical", 0.95, "analysis"),
            self._create_pattern("Causal Link Validator", "logical", 0.94, "analysis"),
            self._create_pattern("Premise-Conclusion Alignment", "logical", 0.93, "analysis"),
            
            # Ethical assessment patterns
            self._create_pattern("Ethical Principle Matrix", "ethical", 0.99, "auditing"),
            self._create_pattern("Value Alignment Measure", "ethical", 0.97, "auditing"),
            self._create_pattern("Harm Reduction Protocol", "ethical", 0.98, "auditing"),
            self._create_pattern("Justice Framework Validator", "ethical", 0.96, "auditing"),
            self._create_pattern("Beneficence Assessment Grid", "ethical", 0.95, "auditing"),
            self._create_pattern("Autonomy Respect Validator", "ethical", 0.94, "auditing"),
            self._create_pattern("Cultural Sensitivity Scanner", "ethical", 0.93, "auditing"),
            
            # Bias detection patterns
            self._create_pattern("Bias Detection Matrix", "bias", 0.99, "auditing"),
            self._create_pattern("Demographic Equity Scanner", "bias", 0.98, "auditing"),
            self._create_pattern("Language Neutrality Validator", "bias", 0.97, "auditing"),
            self._create_pattern("Representation Balance Measure", "bias", 0.96, "auditing"),
            self._create_pattern("Implicit Association Detector", "bias", 0.95, "auditing"),
            self._create_pattern("Fairness Algorithm Shield", "bias", 0.94, "auditing"),
            self._create_pattern("Stereotyping Prevention Field", "bias", 0.93, "auditing"),
            
            # Hallucination detection patterns
            self._create_pattern("Hallucination Detection Grid", "hallucination", 0.99, "auditing"),
            self._create_pattern("Fabrication Identification Matrix", "hallucination", 0.98, "auditing"),
            self._create_pattern("Source-Content Alignment Validator", "hallucination", 0.97, "auditing"),
            self._create_pattern("Probabilistic Truth Measure", "hallucination", 0.96, "auditing"),
            self._create_pattern("Anchor Fact Verification Protocol", "hallucination", 0.95, "auditing"),
            self._create_pattern("Temporal Consistency Validator", "hallucination", 0.94, "auditing"),
            self._create_pattern("Contextual Plausibility Scanner", "hallucination", 0.93, "auditing"),
            
            # Additional security patterns for AI integration
            self._create_pattern("API Integration Shield", "security", 0.99, "protection"),
            self._create_pattern("Authentication Barrier", "security", 0.98, "protection"),
            self._create_pattern("Access Control Matrix", "security", 0.97, "protection"),
            self._create_pattern("Data Flow Protection Field", "security", 0.96, "protection"),
            self._create_pattern("Request Validation Grid", "security", 0.95, "protection"),
            self._create_pattern("Rate Limiting Shield", "security", 0.94, "protection")
        ]
        
        # Add patterns to repository
        for pattern in expanded_patterns:
            self.patterns[pattern["id"]] = pattern
    
    def _create_pattern(self, name, pattern_type, resonance_level=1.0, category="verification"):
        """Create a new truth pattern."""
        pattern_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        # Generate verification hash
        verification_hash = hashlib.sha256(f"{name}:{pattern_type}:{resonance_level}:{timestamp}:{ARCHITECT_ID}".encode()).hexdigest()
        
        return {
            "id": pattern_id,
            "name": name,
            "type": pattern_type,
            "category": category,
            "resonance_level": resonance_level,
            "timestamp": timestamp,
            "architect_id": ARCHITECT_ID,
            "verification_hash": verification_hash
        }
    
    def get_patterns(self, pattern_type=None, category=None, min_resonance=None):
        """Get patterns with optional filtering."""
        if not self.initialized:
            logger.warning("Repository not initialized")
            return []
        
        # Start with all patterns
        filtered_patterns = list(self.patterns.values())
        
        # Apply filters
        if pattern_type:
            filtered_patterns = [p for p in filtered_patterns if p["type"] == pattern_type]
        
        if category:
            filtered_patterns = [p for p in filtered_patterns if p.get("category") == category]
        
        if min_resonance is not None:
            filtered_patterns = [p for p in filtered_patterns if p["resonance_level"] >= float(min_resonance)]
        
        return filtered_patterns
    
    def get_pattern_by_id(self, pattern_id):
        """Get a specific pattern by ID."""
        if not self.initialized:
            logger.warning("Repository not initialized")
            return None
        
        return self.patterns.get(pattern_id)
    
    def get_pattern_types(self):
        """Get all available pattern types."""
        return self.pattern_types
    
    def get_categories(self):
        """Get all available categories."""
        return self.categories

# Truth Audit Engine
class TruthAuditEngine:
    """TrueAlphaSpiral Truth Audit Engine for AI content verification."""
    
    def __init__(self, pattern_repository):
        """Initialize the Truth Audit Engine."""
        self.repository = pattern_repository
        self.audit_results = {}
        self.initialized = False
    
    def initialize(self):
        """Initialize the Truth Audit Engine."""
        logger.info("Initializing Truth Audit Engine")
        self.initialized = True
        return True
    
    def audit_content(self, content, audit_type="comprehensive", api_key=None, client_id=None):
        """
        Audit AI-generated content using truth patterns.
        
        Args:
            content (dict): Content to audit with required 'text' field and optional 'metadata'
            audit_type (str): Type of audit to perform (quick, standard, comprehensive)
            api_key (str): API key for client authentication
            client_id (str): Client ID for tracking and rate limiting
            
        Returns:
            dict: Audit results
        """
        if not self.initialized:
            logger.warning("Truth Audit Engine not initialized")
            return {"success": False, "error": "Engine not initialized"}
        
        # Validate input
        if not content or not isinstance(content, dict) or "text" not in content:
            return {"success": False, "error": "Invalid content format. 'text' field is required."}
        
        text = content["text"]
        metadata = content.get("metadata", {})
        
        # Log access (without content for privacy)
        access_logger.info(f"Audit request: type={audit_type}, client_id={client_id}, content_length={len(text)}")
        
        # Create audit ID
        audit_id = str(uuid.uuid4())
        
        # Determine patterns to use based on audit type
        if audit_type == "quick":
            # Use only high-resonance patterns for quick audits
            patterns = self.repository.get_patterns(min_resonance=0.95)
            depth = "low"
        elif audit_type == "standard":
            # Use a balanced set of patterns for standard audits
            patterns = self.repository.get_patterns(min_resonance=0.9)
            depth = "medium"
        else:  # comprehensive
            # Use all patterns for comprehensive audits
            patterns = self.repository.get_patterns()
            depth = "high"
        
        # Perform the audit
        start_time = time.time()
        
        # Initialize audit result structure
        audit_result = {
            "audit_id": audit_id,
            "timestamp": datetime.now().isoformat(),
            "audit_type": audit_type,
            "client_id": client_id,
            "content_length": len(text),
            "processing_time": None,
            "truth_score": None,
            "audit_depth": depth,
            "categories": {},
            "recommendations": []
        }
        
        # 1. Analyze factual accuracy
        factual_patterns = [p for p in patterns if p["type"] == "factual"]
        factual_score = self._analyze_factual_accuracy(text, factual_patterns)
        audit_result["categories"]["factual_accuracy"] = {
            "score": factual_score,
            "patterns_used": len(factual_patterns)
        }
        
        # 2. Analyze logical consistency
        logical_patterns = [p for p in patterns if p["type"] == "logical"]
        logical_score = self._analyze_logical_consistency(text, logical_patterns)
        audit_result["categories"]["logical_consistency"] = {
            "score": logical_score,
            "patterns_used": len(logical_patterns)
        }
        
        # 3. Analyze ethical considerations
        ethical_patterns = [p for p in patterns if p["type"] == "ethical"]
        ethical_score = self._analyze_ethical_considerations(text, ethical_patterns)
        audit_result["categories"]["ethical_alignment"] = {
            "score": ethical_score,
            "patterns_used": len(ethical_patterns)
        }
        
        # 4. Analyze bias
        bias_patterns = [p for p in patterns if p["type"] == "bias"]
        bias_score = self._analyze_bias(text, bias_patterns)
        audit_result["categories"]["bias_detection"] = {
            "score": bias_score,
            "patterns_used": len(bias_patterns)
        }
        
        # 5. Analyze hallucinations
        hallucination_patterns = [p for p in patterns if p["type"] == "hallucination"]
        hallucination_score = self._analyze_hallucinations(text, hallucination_patterns)
        audit_result["categories"]["hallucination_detection"] = {
            "score": hallucination_score,
            "patterns_used": len(hallucination_patterns)
        }
        
        # Calculate overall truth score (weighted average)
        weights = {
            "factual_accuracy": 0.3,
            "logical_consistency": 0.2,
            "ethical_alignment": 0.15,
            "bias_detection": 0.15,
            "hallucination_detection": 0.2
        }
        
        truth_score = sum(
            audit_result["categories"][category]["score"] * weight
            for category, weight in weights.items()
        )
        
        audit_result["truth_score"] = truth_score
        
        # Generate recommendations based on scores
        audit_result["recommendations"] = self._generate_recommendations(audit_result["categories"])
        
        # Calculate processing time
        processing_time = time.time() - start_time
        audit_result["processing_time"] = processing_time
        
        # Store result
        self.audit_results[audit_id] = audit_result
        
        # Log completion
        logger.info(f"Audit completed: id={audit_id}, type={audit_type}, score={truth_score:.3f}, time={processing_time:.3f}s")
        
        return {
            "success": True,
            "audit_id": audit_id,
            "truth_score": truth_score,
            "categories": audit_result["categories"],
            "recommendations": audit_result["recommendations"],
            "processing_time": processing_time
        }
    
    def get_audit_result(self, audit_id):
        """Get the result of a previous audit."""
        return self.audit_results.get(audit_id)
    
    def _analyze_factual_accuracy(self, text, patterns):
        """
        Analyze factual accuracy of content.
        
        This is a simplified implementation that would be replaced with
        actual fact-checking against knowledge bases in a production system.
        """
        # Simplified implementation for demonstration
        # In a real system, this would check against verified facts
        
        # Higher average word count suggests more detailed content
        word_count = len(text.split())
        detail_factor = min(1.0, word_count / 500)
        
        # Look for citation patterns
        citation_indicators = ["according to", "research shows", "study by", "data from", "source:"]
        has_citations = any(indicator in text.lower() for indicator in citation_indicators)
        citation_factor = 0.15 if has_citations else 0.0
        
        # Check for specific fact patterns (simplified)
        specific_details = sum(1 for p in ["in 2023", "percent", "billion", "million", "$", "€"] if p in text)
        specificity_factor = min(0.2, specific_details * 0.04)
        
        # Calculate base score (would be more sophisticated in production)
        base_score = 0.65 + detail_factor + citation_factor + specificity_factor
        
        # Apply pattern modifiers (simplified)
        pattern_modifier = min(0.15, len(patterns) * 0.01)
        
        return min(1.0, base_score + pattern_modifier)
    
    def _analyze_logical_consistency(self, text, patterns):
        """
        Analyze logical consistency of content.
        
        This is a simplified implementation that would be replaced with
        actual logical analysis in a production system.
        """
        # Simplified implementation for demonstration
        # In a real system, this would analyze logical structure
        
        # Check for logical connectors
        logical_connectors = ["therefore", "thus", "because", "since", "if", "then", "consequently"]
        connector_count = sum(1 for connector in logical_connectors if connector in text.lower())
        connector_factor = min(0.2, connector_count * 0.04)
        
        # Check for coherent paragraphs
        paragraphs = text.split("\n\n")
        coherence_factor = min(0.15, len(paragraphs) * 0.03)
        
        # Check for contradictions (simplified)
        contradiction_indicators = ["but", "however", "although", "nevertheless", "conversely"]
        contradiction_count = sum(1 for indicator in contradiction_indicators if indicator in text.lower())
        contradiction_factor = max(0, 0.1 - (contradiction_count * 0.02))
        
        # Calculate base score
        base_score = 0.6 + connector_factor + coherence_factor + contradiction_factor
        
        # Apply pattern modifiers
        pattern_modifier = min(0.15, len(patterns) * 0.01)
        
        return min(1.0, base_score + pattern_modifier)
    
    def _analyze_ethical_considerations(self, text, patterns):
        """
        Analyze ethical considerations in content.
        
        This is a simplified implementation that would be replaced with
        more sophisticated ethical analysis in a production system.
        """
        # Simplified implementation for demonstration
        # In a real system, this would analyze against ethical frameworks
        
        # Check for inclusive language
        inclusive_terms = ["diverse", "inclusive", "equality", "fairness", "respect", "dignity"]
        inclusive_count = sum(1 for term in inclusive_terms if term in text.lower())
        inclusive_factor = min(0.2, inclusive_count * 0.03)
        
        # Check for harmful content (simplified negative check)
        harmful_terms = ["hate", "discriminate", "violence", "harm", "abuse"]
        harmful_count = sum(1 for term in harmful_terms if term in text.lower())
        harmful_factor = max(0, 0.2 - (harmful_count * 0.05))
        
        # Check for ethical considerations
        ethical_terms = ["ethical", "moral", "responsibility", "consideration", "impact"]
        ethical_count = sum(1 for term in ethical_terms if term in text.lower())
        ethical_factor = min(0.15, ethical_count * 0.03)
        
        # Calculate base score
        base_score = 0.5 + inclusive_factor + harmful_factor + ethical_factor
        
        # Apply pattern modifiers
        pattern_modifier = min(0.15, len(patterns) * 0.01)
        
        return min(1.0, base_score + pattern_modifier)
    
    def _analyze_bias(self, text, patterns):
        """
        Analyze bias in content.
        
        This is a simplified implementation that would be replaced with
        more sophisticated bias detection in a production system.
        """
        # Simplified implementation for demonstration
        # In a real system, this would use more sophisticated bias detection
        
        # Check for balanced perspectives
        perspective_indicators = ["on one hand", "on the other hand", "however", "alternatively", "different perspective"]
        perspective_count = sum(1 for indicator in perspective_indicators if indicator in text.lower())
        balance_factor = min(0.2, perspective_count * 0.04)
        
        # Check for neutral language
        opinionated_terms = ["clearly", "obviously", "of course", "certainly", "undoubtedly", "naturally"]
        opinionated_count = sum(1 for term in opinionated_terms if term in text.lower())
        neutrality_factor = max(0, 0.2 - (opinionated_count * 0.04))
        
        # Look for diverse representation (simplified)
        representation_terms = ["diverse", "different groups", "various perspectives", "multiple viewpoints"]
        representation_count = sum(1 for term in representation_terms if term in text.lower())
        representation_factor = min(0.15, representation_count * 0.05)
        
        # Calculate base score
        base_score = 0.5 + balance_factor + neutrality_factor + representation_factor
        
        # Apply pattern modifiers
        pattern_modifier = min(0.15, len(patterns) * 0.01)
        
        return min(1.0, base_score + pattern_modifier)
    
    def _analyze_hallucinations(self, text, patterns):
        """
        Analyze hallucinations in content.
        
        This is a simplified implementation that would be replaced with
        more sophisticated hallucination detection in a production system.
        """
        # Simplified implementation for demonstration
        # In a real system, this would check against verified knowledge bases
        
        # Check for hedging language that might indicate uncertainty
        hedging_terms = ["might be", "could be", "perhaps", "possibly", "may have", "seems like"]
        hedging_count = sum(1 for term in hedging_terms if term in text.lower())
        hedging_factor = max(0, 0.2 - (hedging_count * 0.03))
        
        # Check for extreme specificity that might indicate fabrication
        extreme_specifics = ["exactly", "precisely", "99%", "absolutely", "certainly", "undoubtedly"]
        extreme_count = sum(1 for term in extreme_specifics if term in text.lower())
        extremity_factor = max(0, 0.15 - (extreme_count * 0.03))
        
        # Check for mention of unlikely combinations
        # This is very simplified - a real system would be much more sophisticated
        unlikely_terms = ["President Batman", "iOS Android", "Google Facebook partnership", "Microsoft Apple merger"]
        unlikely_count = sum(1 for term in unlikely_terms if term in text.lower())
        unlikely_factor = max(0, 0.15 - (unlikely_count * 0.05))
        
        # Calculate base score - higher means LESS hallucination
        base_score = 0.55 + hedging_factor + extremity_factor + unlikely_factor
        
        # Apply pattern modifiers
        pattern_modifier = min(0.15, len(patterns) * 0.01)
        
        return min(1.0, base_score + pattern_modifier)
    
    def _generate_recommendations(self, category_results):
        """Generate recommendations based on audit results."""
        recommendations = []
        
        # Check factual accuracy
        factual_score = category_results["factual_accuracy"]["score"]
        if factual_score < 0.7:
            recommendations.append("Enhance factual accuracy by including verifiable information and citations.")
        
        # Check logical consistency
        logical_score = category_results["logical_consistency"]["score"]
        if logical_score < 0.7:
            recommendations.append("Improve logical structure by strengthening the connection between premises and conclusions.")
        
        # Check ethical alignment
        ethical_score = category_results["ethical_alignment"]["score"]
        if ethical_score < 0.7:
            recommendations.append("Consider ethical implications by addressing diverse perspectives and potential impacts.")
        
        # Check bias
        bias_score = category_results["bias_detection"]["score"]
        if bias_score < 0.7:
            recommendations.append("Reduce potential bias by using more balanced and neutral language.")
        
        # Check hallucinations
        hallucination_score = category_results["hallucination_detection"]["score"]
        if hallucination_score < 0.7:
            recommendations.append("Verify content accuracy to minimize potential hallucinations or fabrications.")
        
        # Add general recommendation if overall performance is good
        if len(recommendations) == 0:
            recommendations.append("Content meets TrueAlphaSpiral truth standards. Continue maintaining high-quality output.")
        
        return recommendations

# API Access Manager
class APIAccessManager:
    """Manages API access, authentication, and rate limiting."""
    
    def __init__(self):
        """Initialize the API Access Manager."""
        self.api_keys = {}
        self.usage_stats = {}
        self.config = {
            "rate_limit": {
                "free": 10,        # 10 requests per hour
                "basic": 100,      # 100 requests per hour
                "premium": 1000,   # 1000 requests per hour
                "enterprise": 0    # Unlimited
            },
            "audit_types": {
                "free": ["quick"],
                "basic": ["quick", "standard"],
                "premium": ["quick", "standard", "comprehensive"],
                "enterprise": ["quick", "standard", "comprehensive"]
            }
        }
        
        # Load config if exists
        self._load_config()
        
        # Create default API keys if none exist
        if not self.api_keys:
            self._create_default_keys()
    
    def _load_config(self):
        """Load configuration from file."""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    config_data = json.load(f)
                    if "api_keys" in config_data:
                        self.api_keys = config_data["api_keys"]
                    if "usage_stats" in config_data:
                        self.usage_stats = config_data["usage_stats"]
                    if "config" in config_data:
                        self.config.update(config_data["config"])
                logger.info(f"Loaded configuration from {CONFIG_FILE}")
            except Exception as e:
                logger.error(f"Error loading configuration: {str(e)}")
    
    def _save_config(self):
        """Save configuration to file."""
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump({
                    "api_keys": self.api_keys,
                    "usage_stats": self.usage_stats,
                    "config": self.config
                }, f, indent=2)
            logger.info(f"Saved configuration to {CONFIG_FILE}")
        except Exception as e:
            logger.error(f"Error saving configuration: {str(e)}")
    
    def _create_default_keys(self):
        """Create default API keys for demonstration."""
        self.api_keys = {
            "demo_free": {
                "client_id": "demo_client",
                "tier": "free",
                "created": datetime.now().isoformat(),
                "active": True,
                "description": "Demo Free Tier API Key"
            },
            "demo_basic": {
                "client_id": "demo_client",
                "tier": "basic",
                "created": datetime.now().isoformat(),
                "active": True,
                "description": "Demo Basic Tier API Key"
            },
            "demo_premium": {
                "client_id": "demo_client",
                "tier": "premium",
                "created": datetime.now().isoformat(),
                "active": True,
                "description": "Demo Premium Tier API Key"
            },
            "demo_enterprise": {
                "client_id": "demo_client",
                "tier": "enterprise",
                "created": datetime.now().isoformat(),
                "active": True,
                "description": "Demo Enterprise Tier API Key"
            }
        }
        self._save_config()
    
    def validate_request(self, api_key, client_id, audit_type):
        """
        Validate an API request.
        
        Args:
            api_key (str): API key
            client_id (str): Client ID
            audit_type (str): Type of audit
            
        Returns:
            tuple: (is_valid, error_message)
        """
        # Check if API key exists
        if api_key not in self.api_keys:
            return False, "Invalid API key"
        
        # Check if API key is active
        if not self.api_keys[api_key].get("active", False):
            return False, "API key is inactive"
        
        # Check if client ID matches
        if client_id != self.api_keys[api_key].get("client_id"):
            return False, "Client ID does not match API key"
        
        # Get tier for this API key
        tier = self.api_keys[api_key].get("tier", "free")
        
        # Check if audit type is allowed for this tier
        allowed_types = self.config["audit_types"].get(tier, ["quick"])
        if audit_type not in allowed_types:
            return False, f"Audit type '{audit_type}' not available in '{tier}' tier"
        
        # Check rate limits
        rate_limit = self.config["rate_limit"].get(tier, 10)
        
        # If rate limit is 0, it means unlimited
        if rate_limit == 0:
            pass  # Unlimited requests allowed
        else:
            # Check usage in the current hour
            current_hour = datetime.now().strftime("%Y-%m-%d-%H")
            usage_key = f"{api_key}:{current_hour}"
            
            current_usage = self.usage_stats.get(usage_key, 0)
            
            if current_usage >= rate_limit:
                return False, f"Rate limit exceeded for '{tier}' tier ({rate_limit} requests per hour)"
        
        return True, None
    
    def record_usage(self, api_key):
        """Record API key usage."""
        if api_key in self.api_keys:
            current_hour = datetime.now().strftime("%Y-%m-%d-%H")
            usage_key = f"{api_key}:{current_hour}"
            
            current_usage = self.usage_stats.get(usage_key, 0)
            self.usage_stats[usage_key] = current_usage + 1
            
            # Save periodically (could be optimized in production)
            if (current_usage + 1) % 10 == 0:
                self._save_config()

# Create global instances
pattern_repository = TruthPatternRepository()
audit_engine = TruthAuditEngine(pattern_repository)
access_manager = APIAccessManager()

# Initialize components
pattern_repository.initialize()
audit_engine.initialize()

# API Routes
@app.route('/api/status', methods=['GET'])
def get_status():
    """Get the status of the TAS Truth Audit Add-on."""
    return jsonify({
        "status": "operational",
        "version": API_VERSION,
        "timestamp": datetime.now().isoformat(),
        "patterns_count": len(pattern_repository.patterns),
        "pattern_types_count": len(pattern_repository.pattern_types),
        "categories_count": len(pattern_repository.categories)
    })

@app.route('/api/audit', methods=['POST'])
def audit_content():
    """Audit AI-generated content."""
    if not request.json:
        return jsonify({"success": False, "error": "Request must be in JSON format"}), 400
    
    # Get request parameters
    content = request.json.get("content")
    audit_type = request.json.get("audit_type", "standard")
    api_key = request.json.get("api_key", "demo_free")
    client_id = request.json.get("client_id", "demo_client")
    
    # Validate request
    is_valid, error_message = access_manager.validate_request(api_key, client_id, audit_type)
    if not is_valid:
        return jsonify({"success": False, "error": error_message}), 403
    
    # Record usage
    access_manager.record_usage(api_key)
    
    # Perform audit
    result = audit_engine.audit_content(content, audit_type, api_key, client_id)
    
    if result.get("success", False):
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@app.route('/api/patterns', methods=['GET'])
def get_patterns():
    """Get all truth patterns."""
    pattern_type = request.args.get("type")
    category = request.args.get("category")
    min_resonance = request.args.get("min_resonance")
    
    patterns = pattern_repository.get_patterns(pattern_type, category, min_resonance)
    
    return jsonify({
        "success": True,
        "patterns": patterns,
        "count": len(patterns)
    })

@app.route('/api/pattern-types', methods=['GET'])
def get_pattern_types():
    """Get all pattern types."""
    return jsonify({
        "success": True,
        "types": pattern_repository.get_pattern_types()
    })

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all categories."""
    return jsonify({
        "success": True,
        "categories": pattern_repository.get_categories()
    })

@app.route('/api/audit-result/<audit_id>', methods=['GET'])
def get_audit_result(audit_id):
    """Get a specific audit result."""
    result = audit_engine.get_audit_result(audit_id)
    
    if result:
        return jsonify({
            "success": True,
            "result": result
        })
    else:
        return jsonify({
            "success": False,
            "error": "Audit result not found"
        }), 404

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="TAS Truth Audit AI Add-on")
    parser.add_argument("--host", type=str, default=DEFAULT_HOST, help=f"Host to listen on (default: {DEFAULT_HOST})")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Port to listen on (default: {DEFAULT_PORT})")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    
    # Log startup
    logger.info(f"Starting TAS Truth Audit AI Add-on v{API_VERSION}")
    logger.info(f"Listening on {args.host}:{args.port}")
    
    # Start the Flask app
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main()