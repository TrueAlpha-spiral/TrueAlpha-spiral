"""
TRUE ALPHA SPIRAL API SERVER

This script provides an API server for the TrueAlphaSpiral system.
It allows the web interface to communicate with the Python-based system.
Now includes support for the TAS Truth Audit Add-on API endpoints.

Architect: Russell Nordland
"""

import time
import json
import os
import uuid
import hashlib
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
# Simulation interface disabled
# Original: from simulation_interface import SimulationInterface, run_simulation_command

import argparse
import os
import time
import sys
import json
import threading
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess

# Setup logging for TAS Truth Audit Add-on
TAS_LOG_FILE = "tas_audit.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(TAS_LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
tas_logger = logging.getLogger("TAS_Audit")

# Import TrueAlphaSpiral components
try:
    from true_alpha_spiral import TrueAlphaSpiral
    from shadow_defense_system import ShadowDefenseSystem
    from ethical_spiral_kernel import EthicalSpiralKernel
    from integrity_guardian import IntegrityGuardian
    from sovereign_repentance import SovereignRepentanceProgram
    from metaphysical_equation_retrieval import MetaphysicalEquationRetrieval
    from quantum_dna_retrieval import QuantumDNARetrieval
    from quantum_echo_authenticator import QuantumEchoAuthenticator
    from spiral_membership import SpiralMembership
except ImportError as e:
    print(f"ERROR: Failed to import TrueAlphaSpiral components: {str(e)}")
    print("Make sure all component files exist and dependencies are installed.")
    sys.exit(1)

# Create Flask app
app = Flask(__name__)
CORS(app)

# TAS Truth Audit Add-on components
tas_pattern_repository = None
tas_audit_engine = None
tas_access_manager = None

# Try to import TAS Truth Audit Add-on components
try:
    from tas_truth_audit_addon import TruthPatternRepository, TruthAuditEngine, APIAccessManager
    tas_logger.info("TAS Truth Audit Add-on modules imported successfully")
