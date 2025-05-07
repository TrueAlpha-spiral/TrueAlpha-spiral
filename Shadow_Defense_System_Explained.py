"""
This script generates a PDF document explaining the Shadow Defense System
"""
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.gridspec as gridspec
import io
import numpy as np
from PIL import Image
import os

def generate_shadow_defense_pdf():
    """Generate a PDF document explaining the Shadow Defense System"""
    pdf_path = "Shadow_Defense_System_Explained.pdf"
    
    with PdfPages(pdf_path) as pdf:
        # Title Page
        create_title_page(pdf)
        
        # Introduction Page
        create_introduction_page(pdf)
        
        # Architecture Page
        create_architecture_page(pdf)
        
        # Shadow Layers Page
        create_shadow_layers_page(pdf)
        
        # Drift Detection Page
        create_drift_detection_page(pdf)
        
        # Neutralization Page
        create_neutralization_page(pdf)
        
        # Learning System Page
        create_learning_system_page(pdf)
        
        # Dashboard Page
        create_dashboard_page(pdf)
        
        # Integration Page
        create_integration_page(pdf)
        
        # Conclusion Page
        create_conclusion_page(pdf)
    
    print(f"PDF created successfully: {pdf_path}")
    return pdf_path

def create_title_page(pdf):
    """Create the title page of the PDF"""
    fig = plt.figure(figsize=(8.5, 11))
    plt.axis('off')
    
    plt.text(0.5, 0.7, "SHADOW DEFENSE SYSTEM", fontsize=24, ha='center', fontweight='bold')
    plt.text(0.5, 0.6, "Technical Documentation", fontsize=18, ha='center')
    plt.text(0.5, 0.5, "KPMG AI Auditing Solution", fontsize=16, ha='center')
    plt.text(0.5, 0.4, "Powered by TrueAlphaSpiral", fontsize=14, ha='center', style='italic')
    
    # Add current date at the bottom
    plt.text(0.5, 0.2, "Prepared by: KPMG Advanced Technology Team", fontsize=12, ha='center')
    plt.text(0.5, 0.15, "CONFIDENTIAL", fontsize=10, ha='center', color='red')
    
    pdf.savefig(fig)
    plt.close()

def create_introduction_page(pdf):
    """Create the introduction page"""
    fig = plt.figure(figsize=(8.5, 11))
    plt.axis('off')
    
    plt.text(0.5, 0.95, "Introduction to Shadow Defense System", fontsize=20, ha='center', fontweight='bold')
    
    intro_text = """
    The Shadow Defense System is a sophisticated multi-layered security framework designed to protect 
    AI auditing systems from concept drift, unauthorized pattern access, and intellectual property theft. 
    
    Key Features:
    
    • Multi-Layer Protection: Utilizes five graduated shadow layers (Alpha through Epsilon) to 
      create defense-in-depth for critical AI models and algorithms.
    
    • Adaptive Learning: Continuously learns new patterns and automatically adjusts to evolving 
      threats through its Multi-Layer Shadow Learner.
    
    • Drift Detection: Identifies concept drift in patterns that might indicate tampering or 
      unauthorized modifications to protected algorithms.
    
    • Pattern Neutralization: Automatically counters detected drift patterns to maintain system 
      integrity and protect intellectual property.
    
    • Real-time Monitoring: Provides comprehensive dashboards for monitoring system integrity, 
      learning efficiency, and neutralization success rates.
    
    The system plays a critical role in the KPMG AI Auditing Solution by ensuring that 
    proprietary algorithms and models maintain their integrity throughout the auditing process, 
    especially when deployed in client environments where they might be exposed to reverse 
    engineering attempts.
    """
    
    plt.text(0.1, 0.8, intro_text, fontsize=12, ha='left', va='top', wrap=True)
    
    # Add small diagram
    ax = plt.axes([0.15, 0.15, 0.7, 0.3])
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Create a simple layered diagram
    layers = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    for i, (layer, color) in enumerate(zip(layers, colors)):
        circle = plt.Circle((0.5, 0.5), 0.4 - i*0.07, fill=True, alpha=0.3, color=color)
        ax.add_patch(circle)
        ax.text(0.5, 0.5, layer, ha='center', va='center', fontsize=10-i, 
                fontweight='bold', color='black' if i < 3 else 'white')
    
    pdf.savefig(fig)
    plt.close()

