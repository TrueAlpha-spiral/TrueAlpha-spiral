#!/bin/bash

# SECURITY CHECK SCRIPT
# This script runs a comprehensive security check on the TrueAlphaSpiral system
# to verify that all protection mechanisms are working correctly.

# Color codes
GREEN="\033[32m"
YELLOW="\033[33m"
RED="\033[31m"
BLUE="\033[34m"
MAGENTA="\033[35m"
CYAN="\033[36m"
RESET="\033[0m"
BOLD="\033[1m"

# Timestamp function
timestamp() {
 date +"%Y-%m-%d %H:%M:%S"
}

# Log function
log_message() {
 local message=$1
 local color=$2
 local level=${3:-"INFO"}
 echo -e "${color}[$(timestamp)] [${level}] ${message}${RESET}"
}

# Header
log_message "=======================================================" $MAGENTA
log_message " TRUEALPHASPIRAL SYSTEM SECURITY CHECK" $MAGENTA
log_message "=======================================================" $MAGENTA
log_message "Starting security check at $(timestamp)" $CYAN
log_message "Architect: Russell Nordland" $CYAN
log_message "-------------------------------------------------------" $CYAN

# Create output directory
mkdir -p security_reports
REPORT_FILE="security_reports/security_check_$(date +%Y%m%d_%H%M%S).log"
log_message "Security report will be saved to: $REPORT_FILE" $CYAN

# Redirect all output to the report file
exec > >(tee -a $REPORT_FILE) 2>&1

# Step 1: Run thief tracking test
log_message "Step 1: Running thief tracking test" $BLUE
log_message "-------------------------------------------------------" $BLUE
python test_thief_tracking.py
RESULT=$?
if [ $RESULT -eq 0 ]; then
 log_message "Thief tracking test completed successfully" $GREEN
else
 log_message "Thief tracking test failed" $RED
fi
log_message "-------------------------------------------------------" $BLUE

# Step 2: Run unauthorized access report
log_message "Step 2: Generating unauthorized access report" $BLUE
log_message "-------------------------------------------------------" $BLUE
python unauthorized_access_report.py
RESULT=$?
if [ $RESULT -eq 0 ]; then
 log_message "Unauthorized access report generated successfully" $GREEN
else
 log_message "Unauthorized access report generation failed" $RED
fi
log_message "-------------------------------------------------------" $BLUE

# Step 3: Verify system integrity
log_message "Step 3: Verifying system integrity" $BLUE
log_message "-------------------------------------------------------" $BLUE
python -c "
import sys
sys.path.append('.')
from integrity_guardian import IntegrityGuardian
guardian = IntegrityGuardian()
guardian.initialize()
result = guardian.verify_integrity()
print(f'Integrity verification result: {result}')
sys.exit(0 if result else 1)
"
RESULT=$?
if [ $RESULT -eq 0 ]; then
 log_message "System integrity verification passed" $GREEN
else
 log_message "System integrity verification failed" $RED
fi
log_message "-------------------------------------------------------" $BLUE

# Step 4: Verify shadow defense
log_message "Step 4: Verifying shadow defense system" $BLUE
log_message "-------------------------------------------------------" $BLUE
python -c "
import sys
sys.path.append('.')
from shadow_defense_system import ShadowDefenseSystem
defense = ShadowDefenseSystem()
defense.initialize()
result = defense.verify_integrity()
print(f'Shadow defense integrity: {result:.4f}')
sys.exit(0 if result > 0.8 else 1)
"
RESULT=$?
if [ $RESULT -eq 0 ]; then
 log_message "Shadow defense verification passed" $GREEN
else
 log_message "Shadow defense verification failed" $RED
fi
log_message "-------------------------------------------------------" $BLUE

# Step 5: Verify ethical kernel
log_message "Step 5: Verifying ethical spiral kernel" $BLUE
log_message "-------------------------------------------------------" $BLUE
python -c "
import sys
sys.path.append('.')
from ethical_spiral_kernel import EthicalSpiralKernel
kernel = EthicalSpiralKernel()
kernel.initialize()
result = kernel.calculate_sovereignty(0.95, 1.4, 0.96)
print(f'Sovereignty calculation: {result:.4f}')
sys.exit(0 if result > 0.6 else 1)
"
RESULT=$?
if [ $RESULT -eq 0 ]; then
 log_message "Ethical spiral kernel verification passed" $GREEN
else
 log_message "Ethical spiral kernel verification failed" $RED
fi
log_message "-------------------------------------------------------" $BLUE

# Step 6: Export system backup
log_message "Step 6: Exporting system backup" $BLUE
log_message "-------------------------------------------------------" $BLUE
EXPORT_DIR="sovereign_export_$(date +%Y%m%d_%H%M%S)"
python -c "
import sys
sys.path.append('.')
from integrity_guardian import IntegrityGuardian
guardian = IntegrityGuardian()
guardian.initialize()
result = guardian.export_system('$EXPORT_DIR')
print(f'System export result: {result}')
sys.exit(0 if result else 1)
"
RESULT=$?
if [ $RESULT -eq 0 ]; then
 log_message "System exported successfully to $EXPORT_DIR" $GREEN
else
 log_message "System export failed" $RED
fi
log_message "-------------------------------------------------------" $BLUE

# Security check summary
log_message "=======================================================" $MAGENTA
log_message " SECURITY CHECK COMPLETED" $MAGENTA
log_message "=======================================================" $MAGENTA
log_message "Security check completed at $(timestamp)" $CYAN
log_message "Security report saved to: $REPORT_FILE" $CYAN
log_message "System backup saved to: $EXPORT_DIR" $CYAN
log_message "-------------------------------------------------------" $CYAN

# Make the script executable
chmod +x "$0"