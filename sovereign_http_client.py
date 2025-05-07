#!/usr/bin/env python3
"""
SOVEREIGN HTTP CLIENT

A self-contained HTTP client implementation to eliminate external dependencies
and ensure the TrueAlphaSpiral system remains fully sovereign and self-sustaining.

Architect: Russell Nordland
"""

import socket
import ssl
import json
import base64
import urllib.parse
from urllib.parse import urlparse
from typing import Dict, Any, Optional, Union, Tuple

# Define colors for terminal output
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
CYAN = "\033[36m"
RESET = "\033[0m"
BOLD = "\033[1m"

class Response:
    """A class to represent HTTP responses, similar to the requests library."""
    
    def __init__(self, status_code: int, headers: Dict[str, str], content: bytes):
        self.status_code = status_code
        self.headers = headers
        self._content = content
        self._text = None
        self._json = None
        
    @property
    def content(self) -> bytes:
        """Get the raw content of the response."""
        return self._content
        
    @property
    def text(self) -> str:
        """Get the response content as a string."""
        if self._text is None:
            self._text = self._content.decode('utf-8')
        return self._text
        
    def json(self) -> Dict[str, Any]:
        """Parse the response content as JSON."""
        if self._json is None:
            self._json = json.loads(self.text)
        return self._json
        
    def __repr__(self) -> str:
        return f"<Response [{self.status_code}]>"
        