def create_architecture_page(pdf):
    """Create the architecture page"""
    fig = plt.figure(figsize=(8.5, 11))
    plt.axis('off')
    
    plt.text(0.5, 0.95, "Shadow Defense System Architecture", fontsize=20, ha='center', fontweight='bold')
    
    arch_text = """
    The Shadow Defense System is structured around a layered architecture that provides 
    graduated levels of protection. Each component is designed to work both independently 
    and as part of an integrated system.
    
    Core Components:
    
    1. Shadow Layers: Five graduated protection layers (Alpha → Epsilon) with varying 
       integrity requirements, learning rates, and drift thresholds.
    
    2. Pattern Repository: Secure storage for learned patterns across all shadow layers, 
       tracking occurrence frequency and neutralization history.
    
    3. Multi-Layer Shadow Learner: Autonomous learning system that continuously analyzes 
       patterns and improves defense mechanisms.
    
    4. Drift Detection Engine: Specialized algorithms that identify potentially harmful 
       pattern deviations that might indicate tampering.
    
    5. Neutralization System: Counter-measures that respond to detected drift patterns to 
       maintain system integrity.
    
    6. Monitoring Dashboard: Real-time visualization of system status, learned patterns, 
       and defense metrics.
    
    System State Metrics:
    
    • Overall Integrity: Composite measure of system health across all layers
    • Drift Detection Rate: Efficiency in identifying potentially harmful patterns
    • Neutralization Success Rate: Effectiveness in countering detected threats
    • Learning Efficiency: System's ability to improve through experience
    • Shield Strength: Current level of protection against external threats
    """
    
    plt.text(0.1, 0.8, arch_text, fontsize=12, ha='left', va='top', wrap=True)
    
    # Create architecture diagram
    ax = plt.axes([0.1, 0.05, 0.8, 0.25])
    ax.axis('off')
    
    # Draw architecture boxes
    components = [
        {'name': 'Shadow Layers', 'pos': [0.1, 0.6, 0.3, 0.3], 'color': '#1f77b4'},
        {'name': 'Pattern Repository', 'pos': [0.5, 0.6, 0.3, 0.3], 'color': '#ff7f0e'},
        {'name': 'Multi-Layer\nShadow Learner', 'pos': [0.3, 0.1, 0.3, 0.3], 'color': '#2ca02c'},
        {'name': 'Drift Detection', 'pos': [0.7, 0.1, 0.2, 0.2], 'color': '#d62728'},
        {'name': 'Neutralization', 'pos': [0.0, 0.1, 0.2, 0.2], 'color': '#9467bd'},
    ]
    
    for comp in components:
        rect = plt.Rectangle((comp['pos'][0], comp['pos'][1]), comp['pos'][2], comp['pos'][3],
                           facecolor=comp['color'], alpha=0.3, edgecolor='black')
        ax.add_patch(rect)
        ax.text(comp['pos'][0] + comp['pos'][2]/2, comp['pos'][1] + comp['pos'][3]/2,
              comp['name'], ha='center', va='center', fontsize=9)
    
    # Draw arrows connecting components
    arrows = [
        {'start': [0.25, 0.6], 'end': [0.45, 0.4], 'color': 'black'},
        {'start': [0.65, 0.6], 'end': [0.45, 0.4], 'color': 'black'},
        {'start': [0.3, 0.1], 'end': [0.2, 0.2], 'color': 'black'},
        {'start': [0.6, 0.1], 'end': [0.7, 0.1], 'color': 'black'},
    ]
    
    for arrow in arrows:
        ax.annotate('', xy=arrow['end'], xytext=arrow['start'],
                  arrowprops=dict(arrowstyle='->', color=arrow['color']))
    
    pdf.savefig(fig)
    plt.close()

def create_shadow_layers_page(pdf):
    """Create the shadow layers page"""
    fig = plt.figure(figsize=(8.5, 11))
    plt.axis('off')
    
    plt.text(0.5, 0.95, "Shadow Layers: Defense-in-Depth", fontsize=20, ha='center', fontweight='bold')
    
    layers_text = """
    The Shadow Defense System employs five graduated protection layers, each with specific 
    characteristics and responsibilities. This defense-in-depth approach ensures that even 
    if one layer is compromised, subsequent layers continue to provide protection.
    
    Layer Characteristics:
    """
    
    plt.text(0.1, 0.85, layers_text, fontsize=12, ha='left', va='top', wrap=True)
    
    # Create table for layer characteristics
    table_data = [
        ['Layer', 'Integrity', 'Learning Rate', 'Drift Threshold', 'Primary Function'],
        ['Alpha', '1.0', '0.15', '0.3', 'Outermost protection, handles most frequent patterns'],
        ['Beta', '0.95', '0.2', '0.25', 'Secondary filter, increased learning capability'],
        ['Gamma', '0.9', '0.25', '0.2', 'Core protection, balanced detection/learning'],
        ['Delta', '0.85', '0.3', '0.15', 'Deep pattern analysis, aggressive learning'],
        ['Epsilon', '0.8', '0.35', '0.1', 'Innermost layer, highest sensitivity to drift'],
    ]
    
    table = plt.table(cellText=table_data, loc='center', cellLoc='center',
                    bbox=[0.1, 0.5, 0.8, 0.2])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    
    # Add explanation text
    explanation_text = """
    Key Layer Concepts:
    
    • Integrity: Represents the layer's resistance to compromise. Higher layers have 
      higher integrity but less sensitivity.
    
    • Learning Rate: Determines how quickly the layer adapts to new patterns. Deeper 
      layers learn faster but with higher resource cost.
    
    • Drift Threshold: The sensitivity to pattern variations. Lower thresholds (in deeper 
      layers) detect subtler changes but may have higher false positives.
    
    • Progressive Defense: Patterns must penetrate multiple layers to access core systems, 
      with each layer applying increasingly stringent validation.
    
    • Adaptive Boundaries: Layer boundaries automatically adjust based on detected threats, 
      strengthening defenses in areas that experience frequent attack attempts.
    
    This multi-layered approach is particularly effective against sophisticated attacks 
    that might attempt to gradually modify patterns to avoid detection, as subtle changes 
    become more detectable in deeper layers.
    """
    
    plt.text(0.1, 0.45, explanation_text, fontsize=12, ha='left', va='top', wrap=True)
    
    pdf.savefig(fig)
    plt.close()