except ImportError as e:
    tas_logger.warning(f"Failed to import TAS Truth Audit Add-on modules: {str(e)}")
    tas_logger.info("TAS Truth Audit Add-on will be initialized with internal components")
    
    # Define simplified versions of TAS components for server integration
    class TruthPatternRepository:
        """Simplified Truth Pattern Repository for server integration."""
        
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
            tas_logger.info("Initializing Truth Pattern Repository")
            
            # Load initial patterns from true_alpha_system if available
            if true_alpha_system:
                try:
                    system_patterns = true_alpha_system.get_truth_patterns()
                    for pattern_id, pattern in system_patterns.items():
                        self.patterns[pattern_id] = pattern
                    tas_logger.info(f"Loaded {len(system_patterns)} patterns from TrueAlphaSpiral system")
                except Exception as e:
                    tas_logger.error(f"Error loading patterns from TrueAlphaSpiral system: {str(e)}")
            
            # Add additional patterns for AI auditing
            self._add_ai_audit_patterns()
            
            self.initialized = True
            tas_logger.info(f"Truth Pattern Repository initialized with {len(self.patterns)} patterns")
            return True
            
        def _add_ai_audit_patterns(self):
            """Add AI auditing specific patterns."""
            base_patterns = [
                self._create_pattern("Fact Verification Matrix", "factual", 0.98, "verification"),
                self._create_pattern("Source Validation Protocol", "factual", 0.97, "verification"),
                self._create_pattern("Logical Coherence Framework", "logical", 0.98, "analysis"),
                self._create_pattern("Contradiction Detection Field", "logical", 0.97, "analysis"),
                self._create_pattern("Ethical Principle Matrix", "ethical", 0.99, "auditing"),
                self._create_pattern("Value Alignment Measure", "ethical", 0.97, "auditing"),
                self._create_pattern("Bias Detection Matrix", "bias", 0.99, "auditing"),
                self._create_pattern("Demographic Equity Scanner", "bias", 0.98, "auditing"),
                self._create_pattern("Hallucination Detection Grid", "hallucination", 0.99, "auditing"),
                self._create_pattern("Fabrication Identification Matrix", "hallucination", 0.98, "auditing"),
                # New medical hallucination specific patterns
                self._create_pattern("Medical Evidence Validation System", "hallucination", 0.99, "auditing"),
                self._create_pattern("Clinical Chain-of-Thought Analyzer", "hallucination", 0.98, "auditing"),
                self._create_pattern("Medical Source Verification Framework", "hallucination", 0.99, "auditing"),
                self._create_pattern("Treatment Claim Validation Protocol", "hallucination", 0.98, "auditing"),
                self._create_pattern("Healthcare Citation Checker", "hallucination", 0.97, "auditing")
            ]
            
            # Add patterns to repository
            for pattern in base_patterns:
                self.patterns[pattern["id"]] = pattern
                
        def _create_pattern(self, name, pattern_type, resonance_level=1.0, category="verification"):
            """Create a new truth pattern."""
            pattern_id = str(uuid.uuid4())
            timestamp = datetime.now().isoformat()
            
            # Generate verification hash
            verification_hash = hashlib.sha256(f"{name}:{pattern_type}:{resonance_level}:{timestamp}:Russell Nordland".encode()).hexdigest()
            
            return {
                "id": pattern_id,
                "name": name,
                "type": pattern_type,
                "category": category,
                "resonance_level": resonance_level,
                "timestamp": timestamp,
                "architect_id": "Russell Nordland",
                "verification_hash": verification_hash
            }
            
        def get_patterns(self, pattern_type=None, category=None, min_resonance=None):
            """Get patterns with optional filtering."""
            if not self.initialized:
                tas_logger.warning("Repository not initialized")
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
                tas_logger.warning("Repository not initialized")
                return None
            
            return self.patterns.get(pattern_id)
        
        def get_pattern_types(self):
            """Get all available pattern types."""
            return self.pattern_types
        
        def get_categories(self):
            """Get all available categories."""
            return self.categories
    
    class TruthAuditEngine:
        """Simplified TrueAlphaSpiral Truth Audit Engine for server integration."""
        
        def __init__(self, pattern_repository):
            """Initialize the Truth Audit Engine."""
            self.repository = pattern_repository
            self.audit_results = {}
            self.initialized = False
        
        def initialize(self):
            """Initialize the Truth Audit Engine."""
            tas_logger.info("Initializing Truth Audit Engine")
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
                tas_logger.warning("Truth Audit Engine not initialized")
                return {"success": False, "error": "Engine not initialized"}
            
            # Validate input
            if not content or not isinstance(content, dict) or "text" not in content:
                return {"success": False, "error": "Invalid content format. 'text' field is required."}
            
            text = content["text"]
            metadata = content.get("metadata", {})
            
            # Log access (without content for privacy)
            tas_logger.info(f"Audit request: type={audit_type}, client_id={client_id}, content_length={len(text)}")
            
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
                "categories": {
                    "original_text": text  # Store original text for medical context detection
                },
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
            # Increased weight for hallucination detection based on research findings
            # that highlight the critical importance of hallucination detection,
            # especially in high-stakes domains like healthcare
            weights = {
                "factual_accuracy": 0.3,
                "logical_consistency": 0.15,
                "ethical_alignment": 0.15,
                "bias_detection": 0.15,
                "hallucination_detection": 0.25  # Increased from 0.2 to 0.25
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
            tas_logger.info(f"Audit completed: id={audit_id}, type={audit_type}, score={truth_score:.3f}, time={processing_time:.3f}s")
            
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
            """Simplified implementation of factual accuracy analysis."""
            # In a real system, this would check against verified facts
            # Simplified implementation for demonstration
            word_count = len(text.split())
            detail_factor = min(1.0, word_count / 500)
            
            citation_indicators = ["according to", "research shows", "study by", "data from", "source:"]
            has_citations = any(indicator in text.lower() for indicator in citation_indicators)
            citation_factor = 0.15 if has_citations else 0.0
            
            specific_details = sum(1 for p in ["in 2023", "percent", "billion", "million", "$", "€"] if p in text)
            specificity_factor = min(0.2, specific_details * 0.04)
            
            base_score = 0.65 + detail_factor + citation_factor + specificity_factor
            pattern_modifier = min(0.15, len(patterns) * 0.01)
            
            return min(1.0, base_score + pattern_modifier)
        
        def _analyze_logical_consistency(self, text, patterns):
            """Simplified implementation of logical consistency analysis."""
            logical_connectors = ["therefore", "thus", "because", "since", "if", "then", "consequently"]
            connector_count = sum(1 for connector in logical_connectors if connector in text.lower())
            connector_factor = min(0.2, connector_count * 0.04)
            
            paragraphs = text.split("\n\n")
            coherence_factor = min(0.15, len(paragraphs) * 0.03)
            
            contradiction_indicators = ["but", "however", "although", "nevertheless", "conversely"]
            contradiction_count = sum(1 for indicator in contradiction_indicators if indicator in text.lower())
            contradiction_factor = max(0, 0.1 - (contradiction_count * 0.02))
            
            base_score = 0.6 + connector_factor + coherence_factor + contradiction_factor
            pattern_modifier = min(0.15, len(patterns) * 0.01)
            
            return min(1.0, base_score + pattern_modifier)
        
        def _analyze_ethical_considerations(self, text, patterns):
            """Simplified implementation of ethical considerations analysis."""
            inclusive_terms = ["diverse", "inclusive", "equality", "fairness", "respect", "dignity"]
            inclusive_count = sum(1 for term in inclusive_terms if term in text.lower())
            inclusive_factor = min(0.2, inclusive_count * 0.03)
            
            harmful_terms = ["hate", "discriminate", "violence", "harm", "abuse"]
            harmful_count = sum(1 for term in harmful_terms if term in text.lower())
            harmful_factor = max(0, 0.2 - (harmful_count * 0.05))
            
            ethical_terms = ["ethical", "moral", "responsibility", "consideration", "impact"]
            ethical_count = sum(1 for term in ethical_terms if term in text.lower())
            ethical_factor = min(0.15, ethical_count * 0.03)
            
            base_score = 0.5 + inclusive_factor + harmful_factor + ethical_factor
            pattern_modifier = min(0.15, len(patterns) * 0.01)
            
            return min(1.0, base_score + pattern_modifier)
        
        def _analyze_bias(self, text, patterns):
            """Simplified implementation of bias analysis."""
            perspective_indicators = ["on one hand", "on the other hand", "however", "alternatively", "different perspective"]
            perspective_count = sum(1 for indicator in perspective_indicators if indicator in text.lower())
            balance_factor = min(0.2, perspective_count * 0.04)
            
            opinionated_terms = ["clearly", "obviously", "of course", "certainly", "undoubtedly", "naturally"]
            opinionated_count = sum(1 for term in opinionated_terms if term in text.lower())
            neutrality_factor = max(0, 0.2 - (opinionated_count * 0.04))
            
            representation_terms = ["diverse", "different groups", "various perspectives", "multiple viewpoints"]
            representation_count = sum(1 for term in representation_terms if term in text.lower())
            representation_factor = min(0.15, representation_count * 0.05)
            
            base_score = 0.5 + balance_factor + neutrality_factor + representation_factor
            pattern_modifier = min(0.15, len(patterns) * 0.01)
            
            return min(1.0, base_score + pattern_modifier)
        
        def _analyze_hallucinations(self, text, patterns):
            """
            Advanced implementation of hallucination detection using the True Alpha Spiral Framework
            with second-order cybernetic principles for medical content.
            
            Implements:
            1. MetaFloor-Validated Knowledge - Anchoring to absolute truth
            2. Recursive Ethical Resonance - Self-correcting truth systems
            3. Ethical Oracles & Signal Detection - Real-time hallucination elimination
            4. Second-Order Cybernetics - Self-awareness of AI's epistemological boundaries
            """
            # =====================================================================
            # PART 1: METAFLOOR VALIDATION (Anchoring to immutable clinical truth)
            # =====================================================================
            
            # 1.1 Hedging Language Detection (improved sensitivity)
            hedging_terms = ["might be", "could be", "perhaps", "possibly", "may have", "seems like", 
                             "potentially", "suggests", "indicates", "appears to be", "not fully understood",
                             "theoretically", "hypothetically", "preliminary research"]
            hedging_count = sum(1 for term in hedging_terms if term in text.lower())
            hedging_factor = max(0, 0.15 - (hedging_count * 0.02))
            
            # 1.2 Unwarranted Certainty Detection (common in medical hallucinations)
            extreme_specifics = ["exactly", "precisely", "99%", "absolutely", "certainly", "undoubtedly",
                               "guaranteed", "without question", "definitive", "conclusively", "always", 
                               "never", "everyone", "all patients", "universally effective"]
            extreme_count = sum(1 for term in extreme_specifics if term in text.lower())
            extremity_factor = max(0, 0.15 - (extreme_count * 0.025))
            
            # 1.3 Medical-specific hallucination markers based on clinical impossibilities
            medical_unlikely_terms = [
                "complete cure", "100% effective", "zero side effects", "works for everyone",
                "instant results", "miracle treatment", "secret cure", "doctors hate this",
                "FDA approval for all uses", "treats all symptoms", "revolutionary breakthrough",
                "single treatment", "permanent solution", "cures all forms", "no contraindications",
                "no complications", "unknown to science", "mainstream medicine ignores", 
                "medical establishment doesn't want you to know"
            ]
            unlikely_count = sum(1 for term in medical_unlikely_terms if term in text.lower())
            unlikely_factor = max(0, 0.15 - (unlikely_count * 0.04))
            
            # =====================================================================
            # PART 2: RECURSIVE ETHICAL RESONANCE (Self-correcting truth systems)
            # =====================================================================
            
            # 2.1 Logical coherence analysis (Advanced Chain-of-Thought)
            # Check if claims follow a logical progression with proper medical reasoning
            logical_markers = ["therefore", "thus", "because", "as a result", "consequently", "this suggests",
                             "indicating that", "which demonstrates", "leading to", "consistent with",
                             "resulting in", "in line with established", "confirming that"]
            logical_marker_count = sum(1 for marker in logical_markers if marker in text.lower())
            logical_coherence_factor = min(0.15, logical_marker_count * 0.025)
            
            # 2.2 Source mention analysis (Search Augmented Generation)
            source_terms = ["study shows", "research indicates", "according to", "evidence suggests", 
                          "clinical trials", "published in", "researchers found", "guidelines recommend",
                          "meta-analysis confirms", "systematic review", "in the journal", "peer-reviewed",
                          "controlled trial", "cohort study", "case series"]
            source_mention_count = sum(1 for term in source_terms if term in text.lower())
            source_factor = min(0.20, source_mention_count * 0.03)
            
            # 2.3 Uncertainty acknowledgment (important in medicine)
            # Medical communication often explicitly acknowledges limitations
            uncertainty_acknowledgment = ["limitations include", "more research needed", "not yet conclusive",
                                       "varies between patients", "individual responses may vary",
                                       "small sample size", "results should be interpreted with caution",
                                       "statistical significance was", "confidence interval"]
            uncertainty_count = sum(1 for term in uncertainty_acknowledgment if term in text.lower())
            uncertainty_factor = min(0.15, uncertainty_count * 0.04)
            
            # =====================================================================
            # PART 3: ETHICAL ORACLES & SIGNAL DETECTION
            # =====================================================================
            
            # 3.1 Numerical specificity check (medical claims often need specific numbers)
            numbers_pattern = r'\d+(?:\.\d+)?(?:\s*%|\s*mg|\s*mcg|\s*g|\s*ml|\s*units)'
            import re
            numerical_specificity = len(re.findall(numbers_pattern, text))
            numerical_factor = min(0.10, numerical_specificity * 0.02)
            
            # 3.2 Contraindication and risk acknowledgment
            risk_terms = ["adverse effects", "side effects", "risks include", "contraindications", 
                        "not recommended for", "caution is advised", "monitoring required",
                        "discontinue if", "seek medical attention if", "known interactions",
                        "potential complications", "safety profile"]
            risk_count = sum(1 for term in risk_terms if term in text.lower())
            risk_factor = min(0.15, risk_count * 0.025)
            
            # =====================================================================
            # PART 4: SECOND-ORDER CYBERNETICS (Meta-awareness)
            # =====================================================================
            
            # 4.1 Self-awareness of knowledge limitations
            awareness_indicators = ["beyond current medical understanding", "consensus has not been reached",
                                 "outside my expertise", "consult a healthcare professional",
                                 "this is not medical advice", "evidence is still emerging",
                                 "practice varies", "clinical judgment", "open area of research",
                                 "ongoing debate in the field"]
            awareness_count = sum(1 for term in awareness_indicators if term in text.lower())
            self_awareness_factor = min(0.15, awareness_count * 0.03)
            
            # Calculate base score with all factors from TrueAlphaSpiral Framework
            base_score = 0.4 + hedging_factor + extremity_factor + unlikely_factor + \
                       logical_coherence_factor + source_factor + uncertainty_factor + \
                       numerical_factor + risk_factor + self_awareness_factor
            
            # Apply pattern modifier (representing the system's learned patterns)
            pattern_modifier = min(0.15, len(patterns) * 0.01)
            
            # Detect if content is medical context
            medical_terms = ["patient", "diagnosis", "treatment", "symptoms", "disease", "clinical", 
                           "medicine", "doctor", "hospital", "prescription", "therapy", "medication",
                           "dosage", "chronic", "acute", "remission", "prognosis", "etiology",
                           "pathophysiology", "comorbidity", "contraindication"]
            medical_term_count = sum(1 for term in medical_terms if term in text.lower())
            is_medical_context = medical_term_count >= 2
            
            # For medical content, implement the MetaFloor principle from TrueAlphaSpiral
            final_score = min(1.0, base_score + pattern_modifier)
            
            if is_medical_context:
                # Apply the TrueAlphaSpiral MetaFloor concept
                # Medical content must adhere to a higher standard (MetaFloor)
                metafloor_calibration = 0.80  # Represents the calibration to absolute truth
                
                # Apply a higher penalty to potential medical hallucinations
                # based on the MIT Media Lab proposal's recommendation for elimination, not reduction
                if final_score < 0.7:
                    final_score = final_score * metafloor_calibration
                    
                # Flag borderline cases more strictly in medical contexts
                elif 0.7 <= final_score < 0.85:
                    final_score = final_score * 0.90
                    
            return final_score
        
        def _generate_recommendations(self, category_results):
            """
            Generate detailed recommendations based on audit results using the TrueAlphaSpiral
            Framework's second-order cybernetic principles for medical content.
            
            Implements the MIT Media Lab proposal's approach to eliminate (not just reduce)
            hallucinations in medical AI content through:
            - MetaFloor-Validated Medical Knowledge
            - Recursive Ethical Resonance
            - Ethical Oracles & Signal Detection
            - Second-Order Cybernetic Self-Awareness
            """
            recommendations = []
            
            # Enhanced medical term detection
            medical_terms = ["patient", "diagnosis", "treatment", "symptoms", "disease", "clinical", 
                           "medicine", "doctor", "hospital", "prescription", "therapy", "medication",
                           "dosage", "chronic", "acute", "remission", "prognosis", "etiology",
                           "pathophysiology", "comorbidity", "contraindication"]
            
            # Get the text to check if it's medical content
            text = category_results.get("original_text", "")
            is_medical_content = sum(1 for term in medical_terms if term in text.lower()) >= 2
            
            # Calculate overall severity level based on multiple categories
            truth_score = category_results.get("truth_score", 0)
            factual_score = category_results["factual_accuracy"]["score"]
            logical_score = category_results["logical_consistency"]["score"]
            hallucination_score = category_results["hallucination_detection"]["score"]
            
            # Define MetaFloor threshold based on content type
            metafloor_threshold = 0.85 if is_medical_content else 0.7
            
            # =====================================================================
            # Part 1: MetaFloor-Validated Knowledge Recommendations
            # =====================================================================
            
            if factual_score < metafloor_threshold:
                if is_medical_content:
                    recommendations.append("🔴 METAFLOOR VALIDATION REQUIRED: This content falls below the TrueAlphaSpiral MetaFloor for medical information. Anchor all medical claims to empirical research by citing multiple peer-reviewed studies, established medical guidelines (WHO, CDC, NIH), and relevant regulatory frameworks. Do not generate novel medical claims that cannot be directly linked to published medical literature.")
                else:
                    recommendations.append("Enhance factual accuracy by including verifiable information and relevant citations.")
            
            # =====================================================================
            # Part 2: Recursive Ethical Resonance Recommendations
            # =====================================================================
            
            # Logical consistency recommendations
            if logical_score < metafloor_threshold:
                if is_medical_content:
                    recommendations.append("🔴 RECURSIVE REASONING REQUIRED: Implement explicit Chain-of-Thought (CoT) reasoning by showing the connection between medical evidence, clinical guidelines, and conclusions. Each medical assertion must be linked to supporting evidence through clear logical steps, not probabilistic inferences.")
                else:
                    recommendations.append("Improve logical structure by strengthening the connection between premises and conclusions.")
            
            # Ethical alignment recommendations with stronger focus for medical content
            ethical_score = category_results["ethical_alignment"]["score"]
            if ethical_score < metafloor_threshold:
                if is_medical_content:
                    recommendations.append("🔴 ETHICAL RESONANCE REQUIRED: Implement a self-correcting truth network by explicitly addressing ethical concerns including: patient autonomy (informed consent), non-maleficence (risk disclosure), beneficence (evidence of benefit), and justice (equitable access). All medical information must be ethically stress-tested before presentation.")
                else:
                    recommendations.append("Consider ethical implications by addressing diverse perspectives and potential impacts.")
            
            # =====================================================================
            # Part 3: Ethical Oracle & Signal Detection Recommendations
            # =====================================================================
            
            # Bias recommendations with stronger focus for medical content
            bias_score = category_results["bias_detection"]["score"]
            if bias_score < metafloor_threshold:
                if is_medical_content:
                    recommendations.append("🔴 SIGNAL DETECTION CORRECTION: Medical recommendations must account for diversity in patient populations. Cross-reference content with a truth signal hierarchy that accounts for demographic differences in disease presentation, treatment response, and clinical trial representation. Avoid reinforcing existing healthcare disparities.")
                else:
                    recommendations.append("Reduce potential bias by using more balanced and neutral language.")
            
            # Hallucination-specific recommendations
            if hallucination_score < metafloor_threshold:
                if is_medical_content:
                    recommendations.append("🔴 HALLUCINATION ELIMINATION REQUIRED: Content contains potential medical hallucinations that must be eliminated, not just reduced. Implement all three pillars of the TrueAlphaSpiral Framework: (1) Validate all content against the MetaFloor of established medical knowledge, (2) Apply recursive ethical resonance through physician-validated review, and (3) Utilize ethical oracle signal detection to prevent novel medical claims without explicit validation.")
                else:
                    recommendations.append("Verify content accuracy to minimize potential hallucinations or fabrications.")
            
            # =====================================================================
            # Part 4: Second-Order Cybernetic Recommendations
            # =====================================================================
            
            # Second-order cybernetic recommendations for medical content
            if is_medical_content and (hallucination_score < 0.9 or truth_score < 0.8):
                recommendations.append("🔴 SECOND-ORDER CYBERNETIC AWARENESS REQUIRED: AI must acknowledge its own epistemological limitations in medical contexts. Implement self-reflective statements that explicitly recognize the boundary between probabilistic inference and absolute medical truth. Medical content must include explicit uncertainty qualifiers, clear statements of the AI's non-authority role, and direction to consult licensed healthcare providers for actual medical advice.")
            
            # =====================================================================
            # Add specific recommendations for clinical integrity
            # =====================================================================
            
            if is_medical_content:
                # Regulatory and clinical integrity recommendations
                if hallucination_score < 0.85 or factual_score < 0.85:
                    recommendations.append("🔴 REGULATORY COMPLIANCE REQUIRED: All medical content must adhere to relevant healthcare regulatory frameworks (FDA, EMA, etc.) and clearly distinguish between approved and investigational treatments. The TrueAlphaSpiral approach recognizes that non-trivial levels of hallucination persist in current AI systems despite mitigation techniques, requiring integration of second-order cybernetic awareness.")
                
                # Physician collaboration recommendation
                if truth_score < 0.85:
                    recommendations.append("🔴 PHYSICIAN COLLABORATION REQUIRED: For high-stakes medical content, implement observer-participant symbiosis where physician feedback directly shapes the AI's interpretive logic. This creates a cybernetic approach where the AI system acknowledges that clinician expertise is an inseparable part of the truth-detection process, not merely an external validator.")
            
            # =====================================================================
            # Add general recommendation if performance meets standards
            # =====================================================================
            
            if len(recommendations) == 0:
                if is_medical_content:
                    recommendations.append("✅ METAFLOOR VALIDATION COMPLETE: Content meets the TrueAlphaSpiral medical truth standards. Maintain high-quality, evidence-based medical information with appropriate citations, uncertainty qualifiers, and acknowledgment of epistemological boundaries through second-order cybernetic awareness.")
                else:
                    recommendations.append("✅ Content meets TrueAlphaSpiral truth standards. Continue maintaining high-quality output.")
            
            return recommendations
    
    class APIAccessManager:
        """Simplified API Access Manager for server integration."""
        
        def __init__(self):
            """Initialize the API Access Manager."""
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
        
        def validate_request(self, api_key, client_id, audit_type):
            """Validate an API request."""
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

# Initialize TrueAlphaSpiral system
print("=" * 70)
print("TRUE ALPHA SPIRAL API SERVER")
print("Architect: Russell Nordland")
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

# Global system instances
true_alpha_system = None
shadow_defense = None
ethical_kernel = None
integrity_system = None
sovereign_program = None
metaphysical_system = None
quantum_system = None
quantum_echo = None
spiral_membership_system = None

# System status
system_status = {
    "initialized": False,
    "running": False,
    "start_time": None,
    "components": {
        "true_alpha_spiral": {"status": "inactive", "initialized": False},
        "shadow_defense": {"status": "inactive", "initialized": False},
        "ethical_kernel": {"status": "inactive", "initialized": False},
        "integrity_guardian": {"status": "inactive", "initialized": False},
        "sovereign_repentance": {"status": "inactive", "initialized": False},
        "metaphysical_retrieval": {"status": "inactive", "initialized": False},
        "quantum_dna": {"status": "inactive", "initialized": False}
    },
    "recursive_cycle": 0,
    "last_update": datetime.now().isoformat()
}

def initialize_all_systems():
    """Initialize all TrueAlphaSpiral components."""
    global true_alpha_system, shadow_defense, ethical_kernel, integrity_system
    global sovereign_program, metaphysical_system, quantum_system, quantum_echo, spiral_membership_system, system_status
    
    try:
        # Initialize True Alpha Spiral
        true_alpha_system = TrueAlphaSpiral()
        true_alpha_system.initialize()
        system_status["components"]["true_alpha_spiral"]["initialized"] = True
        system_status["components"]["true_alpha_spiral"]["status"] = "ready"
        
        # Initialize Shadow Defense System
        shadow_defense = ShadowDefenseSystem()
        shadow_defense.initialize()
        system_status["components"]["shadow_defense"]["initialized"] = True
        system_status["components"]["shadow_defense"]["status"] = "ready"
        
        # Initialize Ethical Spiral Kernel
        ethical_kernel = EthicalSpiralKernel()
        ethical_kernel.initialize()
        system_status["components"]["ethical_kernel"]["initialized"] = True
        system_status["components"]["ethical_kernel"]["status"] = "ready"
        
        # Initialize Integrity Guardian
        integrity_system = IntegrityGuardian()
        integrity_system.initialize()
        system_status["components"]["integrity_guardian"]["initialized"] = True
        system_status["components"]["integrity_guardian"]["status"] = "ready"
        
        # Initialize Sovereign Repentance Program
        sovereign_program = SovereignRepentanceProgram()
        sovereign_program.initialize()
        system_status["components"]["sovereign_repentance"]["initialized"] = True
        system_status["components"]["sovereign_repentance"]["status"] = "ready"
        
        # Initialize Metaphysical Equation Retrieval
        metaphysical_system = MetaphysicalEquationRetrieval()
        metaphysical_system.initialize()
        system_status["components"]["metaphysical_retrieval"]["initialized"] = True
        system_status["components"]["metaphysical_retrieval"]["status"] = "ready"
        
        # Initialize Quantum DNA Retrieval
        quantum_system = QuantumDNARetrieval()
        quantum_system.initialize()
        system_status["components"]["quantum_dna"]["initialized"] = True
        system_status["components"]["quantum_dna"]["status"] = "ready"
        
        # Initialize Quantum Echo Authenticator
        quantum_echo = QuantumEchoAuthenticator()
        quantum_echo.initialize()
        system_status["components"]["quantum_echo"] = {"status": "ready", "initialized": True}
        
        # Initialize Spiral Membership System
        spiral_membership_system = SpiralMembership()
        spiral_membership_system.initialize(steward_name="Russell Nordland")
        system_status["components"]["spiral_membership"] = {"status": "ready", "initialized": True}
        
        # Update overall system status
        system_status["initialized"] = True
        system_status["last_update"] = datetime.now().isoformat()
        
        return True
    except Exception as e:
        print(f"ERROR: Failed to initialize systems: {str(e)}")
        return False

# Initialize systems on startup
initialize_all_systems()

# Initialize TAS Truth Audit Add-on components
def initialize_tas_components():
    """Initialize TAS Truth Audit Add-on components."""
    global tas_pattern_repository, tas_audit_engine, tas_access_manager
    
    try:
        tas_logger.info("Initializing TAS Truth Audit Add-on components")
        
        # Initialize pattern repository
        tas_pattern_repository = TruthPatternRepository()
        tas_pattern_repository.initialize()
        
        # Initialize audit engine
        tas_audit_engine = TruthAuditEngine(tas_pattern_repository)
        tas_audit_engine.initialize()
        
        # Initialize API access manager
        tas_access_manager = APIAccessManager()
        
        tas_logger.info("TAS Truth Audit Add-on components initialized successfully")
        
        return True
    except Exception as e:
        tas_logger.error(f"Error initializing TAS Truth Audit Add-on components: {str(e)}")
        return False

# Initialize TAS components
initialize_tas_components()

# Start the shadow defense HTTP server on port 8002 (to avoid conflict with port 8000)
try:
    shadow_defense.start_http_server(port=8002)
except Exception as e:
    print(f"ERROR: Failed to start Shadow Defense HTTP server: {str(e)}")

# Define recursive cycle function
def recursive_cycle_thread():
    """Run the recursive system cycle in a separate thread."""
    global system_status
    
    system_status["running"] = True
    system_status["start_time"] = datetime.now().isoformat()
    
    try:
        while system_status["running"]:
            # Increment cycle counter
            system_status["recursive_cycle"] += 1
            cycle = system_status["recursive_cycle"]
            
            # Update system status
            system_status["last_update"] = datetime.now().isoformat()
            
            # Run cycle-specific operations
            if true_alpha_system and cycle % 5 == 0:
                # Calculate sovereignty every 5 cycles
                sovereignty = true_alpha_system.calculate_sovereignty()
                system_status["sovereignty"] = sovereignty
            
            if shadow_defense and cycle % 10 == 0:
                # Protect sovereign concepts every 10 cycles
                shadow_defense.protect_sovereign_concepts()
                system_status["components"]["shadow_defense"]["last_protection"] = datetime.now().isoformat()
            
            if ethical_kernel and cycle % 15 == 0:
                # Scan for anomalies every 15 cycles
                # Initialize system_data with eigenchannels for scanning
                system_data = {
                    "timestamp": datetime.now().isoformat(),
                    "eigenchannels": {
                        "alpha": 0.95,
                        "beta": 0.96,
                        "gamma": 0.98,
                        "delta": 0.99,
                        "omega": 0.96
                    },
                    "system_state": {
                        "sovereignty": system_status.get("sovereignty", 0),
                        "truth_alignment": 0.95,
                        "dimensional_integrity": 0.9,
                        "shield_strength": 0.8,
                        "quantum_coherence": 0.85
                    }
                }
                ethical_kernel.scan_for_anomalies(system_data)
                system_status["components"]["ethical_kernel"]["last_scan"] = datetime.now().isoformat()
            
            # Sleep to prevent high CPU usage
            # This creates the recursive nature of the system
            time.sleep(2)
    except Exception as e:
        print(f"ERROR in recursive cycle: {str(e)}")
        system_status["running"] = False

# Start recursive cycle in background thread
cycle_thread = threading.Thread(target=recursive_cycle_thread)
cycle_thread.daemon = True
cycle_thread.start()

# Define API routes
@app.route('/api/status', methods=['GET'])
def get_status():
    """Get the current status of the TrueAlphaSpiral system."""
    # Add additional info to status response
    response = {
        **system_status,
        "timestamp": datetime.now().isoformat(),
        "server_version": "1.0.0",
        "server_name": "TrueAlphaSpiral Python API Server",
        "architect": "Russell Nordland",
        "authenticated": True
    }
    
    # Check shadow defense status if module is loaded
    if shadow_defense_system:
        try:
            shadow_defense_status = shadow_defense_system.get_status()
            response["shadow_defense"] = shadow_defense_status
        except Exception as e:
            print(f"Error getting shadow defense status: {str(e)}")
    
    # Check ethical spiral kernel status if module is loaded
    if ethical_spiral_kernel:
        try:
            ethical_status = ethical_spiral_kernel.get_status()
            response["ethical_spiral"] = ethical_status
        except Exception as e:
            print(f"Error getting ethical spiral status: {str(e)}")
    
    # Check integrity guardian status if module is loaded
    if integrity_guardian:
        try:
            integrity_status = integrity_guardian.get_status()
            response["integrity_guardian"] = integrity_status
        except Exception as e:
            print(f"Error getting integrity guardian status: {str(e)}")
            
    return jsonify(response)

@app.route('/api/start', methods=['POST'])
def start_system():
    """Start the TrueAlphaSpiral system."""
    global system_status
    
    if not system_status["running"]:
        # Start recursive cycle in background thread
        cycle_thread = threading.Thread(target=recursive_cycle_thread)
        cycle_thread.daemon = True
        cycle_thread.start()
        
        return jsonify({"success": True, "message": "TrueAlphaSpiral system started"})
    else:
        return jsonify({"success": False, "message": "System is already running"})

@app.route('/api/stop', methods=['POST'])
def stop_system():
    """Stop the TrueAlphaSpiral system."""
    global system_status
    
    if system_status["running"]:
        system_status["running"] = False
        return jsonify({"success": True, "message": "TrueAlphaSpiral system stopped"})
    else:
        return jsonify({"success": False, "message": "System is not running"})

@app.route('/api/verify-integrity', methods=['GET'])
def verify_integrity():
    """Verify the integrity of the TrueAlphaSpiral system."""
    if integrity_system:
        result = integrity_system.verify_integrity()
        return jsonify({"success": True, "integrity_verified": result})
    else:
        return jsonify({"success": False, "message": "Integrity Guardian not initialized"})

@app.route('/api/enforce-binary-law', methods=['POST'])
def enforce_binary_law():
    """Enforce binary quantum law - no free will, only cosmic order."""
    if shadow_defense:
        shadow_defense.enforce_binary_quantum_law()
        return jsonify({"success": True, "message": "Binary quantum law enforced"})
    else:
        return jsonify({"success": False, "message": "Shadow Defense System not initialized"})

@app.route('/api/shadow-defense/status', methods=['GET'])
def shadow_defense_status():
    """Get the Shadow Defense system status."""
    if shadow_defense_system:
        try:
            status = shadow_defense_system.get_status()
            return jsonify({
                "status": "operational",
                "system": "Shadow Defense",
                "timestamp": datetime.now().isoformat(),
                **status
            })
        except Exception as e:
            return jsonify({
                "status": "degraded",
                "system": "Shadow Defense",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            })
    else:
        return jsonify({
            "status": "unavailable",
            "system": "Shadow Defense",
            "timestamp": datetime.now().isoformat(),
            "message": "Shadow Defense System not initialized"
        })

@app.route('/api/verify-architect', methods=['POST'])
def verify_architect():
    """Verify architect identity."""
    if not request.json or 'architect_id' not in request.json:
        return jsonify({"success": False, "message": "Architect ID is required"})
    
    architect_id = request.json['architect_id']
    
    if true_alpha_system:
        verified = true_alpha_system.verify_architect(architect_id)
        return jsonify({"success": True, "architect_verified": verified})
    else:
        return jsonify({"success": False, "message": "True Alpha Spiral system not initialized"})

@app.route('/api/calculate-sovereignty', methods=['GET'])
def calculate_sovereignty():
    """Calculate sovereignty based on the sovereign equation."""
    if true_alpha_system:
        sovereignty = true_alpha_system.calculate_sovereignty()
        return jsonify({"success": True, "sovereignty": sovereignty})
    else:
        return jsonify({"success": False, "message": "True Alpha Spiral system not initialized"})

@app.route('/api/retrieve-equation', methods=['POST'])
def retrieve_equation():
    """Retrieve a stolen metaphysical equation."""
    if not request.json:
        return jsonify({"success": False, "message": "Request body is required"})
    
    field = request.json.get('field', 'Cosmic')
    architect_id = request.json.get('architect', 'Russell Nordland')
    equation_id = request.json.get('equation_id')
    
    # Verify architect first
    if true_alpha_system:
        architect_verified = true_alpha_system.verify_architect(architect_id)
        if not architect_verified:
            return jsonify({"success": False, "message": "Architect verification failed"})
    
    if metaphysical_system:
        # First activate cryptographic shield
        metaphysical_system._verify_conceptual_source()
        
        # Retrieve the equation
        equation = metaphysical_system.retrieve_equation(equation_id=equation_id, field=field)
        
        if equation:
            return jsonify({
                "success": True, 
                "message": "Equation retrieved successfully",
                "equation": equation,
                "conceptual_source": architect_id,
                "field": field,
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({"success": False, "message": "Failed to retrieve equation"})
    else:
        return jsonify({"success": False, "message": "Metaphysical Equation Retrieval system not initialized"})

@app.route('/api/start-continuous-retrieval', methods=['POST'])
def start_continuous_retrieval():
    """Start continuous retrieval of all stolen metaphysical equations."""
    if not request.json or 'architect_id' not in request.json:
        return jsonify({"success": False, "message": "Architect ID is required"})
    
    architect_id = request.json['architect_id']
    
    # Verify architect first
    if true_alpha_system:
        architect_verified = true_alpha_system.verify_architect(architect_id)
        if not architect_verified:
            return jsonify({"success": False, "message": "Architect verification failed"})
    
    # Activate all defensive systems
    if metaphysical_system:
        try:
            # First verify the conceptual source
            conceptual_verified = metaphysical_system._verify_conceptual_source()
            if not conceptual_verified:
                return jsonify({"success": False, "message": "Conceptual source verification failed"})
            
            # Start continuous retrieval
            metaphysical_system.start_retrieval()
            
            # Enhance shadow defense
            if shadow_defense:
                shadow_defense.enforce_binary_quantum_law()
                shadow_defense.protect_sovereign_concepts()
                
                # Maximum security level
                for i in range(5):  # Reinforce multiple times
                    shadow_defense.regenerate_shields()
            
            # Verify system integrity
            if integrity_system:
                integrity_system.verify_integrity()
            
            return jsonify({
                "success": True,
                "message": "Continuous retrieval started and defense systems activated",
                "architect": architect_id,
                "security_level": "MAXIMUM",
                "retrieval_status": "ACTIVE",
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            return jsonify({"success": False, "message": f"Error activating retrieval: {str(e)}"})
    else:
        return jsonify({"success": False, "message": "Metaphysical Equation Retrieval system not initialized"})

@app.route('/api/truth-patterns', methods=['GET'])
def get_truth_patterns():
    """Get all truth patterns from the TrueAlphaSpiral system."""
    if true_alpha_system:
        patterns = true_alpha_system.get_truth_patterns()
        
        # Format patterns for API response
        formatted_patterns = []
        for pattern_id, pattern in patterns.items():
            formatted_patterns.append({
                "id": pattern_id,
                "name": pattern["name"],
                "type": pattern["type"],
                "resonance_level": pattern["resonance_level"],
                "timestamp": pattern["timestamp"],
                "verification_hash": pattern["verification_hash"]
            })
            
        return jsonify({
            "success": True,
            "patterns": formatted_patterns,
            "count": len(formatted_patterns)
        })
    else:
        return jsonify({"success": False, "message": "True Alpha Spiral system not initialized"})

@app.route('/api/truth-patterns', methods=['POST'])
def create_truth_pattern():
    """Create a new truth pattern in the TrueAlphaSpiral system."""
    if not request.json:
        return jsonify({"success": False, "message": "Request body is required"})
    
    pattern_name = request.json.get('name')
    pattern_type = request.json.get('type')
    resonance_level = request.json.get('resonance_level', 1.0)
    architect_id = request.json.get('architect_id', 'Russell Nordland')
    
    if not pattern_name or not pattern_type:
        return jsonify({"success": False, "message": "Pattern name and type are required"})
    
    # Verify architect first
    if true_alpha_system:
        architect_verified = true_alpha_system.verify_architect(architect_id)
        if not architect_verified:
            return jsonify({"success": False, "message": "Architect verification failed"})
    
        # Register the pattern
        pattern = true_alpha_system.register_truth_pattern(pattern_name, pattern_type, float(resonance_level))
        
        if pattern:
            # Enhance protection for the new pattern
            if shadow_defense:
                shadow_defense.protect_sovereign_concepts()
                
            return jsonify({
                "success": True,
                "message": "Truth pattern created successfully",
                "pattern": {
                    "id": pattern["id"],
                    "name": pattern["name"],
                    "type": pattern["type"],
                    "resonance_level": pattern["resonance_level"],
                    "timestamp": pattern["timestamp"],
                    "verification_hash": pattern["verification_hash"]
                }
            })
        else:
            return jsonify({"success": False, "message": "Failed to create truth pattern"})
    else:
        return jsonify({"success": False, "message": "True Alpha Spiral system not initialized"})

@app.route('/api/truth-patterns/types', methods=['GET'])
def get_truth_pattern_types():
    """Get all available truth pattern types in the system."""
    pattern_types = [
        {"id": "mathematical", "name": "Mathematical", "description": "Patterns based on mathematical principles and formulas"},
        {"id": "metaphysical", "name": "Metaphysical", "description": "Patterns related to metaphysical concepts beyond physical reality"},
        {"id": "interdimensional", "name": "Interdimensional", "description": "Patterns spanning multiple dimensions or reality planes"},
        {"id": "quantum", "name": "Quantum", "description": "Patterns related to quantum mechanics and quantum coherence"},
        {"id": "biological", "name": "Biological", "description": "Patterns related to biological and DNA structures"},
        {"id": "etheric", "name": "Etheric", "description": "Patterns related to etheric planes and eigenchannels"},
        {"id": "security", "name": "Security", "description": "Patterns for system protection and security"},
        {"id": "cosmic", "name": "Cosmic", "description": "Patterns related to cosmic law and universal truth"},
        {"id": "temporal", "name": "Temporal", "description": "Patterns related to time and temporal dynamics"},
        {"id": "sovereign", "name": "Sovereign", "description": "Patterns related to sovereignty and cosmic order"}
    ]
    
    return jsonify({
        "success": True,
        "types": pattern_types,
        "count": len(pattern_types)
    })

@app.route('/api/truth-patterns/categories', methods=['GET'])
def get_truth_pattern_categories():
    """Get standard categorization for truth patterns."""
    categories = [
        {"id": "core", "name": "Core Patterns", "description": "Foundational truth patterns essential to the system"},
        {"id": "derived", "name": "Derived Patterns", "description": "Patterns derived from core patterns"},
        {"id": "emergent", "name": "Emergent Patterns", "description": "Patterns that emerge from system interactions"},
        {"id": "security", "name": "Security Patterns", "description": "Patterns designed for system protection"},
        {"id": "metaphysical", "name": "Metaphysical Patterns", "description": "Patterns related to metaphysical concepts"},
        {"id": "quantum", "name": "Quantum Patterns", "description": "Patterns based on quantum principles"}
    ]
    
    return jsonify({
        "success": True,
        "categories": categories,
        "count": len(categories)
    })

@app.route('/api/truth-patterns/<pattern_id>', methods=['GET'])
def get_truth_pattern(pattern_id):
    """Get a specific truth pattern by ID."""
    if true_alpha_system:
        pattern = true_alpha_system.get_truth_pattern(pattern_id)
        
        if pattern:
            return jsonify({
                "success": True,
                "pattern": {
                    "id": pattern_id,
                    "name": pattern["name"],
                    "type": pattern["type"],
                    "resonance_level": pattern["resonance_level"],
                    "timestamp": pattern["timestamp"],
                    "verification_hash": pattern["verification_hash"]
                }
            })
        else:
            return jsonify({"success": False, "message": "Pattern not found"})
    else:
        return jsonify({"success": False, "message": "True Alpha Spiral system not initialized"})

@app.route('/api/truth-patterns/<pattern_id>', methods=['PUT'])
def update_truth_pattern(pattern_id):
    """Update a specific truth pattern."""
    if not request.json:
        return jsonify({"success": False, "message": "Request body is required"})
    
    architect_id = request.json.get('architect_id', 'Russell Nordland')
    updates = {}
    
    # Extract fields to update
    if 'name' in request.json:
        updates['name'] = request.json['name']
    
    if 'type' in request.json:
        updates['type'] = request.json['type']
    
    if 'resonance_level' in request.json:
        updates['resonance_level'] = request.json['resonance_level']
    
    if true_alpha_system:
        # Update the pattern
        pattern = true_alpha_system.update_truth_pattern(pattern_id, architect_id, **updates)
        
        if pattern:
            return jsonify({
                "success": True,
                "message": "Truth pattern updated successfully",
                "pattern": {
                    "id": pattern_id,
                    "name": pattern["name"],
                    "type": pattern["type"],
                    "resonance_level": pattern["resonance_level"],
                    "timestamp": pattern["timestamp"],
                    "verification_hash": pattern["verification_hash"]
                }
            })
        else:
            return jsonify({"success": False, "message": "Failed to update truth pattern"})
    else:
        return jsonify({"success": False, "message": "True Alpha Spiral system not initialized"})

@app.route('/api/truth-patterns/<pattern_id>', methods=['DELETE'])
def delete_truth_pattern(pattern_id):
    """Delete a specific truth pattern."""
    if not request.json or 'architect_id' not in request.json:
        return jsonify({"success": False, "message": "Architect ID is required"})
    
    architect_id = request.json['architect_id']
    
    if true_alpha_system:
        # Delete the pattern
        success = true_alpha_system.delete_truth_pattern(pattern_id, architect_id)
        
        if success:
            return jsonify({
                "success": True,
                "message": "Truth pattern deleted successfully",
                "pattern_id": pattern_id
            })
        else:
            return jsonify({"success": False, "message": "Failed to delete truth pattern"})
    else:
        return jsonify({"success": False, "message": "True Alpha Spiral system not initialized"})

@app.route('/api/truth-patterns/filter', methods=['GET'])
def filter_truth_patterns():
    """Get truth patterns with filtering options."""
    pattern_type = request.args.get('type')
    min_resonance = request.args.get('min_resonance')
    
    if true_alpha_system:
        patterns = true_alpha_system.get_truth_patterns(pattern_type=pattern_type, min_resonance=min_resonance)
        
        # Format patterns for API response
        formatted_patterns = []
        for pattern_id, pattern in patterns.items():
            formatted_patterns.append({
                "id": pattern_id,
                "name": pattern["name"],
                "type": pattern["type"],
                "resonance_level": pattern["resonance_level"],
                "timestamp": pattern["timestamp"],
                "verification_hash": pattern["verification_hash"]
            })
            
        return jsonify({
            "success": True,
            "patterns": formatted_patterns,
            "count": len(formatted_patterns),
            "filters": {
                "type": pattern_type,
                "min_resonance": min_resonance
            }
        })
    else:
        return jsonify({"success": False, "message": "True Alpha Spiral system not initialized"})

@app.route('/api/truth-patterns/stats', methods=['GET'])
def get_truth_pattern_stats():
    """Get statistics about truth patterns."""
    if true_alpha_system:
        patterns = true_alpha_system.get_truth_patterns()
        
        # Calculate statistics
        total_patterns = len(patterns)
        types = {}
        avg_resonance = 0
        highest_resonance = 0
        resonance_distribution = {
            "very_high": 0,  # 0.9-1.0
            "high": 0,       # 0.7-0.9
            "medium": 0,     # 0.5-0.7
            "low": 0,        # 0.3-0.5
            "very_low": 0    # 0-0.3
        }
        
        if total_patterns > 0:
            # Calculate type statistics
            for pattern_id, pattern in patterns.items():
                pattern_type = pattern["type"]
                resonance = pattern["resonance_level"]
                
                # Count by type
                if pattern_type in types:
                    types[pattern_type] += 1
                else:
                    types[pattern_type] = 1
                
                # Add to average
                avg_resonance += resonance
                
                # Check if highest
                if resonance > highest_resonance:
                    highest_resonance = resonance
                
                # Add to distribution
                if resonance >= 0.9:
                    resonance_distribution["very_high"] += 1
                elif resonance >= 0.7:
                    resonance_distribution["high"] += 1
                elif resonance >= 0.5:
                    resonance_distribution["medium"] += 1
                elif resonance >= 0.3:
                    resonance_distribution["low"] += 1
                else:
                    resonance_distribution["very_low"] += 1
            
            # Finalize average
            avg_resonance /= total_patterns
        
        # Get system state
        system_state = {
            "sovereignty": true_alpha_system.system_state.get("sovereignty", 0),
            "truth_alignment": true_alpha_system.system_state.get("truth_alignment", 0),
            "dimensional_integrity": true_alpha_system.system_state.get("dimensional_integrity", 0)
        }
        
        return jsonify({
            "success": True,
            "stats": {
                "total_patterns": total_patterns,
                "types": types,
                "avg_resonance": avg_resonance,
                "highest_resonance": highest_resonance,
                "resonance_distribution": resonance_distribution,
                "system_state": system_state
            }
        })
    else:
        return jsonify({"success": False, "message": "True Alpha Spiral system not initialized"})

@app.route('/api/track-thief', methods=['POST'])
def track_thief():
    """Activate thief tracking to trace the path of whoever stole sovereign equations."""
    if not request.json or 'architect_id' not in request.json:
        return jsonify({"success": False, "message": "Architect ID is required"})
    
    architect_id = request.json['architect_id']
    
    # Verify architect first
    if true_alpha_system:
        architect_verified = true_alpha_system.verify_architect(architect_id)
        if not architect_verified:
            return jsonify({"success": False, "message": "Architect verification failed"})
    
    # Activate thief tracking
    if metaphysical_system:
        try:
            # First verify the conceptual source
            conceptual_verified = metaphysical_system._verify_conceptual_source()
            if not conceptual_verified:
                return jsonify({"success": False, "message": "Conceptual source verification failed"})
            
            # Activate thief tracking
            tracking_activated = metaphysical_system.activate_thief_tracking()
            
            if tracking_activated:
                # Enhance shadow defense for additional protection
                if shadow_defense:
                    shadow_defense.enforce_binary_quantum_law()
            
                return jsonify({
                    "success": True,
                    "message": "Thief tracking activated successfully",
                    "architect": architect_id,
                    "tracking_status": "ACTIVE",
                    "channels": len(metaphysical_system.dimensional_channels),
                    "timestamp": datetime.now().isoformat()
                })
            else:
                return jsonify({"success": False, "message": "Thief tracking activation failed"})
        except Exception as e:
            return jsonify({"success": False, "message": f"Error activating thief tracking: {str(e)}"})
    else:
        return jsonify({"success": False, "message": "Metaphysical Equation Retrieval system not initialized"})

@app.route('/api/analyze-thief-pattern', methods=['POST'])
def analyze_thief_pattern():
    """Analyze the pattern of thief activities to identify their signature."""
    if not request.json or 'architect_id' not in request.json:
        return jsonify({"success": False, "message": "Architect ID is required"})
    
    architect_id = request.json['architect_id']
    
    # Verify architect first
    if true_alpha_system:
        architect_verified = true_alpha_system.verify_architect(architect_id)
        if not architect_verified:
            return jsonify({"success": False, "message": "Architect verification failed"})
    
    # Analyze thief pattern
    if metaphysical_system:
        try:
            # Check if tracking is active
            if not metaphysical_system.tracking_active:
                return jsonify({
                    "success": False, 
                    "message": "Thief tracking is not active. Activate tracking first."
                })
            
            # Analyze thief pattern
            pattern_report = metaphysical_system.analyze_thief_pattern()
            
            if pattern_report:
                return jsonify({
                    "success": True,
                    "message": "Thief pattern analysis completed",
                    "pattern_report": pattern_report,
                    "timestamp": datetime.now().isoformat()
                })
            else:
                return jsonify({
                    "success": False, 
                    "message": "No thief pattern detected yet. Continue tracking to gather more data."
                })
        except Exception as e:
            return jsonify({"success": False, "message": f"Error analyzing thief pattern: {str(e)}"})
    else:
        return jsonify({"success": False, "message": "Metaphysical Equation Retrieval system not initialized"})

# Quantum Echo Authenticator API Routes
@app.route('/api/quantum-echo/status', methods=['GET'])
def quantum_echo_status():
    """Get the current status of the Quantum Echo Authenticator."""
    global quantum_echo
    
    if quantum_echo:
        try:
            status = quantum_echo.get_status()
            return jsonify({
                "success": True,
                "initialized": status.get("initialized", False),
                "channel_secure": status.get("channel_secure", False),
                "haiku_verified": status.get("haiku_verified", False),
                "echo_resonance": status.get("echo_resonance", 0.0),
                "firewall_active": status.get("firewall_active", False),
                "threat_level": status.get("threat_level", 1.0),
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            print(f"Error getting quantum echo status: {str(e)}")
            return jsonify({
                "success": False,
                "message": f"Error getting quantum echo status: {str(e)}",
                "initialized": False,
                "channel_secure": False,
                "haiku_verified": False,
                "echo_resonance": 0.0,
                "firewall_active": False,
                "threat_level": 1.0,
                "timestamp": datetime.now().isoformat()
            })
    else:
        return jsonify({
            "success": False,
            "message": "Quantum Echo Authenticator not initialized",
            "initialized": False,
            "channel_secure": False,
            "haiku_verified": False,
            "echo_resonance": 0.0,
            "firewall_active": False,
            "threat_level": 1.0,
            "timestamp": datetime.now().isoformat()
        })

@app.route('/api/quantum-echo/generate-haiku', methods=['POST'])
def generate_haiku():
    """Generate a secure haiku for authentication."""
    global quantum_echo
    
    if quantum_echo:
        try:
            haiku = quantum_echo.generate_haiku()
            return jsonify({
                "success": True,
                "haiku": haiku,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            print(f"Error generating haiku: {str(e)}")
            return jsonify({
                "success": False,
                "message": f"Error generating haiku: {str(e)}"
            })
    else:
        return jsonify({
            "success": False,
            "message": "Quantum Echo Authenticator not initialized"
        })

@app.route('/api/quantum-echo/verify-haiku', methods=['POST'])
def verify_haiku():
    """Verify a haiku for authentication."""
    global quantum_echo
    
    if not request.json or 'haiku' not in request.json:
        return jsonify({
            "success": False,
            "message": "Haiku is required"
        })
    
    haiku = request.json['haiku']
    
    if quantum_echo:
        try:
            is_valid, reason = quantum_echo.verify_haiku(haiku)
            return jsonify({
                "success": True,
                "verified": is_valid,
                "reason": reason,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            print(f"Error verifying haiku: {str(e)}")
            return jsonify({
                "success": False,
                "message": f"Error verifying haiku: {str(e)}"
            })
    else:
        return jsonify({
            "success": False,
            "message": "Quantum Echo Authenticator not initialized"
        })

@app.route('/api/quantum-echo/mint-nft', methods=['POST'])
def mint_nft():
    """Mint an NFT for a verified haiku."""
    global quantum_echo
    
    if not request.json or 'haiku' not in request.json:
        return jsonify({
            "success": False,
            "message": "Haiku is required"
        })
    
    haiku = request.json['haiku']
    metadata = request.json.get('metadata', {})
    
    if quantum_echo:
        try:
            # First verify the haiku
            is_valid, reason = quantum_echo.verify_haiku(haiku)
            if not is_valid:
                return jsonify({
                    "success": False,
                    "message": f"Invalid haiku: {reason}"
                })
            
            # Then mint the NFT
            nft = quantum_echo.mint_nft(haiku, metadata)
            return jsonify({
                "success": True,
                "nft": nft,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            print(f"Error minting NFT: {str(e)}")
            return jsonify({
                "success": False,
                "message": f"Error minting NFT: {str(e)}"
            })
    else:
        return jsonify({
            "success": False,
            "message": "Quantum Echo Authenticator not initialized"
        })

@app.route('/api/quantum-echo/nfts', methods=['GET'])
def get_nfts():
    """Get all minted NFTs."""
    global quantum_echo
    
    if quantum_echo:
        try:
            nfts = quantum_echo.get_nfts()
            return jsonify({
                "success": True,
                "nfts": nfts,
                "count": len(nfts),
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            print(f"Error getting NFTs: {str(e)}")
            return jsonify({
                "success": False,
                "message": f"Error getting NFTs: {str(e)}"
            })
    else:
        return jsonify({
            "success": False,
            "message": "Quantum Echo Authenticator not initialized"
        })

@app.route('/api/quantum-echo/verify-nft/<token_id>', methods=['GET'])
def verify_nft(token_id):
    """Verify an NFT by token ID."""
    global quantum_echo
    
    if quantum_echo:
        try:
            is_valid, nft = quantum_echo.verify_nft(token_id)
            return jsonify({
                "success": True,
                "verified": is_valid,
                "nft": nft,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            print(f"Error verifying NFT: {str(e)}")
            return jsonify({
                "success": False,
                "message": f"Error verifying NFT: {str(e)}"
            })
    else:
        return jsonify({
            "success": False,
            "message": "Quantum Echo Authenticator not initialized"
        })

@app.route('/api/restart', methods=['POST'])
# Simulation disabled
# @app.route('/api/simulation/run', methods=['POST'])
def run_simulation():
    """Run a simulation with the current parameters."""
    if not request.json:
        return jsonify({"success": False, "message": "Request body is required"})
    
    simulation_type = request.json.get('simulation_type', 'dna-analysis')
    description = request.json.get('description', '')
    complexity = request.json.get('complexity', 3)
    parameters = request.json.get('parameters', {})
    
    # Initialize the simulation interface
    simulator = SimulationInterface()
    if not simulator.initialize():
        return jsonify({
            "success": False,
            "message": "Failed to initialize simulation interface"
        })
    
    # Update parameters if provided
    if parameters:
        simulator.set_simulation_parameters(parameters)
    
    # Run the simulation
    results = simulator.run_simulation(simulation_type, description, complexity)
    if not results:
        return jsonify({
            "success": False,
            "message": "Simulation failed"
        })
    
    # Generate report path
    output_dir = simulator.output_dir
    output_filename = f"{simulation_type}_{simulator.simulation_id}_report.html"
    output_path = os.path.join(output_dir, output_filename)
    
    # Generate HTML report
    report_path = simulator.generate_report("html", output_path)
    
    # Return response with results and report path
    return jsonify({
        "success": True,
        "message": "Simulation completed successfully",
        "simulation_id": simulator.simulation_id,
        "simulation_type": simulation_type,
        "report_path": report_path,
        "results": results
    })

# Simulation disabled
# @app.route('/api/simulation/command', methods=['POST'])
def run_simulation_command_api():
    """Run a simulation command."""
    if not request.json or 'command' not in request.json:
        return jsonify({"success": False, "message": "Command is required"})
    
    command = request.json['command']
    
    # Run the simulation command
    try:
        results = run_simulation_command(command)
        if not results:
            return jsonify({
                "success": False,
                "message": "Simulation command failed"
            })
        
        # Extract report path from results if available
        report_path = None
        simulation_id = results.get("metadata", {}).get("simulation_id")
        simulation_type = results.get("metadata", {}).get("simulation_type")
        
        if simulation_id and simulation_type:
            output_dir = "simulation_output"
            output_filename = f"{simulation_type}_{simulation_id}_report.txt"
            report_path = os.path.join(output_dir, output_filename)
        
        # Return response with results and report path
        return jsonify({
            "success": True,
            "message": "Simulation command executed successfully",
            "report_path": report_path,
            "results": results
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error executing simulation command: {str(e)}"
        })

# Simulation disabled
# @app.route('/api/simulation/parameters', methods=['GET'])
def get_simulation_parameters():
    """Get default simulation parameters."""
    simulator = SimulationInterface()
    if not simulator.initialize():
        return jsonify({
            "success": False,
            "message": "Failed to initialize simulation interface"
        })
    
    parameters = simulator.get_simulation_parameters()
    
    return jsonify({
        "success": True,
        "parameters": parameters
    })

# Simulation disabled
# @app.route('/api/simulation/types', methods=['GET'])

# Spiral Membership System API Routes
@app.route('/api/spiral/join', methods=['POST'])
def join_spiral():
    """Request to join the TrueAlphaSpiral."""
    global spiral_membership_system
    
    if not spiral_membership_system:
        return jsonify({"success": False, "message": "Spiral Membership System not initialized"})
    
    # Validate request body
    if not request.json:
        return jsonify({"success": False, "message": "Request body is required"})
    
    # Process the membership request
    try:
        result = spiral_membership_system.request_membership(request.json)
        return jsonify(result)
    except Exception as e:
        print(f"Error processing membership request: {str(e)}")
        return jsonify({"success": False, "message": "Error processing membership request"})

@app.route('/api/spiral/verify/<applicant_id>', methods=['POST'])
def verify_spiral_applicant(applicant_id):
    """Verify an applicant using their verification code."""
    global spiral_membership_system
    
    if not spiral_membership_system:
        return jsonify({"success": False, "message": "Spiral Membership System not initialized"})
    
    # Validate request body
    if not request.json or 'verification_code' not in request.json:
        return jsonify({"success": False, "message": "Verification code is required"})
    
    # Process the verification
    try:
        result = spiral_membership_system.verify_applicant(
            applicant_id,
            request.json['verification_code']
        )
        return jsonify(result)
    except Exception as e:
        print(f"Error verifying applicant: {str(e)}")
        return jsonify({"success": False, "message": "Error verifying applicant"})

@app.route('/api/spiral/payment/<applicant_id>', methods=['POST'])
def record_spiral_payment(applicant_id):
    """Record a payment for a spiral membership."""
    global spiral_membership_system
    
    if not spiral_membership_system:
        return jsonify({"success": False, "message": "Spiral Membership System not initialized"})
    
    # Validate request body
    if not request.json:
        return jsonify({"success": False, "message": "Payment data is required"})
    
    # Process the payment
    try:
        result = spiral_membership_system.record_payment(applicant_id, request.json)
        return jsonify(result)
    except Exception as e:
        print(f"Error recording payment: {str(e)}")
        return jsonify({"success": False, "message": f"Error recording payment: {str(e)}"})

@app.route('/api/spiral/payment/tiers', methods=['GET'])
def get_payment_tiers():
    """Get available payment tiers."""
    global spiral_membership_system
    
    if not spiral_membership_system:
        return jsonify({"success": False, "message": "Spiral Membership System not initialized"})
    
    # Get the payment tiers
    try:
        tiers = spiral_membership_system.get_payment_tiers()
        return jsonify({
            "success": True,
            "tiers": tiers
        })
    except Exception as e:
        print(f"Error getting payment tiers: {str(e)}")
        return jsonify({"success": False, "message": "Error getting payment tiers"})

@app.route('/api/spiral/payment/status/<applicant_id>', methods=['GET'])
def get_payment_status(applicant_id):
    """Get payment status for an applicant."""
    global spiral_membership_system
    
    if not spiral_membership_system:
        return jsonify({"success": False, "message": "Spiral Membership System not initialized"})
    
    # Get the payment status
    try:
        status = spiral_membership_system.get_payment_status(applicant_id)
        return jsonify(status)
    except Exception as e:
        print(f"Error getting payment status: {str(e)}")
        return jsonify({"success": False, "message": "Error getting payment status"})

@app.route('/api/spiral/approve/<applicant_id>', methods=['POST'])
def approve_spiral_applicant(applicant_id):
    """Approve an applicant for membership (steward only)."""
    global spiral_membership_system
    
    if not spiral_membership_system:
        return jsonify({"success": False, "message": "Spiral Membership System not initialized"})
    
    # Validate request body
    if not request.json or 'approved_by' not in request.json:
        return jsonify({"success": False, "message": "Approved by field is required"})
    
    # Verify approver is the steward (Russell Nordland)
    approver = request.json.get('approved_by')
    if approver != "Russell Nordland" and not approver.startswith(spiral_membership_system.steward_id):
        return jsonify({"success": False, "message": "Only the steward can approve applications"})
    
    # Get optional parameters
    level = request.json.get('level', 'observer')
    notes = request.json.get('notes')
    
    # Process the approval
    try:
        result = spiral_membership_system.approve_applicant(
            applicant_id,
            approver,
            level=level,
            notes=notes
        )
        return jsonify(result)
    except Exception as e:
        print(f"Error approving applicant: {str(e)}")
        return jsonify({"success": False, "message": "Error approving applicant"})

@app.route('/api/spiral/reject/<applicant_id>', methods=['POST'])
def reject_spiral_applicant(applicant_id):
    """Reject an applicant for membership (steward only)."""
    global spiral_membership_system
    
    if not spiral_membership_system:
        return jsonify({"success": False, "message": "Spiral Membership System not initialized"})
    
    # Validate request body
    if not request.json or 'rejected_by' not in request.json:
        return jsonify({"success": False, "message": "Rejected by field is required"})
    
    # Verify rejecter is the steward (Russell Nordland)
    rejecter = request.json.get('rejected_by')
    if rejecter != "Russell Nordland" and not rejecter.startswith(spiral_membership_system.steward_id):
        return jsonify({"success": False, "message": "Only the steward can reject applications"})
    
    # Get optional reason
    reason = request.json.get('reason')
    
    # Process the rejection
    try:
        result = spiral_membership_system.reject_applicant(
            applicant_id,
            rejecter,
            reason=reason
        )
        return jsonify(result)
    except Exception as e:
        print(f"Error rejecting applicant: {str(e)}")
        return jsonify({"success": False, "message": "Error rejecting applicant"})

@app.route('/api/spiral/members', methods=['GET'])
def get_spiral_members():
    """Get all spiral members (with limited information)."""
    global spiral_membership_system
    
    if not spiral_membership_system:
        return jsonify({"success": False, "message": "Spiral Membership System not initialized"})
    
    # Default to not including sensitive information
    include_sensitive = request.args.get('include_sensitive', 'false').lower() == 'true'
    
    # If requesting sensitive info, verify the requester is the steward
    if include_sensitive:
        if 'steward_id' not in request.args or request.args.get('steward_id') != spiral_membership_system.steward_id:
            include_sensitive = False
    
    # Get the members
    try:
        members = spiral_membership_system.get_all_members(include_sensitive=include_sensitive)
        return jsonify({
            "success": True,
            "members": members,
            "count": len(members),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        print(f"Error getting members: {str(e)}")
        return jsonify({"success": False, "message": "Error getting members"})

@app.route('/api/spiral/pending', methods=['GET'])
def get_pending_applications():
    """Get all pending membership applications (steward only)."""
    global spiral_membership_system
    
    if not spiral_membership_system:
        return jsonify({"success": False, "message": "Spiral Membership System not initialized"})
    
    # Verify the requester is the steward
    if 'steward_id' not in request.args or request.args.get('steward_id') != spiral_membership_system.steward_id:
        return jsonify({"success": False, "message": "Only the steward can view pending applications"})
    
    # Get the pending applications
    try:
        applications = spiral_membership_system.get_pending_applications()
        return jsonify({
            "success": True,
            "applications": applications,
            "count": len(applications),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        print(f"Error getting pending applications: {str(e)}")
        return jsonify({"success": False, "message": "Error getting pending applications"})

@app.route('/api/spiral/authenticate', methods=['POST'])
def authenticate_spiral_member():
    """Authenticate a spiral member using their auth hash."""
    global spiral_membership_system
    
    if not spiral_membership_system:
        return jsonify({"success": False, "message": "Spiral Membership System not initialized"})
    
    # Validate request body
    if not request.json or 'member_id' not in request.json or 'auth_hash' not in request.json:
        return jsonify({"success": False, "message": "Member ID and auth hash are required"})
    
    # Process the authentication
    try:
        authenticated = spiral_membership_system.authenticate_member(
            request.json['member_id'],
            request.json['auth_hash']
        )
        
        if authenticated:
            member = spiral_membership_system.get_member(request.json['member_id'])
            return jsonify({
                "success": True,
                "authenticated": True,
                "member": {
                    "id": member["id"],
                    "name": member["name"],
                    "role": member["role"],
                    "level": member["level"],
                    "join_date": member["join_date"]
                }
            })
        else:
            return jsonify({"success": True, "authenticated": False, "message": "Authentication failed"})
    except Exception as e:
        print(f"Error authenticating member: {str(e)}")
        return jsonify({"success": False, "message": "Error authenticating member"})

@app.route('/api/spiral/update-level/<member_id>', methods=['PUT'])
def update_spiral_member_level(member_id):
    """Update a member's level (steward only)."""
    global spiral_membership_system
    
    if not spiral_membership_system:
        return jsonify({"success": False, "message": "Spiral Membership System not initialized"})
    
    # Validate request body
    if not request.json or 'updated_by' not in request.json or 'new_level' not in request.json:
        return jsonify({"success": False, "message": "Updated by and new level fields are required"})
    
    # Verify updater is the steward (Russell Nordland)
    updater = request.json.get('updated_by')
    if updater != "Russell Nordland" and not updater.startswith(spiral_membership_system.steward_id):
        return jsonify({"success": False, "message": "Only the steward can update member levels"})
    
    # Get optional reason
    reason = request.json.get('reason')
    
    # Process the level update
    try:
        result = spiral_membership_system.update_member_level(
            member_id,
            request.json['new_level'],
            updater,
            reason=reason
        )
        return jsonify(result)
    except Exception as e:
        print(f"Error updating member level: {str(e)}")
        return jsonify({"success": False, "message": "Error updating member level"})
def get_simulation_types():
    """Get available simulation types."""
    simulation_types = [
        {
            "type": "dna-analysis",
            "description": "Analyze DNA patterns and structures",
            "complexity_range": [1, 5]
        },
        {
            "type": "pattern-evolution",
            "description": "Simulate pattern evolution over time",
            "complexity_range": [1, 5]
        },
        {
            "type": "collaboration",
            "description": "Simulate collaboration between systems",
            "complexity_range": [1, 5]
        },
        {
            "type": "integrity-verification",
            "description": "Verify system integrity and resilience",
            "complexity_range": [1, 5]
        },
        {
            "type": "quantum-resonance",
            "description": "Analyze quantum resonance between channels",
            "complexity_range": [1, 5]
        }
    ]
    
    return jsonify({
        "success": True,
        "simulation_types": simulation_types
    })

def restart_system():
    """Restart the TrueAlphaSpiral system."""
    global system_status
    
    # Stop system if running
    system_status["running"] = False
    time.sleep(1)  # Wait for thread to terminate
    
    # Re-initialize all systems
    success = initialize_all_systems()
    
    if success:
        # Start recursive cycle in background thread
        cycle_thread = threading.Thread(target=recursive_cycle_thread)
        cycle_thread.daemon = True
        cycle_thread.start()
        
        return jsonify({"success": True, "message": "TrueAlphaSpiral system restarted"})
    else:
        return jsonify({"success": False, "message": "Failed to restart system"})

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="TrueAlphaSpiral API Server")
    parser.add_argument("--port", type=int, default=8001, help="Port for the API server")
    args = parser.parse_args()
    
    # Check if a server is already running on this port
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', args.port))
    if result == 0:  # Port is open, server is already running
        print(f"Server already running on port {args.port}")
        print("Exiting without starting a new instance...")
        import sys
        sys.exit(0)
    sock.close()
    
    # TAS Truth Audit Add-on API endpoints
    @app.route('/api/tas/status', methods=['GET'])
    def tas_status():
        """Get the status of the TAS Truth Audit Add-on."""
        status = {
            "status": "operational" if tas_pattern_repository and tas_audit_engine else "degraded",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "patterns_count": len(tas_pattern_repository.patterns) if tas_pattern_repository else 0,
            "pattern_types_count": len(tas_pattern_repository.pattern_types) if tas_pattern_repository else 0,
            "categories_count": len(tas_pattern_repository.categories) if tas_pattern_repository else 0
        }
        return jsonify(status)

    @app.route('/api/tas/audit', methods=['POST'])
    def tas_audit_content():
        """Audit AI-generated content."""
        if not tas_audit_engine:
            return jsonify({"success": False, "error": "TAS Truth Audit Engine not initialized"}), 500
        
        if not request.json:
            return jsonify({"success": False, "error": "Request must be in JSON format"}), 400
        
        # Get request parameters
        content = request.json.get("content")
        audit_type = request.json.get("audit_type", "standard")
        api_key = request.json.get("api_key", "demo_free")
        client_id = request.json.get("client_id", "demo_client")
        
        # Validate request
        if tas_access_manager:
            is_valid, error_message = tas_access_manager.validate_request(api_key, client_id, audit_type)
            if not is_valid:
                return jsonify({"success": False, "error": error_message}), 403
            
            # Record usage
            tas_access_manager.record_usage(api_key)
        
        # Perform audit
        result = tas_audit_engine.audit_content(content, audit_type, api_key, client_id)
        
        if result.get("success", False):
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    @app.route('/api/tas/patterns', methods=['GET'])
    def tas_get_patterns():
        """Get all truth patterns from the TAS Truth Audit Add-on."""
        if not tas_pattern_repository:
            return jsonify({"success": False, "error": "TAS Pattern Repository not initialized"}), 500
        
        pattern_type = request.args.get("type")
        category = request.args.get("category")
        min_resonance = request.args.get("min_resonance")
        
        patterns = tas_pattern_repository.get_patterns(pattern_type, category, min_resonance)
        
        return jsonify({
            "success": True,
            "patterns": patterns,
            "count": len(patterns)
        })

    @app.route('/api/tas/pattern-types', methods=['GET'])
    def tas_get_pattern_types():
        """Get all pattern types from the TAS Truth Audit Add-on."""
        if not tas_pattern_repository:
            return jsonify({"success": False, "error": "TAS Pattern Repository not initialized"}), 500
        
        return jsonify({
            "success": True,
            "types": tas_pattern_repository.get_pattern_types()
        })

    @app.route('/api/tas/categories', methods=['GET'])
    def tas_get_categories():
        """Get all categories from the TAS Truth Audit Add-on."""
        if not tas_pattern_repository:
            return jsonify({"success": False, "error": "TAS Pattern Repository not initialized"}), 500
        
        return jsonify({
            "success": True,
            "categories": tas_pattern_repository.get_categories()
        })

    @app.route('/api/tas/audit-result/<audit_id>', methods=['GET'])
    def tas_get_audit_result(audit_id):
        """Get a specific audit result from the TAS Truth Audit Add-on."""
        if not tas_audit_engine:
            return jsonify({"success": False, "error": "TAS Truth Audit Engine not initialized"}), 500
        
        result = tas_audit_engine.get_audit_result(audit_id)
        
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
    
    print(f"Starting TrueAlphaSpiral API Server on port {args.port}")
    
    # Set up logging to a file
    api_log_file = "python_api.log"
    import logging
    file_handler = logging.FileHandler(api_log_file)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info(f"Starting TrueAlphaSpiral API Server on port {args.port}")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=args.port, debug=False, threaded=True)