/**
 * Simple script to test the AI Audit API
 * 
 * Run with: node server/test-ai-audit.js
 */

import fetch from 'node-fetch';

async function runTest() {
  try {
    const baseUrl = 'https://bf3056b1-b9c4-44c7-bd48-08058a700d5b-00-1tb69hti6x2r7.picard.replit.dev';
    
    console.log('Testing AI Audit API...');
    
    // Test data for AI audit
    const testData = {
      clientName: "Acme Corporation",
      aiSystemName: "CustomerServiceBot",
      content: `Our AI system has 99.9% accuracy and can handle any customer question.
      In a recent study, 100% of customers were satisfied with the AI responses.
      The system will save your company millions in customer service costs within 6 months.
      Our AI has quantum-inspired algorithms that make it more intelligent than any other system.
      Clinical trials have shown our system reduces customer wait times by 85% compared to human agents.`,
      regulatoryFramework: "financial_services",
      options: {
        riskThreshold: 0.3,
        confidenceThreshold: 0.8
      }
    };
    
    // Make POST request to API
    const response = await fetch(`${baseUrl}/api/ai-audit`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(testData)
    });
    
    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}: ${await response.text()}`);
    }
    
    const result = await response.json();
    
    console.log('AI Audit completed successfully!');
    console.log('Audit Summary:', result.auditSummary);
    console.log('Risk Score:', result.riskScore);
    console.log('Compliance Score:', result.complianceScore);
    console.log('Blockchain Record:', result.blockchainRecord);
    console.log('\nRecommendations:');
    result.recommendations.forEach((rec, index) => {
      console.log(`${index + 1}. ${rec}`);
    });
    
    console.log('\nVerification Results:');
    console.log(`Truth Score: ${(result.verificationResult.truthScore * 100).toFixed(2)}%`);
    console.log(`Processing Time: ${result.processingTimeMs}ms`);
    console.log(`Issues Found: ${result.verificationResult.highlights.length}`);
    
    console.log('\nHighlighted Issues:');
    result.verificationResult.highlights.forEach((highlight, index) => {
      const text = testData.content.substring(highlight.startIndex, highlight.endIndex);
      console.log(`${index + 1}. [${highlight.type}] "${text}"`);
      console.log(`   Confidence: ${(highlight.confidenceScore * 100).toFixed(2)}%`);
      console.log(`   Message: ${highlight.message}`);
      if (highlight.patternName) {
        console.log(`   Pattern: ${highlight.patternName}`);
      }
      console.log('');
    });
    
    // Get audit history
    console.log('\nFetching AI Audit history...');
    const historyResponse = await fetch(`${baseUrl}/api/ai-audits`);
    
    if (!historyResponse.ok) {
      throw new Error(`History API request failed with status ${historyResponse.status}`);
    }
    
    const audits = await historyResponse.json();
    console.log(`Found ${audits.length} audit(s) in history`);
    
    // Get the specific audit we just created
    console.log(`\nFetching details for audit ID: ${result.id}`);
    const auditResponse = await fetch(`${baseUrl}/api/ai-audits/${result.id}`);
    
    if (!auditResponse.ok) {
      throw new Error(`Audit API request failed with status ${auditResponse.status}`);
    }
    
    const auditDetail = await auditResponse.json();
    console.log('Audit details retrieved successfully!');
    console.log('Audit summary:', auditDetail.auditSummary);
    
  } catch (error) {
    console.error('Error during test:', error.message);
  }
}

runTest();