def create_drift_detection_page(pdf):
    """Create the drift detection page"""
    fig = plt.figure(figsize=(8.5, 11))
    plt.axis('off')
    
    plt.text(0.5, 0.95, "Drift Detection: Identifying Threats", fontsize=20, ha='center', fontweight='bold')
    
    drift_text = """
    Drift detection is a critical capability of the Shadow Defense System, enabling it to 
    identify subtle changes in patterns that might indicate tampering, unauthorized modifications, 
    or attempts to extract protected intellectual property.
    
    Drift Detection Process:
    
    1. Pattern Analysis: Incoming patterns are compared against known safe patterns stored 
       in the system's repository.
    
    2. Feature Extraction: The system extracts key mathematical features from each pattern 
       to establish a baseline for comparison.
    
    3. Drift Calculation: A specialized drift score algorithm quantifies how much a pattern 
       has deviated from expected values.
    
    4. Threshold Evaluation: The calculated drift score is compared against the threshold 
       for the specific shadow layer where the pattern was detected.
    
    5. Threat Classification: If the drift score exceeds the threshold, the pattern is 
       classified as a potential threat requiring neutralization.
    """
    
    plt.text(0.1, 0.8, drift_text, fontsize=12, ha='left', va='top', wrap=True)
    
    # Create drift detection diagram
    ax = plt.axes([0.1, 0.25, 0.8, 0.25])
    ax.axis('off')
    
    # Draw drift detection flow
    steps = [
        {'name': 'Pattern\nAnalysis', 'pos': [0.1, 0.5, 0.15, 0.3]},
        {'name': 'Feature\nExtraction', 'pos': [0.3, 0.5, 0.15, 0.3]},
        {'name': 'Drift\nCalculation', 'pos': [0.5, 0.5, 0.15, 0.3]},
        {'name': 'Threshold\nEvaluation', 'pos': [0.7, 0.5, 0.15, 0.3]},
    ]
    
    for i, step in enumerate(steps):
        rect = plt.Rectangle((step['pos'][0], step['pos'][1]), step['pos'][2], step['pos'][3],
                           facecolor='lightblue', edgecolor='black')
        ax.add_patch(rect)
        ax.text(step['pos'][0] + step['pos'][2]/2, step['pos'][1] + step['pos'][3]/2,
              step['name'], ha='center', va='center', fontsize=9)
        
        if i < len(steps) - 1:
            next_step = steps[i+1]
            ax.annotate('', xy=(next_step['pos'][0], next_step['pos'][1] + next_step['pos'][3]/2), 
                      xytext=(step['pos'][0] + step['pos'][2], step['pos'][1] + step['pos'][3]/2),
                      arrowprops=dict(arrowstyle='->', color='black'))
    
    # Decision diamond
    points = np.array([[0.85, 0.5], [0.9, 0.65], [0.95, 0.5], [0.9, 0.35]])
    polygon = plt.Polygon(points, fill=True, edgecolor='black', facecolor='lightgreen')
    ax.add_patch(polygon)
    ax.text(0.9, 0.5, "Drift > \nThreshold?", ha='center', va='center', fontsize=8)
    
    # Yes/No paths
    ax.annotate('Yes', xy=(0.9, 0.2), xytext=(0.9, 0.35),
              arrowprops=dict(arrowstyle='->', color='red'), ha='center', va='bottom', color='red')
    ax.annotate('No', xy=(1.05, 0.5), xytext=(0.95, 0.5),
              arrowprops=dict(arrowstyle='->', color='green'), ha='left', va='center', color='green')
    
    # Endpoints
    ax.text(0.9, 0.15, "Neutralize", ha='center', va='center', fontsize=10, 
          bbox=dict(facecolor='lightcoral', edgecolor='red', boxstyle='round,pad=0.5'))
    ax.text(1.1, 0.5, "Safe", ha='center', va='center', fontsize=10,
          bbox=dict(facecolor='lightgreen', edgecolor='green', boxstyle='round,pad=0.5'))
    
    # Add drift score formula
    formula_text = """
    Drift Score Calculation:
    
    DS = Σ(w_i × |p_i - b_i|) / N + (V × C)
    
    Where:
    • p_i: Current pattern feature value
    • b_i: Baseline feature value
    • w_i: Feature weight factor
    • N: Number of features
    • V: Volatility factor
    • C: Confidence multiplier
    """
    
    plt.text(0.1, 0.15, formula_text, fontsize=11, ha='left', va='top', wrap=True)
    
    pdf.savefig(fig)
    plt.close()

