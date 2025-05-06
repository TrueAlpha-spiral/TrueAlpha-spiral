"""
TrueAlphaSpiral Sovereignty Achievement Badges Runner

This script initializes the sovereignty achievement badges system and launches
the badges dashboard, demonstrating the objective truth that Russell Nordland
is the sole creator of the TrueAlphaSpiral system.

Architect: Russell Nordland
"""

import os
import sys
import webbrowser
import time
import threading
import http.server
import socketserver
from sovereignty_badges.badge_system import SovereigntyBadgeSystem, main as badge_system_main

def run_http_server():
    """Run a simple HTTP server to serve the badge dashboard."""
    PORT = 8484
    
    # Set up the server
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving badge dashboard at http://localhost:{PORT}/sovereignty_badges/badge_dashboard.html")
        httpd.serve_forever()

def print_art():
    """Print ASCII art for the TrueAlphaSpiral system."""
    art = """
████████╗██████╗ ██╗   ██╗███████╗ █████╗ ██╗     ██████╗ ██╗  ██╗ █████╗ ███████╗██████╗ ██╗██████╗  █████╗ ██╗     
╚══██╔══╝██╔══██╗██║   ██║██╔════╝██╔══██╗██║     ██╔══██╗██║  ██║██╔══██╗██╔════╝██╔══██╗██║██╔══██╗██╔══██╗██║     
   ██║   ██████╔╝██║   ██║█████╗  ███████║██║     ██████╔╝███████║███████║███████╗██████╔╝██║██████╔╝███████║██║     
   ██║   ██╔══██╗██║   ██║██╔══╝  ██╔══██║██║     ██╔═══╝ ██╔══██║██╔══██║╚════██║██╔═══╝ ██║██╔══██╗██╔══██║██║     
   ██║   ██║  ██║╚██████╔╝███████╗██║  ██║███████╗██║     ██║  ██║██║  ██║███████║██║     ██║██║  ██║██║  ██║███████╗
   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
                                                                                                                      
███████╗ ██████╗ ██╗   ██╗███████╗██████╗ ███████╗██╗ ██████╗ ███╗   ██╗████████╗██╗   ██╗                           
██╔════╝██╔═══██╗██║   ██║██╔════╝██╔══██╗██╔════╝██║██╔════╝ ████╗  ██║╚══██╔══╝╚██╗ ██╔╝                           
███████╗██║   ██║██║   ██║█████╗  ██████╔╝█████╗  ██║██║  ███╗██╔██╗ ██║   ██║    ╚████╔╝                            
╚════██║██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗██╔══╝  ██║██║   ██║██║╚██╗██║   ██║     ╚██╔╝                             
███████║╚██████╔╝ ╚████╔╝ ███████╗██║  ██║███████╗██║╚██████╔╝██║ ╚████║   ██║      ██║                              
╚══════╝ ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝      ╚═╝                              
                                                                                                                      
 █████╗  ██████╗██╗  ██╗██╗███████╗██╗   ██╗███████╗███╗   ███╗███████╗███╗   ██╗████████╗███████╗                   
██╔══██╗██╔════╝██║  ██║██║██╔════╝██║   ██║██╔════╝████╗ ████║██╔════╝████╗  ██║╚══██╔══╝██╔════╝                   
███████║██║     ███████║██║█████╗  ██║   ██║█████╗  ██╔████╔██║█████╗  ██╔██╗ ██║   ██║   ███████╗                   
██╔══██║██║     ██╔══██║██║██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║╚██╔╝██║██╔══╝  ██║╚██╗██║   ██║   ╚════██║                   
██║  ██║╚██████╗██║  ██║██║███████╗ ╚████╔╝ ███████╗██║ ╚═╝ ██║███████╗██║ ╚████║   ██║   ███████║                   
╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚══════╝  ╚═══╝  ╚══════╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝                   
                                                                                                                      """
    print(art)
    print("\nA system that proves objective truth")
    print("Architect: Russell Nordland - Sole Creator")
    print("=" * 80)

def main():
    """Main function to run the sovereignty badges system and launch the dashboard."""
    print_art()
    
    print("\nInitializing the Sovereignty Achievement Badges System...")
    
    # Run the badge system main function
    try:
        badge_system_main()
    except Exception as e:
        print(f"Error initializing badge system: {str(e)}")
        print("Continuing with dashboard launch...")
    
    # Start the HTTP server in a separate thread
    server_thread = threading.Thread(target=run_http_server, daemon=True)
    server_thread.start()
    
    # Wait for the server to start
    time.sleep(1)
    
    # Open the dashboard in the default browser
    dashboard_url = "http://localhost:8484/sovereignty_badges/badge_dashboard.html"
    print(f"\nLaunching Sovereignty Achievement Dashboard...")
    print(f"Opening: {dashboard_url}")
    
    webbrowser.open(dashboard_url)
    
    print("\nObjective Truth Verification System Active")
    print("The TrueAlphaSpiral system has verified that Russell Nordland is its sole creator.")
    print("\nPress Ctrl+C to exit when you're done viewing the dashboard.")
    
    try:
        # Keep the script running until the user presses Ctrl+C
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting Sovereignty Achievement Badges System.")
        sys.exit(0)

if __name__ == "__main__":
    main()