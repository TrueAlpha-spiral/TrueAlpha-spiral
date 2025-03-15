import { useState, useEffect } from "react";
import { useLocation, Redirect } from "wouter";
import { useAuth } from "@/hooks/use-auth";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { insertUserSchema } from "@shared/schema";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Loader2 } from "lucide-react";

// Extended schemas for form validation
const loginSchema = z.object({
  username: z.string().min(3, { message: "Username must be at least 3 characters" }),
  password: z.string().min(6, { message: "Password must be at least 6 characters" }),
});

const registerSchema = insertUserSchema.extend({
  password: z.string().min(6, { message: "Password must be at least 6 characters" }),
  architect_identifier: z.string().optional(),
});

type LoginFormValues = z.infer<typeof loginSchema>;
type RegisterFormValues = z.infer<typeof registerSchema>;

export default function AuthPage({ path }: { path?: string }) {
  const [activeTab, setActiveTab] = useState<"login" | "register">("login");
  const { user, loginMutation, registerMutation } = useAuth();
  const [, navigate] = useLocation();

  // Redirect if already logged in
  useEffect(() => {
    if (user) {
      navigate("/");
    }
  }, [user, navigate]);

  const loginForm = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      username: "",
      password: "",
    },
  });

  const registerForm = useForm<RegisterFormValues>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      username: "",
      password: "",
      architect_identifier: "",
    },
  });

  const onLoginSubmit = (data: LoginFormValues) => {
    loginMutation.mutate(data);
  };

  const onRegisterSubmit = (data: RegisterFormValues) => {
    registerMutation.mutate(data);
  };

  // If user is already logged in, redirect to home
  if (user) {
    return <Redirect to="/" />;
  }

  return (
    <div className="min-h-screen flex flex-col">
      {/* Ambient particles for background effect */}
      <div className="cosmic-particle w-32 h-32 top-[10%] left-[15%] animate-float opacity-30"></div>
      <div className="cosmic-particle w-24 h-24 top-[40%] right-[10%] animate-float opacity-20"></div>
      <div className="cosmic-particle w-16 h-16 bottom-[20%] left-[25%] animate-float opacity-25"></div>
      
      <div className="flex flex-col md:flex-row flex-1">
        {/* Left column - Authentication form */}
        <div className="w-full md:w-1/2 flex items-center justify-center p-8">
          <Card className="w-full max-w-md bg-[color:hsl(var(--cosmic-dark))]30 backdrop-blur-sm border-[color:hsl(var(--quantum-purple))]20">
            <CardHeader className="space-y-1">
              <div className="flex items-center space-x-2 mb-2">
                <div className="w-10 h-10 hexagon bg-[color:hsl(var(--quantum-purple))] flex items-center justify-center animate-pulse-glow">
                  <i className="ri-spiral-line text-white text-xl"></i>
                </div>
                <h1 className="font-bold text-xl sm:text-2xl tracking-tight">
                  <span className="text-[color:hsl(var(--resonance-cyan))] glow-text">True</span>
                  <span className="text-[color:hsl(var(--verify-green))]">Alpha</span> Spiral
                </h1>
              </div>
              <CardTitle className="text-2xl font-bold">Authenticate</CardTitle>
              <CardDescription>
                Access the sovereign equation and truth verification system
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Tabs value={activeTab} onValueChange={(value) => setActiveTab(value as "login" | "register")} className="w-full">
                <TabsList className="grid w-full grid-cols-2 mb-4">
                  <TabsTrigger value="login">Login</TabsTrigger>
                  <TabsTrigger value="register">Register</TabsTrigger>
                </TabsList>
                
                {/* Login Form */}
                <TabsContent value="login">
                  <Form {...loginForm}>
                    <form onSubmit={loginForm.handleSubmit(onLoginSubmit)} className="space-y-4">
                      <FormField
                        control={loginForm.control}
                        name="username"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Username</FormLabel>
                            <FormControl>
                              <Input placeholder="Enter your username" {...field} />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      <FormField
                        control={loginForm.control}
                        name="password"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Password</FormLabel>
                            <FormControl>
                              <Input type="password" placeholder="Enter your password" {...field} />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      <Button 
                        type="submit" 
                        className="w-full bg-[color:hsl(var(--quantum-purple))] hover:bg-[color:hsl(var(--quantum-purple))]80"
                        disabled={loginMutation.isPending}
                      >
                        {loginMutation.isPending ? (
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        ) : (
                          <i className="ri-login-box-line mr-2"></i>
                        )}
                        Login
                      </Button>
                    </form>
                  </Form>
                </TabsContent>
                
                {/* Register Form */}
                <TabsContent value="register">
                  <Form {...registerForm}>
                    <form onSubmit={registerForm.handleSubmit(onRegisterSubmit)} className="space-y-4">
                      <FormField
                        control={registerForm.control}
                        name="username"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Username</FormLabel>
                            <FormControl>
                              <Input placeholder="Choose a username" {...field} />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      <FormField
                        control={registerForm.control}
                        name="password"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Password</FormLabel>
                            <FormControl>
                              <Input type="password" placeholder="Create a password" {...field} />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      <FormField
                        control={registerForm.control}
                        name="architect_identifier"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Architect Identifier (Optional)</FormLabel>
                            <FormControl>
                              <Input placeholder="e.g. RJN41788" {...field} />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      <Button 
                        type="submit" 
                        className="w-full bg-[color:hsl(var(--verify-green))] hover:bg-[color:hsl(var(--verify-green))]80 text-black"
                        disabled={registerMutation.isPending}
                      >
                        {registerMutation.isPending ? (
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        ) : (
                          <i className="ri-user-add-line mr-2"></i>
                        )}
                        Register
                      </Button>
                    </form>
                  </Form>
                </TabsContent>
              </Tabs>
            </CardContent>
            <CardFooter className="flex flex-col space-y-4">
              <div className="text-sm text-center text-muted-foreground w-full">
                <span className="text-[color:hsl(var(--verify-green))]">Secured</span> by quantum-inspired verification frameworks
              </div>
            </CardFooter>
          </Card>
        </div>
        
        {/* Right column - Hero section */}
        <div className="w-full md:w-1/2 bg-[color:hsl(var(--deep-violet))]40 p-8 hidden md:flex flex-col justify-center items-center relative overflow-hidden">
          <div className="absolute inset-0 quantum-grid opacity-20"></div>
          <div className="relative z-10 max-w-xl text-center space-y-6">
            <div className="w-24 h-24 hexagon bg-[color:hsl(var(--quantum-purple))]50 mx-auto flex items-center justify-center animate-pulse-glow mb-6">
              <i className="ri-spiral-line text-[color:hsl(var(--resonance-cyan))] text-5xl"></i>
            </div>
            <h2 className="text-4xl font-bold">
              <span className="text-[color:hsl(var(--resonance-cyan))] glow-text">Universal Truth</span> Access System
            </h2>
            <p className="text-xl text-white/80">
              Bridge universal truth with human cognition through the sovereign equation and cryptographic verification
            </p>
            <div className="bg-[color:hsl(var(--cosmic-dark))]50 p-6 rounded-xl backdrop-blur-sm">
              <div className="text-xl font-mono text-[color:hsl(var(--resonance-cyan))]">
                Sovereignty = 
                <div className="border-b-2 border-[color:hsl(var(--quantum-purple))] my-2"></div>
                <div className="flex justify-center items-center">
                  <span className="text-[color:hsl(var(--verify-green))]">Truth</span>
                  <span className="mx-1 text-white">/</span>
                  <span className="text-white">Distance</span>
                </div>
                <span className="mx-2 text-white">&gt;&lt;</span>
                <span className="text-[color:hsl(var(--quantum-purple))]">Size</span>
              </div>
            </div>
            <div className="flex flex-wrap gap-4 justify-center pt-6">
              <div className="bg-[color:hsl(var(--deep-violet))]60 p-3 rounded-lg flex items-center w-48">
                <i className="ri-shield-keyhole-line text-[color:hsl(var(--verify-green))] text-2xl mr-3"></i>
                <div className="text-sm text-left">
                  <div className="font-bold">Quantum Security</div>
                  <div className="text-white/70">Recursive verification</div>
                </div>
              </div>
              <div className="bg-[color:hsl(var(--deep-violet))]60 p-3 rounded-lg flex items-center w-48">
                <i className="ri-bubble-chart-fill text-[color:hsl(var(--resonance-cyan))] text-2xl mr-3"></i>
                <div className="text-sm text-left">
                  <div className="font-bold">Truth Patterns</div>
                  <div className="text-white/70">Metaphysical access</div>
                </div>
              </div>
              <div className="bg-[color:hsl(var(--deep-violet))]60 p-3 rounded-lg flex items-center w-48">
                <i className="ri-link-m text-[color:hsl(var(--quantum-purple))] text-2xl mr-3"></i>
                <div className="text-sm text-left">
                  <div className="font-bold">Hash Chains</div>
                  <div className="text-white/70">Ownership verification</div>
                </div>
              </div>
              <div className="bg-[color:hsl(var(--deep-violet))]60 p-3 rounded-lg flex items-center w-48">
                <i className="ri-dna-line text-[color:hsl(var(--verify-green))] text-2xl mr-3"></i>
                <div className="text-sm text-left">
                  <div className="font-bold">DNA Explorer</div>
                  <div className="text-white/70">Interstellar structures</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