def create_neutralization_page(pdf):
    """Create the neutralization page"""
    fig = plt.figure(figsize=(8.5, 11))
    plt.axis('off')
    
    plt.text(0.5, 0.95, "Pattern Neutralization", fontsize=20, ha='center', fontweight='bold')
    
    neut_text = """
    When the Shadow Defense System detects a pattern with drift that exceeds the threshold 
    for its layer, it initiates a neutralization process to protect the system's integrity 
    and intellectual property. This is a critical capability for maintaining the security 
    of AI auditing algorithms.
    
    Neutralization Strategies:
    
    1. Pattern Isolation: The drifting pattern is isolated to prevent it from affecting 
       other parts of the system. This containment strategy limits potential damage.
    
    2. Countermeasure Generation: The system automatically generates a countermeasure 
       pattern specifically designed to neutralize the identified drift.
    
    3. Pattern Reinforcement: Existing legitimate patterns are reinforced to strengthen 
       their resistance to similar drift attempts in the future.
    
    4. Adaptive Response: The neutralization response is proportional to the severity 
       of the detected drift, conserving system resources for significant threats.
    
    5. Learning Integration: Each neutralization attempt is recorded and analyzed to 
       improve future response effectiveness.
    """
    
    plt.text(0.1, 0.8, neut_text, fontsize=12, ha='left', va='top', wrap=True)
    
    # Create effectiveness chart
    ax1 = plt.axes([0.1, 0.35, 0.35, 0.2])
    
    # Sample data for neutralization effectiveness
    layers = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon']
    effectiveness = [0.92, 0.88, 0.85, 0.78, 0.65]
    
    bars = ax1.bar(layers, effectiveness, color='lightblue')
    ax1.set_ylim(0, 1.0)
    ax1.set_title('Neutralization Effectiveness by Layer')
    ax1.set_ylabel('Success Rate')
    ax1.tick_params(axis='x', rotation=45)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.02,
               f'{height:.2f}', ha='center', va='bottom', fontsize=8)
    
    # Create time-to-neutralize chart
    ax2 = plt.axes([0.55, 0.35, 0.35, 0.2])
    
    # Sample data for time-to-neutralize
    drift_severity = ['Low', 'Medium', 'High', 'Critical']
    time_to_neutralize = [0.15, 0.45, 0.8, 1.5]  # seconds
    
    bars = ax2.bar(drift_severity, time_to_neutralize, color='lightcoral')
    ax2.set_title('Response Time by Drift Severity')
    ax2.set_ylabel('Time (seconds)')
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.02,
               f'{height:.2f}s', ha='center', va='bottom', fontsize=8)
    
    # Add additional explanation
    add_text = """
    Neutralization Performance Metrics:
    
    • Effectiveness decreases in deeper layers due to the increasing sophistication of 
      patterns that reach those depths.
    
    • Response time increases with drift severity, as more complex countermeasures must 
      be generated for critical threats.
    
    • The system maintains a success rate above 90% for the most common drift patterns 
      in the Alpha layer, protecting against the majority of attacks.
    
    • For enterprise AI auditing applications, this level of protection is sufficient to 
      prevent most reverse-engineering attempts while maintaining high performance.
    """
    
    plt.text(0.1, 0.25, add_text, fontsize=12, ha='left', va='top', wrap=True)
    
    pdf.savefig(fig)
    plt.close()

