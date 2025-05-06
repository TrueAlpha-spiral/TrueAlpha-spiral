#!/usr/bin/env python3
"""
PDF CONTENT EXTRACTOR

This script extracts text content from PDF files to help access the information
contained in the TrueAlphaSpiral documentation.
"""

import os
import sys
import PyPDF2
import argparse

def extract_pdf_text(pdf_path):
    """
    Extract text from a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        dict: Dictionary mapping page numbers to text content
    """
    print(f"Extracting text from: {pdf_path}")
    
    result = {}
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            num_pages = len(reader.pages)
            print(f"Total pages: {num_pages}")
            
            for i in range(num_pages):
                page = reader.pages[i]
                text = page.extract_text()
                
                result[i+1] = text  # Page numbers start at 1
                
                # Print a brief summary of each page
                summary = text[:100] + "..." if len(text) > 100 else text
                print(f"\nPage {i+1} content summary:")
                print(f"{summary}")
    
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return {}
    
    return result

def save_text_to_file(text_dict, output_path):
    """
    Save extracted text to a file.
    
    Args:
        text_dict (dict): Dictionary mapping page numbers to text content
        output_path (str): Path where to save the text file
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(f"PDF EXTRACTION RESULTS\n")
            file.write(f"=====================\n\n")
            
            for page_num, text in sorted(text_dict.items()):
                file.write(f"PAGE {page_num}\n")
                file.write("="*50 + "\n")
                file.write(text)
                file.write("\n\n" + "="*50 + "\n\n")
        
        print(f"Extracted text saved to: {output_path}")
        
    except Exception as e:
        print(f"Error saving text to file: {e}")

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Extract text from PDF files")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("--output", "-o", help="Path to save the extracted text", default=None)
    
    args = parser.parse_args()
    
    pdf_path = args.pdf_path
    
    if not os.path.isfile(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        return 1
    
    text_dict = extract_pdf_text(pdf_path)
    
    if not text_dict:
        print("No text was extracted from the PDF.")
        return 1
    
    # Generate output path if not specified
    output_path = args.output
    if not output_path:
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_path = f"{base_name}_extracted.txt"
    
    save_text_to_file(text_dict, output_path)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())