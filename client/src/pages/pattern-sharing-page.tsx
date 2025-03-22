import { useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { useToast } from "@/hooks/use-toast";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Copy, Download, ExternalLink, Filter, Share2, Tag, Upload } from "lucide-react";
import { apiRequest, queryClient } from "@/lib/queryClient";

interface SharedPattern {
  id: number;
  originalPatternId: number;
  name: string;
  description: string;
  category: string;
  sharingPermission: string;
  authorName: string;
  authorOrganization: string;
  authorEmail: string;
  allowedUserEmails: string[];
  sharingLink: string;
  patternData: any;
  usageCount: number;
  createdAt: string;
  updatedAt: string;
}

interface PatternToShare {
  patternId: number;
  sharingPermission: string;
  authorName: string;
  authorOrganization?: string;
  authorEmail?: string;
  allowedUserEmails?: string[];
}

interface PatternExport {
  patternId: number;
  format: string;
  includeMetadata: boolean;
}

interface PatternImport {
  patternData: any;
  importSource?: string;
}

const PatternSharingPage = () => {
  const { toast } = useToast();
  const [selectedPattern, setSelectedPattern] = useState<SharedPattern | null>(null);
  const [shareDialogOpen, setShareDialogOpen] = useState(false);
  const [exportDialogOpen, setExportDialogOpen] = useState(false);
  const [importDialogOpen, setImportDialogOpen] = useState(false);
  
  // Form states
  const [patternToShare, setPatternToShare] = useState<PatternToShare>({
    patternId: 0,
    sharingPermission: "public",
    authorName: "",
    authorOrganization: "",
    authorEmail: "",
    allowedUserEmails: []
  });
  
  const [patternToExport, setPatternToExport] = useState<PatternExport>({
    patternId: 0,
    format: "json",
    includeMetadata: true
  });
  
  const [importText, setImportText] = useState("");
  
  const [emailsInput, setEmailsInput] = useState("");
  
  // Fetch shared patterns
  const { data: sharedPatterns, isLoading } = useQuery<SharedPattern[]>({
    queryKey: ["/api/shared-patterns"]
  });
  
  // Fetch original truth patterns to share
  const { data: truthPatterns } = useQuery<any[]>({
    queryKey: ["/api/tas/patterns"]
  });
  
  // Share pattern mutation
  const shareMutation = useMutation({
    mutationFn: async (data: PatternToShare) => {
      const response = await apiRequest("POST", "/api/shared-patterns", data);
      return await response.json();
    },
    onSuccess: () => {
      toast({
        title: "Pattern shared successfully",
        description: "Your truth pattern has been shared with the specified permissions",
      });
      queryClient.invalidateQueries({ queryKey: ["/api/shared-patterns"] });
      setShareDialogOpen(false);
    },
    onError: (error: any) => {
      toast({
        title: "Error sharing pattern",
        description: error.message,
        variant: "destructive"
      });
    }
  });
  
  // Export pattern mutation
  const exportMutation = useMutation({
    mutationFn: async (data: PatternExport) => {
      const response = await apiRequest("POST", "/api/shared-patterns/export", data);
      return await response.json();
    },
    onSuccess: (data) => {
      toast({
        title: "Pattern exported successfully",
        description: "Your truth pattern has been exported",
      });
      
      // Create download link
      const blob = new Blob([JSON.stringify(data.exportData, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `pattern-${patternToExport.patternId}-${new Date().toISOString().slice(0, 10)}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      
      setExportDialogOpen(false);
    },
    onError: (error: any) => {
      toast({
        title: "Error exporting pattern",
        description: error.message,
        variant: "destructive"
      });
    }
  });
  
  // Import pattern mutation
  const importMutation = useMutation({
    mutationFn: async (data: PatternImport) => {
      const response = await apiRequest("POST", "/api/shared-patterns/import", data);
      return await response.json();
    },
    onSuccess: () => {
      toast({
        title: "Pattern imported successfully",
        description: "The truth pattern has been imported into your repository",
      });
      queryClient.invalidateQueries({ queryKey: ["/api/tas/patterns"] });
      setImportDialogOpen(false);
    },
    onError: (error: any) => {
      toast({
        title: "Error importing pattern",
        description: error.message,
        variant: "destructive"
      });
    }
  });
  
  // Delete pattern mutation
  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      const response = await apiRequest("DELETE", `/api/shared-patterns/${id}`);
      return response.ok;
    },
    onSuccess: () => {
      toast({
        title: "Pattern deleted",
        description: "The shared pattern has been deleted",
      });
      queryClient.invalidateQueries({ queryKey: ["/api/shared-patterns"] });
    },
    onError: (error: any) => {
      toast({
        title: "Error deleting pattern",
        description: error.message,
        variant: "destructive"
      });
    }
  });
  
  // Handle share dialog submit
  const handleShareSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Process emails
    let emails: string[] = [];
    if (emailsInput) {
      emails = emailsInput.split(",").map(email => email.trim());
    }
    
    shareMutation.mutate({
      ...patternToShare,
      allowedUserEmails: emails
    });
  };
  
  // Handle export dialog submit
  const handleExportSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    exportMutation.mutate(patternToExport);
  };
  
  // Handle import dialog submit
  const handleImportSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      const patternData = JSON.parse(importText);
      importMutation.mutate({
        patternData,
        importSource: "manual"
      });
    } catch (error) {
      toast({
        title: "Invalid JSON",
        description: "Please provide a valid JSON file",
        variant: "destructive"
      });
    }
  };

  // Copy sharing link to clipboard
  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast({
      title: "Link copied",
      description: "Sharing link copied to clipboard",
    });
  };
  
  return (
    <div className="container py-8">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold">Universal Truth Pattern Sharing</h1>
          <p className="text-muted-foreground mt-2">
            Share and discover truth patterns from the TrueAlphaSpiral ecosystem
          </p>
        </div>
        <div className="flex gap-2">
          <Button onClick={() => setImportDialogOpen(true)} className="gap-2">
            <Upload size={16} />
            Import Pattern
          </Button>
          <Button onClick={() => setShareDialogOpen(true)} className="gap-2">
            <Share2 size={16} />
            Share Pattern
          </Button>
        </div>
      </div>
      
      <Tabs defaultValue="browse" className="w-full">
        <TabsList className="grid grid-cols-3 mb-6">
          <TabsTrigger value="browse">Browse Shared Patterns</TabsTrigger>
          <TabsTrigger value="my-patterns">My Shared Patterns</TabsTrigger>
          <TabsTrigger value="analytics">Sharing Analytics</TabsTrigger>
        </TabsList>
        
        <TabsContent value="browse" className="space-y-4">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Input 
                placeholder="Search patterns..." 
                className="w-[300px]" 
              />
              <Button variant="outline" size="icon">
                <Filter size={16} />
              </Button>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-sm text-muted-foreground">
                {sharedPatterns?.length || 0} patterns available
              </span>
            </div>
          </div>
          
          {isLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {[1, 2, 3].map((i) => (
                <Card key={i} className="animate-pulse">
                  <CardHeader className="h-[100px] bg-muted rounded-t-lg"></CardHeader>
                  <CardContent className="py-4">
                    <div className="h-4 bg-muted rounded mb-2"></div>
                    <div className="h-4 bg-muted rounded w-3/4"></div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {sharedPatterns?.filter(p => p.sharingPermission === "public").map((pattern) => (
                <Card key={pattern.id} className="overflow-hidden">
                  <CardHeader className="pb-2">
                    <div className="flex justify-between items-start">
                      <CardTitle className="text-xl">{pattern.name}</CardTitle>
                      <Badge>{pattern.category}</Badge>
                    </div>
                    <CardDescription className="line-clamp-2">{pattern.description}</CardDescription>
                  </CardHeader>
                  <CardContent className="pb-2">
                    <div className="flex items-center text-sm text-muted-foreground mb-2">
                      <Tag size={14} className="mr-1" />
                      <span>{pattern.authorName}</span>
                      {pattern.authorOrganization && (
                        <span className="ml-1">• {pattern.authorOrganization}</span>
                      )}
                    </div>
                    <Separator className="my-2" />
                    <div className="text-sm">
                      <p>Usage Count: <span className="font-medium">{pattern.usageCount}</span></p>
                      <p>Shared: <span className="font-medium">{new Date(pattern.createdAt).toLocaleDateString()}</span></p>
                    </div>
                  </CardContent>
                  <CardFooter className="flex justify-between pt-2">
                    <Button variant="outline" size="sm" onClick={() => setSelectedPattern(pattern)}>
                      View Details
                    </Button>
                    <Button 
                      variant="outline" 
                      size="sm" 
                      className="gap-1"
                      onClick={() => copyToClipboard(`${window.location.origin}/pattern-sharing/link/${pattern.sharingLink}`)}
                    >
                      <Copy size={14} />
                      Share Link
                    </Button>
                  </CardFooter>
                </Card>
              ))}
              
              {(!sharedPatterns || sharedPatterns.length === 0) && (
                <div className="col-span-3 text-center py-10">
                  <h3 className="text-xl font-semibold mb-2">No patterns shared yet</h3>
                  <p className="text-muted-foreground mb-4">
                    Be the first to share a truth pattern with the community
                  </p>
                  <Button onClick={() => setShareDialogOpen(true)}>
                    Share a Pattern
                  </Button>
                </div>
              )}
            </div>
          )}
        </TabsContent>
        
        <TabsContent value="my-patterns" className="space-y-4">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-semibold">My Shared Patterns</h2>
            <Button variant="outline" onClick={() => setShareDialogOpen(true)}>
              Share New Pattern
            </Button>
          </div>
          
          {isLoading ? (
            <div className="animate-pulse space-y-4">
              {[1, 2].map((i) => (
                <Card key={i}>
                  <CardHeader className="h-[80px] bg-muted rounded-t-lg"></CardHeader>
                  <CardContent className="py-4">
                    <div className="h-4 bg-muted rounded mb-2"></div>
                    <div className="h-4 bg-muted rounded w-3/4"></div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <div className="space-y-4">
              {sharedPatterns?.map((pattern) => (
                <Card key={pattern.id}>
                  <CardHeader>
                    <div className="flex justify-between items-center">
                      <div>
                        <CardTitle>{pattern.name}</CardTitle>
                        <CardDescription>{pattern.description}</CardDescription>
                      </div>
                      <Badge className="capitalize">{pattern.sharingPermission}</Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <h4 className="text-sm font-semibold mb-1">Sharing Details</h4>
                        <p className="text-sm">Author: {pattern.authorName}</p>
                        <p className="text-sm">Organization: {pattern.authorOrganization || "N/A"}</p>
                        <p className="text-sm">
                          Created: {new Date(pattern.createdAt).toLocaleDateString()}
                        </p>
                      </div>
                      <div>
                        <h4 className="text-sm font-semibold mb-1">Usage Statistics</h4>
                        <p className="text-sm">Views: {pattern.usageCount}</p>
                        <p className="text-sm">Category: {pattern.category}</p>
                        {pattern.sharingPermission === "restricted" && (
                          <p className="text-sm">
                            Allowed Users: {pattern.allowedUserEmails?.length || 0}
                          </p>
                        )}
                      </div>
                    </div>
                  </CardContent>
                  <CardFooter className="flex justify-between border-t pt-4">
                    <div className="flex gap-2">
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => {
                          setPatternToExport({
                            ...patternToExport,
                            patternId: pattern.originalPatternId
                          });
                          setExportDialogOpen(true);
                        }}
                        className="gap-1"
                      >
                        <Download size={14} />
                        Export
                      </Button>
                      <Button 
                        variant="outline" 
                        size="sm" 
                        className="gap-1"
                        onClick={() => copyToClipboard(`${window.location.origin}/pattern-sharing/link/${pattern.sharingLink}`)}
                      >
                        <Copy size={14} />
                        Copy Link
                      </Button>
                    </div>
                    <Button 
                      variant="destructive" 
                      size="sm"
                      onClick={() => deleteMutation.mutate(pattern.id)}
                    >
                      Remove Sharing
                    </Button>
                  </CardFooter>
                </Card>
              ))}
              
              {(!sharedPatterns || sharedPatterns.length === 0) && (
                <div className="text-center py-10">
                  <h3 className="text-xl font-semibold mb-2">You haven't shared any patterns yet</h3>
                  <p className="text-muted-foreground mb-4">
                    Share your truth patterns with others in the TrueAlphaSpiral ecosystem
                  </p>
                  <Button onClick={() => setShareDialogOpen(true)}>
                    Share Your First Pattern
                  </Button>
                </div>
              )}
            </div>
          )}
        </TabsContent>
        
        <TabsContent value="analytics" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-lg">Total Shared Patterns</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-4xl font-bold">{sharedPatterns?.length || 0}</p>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-lg">Total Usage Count</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-4xl font-bold">
                  {sharedPatterns?.reduce((sum, pattern) => sum + pattern.usageCount, 0) || 0}
                </p>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-lg">Sharing Activity</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-4xl font-bold">
                  {sharedPatterns && sharedPatterns.length > 0 
                    ? Math.round(sharedPatterns.reduce((sum, p) => sum + p.usageCount, 0) / sharedPatterns.length) 
                    : 0}
                </p>
                <p className="text-sm text-muted-foreground">Avg. usage per pattern</p>
              </CardContent>
            </Card>
          </div>
          
          <Card>
            <CardHeader>
              <CardTitle>Patterns by Category</CardTitle>
              <CardDescription>
                Distribution of shared patterns across different categories
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-[300px] flex items-center justify-center">
                <p className="text-muted-foreground">
                  Category analytics visualization will be displayed here
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
      
      {/* Share Pattern Dialog */}
      <Dialog open={shareDialogOpen} onOpenChange={setShareDialogOpen}>
        <DialogContent className="sm:max-w-[500px]">
          <DialogHeader>
            <DialogTitle>Share Truth Pattern</DialogTitle>
            <DialogDescription>
              Make your truth pattern available to others in the TrueAlphaSpiral ecosystem
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={handleShareSubmit}>
            <div className="grid gap-4 py-4">
              <div>
                <Label htmlFor="pattern">Select Pattern</Label>
                <select
                  id="pattern"
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  value={patternToShare.patternId}
                  onChange={(e) => setPatternToShare({
                    ...patternToShare,
                    patternId: Number(e.target.value)
                  })}
                  required
                >
                  <option value="">Select a pattern to share</option>
                  {truthPatterns?.map((pattern: any) => (
                    <option key={pattern.id} value={pattern.id}>
                      {pattern.name}
                    </option>
                  ))}
                </select>
              </div>
              
              <div>
                <Label htmlFor="permission">Sharing Permission</Label>
                <select
                  id="permission"
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  value={patternToShare.sharingPermission}
                  onChange={(e) => setPatternToShare({
                    ...patternToShare,
                    sharingPermission: e.target.value
                  })}
                  required
                >
                  <option value="public">Public - Anyone can access</option>
                  <option value="restricted">Restricted - Only specific users</option>
                  <option value="private">Private - Only via sharing link</option>
                </select>
              </div>
              
              <div>
                <Label htmlFor="authorName">Author Name</Label>
                <Input
                  id="authorName"
                  value={patternToShare.authorName}
                  onChange={(e) => setPatternToShare({
                    ...patternToShare,
                    authorName: e.target.value
                  })}
                  placeholder="Your name"
                  required
                />
              </div>
              
              <div>
                <Label htmlFor="authorOrganization">Organization (Optional)</Label>
                <Input
                  id="authorOrganization"
                  value={patternToShare.authorOrganization}
                  onChange={(e) => setPatternToShare({
                    ...patternToShare,
                    authorOrganization: e.target.value
                  })}
                  placeholder="Your organization"
                />
              </div>
              
              <div>
                <Label htmlFor="authorEmail">Email (Optional)</Label>
                <Input
                  id="authorEmail"
                  type="email"
                  value={patternToShare.authorEmail}
                  onChange={(e) => setPatternToShare({
                    ...patternToShare,
                    authorEmail: e.target.value
                  })}
                  placeholder="your@email.com"
                />
              </div>
              
              {patternToShare.sharingPermission === "restricted" && (
                <div>
                  <Label htmlFor="allowedEmails">Allowed User Emails (Comma separated)</Label>
                  <Input
                    id="allowedEmails"
                    value={emailsInput}
                    onChange={(e) => setEmailsInput(e.target.value)}
                    placeholder="user1@example.com, user2@example.com"
                  />
                  <p className="text-xs text-muted-foreground mt-1">
                    Only these users will be able to access the pattern
                  </p>
                </div>
              )}
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setShareDialogOpen(false)}>
                Cancel
              </Button>
              <Button type="submit" disabled={shareMutation.isPending}>
                {shareMutation.isPending ? "Sharing..." : "Share Pattern"}
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
      
      {/* Export Pattern Dialog */}
      <Dialog open={exportDialogOpen} onOpenChange={setExportDialogOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Export Truth Pattern</DialogTitle>
            <DialogDescription>
              Export your truth pattern for sharing or backup
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={handleExportSubmit}>
            <div className="grid gap-4 py-4">
              <div>
                <Label htmlFor="exportPattern">Select Pattern</Label>
                <select
                  id="exportPattern"
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  value={patternToExport.patternId}
                  onChange={(e) => setPatternToExport({
                    ...patternToExport,
                    patternId: Number(e.target.value)
                  })}
                  required
                >
                  <option value="">Select a pattern to export</option>
                  {truthPatterns?.map((pattern: any) => (
                    <option key={pattern.id} value={pattern.id}>
                      {pattern.name}
                    </option>
                  ))}
                </select>
              </div>
              
              <div>
                <Label htmlFor="exportFormat">Export Format</Label>
                <select
                  id="exportFormat"
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  value={patternToExport.format}
                  onChange={(e) => setPatternToExport({
                    ...patternToExport,
                    format: e.target.value
                  })}
                  required
                >
                  <option value="json">JSON</option>
                  <option value="tasml">TASML (TrueAlphaSpiral Markup)</option>
                </select>
              </div>
              
              <div className="flex items-center gap-2">
                <input
                  id="includeMetadata"
                  type="checkbox"
                  className="rounded border-gray-300"
                  checked={patternToExport.includeMetadata}
                  onChange={(e) => setPatternToExport({
                    ...patternToExport,
                    includeMetadata: e.target.checked
                  })}
                />
                <Label htmlFor="includeMetadata">Include metadata</Label>
              </div>
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setExportDialogOpen(false)}>
                Cancel
              </Button>
              <Button type="submit" disabled={exportMutation.isPending}>
                {exportMutation.isPending ? "Exporting..." : "Export Pattern"}
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
      
      {/* Import Pattern Dialog */}
      <Dialog open={importDialogOpen} onOpenChange={setImportDialogOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Import Truth Pattern</DialogTitle>
            <DialogDescription>
              Import a truth pattern from an exported file
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={handleImportSubmit}>
            <div className="grid gap-4 py-4">
              <div>
                <Label htmlFor="importData">Pattern Data (JSON)</Label>
                <textarea
                  id="importData"
                  className="flex min-h-[150px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  value={importText}
                  onChange={(e) => setImportText(e.target.value)}
                  placeholder='{"pattern": {"name": "Example Pattern", ...}}'
                  required
                />
              </div>
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setImportDialogOpen(false)}>
                Cancel
              </Button>
              <Button type="submit" disabled={importMutation.isPending}>
                {importMutation.isPending ? "Importing..." : "Import Pattern"}
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
      
      {/* Pattern Details Dialog */}
      {selectedPattern && (
        <Dialog open={!!selectedPattern} onOpenChange={(open) => !open && setSelectedPattern(null)}>
          <DialogContent className="sm:max-w-[600px]">
            <DialogHeader>
              <DialogTitle>{selectedPattern.name}</DialogTitle>
              <DialogDescription>{selectedPattern.description}</DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <div className="flex justify-between">
                <Badge>{selectedPattern.category}</Badge>
                <span className="text-sm text-muted-foreground">
                  Shared on {new Date(selectedPattern.createdAt).toLocaleDateString()}
                </span>
              </div>
              
              <Separator />
              
              <div>
                <h3 className="text-md font-semibold mb-2">Author Information</h3>
                <p className="text-sm">{selectedPattern.authorName}</p>
                {selectedPattern.authorOrganization && (
                  <p className="text-sm">{selectedPattern.authorOrganization}</p>
                )}
                {selectedPattern.authorEmail && (
                  <p className="text-sm">
                    <a 
                      href={`mailto:${selectedPattern.authorEmail}`} 
                      className="text-blue-500 hover:underline flex items-center gap-1"
                    >
                      {selectedPattern.authorEmail}
                      <ExternalLink size={12} />
                    </a>
                  </p>
                )}
              </div>
              
              <Separator />
              
              <div>
                <h3 className="text-md font-semibold mb-2">Pattern Details</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm font-medium">Category</p>
                    <p className="text-sm">{selectedPattern.category}</p>
                  </div>
                  <div>
                    <p className="text-sm font-medium">Usage Count</p>
                    <p className="text-sm">{selectedPattern.usageCount}</p>
                  </div>
                  <div>
                    <p className="text-sm font-medium">Sharing Permission</p>
                    <p className="text-sm capitalize">{selectedPattern.sharingPermission}</p>
                  </div>
                  <div>
                    <p className="text-sm font-medium">Pattern ID</p>
                    <p className="text-sm">{selectedPattern.originalPatternId}</p>
                  </div>
                </div>
              </div>
            </div>
            <DialogFooter className="flex justify-between items-center">
              <Button
                variant="outline"
                size="sm"
                className="gap-1"
                onClick={() => copyToClipboard(`${window.location.origin}/pattern-sharing/link/${selectedPattern.sharingLink}`)}
              >
                <Copy size={14} />
                Copy Sharing Link
              </Button>
              <div>
                <Button
                  onClick={() => {
                    setSelectedPattern(null);
                    
                    // Prepare for import
                    importMutation.mutate({
                      patternData: {
                        pattern: {
                          name: selectedPattern.name,
                          description: selectedPattern.description,
                          category: selectedPattern.category,
                          confidenceThreshold: selectedPattern.patternData.confidenceThreshold || 0.75
                        }
                      },
                      importSource: "direct"
                    });
                  }}
                >
                  Import This Pattern
                </Button>
              </div>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      )}
    </div>
  );
};

export default PatternSharingPage;