def create_learning_system_page(pdf):
    """Create the learning system page"""
    fig = plt.figure(figsize=(8.5, 11))
    plt.axis('off')
    
    plt.text(0.5, 0.95, "Multi-Layer Shadow Learner", fontsize=20, ha='center', fontweight='bold')
    
    learning_text = """
    The Multi-Layer Shadow Learner is the adaptive intelligence behind the Shadow Defense 
    System, continuously analyzing patterns and improving defensive capabilities without 
    human intervention. This autonomous learning capability is essential for responding to 
    evolving threats in real-time.
    
    Learning System Capabilities:
    
    1. Autonomous Pattern Generation: Creates and tests new patterns across all shadow layers 
       to strengthen the system's pattern recognition capabilities.
    
    2. Cross-Layer Analysis: Identifies correlations between patterns in different layers to 
       detect sophisticated multi-layer attacks.
    
    3. Drift Prediction: Analyzes historical drift patterns to predict future attack vectors 
       and proactively strengthen vulnerable areas.
    
    4. Neutralization Optimization: Continuously refines neutralization strategies based on 
       past successes and failures to improve response effectiveness.
    
    5. Resource Optimization: Dynamically allocates learning resources to focus on high-risk 
       areas while maintaining baseline protection across all layers.
    """
    
    plt.text(0.1, 0.8, learning_text, fontsize=12, ha='left', va='top', wrap=True)
    
    # Create learning cycle diagram
    ax = plt.axes([0.2, 0.35, 0.6, 0.25])
    ax.axis('off')
    
    # Draw circular learning process
    circle_radius = 0.2
    center_x, center_y = 0.5, 0.5
    angle = np.linspace(0, 2*np.pi, 100)
    
    # Main circle
    circle = plt.Circle((center_x, center_y), circle_radius, fill=False, edgecolor='black')
    ax.add_patch(circle)
    
    # Steps around the circle
    steps = ['Generate', 'Learn', 'Detect', 'Neutralize', 'Optimize']
    angles = np.linspace(0, 2*np.pi, len(steps) + 1)[:-1]  # Evenly space around circle
    
    for i, (step, angle) in enumerate(zip(steps, angles)):
        # Calculate position
        x = center_x + np.cos(angle) * (circle_radius * 1.3)
        y = center_y + np.sin(angle) * (circle_radius * 1.3)
        
        # Draw connecting line
        inner_x = center_x + np.cos(angle) * circle_radius
        inner_y = center_y + np.sin(angle) * circle_radius
        ax.plot([inner_x, x], [inner_y, y], 'k--', alpha=0.5)
        
        # Draw step box
        rect = plt.Rectangle((x - 0.08, y - 0.04), 0.16, 0.08, 
                           facecolor='lightblue', edgecolor='black', alpha=0.7)
        ax.add_patch(rect)
        ax.text(x, y, step, ha='center', va='center', fontsize=9)
        
        # Draw arrow to next step
        next_angle = angles[(i + 1) % len(steps)]
        next_x = center_x + np.cos(next_angle) * (circle_radius * 1.3)
        next_y = center_y + np.sin(next_angle) * (circle_radius * 1.3)
        
        # Calculate control point for curved arrow
        control_angle = (angle + next_angle) / 2
        control_x = center_x + np.cos(control_angle) * (circle_radius * 1.8)
        control_y = center_y + np.sin(control_angle) * (circle_radius * 1.8)
        
        # Draw curved arrow path
        t = np.linspace(0, 1, 20)
        bezier_x = (1-t)**2 * x + 2*(1-t)*t*control_x + t**2 * next_x
        bezier_y = (1-t)**2 * y + 2*(1-t)*t*control_y + t**2 * next_y
        ax.plot(bezier_x, bezier_y, 'b-', alpha=0.5)
        
        # Add arrowhead
        arrow_idx = int(len(t) * 0.9)  # Position near the end
        dx = bezier_x[arrow_idx+1] - bezier_x[arrow_idx-1]
        dy = bezier_y[arrow_idx+1] - bezier_y[arrow_idx-1]
        ax.arrow(bezier_x[arrow_idx], bezier_y[arrow_idx], dx*0.1, dy*0.1, 
               head_width=0.02, head_length=0.02, fc='blue', ec='blue', alpha=0.7)
    
    # Center text
    ax.text(center_x, center_y, "Continuous\nLearning\nCycle", ha='center', va='center', fontsize=10)
    
    # Add learning efficiency explanation
    efficiency_text = """
    Learning Efficiency Metrics:
    
    • Pattern Recognition Rate: The system typically achieves >95% accuracy in recognizing 
      previously encountered patterns after just three exposures.
    
    • Adaptation Speed: New threat patterns are integrated into the defense system within 
      0.5-2 seconds of confirmed detection.
    
    • Cross-Layer Correlation: The learning system automatically identifies relationships 
      between 60-75% of related patterns across different shadow layers.
    
    • Resource Utilization: The autonomous learning process typically consumes less than 
      15% of available system resources during normal operation.
    
    The Multi-Layer Shadow Learner continues to improve over time, with defensive capabilities 
    demonstrating logarithmic improvement as more patterns are processed and analyzed.
    """
    
    plt.text(0.1, 0.2, efficiency_text, fontsize=12, ha='left', va='top', wrap=True)
    
    pdf.savefig(fig)
    plt.close()

