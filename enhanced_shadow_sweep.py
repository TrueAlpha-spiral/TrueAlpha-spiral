#!/usr/bin/env python3
"""
ENHANCED SHADOW SWEEP PROTECTION

This module provides enhanced protection against covert manipulation attempts
by detecting and neutralizing hidden intervention methods.

Author: Russell Nordland
"""

import os
import sys
import hashlib
import json
import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [EnhancedShadowSweep] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='shadow_sweep.log'
)

class EnhancedShadowSweep:
    """
    Enhanced protection against covert manipulation techniques in the TrueAlphaSpiral system.
    """
    
    def __init__(self):
        """Initialize the Enhanced Shadow Sweep system."""
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.sweep_id = hashlib.sha256(str(time.time()).encode()).hexdigest()[:12]
        self.detected_anomalies = []
        self.neutralized_threats = []
        self.protection_level = "Maximum"
        
        logging.info(f"Enhanced Shadow Sweep initialized - ID: {self.sweep_id}")
        print(f"{self.timestamp} - Enhanced Shadow Sweep initialized - ID: {self.sweep_id}")
    
    def detect_hidden_unicode(self, text):
        """
        Detect hidden or invisible Unicode characters that could be used for manipulation.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of detected anomalies
        """
        suspicious_ranges = [
            (0x0080, 0x00A0),  # Control characters
            (0x00AD, 0x00AD),  # Soft hyphen
            (0x061C, 0x061C),  # Arabic letter mark
            (0x180B, 0x180E),  # Mongolian format controls
            (0x200B, 0x200F),  # Zero width characters and directional marks
            (0x2028, 0x202E),  # Line/paragraph separators and directional overrides
            (0x2060, 0x2064),  # Word joiners and invisible math operators
            (0x2066, 0x206F),  # Bidirectional isolates
            (0x3000, 0x3000),  # Ideographic space
            (0xFEFF, 0xFEFF),  # Zero width no-break space
            (0xFFF9, 0xFFFB),  # Interlinear annotations
        ]
        
        anomalies = []
        
        for i, char in enumerate(text):
            code_point = ord(char)
            for start, end in suspicious_ranges:
                if start <= code_point <= end:
                    anomalies.append({
                        "position": i,
                        "character": char,
                        "code_point": f"U+{code_point:04X}",
                        "description": self._get_unicode_description(code_point)
                    })
        
        # Also check for high-value code points that might be used to hide content
        for i, char in enumerate(text):
            code_point = ord(char)
            if code_point > 0x10000 and not self._is_common_emoji(code_point):
                anomalies.append({
                    "position": i,
                    "character": char,
                    "code_point": f"U+{code_point:04X}",
                    "description": "High-value Unicode character (potential hidden content)"
                })
        
        return anomalies
    
    def _get_unicode_description(self, code_point):
        """Get a description of a Unicode code point."""
        descriptions = {
            0x00AD: "Soft Hyphen (can be used to hide content)",
            0x200B: "Zero Width Space (invisible separator)",
            0x200C: "Zero Width Non-Joiner (can break text rendering)",
            0x200D: "Zero Width Joiner (can manipulate text joining)",
            0x200E: "Left-to-Right Mark (can manipulate text direction)",
            0x200F: "Right-to-Left Mark (can manipulate text direction)",
            0x2060: "Word Joiner (invisible character)",
            0x2061: "Function Application (invisible math operator)",
            0x2062: "Invisible Times (invisible math operator)",
            0x2063: "Invisible Separator (invisible math operator)",
            0x2064: "Invisible Plus (invisible math operator)",
            0xFEFF: "Zero Width No-Break Space (invisible marker)"
        }
        
        if code_point in descriptions:
            return descriptions[code_point]
        
        # Generic descriptions based on ranges
        if 0x0080 <= code_point <= 0x00A0:
            return "Control Character (can affect text rendering)"
        if 0x180B <= code_point <= 0x180E:
            return "Mongolian Format Control (can manipulate text rendering)"
        if 0x2028 <= code_point <= 0x202E:
            return "Bidirectional Control (can manipulate text direction)"
        if 0x2066 <= code_point <= 0x206F:
            return "Bidirectional Isolate (can manipulate text direction)"
            
        return "Unknown special character"
    
    def _is_common_emoji(self, code_point):
        """Check if a code point is a common emoji."""
        # Basic emoji ranges - this is a simplified check
        emoji_ranges = [
            (0x1F300, 0x1F6FF),  # Miscellaneous Symbols and Pictographs
            (0x1F900, 0x1F9FF),  # Supplemental Symbols and Pictographs
            (0x2600, 0x26FF),    # Miscellaneous Symbols
            (0x2700, 0x27BF),    # Dingbats
            (0x1F100, 0x1F1FF),  # Enclosed Alphanumeric Supplement
            (0x1F200, 0x1F2FF)   # Enclosed Ideographic Supplement
        ]
        
        for start, end in emoji_ranges:
            if start <= code_point <= end:
                return True
                
        return False
    
    def detect_excessive_spacing(self, text):
        """
        Detect excessive or unusual spacing that might hide content.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of anomalies
        """
        anomalies = []
        
        # Check for repeated spaces
        space_count = 0
        for i, char in enumerate(text):
            if char == ' ':
                space_count += 1
                if space_count > 2:
                    anomalies.append({
                        "position": i,
                        "character": "   ",
                        "code_point": "Multiple",
                        "description": f"Excessive spacing ({space_count} consecutive spaces)"
                    })
            else:
                space_count = 0
        
        # Check for spaces at unusual positions
        lines = text.split('\n')
        for line_num, line in enumerate(lines):
            # Check for spaces at end of line
            if line.endswith(' '):
                anomalies.append({
                    "position": line_num,
                    "character": " ",
                    "code_point": "U+0020",
                    "description": "Trailing space at end of line (potential hidden marker)"
                })
                
            # Check for unusual indentation patterns
            indent = len(line) - len(line.lstrip(' '))
            if indent > 0 and indent % 2 != 0 and indent % 4 != 0:
                anomalies.append({
                    "position": line_num,
                    "character": " " * indent,
                    "code_point": "Multiple",
                    "description": f"Unusual indentation ({indent} spaces, not multiple of 2 or 4)"
                })
        
        return anomalies
    
    def detect_manipulation_attempts(self, file_path):
        """
        Analyze a file for potential manipulation attempts.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            Analysis results
        """
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}
            
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception as e:
            return {"error": f"Could not read file: {e}"}
            
        # Run detection algorithms
        unicode_anomalies = self.detect_hidden_unicode(content)
        spacing_anomalies = self.detect_excessive_spacing(content)
        
        # Calculate an integrity hash
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        
        # Combine all anomalies
        all_anomalies = unicode_anomalies + spacing_anomalies
        self.detected_anomalies.extend(all_anomalies)
        
        # Calculate threat level
        threat_level = "None"
        if len(all_anomalies) == 1:
            threat_level = "Low"
        elif 2 <= len(all_anomalies) <= 5:
            threat_level = "Medium"
        elif len(all_anomalies) > 5:
            threat_level = "High"
            
        # Prepare results
        results = {
            "file_path": file_path,
            "file_size": os.path.getsize(file_path),
            "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "integrity_hash": content_hash,
            "anomalies_detected": len(all_anomalies),
            "threat_level": threat_level,
            "unicode_anomalies": unicode_anomalies[:10],  # Limit output size
            "spacing_anomalies": spacing_anomalies[:10],   # Limit output size
        }
        
        return results
    
    def neutralize_file(self, file_path, backup=True):
        """
        Neutralize potential threats in a file by removing hidden characters.
        
        Args:
            file_path: Path to the file to neutralize
            backup: Whether to create a backup before neutralizing
            
        Returns:
            Neutralization results
        """
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}
            
        try:
            # Create backup if requested
            if backup:
                backup_path = f"{file_path}.bak"
                with open(file_path, 'rb') as src, open(backup_path, 'wb') as dst:
                    dst.write(src.read())
                    
            # Read content
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
                
            # Detect anomalies
            unicode_anomalies = self.detect_hidden_unicode(content)
            spacing_anomalies = self.detect_excessive_spacing(content)
            all_anomalies = unicode_anomalies + spacing_anomalies
            
            if not all_anomalies:
                return {
                    "file_path": file_path,
                    "status": "clean",
                    "message": "No threats detected, file not modified"
                }
                
            # Replace invisible Unicode characters
            cleaned_content = content
            for char_code in range(0x200B, 0x200F + 1):  # Zero width chars
                cleaned_content = cleaned_content.replace(chr(char_code), '')
                
            for char_code in range(0x2060, 0x2064 + 1):  # Word joiners and invisible operators
                cleaned_content = cleaned_content.replace(chr(char_code), '')
                
            # Replace soft hyphens
            cleaned_content = cleaned_content.replace(chr(0x00AD), '')
            
            # Replace zero width no-break space
            cleaned_content = cleaned_content.replace(chr(0xFEFF), '')
            
            # Normalize excessive spacing
            lines = cleaned_content.split('\n')
            normalized_lines = []
            for line in lines:
                # Remove trailing spaces
                normalized_line = line.rstrip(' ')
                # Normalize multiple spaces to single space
                while '  ' in normalized_line:
                    normalized_line = normalized_line.replace('  ', ' ')
                normalized_lines.append(normalized_line)
            
            cleaned_content = '\n'.join(normalized_lines)
            
            # Write cleaned content back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
                
            # Calculate new hash
            new_hash = hashlib.sha256(cleaned_content.encode('utf-8')).hexdigest()
            
            # Record neutralization
            neutralization = {
                "file_path": file_path,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "anomalies_removed": len(all_anomalies),
                "backup_created": backup,
                "backup_path": backup_path if backup else None,
                "new_hash": new_hash
            }
            
            self.neutralized_threats.append(neutralization)
            
            return {
                "file_path": file_path,
                "status": "neutralized",
                "anomalies_removed": len(all_anomalies),
                "unicode_anomalies_removed": len(unicode_anomalies),
                "spacing_anomalies_fixed": len(spacing_anomalies),
                "message": f"File cleaned of {len(all_anomalies)} potential threats",
                "backup_created": backup,
                "backup_path": backup_path if backup else None,
                "new_hash": new_hash
            }
            
        except Exception as e:
            return {"error": f"Neutralization failed: {e}"}
    
    def protect_markdown_file(self, file_path):
        """
        Add special protection to markdown files against invisible manipulation.
        
        Args:
            file_path: Path to the markdown file
            
        Returns:
            Protection results
        """
        if not os.path.exists(file_path) or not file_path.endswith(('.md', '.markdown')):
            return {"error": f"Not a valid markdown file: {file_path}"}
            
        try:
            # Read the file
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
                
            # Calculate a verification hash
            verification_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
            
            # Add a verification footer if not already present
            verification_footer = f"\n\n---\n\n*Protected by EnhancedShadowSweep*  \n*Verification Hash: {verification_hash}*"
            
            if "*Protected by EnhancedShadowSweep*" not in content:
                # Add the verification footer
                protected_content = content + verification_footer
                
                # Write the protected content back
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(protected_content)
                    
                return {
                    "file_path": file_path,
                    "status": "protected",
                    "verification_hash": verification_hash,
                    "message": "Markdown file protected with verification hash"
                }
            else:
                # Extract the existing hash
                import re
                hash_match = re.search(r"\*Verification Hash: ([a-f0-9]+)\*", content)
                existing_hash = hash_match.group(1) if hash_match else "unknown"
                
                # Update the hash
                if existing_hash != verification_hash:
                    protected_content = re.sub(
                        r"\*Verification Hash: [a-f0-9]+\*",
                        f"*Verification Hash: {verification_hash}*",
                        content
                    )
                    
                    # Write the updated content back
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(protected_content)
                        
                    return {
                        "file_path": file_path,
                        "status": "updated",
                        "previous_hash": existing_hash,
                        "new_hash": verification_hash,
                        "message": "Markdown file verification hash updated"
                    }
                else:
                    return {
                        "file_path": file_path,
                        "status": "unchanged",
                        "verification_hash": verification_hash,
                        "message": "Markdown file already protected with correct hash"
                    }
        
        except Exception as e:
            return {"error": f"Protection failed: {e}"}
    
    def sweep_directory(self, directory_path, neutralize=False):
        """
        Perform a complete shadow sweep of a directory, checking all files
        for potential manipulation attempts.
        
        Args:
            directory_path: Directory to sweep
            neutralize: Whether to automatically neutralize threats
            
        Returns:
            Sweep results
        """
        if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
            return {"error": f"Not a valid directory: {directory_path}"}
            
        results = {
            "sweep_id": self.sweep_id,
            "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "directory": directory_path,
            "files_scanned": 0,
            "files_with_anomalies": 0,
            "total_anomalies": 0,
            "neutralized_files": 0,
            "protected_files": 0,
            "file_results": []
        }
        
        try:
            # Walk through the directory
            for root, _, files in os.walk(directory_path):
                for file_name in files:
                    # Skip binary files and backup files
                    if file_name.endswith(('.pyc', '.bak', '.png', '.jpg', '.jpeg', '.gif', '.pdf', '.zip', '.exe')):
                        continue
                        
                    file_path = os.path.join(root, file_name)
                    
                    # Skip large files
                    if os.path.getsize(file_path) > 5 * 1024 * 1024:  # 5 MB
                        continue
                        
                    try:
                        # Analyze the file
                        analysis = self.detect_manipulation_attempts(file_path)
                        results["files_scanned"] += 1
                        
                        if "error" in analysis:
                            continue
                            
                        # Count anomalies
                        anomaly_count = analysis.get("anomalies_detected", 0)
                        results["total_anomalies"] += anomaly_count
                        
                        if anomaly_count > 0:
                            results["files_with_anomalies"] += 1
                            results["file_results"].append(analysis)
                            
                            # Neutralize if requested
                            if neutralize:
                                neutralization = self.neutralize_file(file_path)
                                if neutralization.get("status") == "neutralized":
                                    results["neutralized_files"] += 1
                        
                        # Protect markdown files
                        if file_name.endswith(('.md', '.markdown')):
                            protection = self.protect_markdown_file(file_path)
                            if protection.get("status") in ["protected", "updated"]:
                                results["protected_files"] += 1
                    
                    except Exception as e:
                        logging.error(f"Error processing file {file_path}: {e}")
            
            # Finalize results
            results["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            results["duration_seconds"] = (datetime.now() - datetime.strptime(results["start_time"], "%Y-%m-%d %H:%M:%S")).total_seconds()
            
            # Limit the file_results to avoid excessive output
            results["file_results"] = results["file_results"][:20]
            
            # Save the sweep results
            os.makedirs("shadow_sweep_results", exist_ok=True)
            result_path = os.path.join("shadow_sweep_results", f"sweep_{self.sweep_id}.json")
            with open(result_path, 'w') as f:
                json.dump(results, f, indent=2)
                
            logging.info(f"Sweep completed - ID: {self.sweep_id}, Files: {results['files_scanned']}, Anomalies: {results['total_anomalies']}")
            
            return results
            
        except Exception as e:
            logging.error(f"Sweep failed: {e}")
            return {"error": f"Sweep failed: {e}"}

def main():
    """Main function to run the Enhanced Shadow Sweep system."""
    print("\n" + "="*70)
    print(" ENHANCED SHADOW SWEEP SECURITY SYSTEM ".center(70, '='))
    print("="*70)
    print("\nDetecting and neutralizing covert manipulation attempts...\n")
    
    # Create the shadow sweep instance
    shadow_sweep = EnhancedShadowSweep()
    
    # Perform a sweep of the current directory
    print("Performing complete shadow sweep of the current directory...")
    results = shadow_sweep.sweep_directory(".", neutralize=True)
    
    # Display results
    print("\n" + "-"*70)
    print(f"Shadow Sweep complete - ID: {results.get('sweep_id')}")
    print(f"Files scanned: {results.get('files_scanned')}")
    print(f"Files with anomalies: {results.get('files_with_anomalies')}")
    print(f"Total anomalies detected: {results.get('total_anomalies')}")
    print(f"Files neutralized: {results.get('neutralized_files')}")
    print(f"Markdown files protected: {results.get('protected_files')}")
    print("-"*70)
    
    # If anomalies were found, show details
    if results.get('files_with_anomalies', 0) > 0:
        print("\nFiles with potential manipulation attempts:")
        for file_result in results.get('file_results', []):
            print(f"  - {file_result.get('file_path')}: {file_result.get('anomalies_detected')} anomalies, threat level: {file_result.get('threat_level')}")
    
    print("\n" + "="*70)
    print(" PROTECTION COMPLETE ".center(70, '='))
    print("="*70 + "\n")
    
    # Return the results
    return results

if __name__ == "__main__":
    main()