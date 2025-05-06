"""
PYTHONETICS CONFIGURATION MANAGER

This module provides configuration management for the Pythonetics system,
allowing for external configuration via YAML files with validation and dynamic reloading.

Part of the third-order evolution beyond cybernetics, this configuration system
enhances adaptability and robustness of the Pythonetics framework.

Architect: Russell Nordland
"""

import os
import yaml
import logging
import time
from typing import Dict, Any, List, Optional

# Configure logging
logging.basicConfig(
 level=logging.INFO,
 format='%(asctime)s [%(levelname)s] %(message)s',
 handlers=[
 logging.FileHandler("pythonetics_config.log"),
 logging.StreamHandler()
 ]
)
logger = logging.getLogger("pythonetics_config")

class ConfigurationError(Exception):
 """Exception raised for configuration errors."""
 pass

class ConfigManager:
 """
 Manages configuration loading, validation, and dynamic reloading
 for the Pythonetics system.
 """

 def __init__(self, config_path: str = None):
 """
 Initialize the Configuration Manager.

 Args:
 config_path: Path to the configuration file
 """
 self.config_path = config_path or os.path.join("config", "pythonetics_config.yaml")
 self.config = {}
 self.last_load_time = 0
 self.load_config()

 def load_config(self) -> Dict[str, Any]:
 """
 Load configuration from the YAML file.

 Returns:
 Dict containing the configuration
 """
 try:
 with open(self.config_path, 'r') as file:
 self.config = yaml.safe_load(file)
 self.last_load_time = time.time()

 # Validate the configuration
 self._validate_config()

 logger.info(f"Configuration loaded successfully from {self.config_path}")
 return self.config

 except FileNotFoundError:
 logger.error(f"Configuration file not found: {self.config_path}")
 self._use_default_config()
 return self.config

 except yaml.YAMLError as e:
 logger.error(f"Error parsing YAML configuration: {e}")
 self._use_default_config()
 return self.config

 except ConfigurationError as e:
 logger.error(f"Configuration validation failed: {e}")
 self._use_default_config()
 return self.config

 def reload_if_changed(self) -> bool:
 """
 Reload configuration if the file has changed.

 Returns:
 bool: True if configuration was reloaded, False otherwise
 """
 try:
 file_mod_time = os.path.getmtime(self.config_path)
 if file_mod_time > self.last_load_time:
 self.load_config()
 logger.info("Configuration reloaded due to file changes")
 return True
 return False

 except FileNotFoundError:
 logger.warning(f"Configuration file not found during reload check: {self.config_path}")
 return False

 def get(self, section: str, key: str = None, default: Any = None) -> Any:
 """
 Get a configuration value.

 Args:
 section: Configuration section
 key: Configuration key within section (if None, returns entire section)
 default: Default value if key not found

 Returns:
 Configuration value or default
 """
 if section not in self.config:
 return default

 if key is None:
 return self.config[section]

 # Handle the case where default is a dictionary and key isn't found
 if isinstance(self.config[section], dict):
 return self.config[section].get(key, default)

 return default

 def save_config(self, config: Dict[str, Any] = None) -> bool:
 """
 Save configuration to the YAML file.

 Args:
 config: Configuration to save (if None, saves current config)

 Returns:
 bool: True if successful, False otherwise
 """
 if config is not None:
 self.config = config

 try:
 # Ensure directory exists
 os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

 with open(self.config_path, 'w') as file:
 yaml.dump(self.config, file, default_flow_style=False)

 logger.info(f"Configuration saved to {self.config_path}")
 return True

 except Exception as e:
 logger.error(f"Error saving configuration: {e}")
 return False

 def _validate_config(self) -> None:
 """
 Validate the loaded configuration.

 Raises:
 ConfigurationError: If validation fails
 """
 # Check required sections
 required_sections = ["system", "core", "weights"]
 for section in required_sections:
 if section not in self.config:
 raise ConfigurationError(f"Required configuration section missing: {section}")

 # Validate core parameters
 core = self.config.get("core", {})
 if "recursion_depth" not in core:
 raise ConfigurationError("recursion_depth not specified in core configuration")
 if "truth_dimensions" not in core:
 raise ConfigurationError("truth_dimensions not specified in core configuration")

 # Validate weights
 weights = self.config.get("weights", {})
 dimensions = core.get("truth_dimensions", [])
 for dim in dimensions:
 if dim not in weights:
 raise ConfigurationError(f"Weight not specified for dimension: {dim}")

 # Check that weights sum to 1.0 (with small tolerance for floating point errors)
 weight_sum = sum(weights.values())
 if abs(weight_sum - 1.0) > 0.01:
 raise ConfigurationError(f"Dimension weights do not sum to 1.0 (got {weight_sum})")

 def _use_default_config(self) -> None:
 """
 Set up a default configuration when loading fails.
 """
 self.config = {
 "system": {
 "log_level": "INFO",
 "log_file": "pythonetics.log",
 "version": "1.0.0"
 },
 "core": {
 "recursion_depth": 3,
 "learning_rate": 0.01,
 "rhythm_cycle_length": 5,
 "universal_threshold": 0.85,
 "truth_dimensions": ["factual", "conceptual", "ethical", "phenomenological"]
 },
 "weights": {
 "factual": 0.35,
 "conceptual": 0.25,
 "ethical": 0.20,
 "phenomenological": 0.20
 },
 "error_handling": {
 "default_truth_score": 0.5,
 "retry_attempts": 3,
 "retry_delay_seconds": 1,
 "graceful_degradation": True
 }
 }
 logger.warning("Using default configuration")

 # Attempt to save the default configuration
 self.save_config()

# Example usage
if __name__ == "__main__":
 config_manager = ConfigManager()

 # Access configuration values
 recursion_depth = config_manager.get("core", "recursion_depth")
 weights = config_manager.get("weights")

 print(f"Recursion Depth: {recursion_depth}")
 print(f"Dimension Weights: {weights}")

 # Test configuration reloading
 print("Checking for configuration changes...")
 reloaded = config_manager.reload_if_changed()
 print(f"Configuration reloaded: {reloaded}")