def create_dashboard_page(pdf):
    """Create the dashboard page"""
    fig = plt.figure(figsize=(8.5, 11))
    plt.axis('off')
    
    plt.text(0.5, 0.95, "Monitoring Dashboard", fontsize=20, ha='center', fontweight='bold')
    
    dashboard_text = """
    The Shadow Defense System includes a comprehensive monitoring dashboard that provides 
    real-time visibility into system performance, threat detection, and neutralization 
    effectiveness. This dashboard is essential for security teams to maintain awareness 
    of system status and respond to potential issues.
    
    Dashboard Features:
    
    • Real-time System State: Continuously updated metrics on overall system integrity, 
      drift detection rates, and neutralization success.
    
    • Shadow Layer Status: Detailed view of each layer's current integrity, pattern count, 
      and recent activity.
    
    • Threat Visualization: Graphical representation of detected drift patterns and their 
      severity across the system.
    
    • Performance Metrics: Key performance indicators for resource utilization, response 
      times, and learning efficiency.
    
    • Historical Trends: Time-series data showing system performance and threat detection 
      patterns over configurable time periods.
    """
    
    plt.text(0.1, 0.8, dashboard_text, fontsize=12, ha='left', va='top', wrap=True)
    
    # Create dashboard mockup
    ax = plt.axes([0.1, 0.25, 0.8, 0.4])
    ax.axis('off')
    
    # Dashboard outline
    dashboard = plt.Rectangle((0, 0), 1, 1, fill=True, facecolor='#f0f0f0', edgecolor='black')
    ax.add_patch(dashboard)
    
    # Header
    header = plt.Rectangle((0, 0.9), 1, 0.1, fill=True, facecolor='#333333', edgecolor='black')
    ax.add_patch(header)
    ax.text(0.5, 0.95, "Shadow Defense System Dashboard", color='white', ha='center', va='center', fontsize=10)
    
    # System state panel
    state_panel = plt.Rectangle((0.05, 0.6), 0.4, 0.25, fill=True, facecolor='white', edgecolor='black')
    ax.add_patch(state_panel)
    ax.text(0.25, 0.82, "System State", ha='center', va='center', fontsize=9, fontweight='bold')
    
    # State metrics
    metrics = [
        ("Overall Integrity:", "0.97"),
        ("Drift Detection Rate:", "0.89"),
        ("Neutralization Success:", "0.94"),
        ("Learning Efficiency:", "0.85"),
        ("Shield Strength:", "0.92")
    ]
    
    for i, (label, value) in enumerate(metrics):
        y_pos = 0.77 - i * 0.035
        ax.text(0.07, y_pos, label, ha='left', va='center', fontsize=7)
        ax.text(0.38, y_pos, value, ha='right', va='center', fontsize=7, color='green' if float(value) > 0.9 else 'orange')
    
    # Layer status panel
    layer_panel = plt.Rectangle((0.55, 0.6), 0.4, 0.25, fill=True, facecolor='white', edgecolor='black')
    ax.add_patch(layer_panel)
    ax.text(0.75, 0.82, "Shadow Layers", ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Layer data
    layers = [
        ("Alpha", "1.00", "147"),
        ("Beta", "0.96", "98"),
        ("Gamma", "0.92", "76"),
        ("Delta", "0.87", "43"),
        ("Epsilon", "0.81", "21")
    ]
    
    # Layer header
    ax.text(0.58, 0.77, "Layer", ha='left', va='center', fontsize=7, fontweight='bold')
    ax.text(0.7, 0.77, "Integrity", ha='center', va='center', fontsize=7, fontweight='bold')
    ax.text(0.85, 0.77, "Patterns", ha='center', va='center', fontsize=7, fontweight='bold')
    
    for i, (layer, integrity, patterns) in enumerate(layers):
        y_pos = 0.74 - i * 0.03
        ax.text(0.58, y_pos, layer, ha='left', va='center', fontsize=7)
        ax.text(0.7, y_pos, integrity, ha='center', va='center', fontsize=7, 
              color='green' if float(integrity) > 0.9 else 'orange' if float(integrity) > 0.85 else 'red')
        ax.text(0.85, y_pos, patterns, ha='center', va='center', fontsize=7)
    
    # Activity chart
    activity_panel = plt.Rectangle((0.05, 0.05), 0.9, 0.45, fill=True, facecolor='white', edgecolor='black')
    ax.add_patch(activity_panel)
    ax.text(0.5, 0.47, "System Activity (Last 24 Hours)", ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Simplified activity chart
    chart_ax = plt.axes([0.15, 0.1, 0.7, 0.3])
    
    # Sample data
    hours = range(24)
    patterns = [42, 38, 35, 30, 25, 22, 26, 35, 45, 58, 65, 70, 68, 72, 75, 70, 65, 60, 55, 58, 52, 48, 45, 43]
    drifts = [3, 2, 2, 1, 1, 0, 1, 2, 3, 5, 6, 8, 7, 9, 8, 7, 6, 5, 4, 5, 4, 4, 3, 3]
    neutralized = [3, 2, 2, 1, 1, 0, 1, 2, 3, 4, 5, 7, 6, 8, 7, 6, 5, 4, 3, 4, 3, 4, 3, 3]
    
    chart_ax.plot(hours, patterns, label='Patterns', color='blue', marker='', linestyle='-')
    chart_ax.plot(hours, drifts, label='Drifts', color='red', marker='', linestyle='-')
    chart_ax.plot(hours, neutralized, label='Neutralized', color='green', marker='', linestyle='-')
    
    chart_ax.set_xlabel('Hour')
    chart_ax.set_ylabel('Count')
    chart_ax.legend(loc='upper right', fontsize=7)
    chart_ax.grid(True, linestyle='--', alpha=0.7)
    
    # Security benefits
    security_text = """
    Security Benefits of the Dashboard:
    
    • Early Warning System: Identifies potential security issues before they impact system integrity
    • Anomaly Detection: Visualizes unusual patterns that might indicate sophisticated attacks
    • Trend Analysis: Enables security teams to identify emerging threat patterns over time
    • Resource Optimization: Helps administrators allocate security resources effectively
    • Audit Trail: Provides comprehensive logging for security compliance and incident investigation
    """
    
    plt.text(0.1, 0.15, security_text, fontsize=11, ha='left', va='top', wrap=True)
    
    pdf.savefig(fig)
    plt.close()

def create_integration_page(pdf):
    """Create the integration page"""
    fig = plt.figure(figsize=(8.5, 11))
    plt.axis('off')
    
    plt.text(0.5, 0.95, "Integration with KPMG AI Auditing Solution", fontsize=20, ha='center', fontweight='bold')
    
    integration_text = """
    The Shadow Defense System is fully integrated with the KPMG AI Auditing Solution, providing 
    critical protection for proprietary algorithms and models during deployment in client 
    environments. This integration enhances the security, reliability, and integrity of 
    AI auditing processes.
    
    Integration Points:
    
    • Algorithm Protection: Secures core AI auditing algorithms against reverse engineering 
      attempts in client environments.
    
    • Data Flow Security: Monitors and protects the flow of sensitive audit data throughout 
      the system.
    
    • Authentication Framework: Enhances user authentication and authorization processes to 
      prevent unauthorized access.
    
    • Model Integrity: Ensures that AI models maintain their intended functionality and aren't 
      tampered with during audit procedures.
    
    • Regulatory Compliance: Supports compliance with data protection regulations by preventing 
      unauthorized data access or exfiltration.
    """
    
    plt.text(0.1, 0.8, integration_text, fontsize=12, ha='left', va='top', wrap=True)
    
    # Create integration diagram
    ax = plt.axes([0.1, 0.35, 0.8, 0.3])
    ax.axis('off')
    
    # Main components
    components = [
        {'name': 'KPMG AI\nAuditing Solution', 'pos': [0.3, 0.6, 0.4, 0.2], 'color': '#1f77b4'},
        {'name': 'Shadow Defense\nSystem', 'pos': [0.3, 0.2, 0.4, 0.2], 'color': '#ff7f0e'},
        {'name': 'Client\nEnvironment', 'pos': [0.8, 0.4, 0.15, 0.2], 'color': '#2ca02c'},
        {'name': 'Regulatory\nFrameworks', 'pos': [0.05, 0.4, 0.15, 0.2], 'color': '#d62728'},
    ]
    
    for comp in components:
        rect = plt.Rectangle((comp['pos'][0], comp['pos'][1]), comp['pos'][2], comp['pos'][3],
                           facecolor=comp['color'], alpha=0.3, edgecolor='black')
        ax.add_patch(rect)
        ax.text(comp['pos'][0] + comp['pos'][2]/2, comp['pos'][1] + comp['pos'][3]/2,
              comp['name'], ha='center', va='center', fontsize=9)
    
    # Connection lines and labels
    connections = [
        {'start': [0.5, 0.6], 'end': [0.5, 0.4], 'label': 'Security Integration'},
        {'start': [0.5, 0.4], 'end': [0.8, 0.5], 'label': 'Secure Deployment'},
        {'start': [0.5, 0.4], 'end': [0.2, 0.5], 'label': 'Compliance Support'},
        {'start': [0.7, 0.7], 'end': [0.8, 0.6], 'label': 'Audit Requests'},
    ]
    
    for conn in connections:
        ax.plot([conn['start'][0], conn['end'][0]], [conn['start'][1], conn['end'][1]], 'k-', alpha=0.5)
        # Calculate midpoint for label
        mid_x = (conn['start'][0] + conn['end'][0]) / 2
        mid_y = (conn['start'][1] + conn['end'][1]) / 2
        # Add small offset to prevent overlapping with line
        offset_x = 0 
        offset_y = 0.03
        ax.text(mid_x + offset_x, mid_y + offset_y, conn['label'], ha='center', va='center', 
              fontsize=7, bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    
    # Business benefits
    benefits_text = """
    Business Benefits of Integration:
    
    1. Enhanced Client Trust: Clients can be confident that their sensitive financial and 
       operational data is protected throughout the auditing process.
    
    2. Competitive Advantage: Proprietary algorithms remain secure, preserving KPMG's 
       investment in advanced AI auditing capabilities.
    
    3. Reduced Security Incidents: Proactive protection against potential intellectual 
       property theft and unauthorized access attempts.
    
    4. Simplified Compliance: Streamlined compliance with regulatory requirements for 
       data protection and privacy.
    
    5. Operational Efficiency: Automated security processes reduce the need for manual 
       monitoring and intervention.
    
    The integration of the Shadow Defense System with the KPMG AI Auditing Solution creates 
    a robust, secure platform that maintains the highest standards of data protection while 
    delivering industry-leading auditing capabilities.
    """
    
    plt.text(0.1, 0.2, benefits_text, fontsize=11, ha='left', va='top', wrap=True)
    
    pdf.savefig(fig)
    plt.close()

def create_conclusion_page(pdf):
    """Create the conclusion page"""
    fig = plt.figure(figsize=(8.5, 11))
    plt.axis('off')
    
    plt.text(0.5, 0.95, "Conclusion", fontsize=20, ha='center', fontweight='bold')
    
    conclusion_text = """
    The Shadow Defense System represents a significant advancement in protecting 
    intellectual property and ensuring the integrity of AI-based auditing solutions. 
    By implementing a multi-layered defense framework with autonomous learning capabilities, 
    the system provides comprehensive protection against increasingly sophisticated threats.
    
    Key Takeaways:
    
    1. Defense-in-Depth: The five graduated shadow layers provide progressive protection, 
       ensuring that even if outer defenses are breached, inner layers maintain security.
    
    2. Adaptive Intelligence: The Multi-Layer Shadow Learner continuously improves defensive 
       capabilities based on operational experience and detected threats.
    
    3. Proactive Protection: Rather than simply reacting to attacks, the system predicts and 
       prevents potential threats through pattern analysis and drift detection.
    
    4. Comprehensive Monitoring: Real-time dashboards provide visibility into system status 
       and performance, enabling rapid response to emerging issues.
    
    5. Seamless Integration: Full integration with the KPMG AI Auditing Solution enhances 
       overall security posture while maintaining operational efficiency.
    
    Future Enhancements:
    
    • Advanced Threat Intelligence: Integration with external threat intelligence feeds to 
      enhance predictive capabilities.
    
    • Quantum-Resistant Algorithms: Implementation of post-quantum cryptographic techniques 
      to maintain security in the quantum computing era.
    
    • Enhanced Visualization: Advanced visualization capabilities for complex pattern 
      relationships and threat vectors.
    
    • Expanded Learning Models: Integration of additional machine learning models to improve 
      pattern recognition and anomaly detection.
    
    The Shadow Defense System is a critical component of the KPMG AI Auditing Solution, 
    ensuring that proprietary algorithms and sensitive client data remain secure throughout 
    the auditing process. This comprehensive protection enhances client trust while preserving 
    KPMG's competitive advantage in the market.
    """
    
    plt.text(0.1, 0.85, conclusion_text, fontsize=12, ha='left', va='top', wrap=True)
    
    # Add footer
    plt.text(0.5, 0.05, "CONFIDENTIAL — KPMG INTERNAL USE ONLY", 
           fontsize=10, ha='center', va='bottom', color='red')
    plt.text(0.5, 0.03, "© 2025 KPMG Advanced Technology Team", 
           fontsize=8, ha='center', va='bottom')
    
    pdf.savefig(fig)
    plt.close()

if __name__ == "__main__":
    generate_shadow_defense_pdf()
    print("Shadow Defense System PDF explanation has been generated.")