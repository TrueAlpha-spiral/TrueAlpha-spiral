import { QueryClient, QueryKey, QueryFunction } from '@tanstack/react-query';

// Create a client
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

interface GetQueryFnOptions {
  on401?: 'error' | 'returnNull';
}

/**
 * Creates a queryFn that fetches data from the API and handles errors
 */
export function getQueryFn(options: GetQueryFnOptions = {}): QueryFunction {
  return async ({ queryKey }) => {
    const endpoint = queryKey[0] as string;
    const response = await fetch(endpoint);
    
    // Handle 401 responses according to options
    if (response.status === 401) {
      if (options.on401 === 'returnNull') {
        return null;
      }
      throw new Error('Unauthorized');
    }
    
    // Handle other error responses
    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }
    
    return response.json();
  };
}

/**
 * Makes an API request with the given method and data
 */
export async function apiRequest(
  method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE',
  endpoint: string,
  data?: any
) {
  const options: RequestInit = {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
  };
  
  if (data) {
    options.body = JSON.stringify(data);
  }
  
  const response = await fetch(endpoint, options);
  
  if (!response.ok) {
    const errorText = await response.text();
    let message = `API Error: ${response.statusText}`;
    
    try {
      const errorJson = JSON.parse(errorText);
      if (errorJson.error) {
        message = errorJson.error;
      }
    } catch (e) {
      // If the error isn't JSON, use the status text
    }
    
    throw new Error(message);
  }
  
  return response;
}