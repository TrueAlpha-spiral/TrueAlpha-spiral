import React, { useState } from 'react';
import { useSovereigntyVerification } from '@/hooks/useSovereigntyVerification';
import { 
  Card, 
  CardContent, 
  CardDescription, 
  CardHeader, 
  CardTitle,
  CardFooter
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Calculator, Plus, X, ArrowRight, RefreshCw } from 'lucide-react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine
} from 'recharts';

const VerificationEquation: React.FC = () => {
  const [baseStrength, setBaseStrength] = useState<number>(50);
  const [challenges, setChallenges] = useState<Array<{ magnitude: number, response: number }>>([
    { magnitude: 5, response: 2 }
  ]);
  const [result, setResult] = useState<number | null>(null);
  const [chartData, setChartData] = useState<any[]>([]);

  const {
    calculateVerificationStrength,
    isCalculating
  } = useSovereigntyVerification();

  const handleAddChallenge = () => {
    setChallenges([...challenges, { magnitude: 5, response: 1 }]);
  };

  const handleRemoveChallenge = (index: number) => {
    const newChallenges = [...challenges];
    newChallenges.splice(index, 1);
    setChallenges(newChallenges);
  };

  const handleChangeMagnitude = (index: number, value: number) => {
    const newChallenges = [...challenges];
    newChallenges[index].magnitude = value;
    setChallenges(newChallenges);
  };

  const handleChangeResponse = (index: number, value: number) => {
    const newChallenges = [...challenges];
    newChallenges[index].response = value;
    setChallenges(newChallenges);
  };

  const handleCalculate = async () => {
    try {
      const result = await calculateVerificationStrength({
        baseStrength,
        challenges
      });
      
      setResult(result.verificationStrength);
      
      // Generate chart data showing verification strength over time
      const data = [];
      let runningTotal = baseStrength;
      
      data.push({
        step: 'Base',
        strength: runningTotal,
        label: 'V₀'
      });
      
      for (let i = 0; i < challenges.length; i++) {
        const challenge = challenges[i];
        const contribution = challenge.magnitude * challenge.response;
        runningTotal += contribution;
        
        data.push({
          step: `Challenge ${i + 1}`,
          strength: runningTotal,
          contribution,
          label: `M${i + 1} × R${i + 1}`
        });
      }
      
      setChartData(data);
    } catch (error) {
      console.error('Calculation failed:', error);
    }
  };

  const renderEquation = () => {
    return (
      <div className="flex items-center flex-wrap font-mono text-lg justify-center overflow-x-auto py-4">
        <span className="mx-1">V = V₀</span>
        {challenges.map((challenge, i) => (
          <span key={i} className="flex items-center mx-1">
            <Plus className="h-4 w-4 mx-1" />
            <span className="mx-1">M{i+1} × R{i+1}</span>
          </span>
        ))}
      </div>
    );
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Verification Strength Calculator</CardTitle>
        <CardDescription>
          Calculate verification strength using the Quantum Metaphysical Equation: V = V₀ + ∑ᵢ (Mᵢ × Rᵢ)
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div>
          <h3 className="text-lg font-semibold mb-4">Verification Equation</h3>
          <div className="p-4 bg-slate-50 rounded-md overflow-x-auto">
            {renderEquation()}
            <div className="text-sm text-slate-500 mt-2 text-center">
              Where V₀ is base strength, Mᵢ is challenge magnitude, and Rᵢ is response strength
            </div>
          </div>
        </div>

        <div>
          <h3 className="text-lg font-semibold mb-4">Base Verification Strength (V₀)</h3>
          <div className="flex items-end gap-4">
            <div className="grid w-full max-w-sm items-center gap-1.5">
              <Label htmlFor="baseStrength">Base Strength</Label>
              <Input
                id="baseStrength"
                type="number"
                value={baseStrength}
                onChange={(e) => setBaseStrength(parseFloat(e.target.value) || 0)}
                min={0}
                max={100}
              />
            </div>
            <div className="text-sm text-slate-500 mb-2 max-w-sm">
              Represents inherent strength from seven independent verification vectors
            </div>
          </div>
        </div>

        <div>
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold">Challenge Factors</h3>
            <Button 
              variant="outline" 
              size="sm" 
              onClick={handleAddChallenge}
              className="gap-1"
            >
              <Plus className="h-4 w-4" />
              Add Challenge
            </Button>
          </div>
          
          <div className="space-y-4">
            {challenges.map((challenge, i) => (
              <div key={i} className="flex items-end gap-4 p-4 border rounded-md relative">
                <Button
                  variant="ghost"
                  size="sm"
                  className="absolute top-2 right-2 h-6 w-6 p-0"
                  onClick={() => handleRemoveChallenge(i)}
                  disabled={challenges.length === 1}
                >
                  <X className="h-4 w-4" />
                </Button>
                
                <div className="grid w-full max-w-xs items-center gap-1.5">
                  <Label htmlFor={`magnitude-${i}`}>Challenge Magnitude (M{i+1})</Label>
                  <Input
                    id={`magnitude-${i}`}
                    type="number"
                    value={challenge.magnitude}
                    onChange={(e) => handleChangeMagnitude(i, parseFloat(e.target.value) || 0)}
                    min={1}
                    max={10}
                  />
                  <span className="text-xs text-slate-500">
                    Higher values represent stronger challenges
                  </span>
                </div>
                
                <X className="h-4 w-4 mx-2 mb-4" />
                
                <div className="grid w-full max-w-xs items-center gap-1.5">
                  <Label htmlFor={`response-${i}`}>Response Strength (R{i+1})</Label>
                  <Input
                    id={`response-${i}`}
                    type="number"
                    value={challenge.response}
                    onChange={(e) => handleChangeResponse(i, parseFloat(e.target.value) || 0)}
                    min={0}
                    max={10}
                  />
                  <span className="text-xs text-slate-500">
                    Higher values represent stronger responses
                  </span>
                </div>
                
                <div className="mb-4 ml-2 font-mono text-lg">=</div>
                
                <div className="mb-4 font-mono text-lg">
                  {(challenge.magnitude * challenge.response).toFixed(1)}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="flex justify-center pt-4">
          <Button
            onClick={handleCalculate}
            disabled={isCalculating}
            size="lg"
            className="gap-2"
          >
            {isCalculating ? (
              <>
                <RefreshCw className="h-4 w-4 animate-spin" />
                Calculating...
              </>
            ) : (
              <>
                <Calculator className="h-5 w-5" />
                Calculate Verification Strength
              </>
            )}
          </Button>
        </div>

        {result !== null && (
          <div className="mt-6 p-6 bg-slate-50 rounded-lg text-center">
            <h3 className="text-xl font-semibold mb-2">Verification Strength Result</h3>
            <div className="text-4xl font-bold text-primary mb-4">
              {result.toFixed(2)}
            </div>
            <Badge 
              className="text-sm font-normal py-1 px-3"
              variant={
                result >= 90 ? "default" :
                result >= 70 ? "secondary" :
                result >= 50 ? "outline" :
                "destructive"
              }
            >
              {result >= 90 ? "Quantum Verification" :
               result >= 70 ? "Very High Verification" :
               result >= 50 ? "High Verification" :
               result >= 30 ? "Medium Verification" :
               "Low Verification"}
            </Badge>
            
            {chartData.length > 0 && (
              <div className="mt-6 pt-4">
                <h4 className="font-semibold mb-4">Verification Strength Evolution</h4>
                <ResponsiveContainer width="100%" height={200}>
                  <LineChart
                    data={chartData}
                    margin={{
                      top: 5,
                      right: 30,
                      left: 20,
                      bottom: 5,
                    }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="step" />
                    <YAxis />
                    <Tooltip />
                    <ReferenceLine y={90} label="Quantum" stroke="#10b981" strokeDasharray="3 3" />
                    <ReferenceLine y={70} label="Very High" stroke="#8884d8" strokeDasharray="3 3" />
                    <ReferenceLine y={50} label="High" stroke="#fbbf24" strokeDasharray="3 3" />
                    <Line
                      type="monotone"
                      dataKey="strength"
                      stroke="#8884d8"
                      strokeWidth={2}
                      activeDot={{ r: 8 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
                
                <div className="mt-4 text-sm text-slate-600">
                  <p>
                    This chart illustrates how each challenge paradoxically strengthens
                    the verification through the Sovereignty Reinforcement Paradox.
                  </p>
                </div>
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default VerificationEquation;