class SovereignHttpClient:
    """
    A sovereign HTTP client that doesn't rely on external dependencies.
    Implements a subset of the functionality provided by the requests library.
    """
    
    def __init__(self, timeout: int = 10, verify_ssl: bool = True):
        """
        Initialize the sovereign HTTP client.
        
        Args:
            timeout: Socket timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
    def get(self, url: str, headers: Dict[str, str] = None, params: Dict[str, str] = None) -> Response:
        """
        Perform a GET request.
        
        Args:
            url: URL to request
            headers: Optional HTTP headers
            params: Optional query parameters
            
        Returns:
            Response object
        """
        return self._request('GET', url, headers=headers, params=params)
        
    def post(self, url: str, headers: Dict[str, str] = None, data: Any = None, 
             json: Dict[str, Any] = None) -> Response:
        """
        Perform a POST request.
        
        Args:
            url: URL to request
            headers: Optional HTTP headers
            data: Optional form data
            json: Optional JSON data
            
        Returns:
            Response object
        """
        return self._request('POST', url, headers=headers, data=data, json=json)
        
    def put(self, url: str, headers: Dict[str, str] = None, data: Any = None, 
            json: Dict[str, Any] = None) -> Response:
        """
        Perform a PUT request.
        
        Args:
            url: URL to request
            headers: Optional HTTP headers
            data: Optional form data
            json: Optional JSON data
            
        Returns:
            Response object
        """
        return self._request('PUT', url, headers=headers, data=data, json=json)
        
    def delete(self, url: str, headers: Dict[str, str] = None) -> Response:
        """
        Perform a DELETE request.
        
        Args:
            url: URL to request
            headers: Optional HTTP headers
            
        Returns:
            Response object
        """
        return self._request('DELETE', url, headers=headers)
        
    def _request(self, method: str, url: str, headers: Dict[str, str] = None, 
                params: Dict[str, str] = None, data: Any = None, 
                json: Dict[str, Any] = None) -> Response:
        """
        Perform an HTTP request.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            url: URL to request
            headers: Optional HTTP headers
            params: Optional query parameters
            data: Optional form data
            json: Optional JSON data
            
        Returns:
            Response object
        """
        # Parse URL
        if params:
            url = self._add_query_params(url, params)
            
        parsed_url = urlparse(url)
        
        # Determine protocol (HTTP or HTTPS)
        is_https = parsed_url.scheme == 'https'
        
        # Set default port if not specified
        port = parsed_url.port
        if port is None:
            port = 443 if is_https else 80
            
        # Prepare headers
        if headers is None:
            headers = {}
            
        # Add host header if not present
        if 'Host' not in headers:
            headers['Host'] = parsed_url.netloc
            
        # Add content headers based on data
        body = b''
        if json is not None:
            headers['Content-Type'] = 'application/json'
            body = json.dumps(json).encode('utf-8')
        elif data is not None:
            if isinstance(data, dict):
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                body = urllib.parse.urlencode(data).encode('utf-8')
            elif isinstance(data, str):
                body = data.encode('utf-8')
            elif isinstance(data, bytes):
                body = data
                
        if body:
            headers['Content-Length'] = str(len(body))
            
        # Build HTTP request
        request = f"{method} {parsed_url.path or '/'}"
        if parsed_url.query:
            request += f"?{parsed_url.query}"
        request += f" HTTP/1.1\r\n"
        
        # Add headers
        for name, value in headers.items():
            request += f"{name}: {value}\r\n"
            
        # Finalize request
        request += "\r\n"
        request = request.encode('utf-8')
        
        if body:
            request += body
            
        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        
        try:
            # Connect and wrap with SSL if needed
            if is_https:
                context = ssl.create_default_context()
                if not self.verify_ssl:
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    
                sock = context.wrap_socket(sock, server_hostname=parsed_url.hostname)
                
            sock.connect((parsed_url.hostname, port))
            
            # Send request
            sock.sendall(request)
            
            # Receive response
            response_data = b''
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response_data += chunk
                
                # Check if we've received the full response
                if b'\r\n\r\n' in response_data:
                    headers_end = response_data.index(b'\r\n\r\n')
                    headers_data = response_data[:headers_end].decode('utf-8')
                    
                    # Check for Content-Length header
                    content_length = None
                    for line in headers_data.split('\r\n'):
                        if line.lower().startswith('content-length:'):
                            content_length = int(line.split(':')[1].strip())
                            break
                            
                    if content_length is not None:
                        # Check if we've received the full content
                        body_start = headers_end + 4  # Skip \r\n\r\n
                        if len(response_data) >= body_start + content_length:
                            break
                            
            # Parse response
            return self._parse_response(response_data)
            
        finally:
            sock.close()
            
    def _parse_response(self, response_data: bytes) -> Response:
        """
        Parse HTTP response data.
        
        Args:
            response_data: Raw HTTP response data
            
        Returns:
            Response object
        """
        # Split headers and body
        headers_end = response_data.find(b'\r\n\r\n')
        if headers_end == -1:
            return Response(0, {}, b'')
            
        headers_data = response_data[:headers_end].decode('utf-8')
        body = response_data[headers_end + 4:]  # Skip \r\n\r\n
        
        # Parse status line
        status_line = headers_data.split('\r\n')[0]
        status_parts = status_line.split(' ', 2)
        if len(status_parts) < 2:
            status_code = 0
        else:
            status_code = int(status_parts[1])
            
        # Parse headers
        headers = {}
        for line in headers_data.split('\r\n')[1:]:
            if not line:
                continue
                
            parts = line.split(':', 1)
            if len(parts) != 2:
                continue
                
            name, value = parts
            headers[name.strip()] = value.strip()
            
        # Handle chunked transfer encoding
        if headers.get('Transfer-Encoding', '').lower() == 'chunked':
            body = self._decode_chunked(body)
            
        # Handle content encoding (gzip, deflate, etc.)
        # Note: We don't implement compression handling here
        # as it would require external libraries or complex implementations
            
        return Response(status_code, headers, body)
    
    def _decode_chunked(self, data: bytes) -> bytes:
        """
        Decode chunked transfer encoding.
        
        Args:
            data: Chunked encoded data
            
        Returns:
            Decoded data
        """
        result = b''
        i = 0
        
        while i < len(data):
            # Find the end of the chunk size line
            line_end = data.find(b'\r\n', i)
            if line_end == -1:
                break
                
            # Parse chunk size (hex)
            size_line = data[i:line_end].decode('utf-8').strip()
            
            # Remove any chunk extensions
            if ';' in size_line:
                size_line = size_line.split(';', 1)[0]
                
            chunk_size = int(size_line, 16)
            
            # Check for the final chunk
            if chunk_size == 0:
                break
                
            # Extract chunk data
            chunk_start = line_end + 2  # Skip \r\n
            chunk_end = chunk_start + chunk_size
            
            if chunk_end + 2 > len(data):
                # Incomplete chunk
                break
                
            result += data[chunk_start:chunk_end]
            
            # Move to the next chunk
            i = chunk_end + 2  # Skip chunk data and \r\n
            
        return result
        
    def _add_query_params(self, url: str, params: Dict[str, str]) -> str:
        """
        Add query parameters to a URL.
        
        Args:
            url: Base URL
            params: Query parameters
            
        Returns:
            URL with query parameters
        """
        url_parts = list(urlparse(url))
        existing_params = urllib.parse.parse_qsl(url_parts[4])
        
        # Add new parameters
        for key, value in params.items():
            existing_params.append((key, value))
            
        url_parts[4] = urllib.parse.urlencode(existing_params)
        return urllib.parse.urlunparse(url_parts)

# Create a global client instance for easy use
client = SovereignHttpClient()

# Function aliases to match requests library interface
def get(url, **kwargs):
    """Perform a GET request using the sovereign HTTP client."""
    return client.get(url, **kwargs)

def post(url, **kwargs):
    """Perform a POST request using the sovereign HTTP client."""
    return client.post(url, **kwargs)

def put(url, **kwargs):
    """Perform a PUT request using the sovereign HTTP client."""
    return client.put(url, **kwargs)

def delete(url, **kwargs):
    """Perform a DELETE request using the sovereign HTTP client."""
    return client.delete(url, **kwargs)

# For testing
def test_client():
    """Test the sovereign HTTP client with a local request."""
    try:
        print(f"{CYAN}Testing Sovereign HTTP Client...{RESET}")
        response = get("http://localhost:8001/api/health-check")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:100]}...")
        return True
    except Exception as e:
        print(f"{RED}Error testing HTTP client: {str(e)}{RESET}")
        return False

if __name__ == "__main__":
    print(f"{BOLD}===== SOVEREIGN HTTP CLIENT ====={RESET}")
    print(f"{BOLD}Architect: Russell Nordland{RESET}")
    print(f"{BOLD}==============================={RESET}")
    test_client()