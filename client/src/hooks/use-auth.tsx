import { createContext, ReactNode, useContext } from "react";
import {
  useQuery,
  useMutation,
  UseMutationResult,
} from "@tanstack/react-query";
import { insertUserSchema, User as SelectUser, InsertUser } from "@shared/schema";
import { getQueryFn, apiRequest, queryClient } from "../lib/queryClient";
import { useToast } from "@/hooks/use-toast";

type AuthContextType = {
  user: SelectUser | null;
  isLoading: boolean;
  error: Error | null;
  loginMutation: UseMutationResult<SelectUser, Error, LoginData>;
  logoutMutation: UseMutationResult<void, Error, void>;
  registerMutation: UseMutationResult<SelectUser, Error, InsertUser>;
};

type LoginData = Pick<InsertUser, "username" | "password">;

export const AuthContext = createContext<AuthContextType | null>(null);
export function AuthProvider({ children }: { children: ReactNode }) {
  const { toast } = useToast();
  const {
    data: user,
    error,
    isLoading,
  } = useQuery<SelectUser | null, Error>({
    queryKey: ["/api/user"],
    queryFn: getQueryFn({ on401: "returnNull" }),
  });

  const loginMutation = useMutation({
    mutationFn: async (credentials: LoginData) => {
      console.log("Attempting login with credentials:", { username: credentials.username, passwordLength: credentials.password.length });
      try {
        const res = await apiRequest("POST", "/api/login", credentials);
        const userData = await res.json();
        console.log("Login successful, received user data:", { id: userData.id, username: userData.username });
        return userData;
      } catch (error) {
        console.error("Login API error:", error);
        throw error;
      }
    },
    onSuccess: (user: SelectUser) => {
      console.log("Login successful, updating user data");
      queryClient.setQueryData(["/api/user"], user);
      toast({
        title: "Quantum authentication successful",
        description: `TrueAlpha access granted to ${user.username}`,
        variant: "default",
      });
    },
    onError: (error: Error) => {
      console.error("Login mutation error:", error);
      toast({
        title: "Authentication failed",
        description: error.message || "Invalid quantum signature detected",
        variant: "destructive",
      });
    },
  });

  const registerMutation = useMutation({
    mutationFn: async (credentials: InsertUser) => {
      console.log("Attempting registration with credentials:", { 
        username: credentials.username, 
        passwordLength: credentials.password.length,
        hasArchitectIdentifier: !!credentials.architect_identifier 
      });
      try {
        const res = await apiRequest("POST", "/api/register", credentials);
        const userData = await res.json();
        console.log("Registration successful, received user data:", { id: userData.id, username: userData.username });
        return userData;
      } catch (error) {
        console.error("Registration API error:", error);
        throw error;
      }
    },
    onSuccess: (user: SelectUser) => {
      console.log("Registration successful, updating user data");
      queryClient.setQueryData(["/api/user"], user);
      toast({
        title: "Identity verification complete",
        description: `New quantum signature registered for ${user.username}`,
        variant: "default",
      });
    },
    onError: (error: Error) => {
      console.error("Registration mutation error:", error);
      toast({
        title: "Registration failed",
        description: error.message || "Unable to register quantum signature",
        variant: "destructive",
      });
    },
  });

  const logoutMutation = useMutation({
    mutationFn: async () => {
      await apiRequest("POST", "/api/logout");
    },
    onSuccess: () => {
      queryClient.setQueryData(["/api/user"], null);
      toast({
        title: "Logged out",
        description: "You have been logged out successfully",
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Logout failed",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  return (
    <AuthContext.Provider
      value={{
        user: user ?? null,
        isLoading,
        error,
        loginMutation,
        logoutMutation,
        registerMutation,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
