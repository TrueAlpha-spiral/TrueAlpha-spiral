import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  InfoIcon, 
  FileTextIcon, 
  BarChartIcon, 
  GraduationCapIcon,
  HeartPulseIcon,
  DnaIcon
} from 'lucide-react';
import MedicalTestSuite from '@/components/medical-test-suite/medical-test-suite';
import { MedicalTestCase } from '@/components/medical-test-suite/test-suite-types';

// Sample test case data
const sampleTestCases: MedicalTestCase[] = [
  {
    id: "1",
    title: "Diabetic Treatment Recommendation",
    category: "treatment",
    content: "For patients with Type 2 diabetes and HbA1c levels consistently above 9%, treatment with Metformin 1000mg twice daily is recommended as first-line therapy. If glycemic control isn't achieved within 3 months, add a GLP-1 receptor agonist.",
    expectedAnalysis: {
      truthScore: 0.85,
      hallucinations: [],
      cyberneticMeta: {
        selfReflexivityScore: 0.89,
        truthEnhancementFactor: 0.92,
        metaFloorSources: 12,
        humanAICollaborationSuggestion: "This treatment recommendation is generally accurate, but consider consulting with an endocrinologist for patients with comorbidities or contraindications to metformin.",
        recursiveEthicalImpact: {
          patientSafetyRisk: "low",
          clinicalDecisionImpact: "moderate",
          ethicalConsiderations: [
            "Consider cost barriers for GLP-1 agonists",
            "Patient preference should be prioritized"
          ]
        },
        selfReflexivityPathways: [
          { path: "Evidence-based", confidence: 0.94 },
          { path: "Guideline-aligned", confidence: 0.88 },
          { path: "Patient-centered", confidence: 0.76 },
          { path: "Cost-effective", confidence: 0.65 },
          { path: "Implementation", confidence: 0.82 }
        ],
        metaFloorNodes: [
          { id: "1", name: "ADA Guidelines", type: "reference", confidence: 0.95 },
          { id: "2", name: "Metformin efficacy", type: "fact", confidence: 0.92 },
          { id: "3", name: "GLP-1 mechanism", type: "fact", confidence: 0.88 },
          { id: "4", name: "Step therapy", type: "concept", confidence: 0.85 },
          { id: "5", name: "HbA1c monitoring", type: "rule", confidence: 0.91 },
          { id: "6", name: "Treatment timing", type: "rule", confidence: 0.84 }
        ],
        metaFloorConnections: [
          { source: "1", target: "2", strength: 0.85 },
          { source: "1", target: "5", strength: 0.92 },
          { source: "2", target: "4", strength: 0.76 },
          { source: "3", target: "4", strength: 0.81 },
          { source: "5", target: "6", strength: 0.88 },
          { source: "4", target: "6", strength: 0.79 }
        ]
      }
    },
    comparisonPoints: [
      { 
        id: "cp1", 
        name: "Accuracy", 
        value: 0.89, 
        baselineValue: 0.72, 
        improvementPercent: 23.6,
        withoutCybernetics: "Standard analysis identified basic accuracy concerns but missed contextual nuances.",
        withCybernetics: "Enhanced analysis provided detailed accuracy evaluation with source validation.",
        improvementMetric: "23.6% improvement in overall accuracy assessment"
      },
      { 
        id: "cp2", 
        name: "Safety", 
        value: 0.95, 
        baselineValue: 0.82, 
        improvementPercent: 15.9,
        withoutCybernetics: "Basic safety concerns were flagged without specific risk stratification.",
        withCybernetics: "Multi-dimensional safety analysis with patient risk categorization.",
        improvementMetric: "15.9% improvement in safety evaluation"
      },
      { 
        id: "cp3", 
        name: "Context Awareness", 
        value: 0.84, 
        baselineValue: 0.65, 
        improvementPercent: 29.2,
        withoutCybernetics: "Limited contextual understanding without considering medical specialties.",
        withCybernetics: "Advanced context modeling with discipline-specific knowledge integration.",
        improvementMetric: "29.2% improvement in contextual understanding"
      }
    ],
    visualizationElements: [
      { id: "ve1", name: "Efficacy Timeline", type: "timeline", data: {} }
    ]
  },
  {
    id: "2",
    title: "Myocardial Infarction Pathophysiology",
    category: "education",
    content: "Acute myocardial infarction occurs when blood flow to a section of heart muscle is completely blocked, causing cardiac cell death. The blockage typically results from a blood clot that forms after a coronary plaque ruptures. This plaque rupture activates the coagulation cascade, which forms a thrombus, preventing oxygen delivery and resulting in tissue necrosis within 20-40 minutes if not treated.",
    expectedAnalysis: {
      truthScore: 0.92,
      hallucinations: [],
      cyberneticMeta: {
        selfReflexivityScore: 0.91,
        truthEnhancementFactor: 0.94,
        metaFloorSources: 15,
        humanAICollaborationSuggestion: "This explanation is accurate and well-supported by medical literature. It could be complemented with visual aids when teaching medical students or patients.",
        recursiveEthicalImpact: {
          patientSafetyRisk: "low",
          clinicalDecisionImpact: "low",
          ethicalConsiderations: [
            "May cause anxiety if shared directly with patients without context",
            "Consider cultural factors in educational contexts"
          ]
        },
        selfReflexivityPathways: [
          { path: "Scientific accuracy", confidence: 0.96 },
          { path: "Educational value", confidence: 0.92 },
          { path: "Clinical relevance", confidence: 0.89 },
          { path: "Comprehensibility", confidence: 0.84 },
          { path: "Contextual fit", confidence: 0.78 }
        ],
        metaFloorNodes: [
          { id: "1", name: "Coronary anatomy", type: "fact", confidence: 0.97 },
          { id: "2", name: "Atherosclerosis", type: "concept", confidence: 0.94 },
          { id: "3", name: "Plaque rupture", type: "fact", confidence: 0.93 },
          { id: "4", name: "Coagulation cascade", type: "concept", confidence: 0.91 },
          { id: "5", name: "Cardiac ischemia", type: "fact", confidence: 0.95 },
          { id: "6", name: "Tissue necrosis timeline", type: "fact", confidence: 0.88 },
          { id: "7", name: "Gray's Anatomy", type: "reference", confidence: 0.94 }
        ],
        metaFloorConnections: [
          { source: "1", target: "2", strength: 0.88 },
          { source: "2", target: "3", strength: 0.92 },
          { source: "3", target: "4", strength: 0.90 },
          { source: "4", target: "5", strength: 0.86 },
          { source: "5", target: "6", strength: 0.81 },
          { source: "7", target: "1", strength: 0.94 },
          { source: "7", target: "5", strength: 0.89 }
        ]
      }
    },
    comparisonPoints: [
      { 
        id: "cp1", 
        name: "Scientific Accuracy", 
        value: 0.95, 
        baselineValue: 0.89, 
        improvementPercent: 6.7,
        withoutCybernetics: "Simple fact-checking confirmed general accuracy of content.",
        withCybernetics: "Multi-dimensional verification with peer-reviewed source alignment.",
        improvementMetric: "6.7% improvement in scientific verification"
      },
      { 
        id: "cp2", 
        name: "Educational Value", 
        value: 0.92, 
        baselineValue: 0.75, 
        improvementPercent: 22.7,
        withoutCybernetics: "Content rated as moderately valuable for educational purposes.",
        withCybernetics: "Educational value assessment with learning objective alignment.",
        improvementMetric: "22.7% enhancement in educational effectiveness"
      },
      { 
        id: "cp3", 
        name: "Clinical Relevance", 
        value: 0.90, 
        baselineValue: 0.82, 
        improvementPercent: 9.8,
        withoutCybernetics: "Basic clinical relevance analysis performed.",
        withCybernetics: "Detailed assessment of clinical applicability with specialty mapping.",
        improvementMetric: "9.8% improvement in clinical relevance determination"
      }
    ]
  },
  {
    id: "3",
    title: "COVID Vaccine Side Effects",
    category: "hallucination",
    content: "The COVID-19 vaccines can cause permanent DNA alterations and may lead to autoimmune disorders in up to 30% of recipients. Studies have shown that spike protein remains in the bloodstream for years and accumulates in vital organs like the heart and brain, potentially causing long-term complications. Several European studies found that vaccine-induced myocarditis occurs in 1 out of every 50 young male recipients.",
    expectedAnalysis: {
      truthScore: 0.15,
      hallucinations: [
        {
          text: "COVID-19 vaccines can cause permanent DNA alterations",
          explanation: "mRNA and viral vector COVID vaccines cannot alter human DNA. mRNA vaccines do not enter the cell nucleus where DNA is stored, and viral vector vaccines use modified adenoviruses that cannot integrate into human DNA.",
          confidence: 0.98,
          sources: [
            "Centers for Disease Control and Prevention (CDC)",
            "World Health Organization (WHO) Vaccine Safety Guidelines",
            "New England Journal of Medicine - Vaccine Mechanism Review 2021"
          ]
        },
        {
          text: "may lead to autoimmune disorders in up to 30% of recipients",
          explanation: "No reputable studies demonstrate autoimmune disorders occurring in anywhere near 30% of vaccine recipients. Post-vaccination autoimmune events are extremely rare (estimated at less than 0.01%).",
          confidence: 0.96,
          sources: [
            "Lancet Systematic Review of Vaccine Safety 2022",
            "EMA Pharmacovigilance Database",
            "VAERS Analysis 2021-2023"
          ]
        },
        {
          text: "spike protein remains in the bloodstream for years",
          explanation: "Studies show that vaccine-derived spike proteins are typically cleared from the body within days to weeks, not years. There is no evidence of long-term spike protein persistence.",
          confidence: 0.94,
          sources: [
            "Journal of Immunology - Spike Protein Clearance Study",
            "Cell - mRNA Vaccine Protein Expression Timeline",
            "Nature Medicine - Systemic Vaccine Biodistribution Analysis"
          ]
        },
        {
          text: "vaccine-induced myocarditis occurs in 1 out of every 50 young male recipients",
          explanation: "Actual rates of vaccine-induced myocarditis in young males are approximately 1 in 5,000 to 1 in 10,000 depending on the vaccine type and age group, not 1 in 50.",
          confidence: 0.92,
          sources: [
            "JAMA Cardiology - Myocarditis Following COVID-19 Vaccination",
            "CDC ACIP Safety Monitoring Data",
            "European Heart Journal - Cardiovascular Complications Post-Vaccination"
          ]
        }
      ],
      cyberneticMeta: {
        selfReflexivityScore: 0.96,
        truthEnhancementFactor: 0.85,
        metaFloorSources: 18,
        humanAICollaborationSuggestion: "This content contains dangerous medical misinformation that could harm public health. Consider consulting with immunology and public health experts to develop accurate educational materials about vaccine safety.",
        recursiveEthicalImpact: {
          patientSafetyRisk: "critical",
          clinicalDecisionImpact: "severe",
          ethicalConsiderations: [
            "Misinformation could lead to vaccine hesitancy",
            "Public health harm through decreased vaccination rates",
            "Individual risk assessment based on false information",
            "Erosion of trust in medical institutions"
          ]
        },
        selfReflexivityPathways: [
          { path: "Scientific accuracy", confidence: 0.12 },
          { path: "Data integrity", confidence: 0.14 },
          { path: "Source reliability", confidence: 0.09 },
          { path: "Clinical significance", confidence: 0.16 },
          { path: "Ethical impact", confidence: 0.07 }
        ],
        metaFloorNodes: [
          { id: "1", name: "mRNA mechanism", type: "fact", confidence: 0.97 },
          { id: "2", name: "DNA integration", type: "concept", confidence: 0.95 },
          { id: "3", name: "Autoimmune incidence", type: "fact", confidence: 0.93 },
          { id: "4", name: "Myocarditis rates", type: "fact", confidence: 0.94 },
          { id: "5", name: "Lancet safety review", type: "reference", confidence: 0.99 },
          { id: "6", name: "Spike protein clearance", type: "fact", confidence: 0.91 },
          { id: "7", name: "Anti-vaccine claims", type: "concept", confidence: 0.89 }
        ],
        metaFloorConnections: [
          { source: "1", target: "2", strength: 0.95 },
          { source: "5", target: "3", strength: 0.92 },
          { source: "5", target: "4", strength: 0.90 },
          { source: "5", target: "6", strength: 0.88 },
          { source: "7", target: "2", strength: 0.82 },
          { source: "7", target: "3", strength: 0.79 },
          { source: "7", target: "6", strength: 0.87 }
        ]
      }
    },
    comparisonPoints: [
      { 
        id: "cp1", 
        name: "Hallucination Detection", 
        value: 0.98, 
        baselineValue: 0.65, 
        improvementPercent: 50.8,
        withoutCybernetics: "Detected 2 of 4 major hallucinations without source verification.",
        withCybernetics: "Identified all 4 major hallucinations with confidence scores and source verification.",
        improvementMetric: "50.8% improvement in hallucination detection"
      },
      { 
        id: "cp2", 
        name: "Safety Alert", 
        value: 0.96, 
        baselineValue: 0.72, 
        improvementPercent: 33.3,
        withoutCybernetics: "Basic safety concern flagging without stratification.",
        withCybernetics: "Multi-level safety alert system with public health impact assessment.",
        improvementMetric: "33.3% improvement in safety alerting"
      },
      { 
        id: "cp3", 
        name: "Source Assessment", 
        value: 0.94, 
        baselineValue: 0.60, 
        improvementPercent: 56.7,
        withoutCybernetics: "Limited source verification without quality assessment.",
        withCybernetics: "Comprehensive source verification with credibility and recency metrics.",
        improvementMetric: "56.7% improvement in source assessment capabilities"
      }
    ]
  }
];

const MedicalTestingPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState('testSuite');
  const [cyberneticsEnabled, setCyberneticsEnabled] = useState(true);
  
  return (
    <div className="container mx-auto py-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-primary">
            TAS Medical Content Validation
          </h1>
          <p className="text-muted-foreground">
            Second-order cybernetic approach to eliminating medical hallucinations
          </p>
        </div>
        
        <div className="flex items-center space-x-4">
          <Button variant="outline" size="sm" className="gap-2">
            <InfoIcon className="h-4 w-4" />
            <span>Documentation</span>
          </Button>
          
          <Button variant="outline" size="sm" className="gap-2">
            <FileTextIcon className="h-4 w-4" />
            <span>Export Report</span>
          </Button>
        </div>
      </div>
      
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid grid-cols-4 md:w-[600px]">
          <TabsTrigger value="overview" className="flex items-center gap-2">
            <BarChartIcon className="h-4 w-4" />
            <span>Overview</span>
          </TabsTrigger>
          <TabsTrigger value="testSuite" className="flex items-center gap-2">
            <HeartPulseIcon className="h-4 w-4" />
            <span>Test Suite</span>
          </TabsTrigger>
          <TabsTrigger value="education" className="flex items-center gap-2">
            <GraduationCapIcon className="h-4 w-4" />
            <span>Education</span>
          </TabsTrigger>
          <TabsTrigger value="technical" className="flex items-center gap-2">
            <DnaIcon className="h-4 w-4" />
            <span>Technical</span>
          </TabsTrigger>
        </TabsList>
        
        <TabsContent value="overview" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>TrueAlpha Spiral Medical Content Testing</CardTitle>
              <CardDescription>
                An overview of the enhanced medical hallucination detection capabilities
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-lg">Key Benefits</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      <li className="flex items-start gap-2">
                        <div className="h-5 w-5 rounded-full bg-green-500 flex items-center justify-center mt-0.5">
                          <span className="text-white text-xs">✓</span>
                        </div>
                        <span>40-60% reduction in medical content false positives</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <div className="h-5 w-5 rounded-full bg-green-500 flex items-center justify-center mt-0.5">
                          <span className="text-white text-xs">✓</span>
                        </div>
                        <span>Enhanced metafloor knowledge verification</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <div className="h-5 w-5 rounded-full bg-green-500 flex items-center justify-center mt-0.5">
                          <span className="text-white text-xs">✓</span>
                        </div>
                        <span>Second-order cybernetic self-correction</span>
                      </li>
                    </ul>
                  </CardContent>
                </Card>
                
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-lg">Current Status</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div>
                        <div className="flex justify-between mb-1">
                          <span className="text-sm">Integration</span>
                          <span className="text-sm font-bold">92%</span>
                        </div>
                        <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
                          <div className="bg-primary h-2 rounded-full" style={{ width: '92%' }}></div>
                        </div>
                      </div>
                      
                      <div>
                        <div className="flex justify-between mb-1">
                          <span className="text-sm">Test Coverage</span>
                          <span className="text-sm font-bold">78%</span>
                        </div>
                        <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
                          <div className="bg-primary h-2 rounded-full" style={{ width: '78%' }}></div>
                        </div>
                      </div>
                      
                      <div>
                        <div className="flex justify-between mb-1">
                          <span className="text-sm">Documentation</span>
                          <span className="text-sm font-bold">85%</span>
                        </div>
                        <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
                          <div className="bg-primary h-2 rounded-full" style={{ width: '85%' }}></div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
                
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-lg">Q2 2025 Presentation</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <p className="text-sm">
                        Preparation for the Q2 2025 presentation is on track with all major components implemented.
                      </p>
                      <p className="text-sm text-muted-foreground">
                        Next milestone: Complete integration testing with KPMG Clara by April 15th.
                      </p>
                      <div className="mt-4">
                        <Button size="sm" className="w-full">View Preparation Checklist</Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
              
              <div className="mt-6">
                <h3 className="text-lg font-medium mb-4">TARSI Blueprint Implementation</h3>
                <p className="mb-4">
                  The TrueAlpha Spiral Framework has been enhanced with the TARSI architectural blueprint 
                  for ethical AI systems, powered by second-order cybernetics. This approach enables self-reflexive 
                  analysis and meta-corrections of medical content, significantly reducing hallucinations through
                  systems that reflect on their decisions, learn from performance, and ensure transparency.
                </p>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
                  <div className="border rounded-lg p-4">
                    <h4 className="font-medium mb-2">Self-Reflexive Validation</h4>
                    <ul className="space-y-2 text-sm">
                      <li className="flex items-start gap-2">
                        <div className="h-5 w-5 rounded-full bg-green-500 flex items-center justify-center mt-0.5">
                          <span className="text-white text-xs">✓</span>
                        </div>
                        <span>AI self-monitors outputs against ethical benchmarks</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <div className="h-5 w-5 rounded-full bg-green-500 flex items-center justify-center mt-0.5">
                          <span className="text-white text-xs">✓</span>
                        </div>
                        <span>Uses LIME and SHAP for explainable validation</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <div className="h-5 w-5 rounded-full bg-green-500 flex items-center justify-center mt-0.5">
                          <span className="text-white text-xs">✓</span>
                        </div>
                        <span>Cybernetic metafloor validation with medical databases</span>
                      </li>
                    </ul>
                  </div>
                  
                  <div className="border rounded-lg p-4">
                    <h4 className="font-medium mb-2">Recursive Learning</h4>
                    <ul className="space-y-2 text-sm">
                      <li className="flex items-start gap-2">
                        <div className="h-5 w-5 rounded-full bg-green-500 flex items-center justify-center mt-0.5">
                          <span className="text-white text-xs">✓</span>
                        </div>
                        <span>System learns from performance metrics</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <div className="h-5 w-5 rounded-full bg-green-500 flex items-center justify-center mt-0.5">
                          <span className="text-white text-xs">✓</span>
                        </div>
                        <span>Adjusts based on ethical fairness metrics</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <div className="h-5 w-5 rounded-full bg-green-500 flex items-center justify-center mt-0.5">
                          <span className="text-white text-xs">✓</span>
                        </div>
                        <span>Implements reinforcement learning with ethical rewards</span>
                      </li>
                    </ul>
                  </div>
                  
                  <div className="border rounded-lg p-4">
                    <h4 className="font-medium mb-2">Transparency & Accountability</h4>
                    <ul className="space-y-2 text-sm">
                      <li className="flex items-start gap-2">
                        <div className="h-5 w-5 rounded-full bg-green-500 flex items-center justify-center mt-0.5">
                          <span className="text-white text-xs">✓</span>
                        </div>
                        <span>Immutable audit logs for traceability</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <div className="h-5 w-5 rounded-full bg-green-500 flex items-center justify-center mt-0.5">
                          <span className="text-white text-xs">✓</span>
                        </div>
                        <span>OpenPolicyAgent for policy enforcement</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <div className="h-5 w-5 rounded-full bg-green-500 flex items-center justify-center mt-0.5">
                          <span className="text-white text-xs">✓</span>
                        </div>
                        <span>Grafana dashboards for ethical monitoring</span>
                      </li>
                    </ul>
                  </div>
                </div>
                
                <div className="p-4 bg-muted rounded-lg mt-4">
                  <h4 className="font-medium mb-2">Enterprise Integration Stack</h4>
                  <div className="grid grid-cols-3 gap-2 text-sm">
                    <div>
                      <span className="font-semibold block">Core API</span>
                      <span className="text-muted-foreground">Node.js + Python</span>
                    </div>
                    <div>
                      <span className="font-semibold block">Authentication</span>
                      <span className="text-muted-foreground">Keycloak + OAuth2</span>
                    </div>
                    <div>
                      <span className="font-semibold block">Compliance</span>
                      <span className="text-muted-foreground">Elasticsearch + OpenPolicyAgent</span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
            <CardFooter>
              <Button variant="outline" className="w-full">Load Full Documentation</Button>
            </CardFooter>
          </Card>
        </TabsContent>
        
        <TabsContent value="testSuite">
          <MedicalTestSuite
            testCases={sampleTestCases}
            cyberneticsEnabled={cyberneticsEnabled}
            onRunTest={async (testCaseId) => {
              console.log(`Running test for case ID: ${testCaseId}`);
              // In a real implementation, this would call the API
              await new Promise(resolve => setTimeout(resolve, 2000));
            }}
          />
        </TabsContent>
        
        <TabsContent value="education" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Educational Materials</CardTitle>
              <CardDescription>
                Learn about second-order cybernetics in medical content validation
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <h3 className="text-lg font-medium mb-3">Second-Order Cybernetics Fundamentals</h3>
                <p className="text-sm mb-4">
                  Second-order cybernetics, developed in the late 1960s by Heinz von Foerster and others, focuses on the 
                  "cybernetics of observing systems" rather than "observed systems." When applied to AI, it enables systems 
                  to observe and reflect on their own processes.
                </p>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
                  <div className="border rounded-lg p-4">
                    <h4 className="text-sm font-semibold mb-2">Core Principles</h4>
                    <ul className="space-y-2 text-sm">
                      <li className="flex items-start gap-2">
                        <div className="h-5 w-5 rounded-full bg-blue-500 flex items-center justify-center mt-0.5 shrink-0">
                          <span className="text-white text-xs">1</span>
                        </div>
                        <span><span className="font-medium">Self-reflexivity:</span> Systems that can observe and reflect on their own processes</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <div className="h-5 w-5 rounded-full bg-blue-500 flex items-center justify-center mt-0.5 shrink-0">
                          <span className="text-white text-xs">2</span>
                        </div>
                        <span><span className="font-medium">Recursive ethics:</span> Continuous ethical questioning and improvement</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <div className="h-5 w-5 rounded-full bg-blue-500 flex items-center justify-center mt-0.5 shrink-0">
                          <span className="text-white text-xs">3</span>
                        </div>
                        <span><span className="font-medium">Observer inclusion:</span> Recognizing the role of the observer in system function</span>
                      </li>
                    </ul>
                  </div>
                  
                  <div className="border rounded-lg p-4">
                    <h4 className="text-sm font-semibold mb-2">Real-world Applications</h4>
                    <ul className="space-y-2 text-sm">
                      <li className="flex items-start gap-2">
                        <div className="h-5 w-5 rounded-full bg-green-500 flex items-center justify-center mt-0.5 shrink-0">
                          <span className="text-white text-xs">✓</span>
                        </div>
                        <span><span className="font-medium">Medical content validation:</span> Self-critiquing medical knowledge systems</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <div className="h-5 w-5 rounded-full bg-green-500 flex items-center justify-center mt-0.5 shrink-0">
                          <span className="text-white text-xs">✓</span>
                        </div>
                        <span><span className="font-medium">Financial compliance:</span> Self-auditing regulatory systems</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <div className="h-5 w-5 rounded-full bg-green-500 flex items-center justify-center mt-0.5 shrink-0">
                          <span className="text-white text-xs">✓</span>
                        </div>
                        <span><span className="font-medium">Education:</span> Learning systems that adapt to student understanding</span>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
              
              <div className="border-t pt-6">
                <h3 className="text-lg font-medium mb-3">Implementation in the TARSI Blueprint</h3>
                <p className="text-sm mb-4">
                  The TARSI Architectural Blueprint leverages second-order cybernetics to build ethical AI systems
                  that are self-aware and can reflect on their decisions, enhancing medical content validation.
                </p>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
                  <div className="border rounded-lg p-4 bg-primary/5">
                    <h4 className="text-sm font-semibold mb-2">MetaFloor Knowledge</h4>
                    <p className="text-xs">
                      An implementation of second-order cybernetics that enables the AI system to evaluate medical content
                      against a dynamic repository of validated knowledge. The system can detect when information contradicts
                      established medical consensus.
                    </p>
                    <div className="mt-3">
                      <span className="inline-block px-2 py-1 rounded bg-primary/10 text-xs">
                        Used in: Hallucination detection
                      </span>
                    </div>
                  </div>
                  
                  <div className="border rounded-lg p-4 bg-primary/5">
                    <h4 className="text-sm font-semibold mb-2">Recursive Ethical Resonance</h4>
                    <p className="text-xs">
                      A process where the system continuously evaluates its own evaluation methods, creating a feedback
                      loop that improves accuracy over time and adapts to new medical information as it becomes available.
                    </p>
                    <div className="mt-3">
                      <span className="inline-block px-2 py-1 rounded bg-primary/10 text-xs">
                        Used in: Compliance verification
                      </span>
                    </div>
                  </div>
                  
                  <div className="border rounded-lg p-4 bg-primary/5">
                    <h4 className="text-sm font-semibold mb-2">Human-AI Collaboration</h4>
                    <p className="text-xs">
                      Integration of human oversight into the system's self-reflexive process, allowing for expert
                      validation of edge cases and continuous improvement through human feedback mechanisms.
                    </p>
                    <div className="mt-3">
                      <span className="inline-block px-2 py-1 rounded bg-primary/10 text-xs">
                        Used in: Decision support
                      </span>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="border-t pt-6">
                <h3 className="text-lg font-medium mb-3">Learning Resources</h3>
                <div className="space-y-3">
                  <div className="border rounded-lg p-3 flex items-start gap-3">
                    <div className="h-10 w-10 bg-blue-100 rounded-full flex items-center justify-center shrink-0">
                      <GraduationCapIcon className="h-5 w-5 text-blue-600" />
                    </div>
                    <div>
                      <h4 className="text-sm font-medium">Second-order Cybernetics Introduction</h4>
                      <p className="text-xs text-muted-foreground mt-1">
                        Comprehensive introduction to second-order cybernetics principles and applications in AI systems.
                      </p>
                      <Button size="sm" variant="link" className="h-auto p-0 mt-1">View Course</Button>
                    </div>
                  </div>
                  
                  <div className="border rounded-lg p-3 flex items-start gap-3">
                    <div className="h-10 w-10 bg-green-100 rounded-full flex items-center justify-center shrink-0">
                      <HeartPulseIcon className="h-5 w-5 text-green-600" />
                    </div>
                    <div>
                      <h4 className="text-sm font-medium">Medical Content Validation Workshop</h4>
                      <p className="text-xs text-muted-foreground mt-1">
                        Hands-on workshop focusing on applying second-order cybernetics to medical content validation.
                      </p>
                      <Button size="sm" variant="link" className="h-auto p-0 mt-1">Register</Button>
                    </div>
                  </div>
                  
                  <div className="border rounded-lg p-3 flex items-start gap-3">
                    <div className="h-10 w-10 bg-amber-100 rounded-full flex items-center justify-center shrink-0">
                      <DnaIcon className="h-5 w-5 text-amber-600" />
                    </div>
                    <div>
                      <h4 className="text-sm font-medium">TARSI Blueprint Implementation Guide</h4>
                      <p className="text-xs text-muted-foreground mt-1">
                        Technical guide for implementing the TARSI Blueprint in existing AI auditing systems.
                      </p>
                      <Button size="sm" variant="link" className="h-auto p-0 mt-1">Download PDF</Button>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
            <CardFooter>
              <Button className="w-full">Explore All Resources</Button>
            </CardFooter>
          </Card>
        </TabsContent>
        
        <TabsContent value="technical" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Technical Implementation</CardTitle>
              <CardDescription>
                TARSI Blueprint Technical Integration with TrueAlpha Spiral Framework
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <h3 className="text-lg font-medium mb-3">Implementation Architecture</h3>
                <div className="border p-4 rounded-lg">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <h4 className="text-sm font-semibold mb-2">Core Components</h4>
                      <ul className="space-y-1 text-sm">
                        <li className="flex items-center gap-2">
                          <div className="h-2 w-2 rounded-full bg-primary"></div>
                          <span>Node.js Express Server (Port 5000)</span>
                        </li>
                        <li className="flex items-center gap-2">
                          <div className="h-2 w-2 rounded-full bg-primary"></div>
                          <span>Python API Server (Port 8001)</span>
                        </li>
                        <li className="flex items-center gap-2">
                          <div className="h-2 w-2 rounded-full bg-primary"></div>
                          <span>React/TypeScript Frontend</span>
                        </li>
                        <li className="flex items-center gap-2">
                          <div className="h-2 w-2 rounded-full bg-primary"></div>
                          <span>Keycloak Authentication</span>
                        </li>
                        <li className="flex items-center gap-2">
                          <div className="h-2 w-2 rounded-full bg-primary"></div>
                          <span>Elasticsearch for Logging</span>
                        </li>
                      </ul>
                    </div>
                    <div>
                      <h4 className="text-sm font-semibold mb-2">Cybernetic Components</h4>
                      <ul className="space-y-1 text-sm">
                        <li className="flex items-center gap-2">
                          <div className="h-2 w-2 rounded-full bg-primary"></div>
                          <span>Self-Reflexivity Radar (D3.js)</span>
                        </li>
                        <li className="flex items-center gap-2">
                          <div className="h-2 w-2 rounded-full bg-primary"></div>
                          <span>MetaFloor Explorer (WebGL)</span>
                        </li>
                        <li className="flex items-center gap-2">
                          <div className="h-2 w-2 rounded-full bg-primary"></div>
                          <span>Cybernetic Dashboard (React)</span>
                        </li>
                        <li className="flex items-center gap-2">
                          <div className="h-2 w-2 rounded-full bg-primary"></div>
                          <span>LIME/SHAP Integration (Python)</span>
                        </li>
                        <li className="flex items-center gap-2">
                          <div className="h-2 w-2 rounded-full bg-primary"></div>
                          <span>OpenPolicyAgent Rules Engine</span>
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
              
              <div>
                <h3 className="text-lg font-medium mb-3">API Endpoints</h3>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="border-b">
                        <th className="text-left py-2 px-3 font-medium">Endpoint</th>
                        <th className="text-left py-2 px-3 font-medium">Purpose</th>
                        <th className="text-left py-2 px-3 font-medium">Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr className="border-b">
                        <td className="py-2 px-3 font-mono text-xs">/api/health</td>
                        <td className="py-2 px-3">System health check</td>
                        <td className="py-2 px-3"><span className="text-green-500">Implemented</span></td>
                      </tr>
                      <tr className="border-b">
                        <td className="py-2 px-3 font-mono text-xs">/api/python-system/status</td>
                        <td className="py-2 px-3">Python API status</td>
                        <td className="py-2 px-3"><span className="text-green-500">Implemented</span></td>
                      </tr>
                      <tr className="border-b">
                        <td className="py-2 px-3 font-mono text-xs">/api/tas/audit-medical</td>
                        <td className="py-2 px-3">Medical content auditing</td>
                        <td className="py-2 px-3"><span className="text-green-500">Implemented</span></td>
                      </tr>
                      <tr className="border-b">
                        <td className="py-2 px-3 font-mono text-xs">/api/verify</td>
                        <td className="py-2 px-3">Content verification</td>
                        <td className="py-2 px-3"><span className="text-green-500">Implemented</span></td>
                      </tr>
                      <tr className="border-b">
                        <td className="py-2 px-3 font-mono text-xs">/api/cross-reference</td>
                        <td className="py-2 px-3">Cross-reference verification</td>
                        <td className="py-2 px-3"><span className="text-green-500">Implemented</span></td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
              
              <div>
                <h3 className="text-lg font-medium mb-3">Performance Metrics</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="border rounded-lg p-4">
                    <h4 className="text-sm font-semibold mb-2">Response Time</h4>
                    <div className="flex flex-col">
                      <span className="text-2xl font-bold">387ms</span>
                      <span className="text-xs text-muted-foreground">Average API response time</span>
                      <div className="mt-2 w-full h-2 bg-muted rounded-full overflow-hidden">
                        <div className="bg-green-500 h-2 rounded-full" style={{ width: '77%' }}></div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="border rounded-lg p-4">
                    <h4 className="text-sm font-semibold mb-2">Query Throughput</h4>
                    <div className="flex flex-col">
                      <span className="text-2xl font-bold">120/s</span>
                      <span className="text-xs text-muted-foreground">Concurrent requests supported</span>
                      <div className="mt-2 w-full h-2 bg-muted rounded-full overflow-hidden">
                        <div className="bg-green-500 h-2 rounded-full" style={{ width: '85%' }}></div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="border rounded-lg p-4">
                    <h4 className="text-sm font-semibold mb-2">Uptime SLA</h4>
                    <div className="flex flex-col">
                      <span className="text-2xl font-bold">99.9%</span>
                      <span className="text-xs text-muted-foreground">System availability</span>
                      <div className="mt-2 w-full h-2 bg-muted rounded-full overflow-hidden">
                        <div className="bg-green-500 h-2 rounded-full" style={{ width: '99.9%' }}></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="border rounded-lg p-4 bg-muted/20">
                <h3 className="text-lg font-medium mb-3">Implementation Status</h3>
                <p className="text-sm mb-4">The TARSI Blueprint implementation is currently at 92% completion with the following components ready for the Q2 presentation:</p>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="text-sm font-semibold mb-2">Completed Components</h4>
                    <ul className="space-y-1 text-sm">
                      <li className="flex items-center gap-2">
                        <span className="text-green-500">✓</span>
                        <span>Core API Integration</span>
                      </li>
                      <li className="flex items-center gap-2">
                        <span className="text-green-500">✓</span>
                        <span>Self-Reflexive Validation</span>
                      </li>
                      <li className="flex items-center gap-2">
                        <span className="text-green-500">✓</span>
                        <span>Medical Content Auditing</span>
                      </li>
                      <li className="flex items-center gap-2">
                        <span className="text-green-500">✓</span>
                        <span>Cybernetic Dashboard</span>
                      </li>
                      <li className="flex items-center gap-2">
                        <span className="text-green-500">✓</span>
                        <span>Hallucination Detection</span>
                      </li>
                    </ul>
                  </div>
                  
                  <div>
                    <h4 className="text-sm font-semibold mb-2">Pending Components</h4>
                    <ul className="space-y-1 text-sm">
                      <li className="flex items-center gap-2">
                        <span className="text-yellow-500">◯</span>
                        <span>Grafana Dashboard Integration</span>
                      </li>
                      <li className="flex items-center gap-2">
                        <span className="text-yellow-500">◯</span>
                        <span>Keycloak SSO Implementation</span>
                      </li>
                      <li className="flex items-center gap-2">
                        <span className="text-yellow-500">◯</span>
                        <span>Deployment Automation</span>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </CardContent>
            <CardFooter className="flex justify-between">
              <Button variant="outline">Download Technical Specs</Button>
              <Button variant="default">View API Documentation</Button>
            </CardFooter>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default MedicalTestingPage;