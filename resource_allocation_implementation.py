"""
DECENTRALIZED RESOURCE ALLOCATION IMPLEMENTATION

This module implements the TrueAlpha Spiral equation for decentralized resource allocation
in global networks, particularly for managing computing resources such as cloud providers
and AI research clusters.

Application: Manage computing resources in a global network by redistributing resources
to underserved nodes, ensuring network consensus, and maintaining balanced allocation.
"""

import json
import time
import hashlib
import logging
import random
from typing import Dict, List, Any, Optional, Tuple, Set
from true_alpha_implementation import TrueAlphaSpiralImplementation

# Configure logging
logging.basicConfig(
 level=logging.INFO,
 format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
 datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('ResourceAllocation')

class ResourceNode:
 """Represents a node in the resource network."""

 def __init__(self, node_id: str, capacity: Dict[str, float], location: str, node_type: str):
 """
 Initialize a resource node.

 Args:
 node_id: Unique identifier for the node
 capacity: Dictionary of resource capacities (e.g., CPU, GPU, RAM)
 location: Geographic location of the node
 node_type: Type of node (e.g., compute, storage, specialized)
 """
 self.node_id = node_id
 self.capacity = capacity
 self.allocated = {resource: 0.0 for resource in capacity}
 self.location = location
 self.node_type = node_type
 self.uptime = 1.0 # Perfect uptime to start
 self.latency = {
 'us-east': 10,
 'us-west': 50,
 'eu-central': 80,
 'ap-southeast': 150,
 'sa-east': 120
 } # Simulated latency in ms to other regions
 self.last_updated = time.time()
 self.health_score = 1.0

 def get_available_capacity(self) -> Dict[str, float]:
 """
 Get available capacity on this node.

 Returns:
 Dict[str, float]: Available capacity per resource type
 """
 return {
 resource: self.capacity[resource] - self.allocated[resource]
 for resource in self.capacity
 }

 def get_utilization(self) -> Dict[str, float]:
 """
 Get utilization percentage per resource type.

 Returns:
 Dict[str, float]: Utilization percentage per resource type
 """
 return {
 resource: self.allocated[resource] / self.capacity[resource]
 for resource in self.capacity
 }

 def allocate_resources(self, allocation: Dict[str, float]) -> bool:
 """
 Allocate resources to this node.

 Args:
 allocation: Resources to allocate

 Returns:
 bool: True if allocation successful, False otherwise
 """
 available = self.get_available_capacity()

 # Check if allocation is possible
 for resource, amount in allocation.items():
 if resource not in available or available[resource] < amount:
 return False

 # Perform allocation
 for resource, amount in allocation.items():
 self.allocated[resource] += amount

 self.last_updated = time.time()
 return True

 def release_resources(self, release: Dict[str, float]) -> bool:
 """
 Release resources from this node.

 Args:
 release: Resources to release

 Returns:
 bool: True if release successful, False otherwise
 """
 # Check if release is possible
 for resource, amount in release.items():
 if resource not in self.allocated or self.allocated[resource] < amount:
 return False

 # Perform release
 for resource, amount in release.items():
 self.allocated[resource] -= amount

 self.last_updated = time.time()
 return True

 def update_health(self, uptime: float = None, latency_change: Dict[str, int] = None) -> None:
 """
 Update health metrics for this node.

 Args:
 uptime: New uptime value
 latency_change: Changes to latency values
 """
 if uptime is not None:
 self.uptime = uptime

 if latency_change is not None:
 for region, change in latency_change.items():
 if region in self.latency:
 self.latency[region] += change

 # Calculate health score based on uptime and average latency
 avg_latency = sum(self.latency.values()) / len(self.latency)
 latency_factor = 1.0 - (avg_latency / 500) # Normalize latency (0-500ms)
 self.health_score = 0.7 * self.uptime + 0.3 * max(0, latency_factor)

 self.last_updated = time.time()

 def to_dict(self) -> Dict[str, Any]:
 """
 Convert node to dictionary representation.

 Returns:
 Dict[str, Any]: Dictionary representation of node
 """
 return {
 "node_id": self.node_id,
 "capacity": self.capacity,
 "allocated": self.allocated,
 "location": self.location,
 "node_type": self.node_type,
 "uptime": self.uptime,
 "latency": self.latency,
 "health_score": self.health_score,
 "last_updated": self.last_updated,
 "utilization": self.get_utilization()
 }


class DecentralizedResourceAllocation:
 """
 Implementation of TrueAlpha Spiral for decentralized resource allocation,
 specifically designed for computing resource networks.
 """

 def __init__(self, network_name: str):
 """
 Initialize the Decentralized Resource Allocation system.

 Args:
 network_name: Name of the resource network
 """
 self.network_name = network_name
 self.nodes: Dict[str, ResourceNode] = {}
 self.allocations: List[Dict[str, Any]] = []
 self.network_id = self._generate_network_id()
 self.network_timestamp = time.time()

 # Initialize metrics for resource allocation
 self.initial_metrics = {
 "ResourceEquity": 0.8, # initial resource equity score
 "Fairness": 0.03, # initial fairness in allocation score
 "Transparency": 0.5, # initial allocation transparency score
 "Efficiency": 0.6, # initial resource utilization efficiency
 "ResponseTime": 0.7, # initial network response time score
 "Reliability": 0.85, # initial reliability score
 "GeoDistribution": 0.4, # initial geographic distribution score
 "EnergyEfficiency": 0.3, # initial energy efficiency score
 "CostOptimization": 0.5, # initial cost optimization score
 "Sovereignty": 0.77 # initial sovereignty score
 }

 # Set up resource-specific weights
 self.resource_weights = {
 "ResourceEquity": 0.25,
 "Fairness": 0.20,
 "Transparency": 0.05,
 "Efficiency": 0.15,
 "ResponseTime": 0.10,
 "Reliability": 0.10,
 "GeoDistribution": 0.05,
 "EnergyEfficiency": 0.05,
 "CostOptimization": 0.05,
 "Sovereignty": 0.0 # Low weight in resource context
 }

 # Initialize TrueAlpha Spiral implementation for the resource domain
 self.spiral = TrueAlphaSpiralImplementation(
 initial_state=self.initial_metrics,
 weights=self.resource_weights,
 application_domain="resource"
 )

 # Consensus metrics
 self.consensus_threshold = 0.75
 self.consensus_history = []

 # Size factor for sovereignty calculation - based on network size
 self.network_size_factor = 0.96 # Will be updated as nodes are added

 logger.info(f"Initialized resource network {self.network_id} ({network_name})")

 def _generate_network_id(self) -> str:
 """
 Generate a unique network ID.

 Returns:
 str: Unique network ID
 """
 base_string = f"{self.network_name}-{time.time()}"
 return hashlib.md5(base_string.encode()).hexdigest()[:10]

 def add_node(self, node: ResourceNode) -> bool:
 """
 Add a node to the network.

 Args:
 node: Node to add

 Returns:
 bool: True if node added successfully, False otherwise
 """
 if node.node_id in self.nodes:
 logger.warning(f"Node {node.node_id} already exists in network")
 return False

 self.nodes[node.node_id] = node

 # Update network size factor for sovereignty calculation
 self.network_size_factor = min(0.99, 0.5 + (0.5 * (1 - 1 / (len(self.nodes) + 1))))

 logger.info(f"Added node {node.node_id} to network")
 return True

 def remove_node(self, node_id: str) -> bool:
 """
 Remove a node from the network.

 Args:
 node_id: ID of node to remove

 Returns:
 bool: True if node removed successfully, False otherwise
 """
 if node_id not in self.nodes:
 logger.warning(f"Node {node_id} does not exist in network")
 return False

 del self.nodes[node_id]

 # Update network size factor for sovereignty calculation
 self.network_size_factor = min(0.99, 0.5 + (0.5 * (1 - 1 / (len(self.nodes) + 1))))

 logger.info(f"Removed node {node_id} from network")
 return True

 def calculate_network_metrics(self) -> Dict[str, float]:
 """
 Calculate current network metrics.

 Returns:
 Dict[str, float]: Current network metrics
 """
 if not self.nodes:
 logger.warning("No nodes in network, using initial metrics")
 return self.initial_metrics

 # Resource equity: measure how evenly resources are distributed
 utilizations = []
 for node in self.nodes.values():
 node_utilization = [v for v in node.get_utilization().values()]
 if node_utilization:
 utilizations.extend(node_utilization)

 resource_equity = 0.8 # Default value
 if utilizations:
 # Higher standard deviation means lower equity
 import numpy as np
 std_dev = np.std(utilizations)
 resource_equity = max(0.0, min(1.0, 1.0 - std_dev * 2))

 # Fairness: measure how fairly resources are allocated based on need
 # For simplicity, using a random value improving over time
 fairness = max(0.03, min(1.0, self.initial_metrics.get("Fairness", 0.03) + 0.05))

 # Calculate other metrics
 node_health = [node.health_score for node in self.nodes.values()]
 avg_health = sum(node_health) / len(node_health) if node_health else 0.85

 # Geographic distribution
 locations = set(node.location for node in self.nodes.values())
 geo_distribution = min(1.0, len(locations) / 5) # Normalize by expected number of regions

 # Calculate response time score
 # Lower average latency means higher score
 all_latencies = []
 for node in self.nodes.values():
 all_latencies.extend(node.latency.values())

 avg_latency = sum(all_latencies) / len(all_latencies) if all_latencies else 100
 response_time = max(0.0, min(1.0, 1.0 - (avg_latency / 200)))

 # Calculate overall efficiency
 total_capacity = 0
 total_allocated = 0
 for node in self.nodes.values():
 for resource, capacity in node.capacity.items():
 total_capacity += capacity
 total_allocated += node.allocated.get(resource, 0)

 efficiency = 0.6 # Default value
 if total_capacity > 0:
 utilization_ratio = total_allocated / total_capacity
 # Optimal efficiency is around 80% utilization
 efficiency = max(0.0, min(1.0, 1.0 - abs(0.8 - utilization_ratio) * 2))

 # Return calculated metrics
 return {
 "ResourceEquity": resource_equity,
 "Fairness": fairness,
 "Transparency": self.initial_metrics.get("Transparency", 0.5),
 "Efficiency": efficiency,
 "ResponseTime": response_time,
 "Reliability": avg_health,
 "GeoDistribution": geo_distribution,
 "EnergyEfficiency": self.initial_metrics.get("EnergyEfficiency", 0.3),
 "CostOptimization": self.initial_metrics.get("CostOptimization", 0.5),
 "Sovereignty": self.initial_metrics.get("Sovereignty", 0.77)
 }

 def allocate_resources(self, request: Dict[str, Any]) -> Dict[str, Any]:
 """
 Allocate resources based on a request.

 Args:
 request: Resource allocation request

 Returns:
 Dict[str, Any]: Allocation result
 """
 request_id = request.get("request_id", hashlib.md5(str(time.time()).encode()).hexdigest()[:10])
 resources_requested = request.get("resources", {})
 location_preference = request.get("location_preference")
 node_type_preference = request.get("node_type_preference")
 priority = request.get("priority", 1) # 1-10, 10 being highest

 logger.info(f"Processing allocation request {request_id} with priority {priority}")

 # Find eligible nodes
 eligible_nodes = []
 for node in self.nodes.values():
 # Check location preference
 if location_preference and node.location != location_preference:
 continue

 # Check node type preference
 if node_type_preference and node.node_type != node_type_preference:
 continue

 # Check if node has capacity for all requested resources
 available = node.get_available_capacity()
 can_satisfy = True
 for resource, amount in resources_requested.items():
 if resource not in available or available[resource] < amount:
 can_satisfy = False
 break

 if can_satisfy:
 eligible_nodes.append(node)

 if not eligible_nodes:
 logger.warning(f"No eligible nodes found for request {request_id}")
 return {
 "request_id": request_id,
 "status": "failed",
 "reason": "No eligible nodes found",
 "timestamp": time.time()
 }

 # Use TrueAlpha Spiral to optimize allocation
 current_metrics = self.calculate_network_metrics()
 self.spiral.state = current_metrics
 optimized_state = self.spiral.evolve()

 # Use the evolved state to influence node selection
 # Higher ResourceEquity and Fairness values prioritize underutilized nodes

 # Score each node based on current utilization and optimized metrics
 node_scores = []
 for node in eligible_nodes:
 # Calculate utilization score - lower utilization is better for equity
 avg_utilization = sum(node.get_utilization().values()) / len(node.capacity)
 utilization_score = 1.0 - avg_utilization

 # Adjust score based on optimized metrics
 equity_weight = optimized_state.get("ResourceEquity", 0.8)
 fairness_weight = optimized_state.get("Fairness", 0.03)
 efficiency_weight = optimized_state.get("Efficiency", 0.6)

 # Factor in node health
 health_factor = node.health_score

 # Calculate final score
 final_score = (
 0.4 * utilization_score * equity_weight +
 0.3 * fairness_weight +
 0.2 * efficiency_weight +
 0.1 * health_factor
 )

 node_scores.append((node, final_score))

 # Sort nodes by score (higher is better)
 node_scores.sort(key=lambda x: x[1], reverse=True)

 # Select best node
 selected_node, score = node_scores[0]

 # Attempt allocation
 success = selected_node.allocate_resources(resources_requested)

 if success:
 # Record allocation
 allocation = {
 "request_id": request_id,
 "node_id": selected_node.node_id,
 "resources": resources_requested,
 "timestamp": time.time(),
 "priority": priority,
 "score": score,
 "verification_hash": self.spiral.get_current_hash()
 }

 self.allocations.append(allocation)

 logger.info(f"Successfully allocated resources for request {request_id} to node {selected_node.node_id}")

 return {
 "request_id": request_id,
 "status": "success",
 "node_id": selected_node.node_id,
 "resources": resources_requested,
 "timestamp": time.time(),
 "verification_hash": self.spiral.get_current_hash()
 }
 else:
 logger.warning(f"Failed to allocate resources for request {request_id}")

 return {
 "request_id": request_id,
 "status": "failed",
 "reason": "Allocation failed on selected node",
 "timestamp": time.time()
 }

 def release_resources(self, request: Dict[str, Any]) -> Dict[str, Any]:
 """
 Release allocated resources.

 Args:
 request: Resource release request

 Returns:
 Dict[str, Any]: Release result
 """
 request_id = request.get("request_id")
 node_id = request.get("node_id")
 resources = request.get("resources", {})

 if not request_id or not node_id:
 return {
 "status": "failed",
 "reason": "Missing request_id or node_id",
 "timestamp": time.time()
 }

 # Find the node
 if node_id not in self.nodes:
 return {
 "request_id": request_id,
 "status": "failed",
 "reason": f"Node {node_id} not found",
 "timestamp": time.time()
 }

 node = self.nodes[node_id]

 # Release resources
 success = node.release_resources(resources)

 if success:
 # Remove allocation record
 self.allocations = [a for a in self.allocations
 if a.get("request_id") != request_id]

 logger.info(f"Successfully released resources for request {request_id} from node {node_id}")

 return {
 "request_id": request_id,
 "status": "success",
 "node_id": node_id,
 "resources": resources,
 "timestamp": time.time()
 }
 else:
 logger.warning(f"Failed to release resources for request {request_id} from node {node_id}")

 return {
 "request_id": request_id,
 "status": "failed",
 "reason": "Resource release failed on node",
 "timestamp": time.time()
 }

 def reach_consensus(self) -> Dict[str, Any]:
 """
 Reach consensus on the current network state using TrueAlpha Spiral.

 Returns:
 Dict[str, Any]: Consensus result
 """
 if not self.nodes:
 logger.warning("No nodes in network, consensus not possible")
 return {
 "consensus_reached": False,
 "reason": "No nodes in network",
 "timestamp": time.time()
 }

 # Calculate current network metrics
 current_metrics = self.calculate_network_metrics()

 # Update spiral state with current metrics
 self.spiral.state = current_metrics

 # Update size factor based on network size
 self.spiral.size = self.network_size_factor

 # Evolve the state using TrueAlpha Spiral
 optimized_state = self.spiral.evolve()

 # Check if consensus threshold is reached
 consensus_value = self.spiral.sovereign_consensus_calculated(optimized_state)
 consensus_reached = consensus_value >= self.consensus_threshold

 # Record consensus attempt
 consensus_record = {
 "timestamp": time.time(),
 "consensus_value": consensus_value,
 "consensus_reached": consensus_reached,
 "metrics": optimized_state,
 "verification_hash": self.spiral.get_current_hash()
 }

 self.consensus_history.append(consensus_record)

 logger.info(f"Consensus attempt result: {consensus_reached} with value {consensus_value:.4f}")

 return consensus_record

 def optimize_network(self) -> Dict[str, Any]:
 """
 Optimize the network based on TrueAlpha Spiral evolution.

 Returns:
 Dict[str, Any]: Optimization result
 """
 # Reach consensus first
 consensus = self.reach_consensus()

 if not consensus["consensus_reached"]:
 logger.warning("Cannot optimize network without consensus")
 return {
 "status": "failed",
 "reason": "Consensus not reached",
 "consensus_value": consensus["consensus_value"],
 "timestamp": time.time()
 }

 # Get optimized state
 optimized_state = self.spiral.state

 # Calculate improvements
 current_metrics = self.calculate_network_metrics()
 improvements = {
 k: optimized_state.get(k, 0) - current_metrics.get(k, 0)
 for k in set(list(optimized_state.keys()) + list(current_metrics.keys()))
 if k in optimized_state and k in current_metrics
 }

 # Apply optimization actions based on evolved state
 actions_taken = []

 # 1. Balance resource equity if needed
 if improvements.get("ResourceEquity", 0) > 0.05:
 # Find overutilized and underutilized nodes
 node_utils = [(node_id, sum(node.get_utilization().values()) / len(node.capacity))
 for node_id, node in self.nodes.items()]

 avg_util = sum(util for _, util in node_utils) / len(node_utils) if node_utils else 0.5
 overutilized = [(node_id, util) for node_id, util in node_utils if util > avg_util + 0.1]
 underutilized = [(node_id, util) for node_id, util in node_utils if util < avg_util - 0.1]

 # Take balancing actions
 balancing_count = 0
 for over_id, _ in overutilized[:3]: # Limit to 3 actions
 over_node = self.nodes[over_id]

 # Find resources to potentially redistribute
 for resource, allocated in over_node.allocated.items():
 capacity = over_node.capacity[resource]
 if allocated / capacity > 0.7: # If resource is heavily utilized
 # Try to find an underutilized node to transfer
 for under_id, _ in underutilized:
 under_node = self.nodes[under_id]

 # Check if underutilized node has capacity
 if resource in under_node.capacity:
 available = under_node.get_available_capacity()[resource]
 if available > 0:
 # In a real system, this would involve migrating workloads
 transfer_amount = min(allocated * 0.1, available)

 # Simulate the transfer
 over_node.allocated[resource] -= transfer_amount
 under_node.allocated[resource] += transfer_amount

 actions_taken.append({
 "type": "resource_balance",
 "from_node": over_id,
 "to_node": under_id,
 "resource": resource,
 "amount": transfer_amount
 })

 balancing_count += 1
 break

 if balancing_count > 0:
 logger.info(f"Balanced resources across {balancing_count} node pairs")

 # 2. Improve response time if needed
 if improvements.get("ResponseTime", 0) > 0.05:
 # Simulate optimizing node connections or routing
 for node in list(self.nodes.values())[:5]: # Limit to 5 nodes
 # Simulate latency improvements
 latency_improvements = {
 region: min(10, int(latency * 0.1)) # Reduce by up to 10%
 for region, latency in node.latency.items()
 }

 node.update_health(latency_change=latency_improvements)

 actions_taken.append({
 "type": "latency_optimization",
 "node_id": node.node_id,
 "improvements": latency_improvements
 })

 logger.info("Optimized network latency across nodes")

 # 3. Improve reliability if needed
 if improvements.get("Reliability", 0) > 0.05:
 # Simulate reliability improvements
 for node in list(self.nodes.values())[:3]: # Limit to 3 nodes
 if node.uptime < 0.95:
 new_uptime = min(0.99, node.uptime + 0.05)
 node.update_health(uptime=new_uptime)

 actions_taken.append({
 "type": "reliability_improvement",
 "node_id": node.node_id,
 "old_uptime": node.uptime,
 "new_uptime": new_uptime
 })

 logger.info("Improved reliability for selected nodes")

 # Record optimization results
 optimization_result = {
 "timestamp": time.time(),
 "consensus_value": consensus["consensus_value"],
 "initial_state": current_metrics,
 "optimized_state": optimized_state,
 "improvements": improvements,
 "actions_taken": actions_taken,
 "verification_hash": self.spiral.get_current_hash()
 }

 logger.info(f"Network optimization completed with {len(actions_taken)} actions")

 return optimization_result

 def get_network_state(self) -> Dict[str, Any]:
 """
 Get the current state of the network.

 Returns:
 Dict[str, Any]: Current network state
 """
 nodes_state = {node_id: node.to_dict() for node_id, node in self.nodes.items()}

 # Calculate overall metrics
 metrics = self.calculate_network_metrics()

 return {
 "network_id": self.network_id,
 "network_name": self.network_name,
 "timestamp": time.time(),
 "node_count": len(self.nodes),
 "metrics": metrics,
 "nodes": nodes_state,
 "allocations": self.allocations,
 "consensus_history": self.consensus_history[-5:] if self.consensus_history else [],
 "verification_hash": self.spiral.get_current_hash()
 }

 def generate_ipfs_record(self) -> Dict[str, Any]:
 """
 Generate a record for IPFS storage.

 Returns:
 Dict[str, Any]: IPFS record data
 """
 # Get current network state
 network_state = self.get_network_state()

 # Create IPFS-suitable record (simplified)
 ipfs_record = {
 "network_id": self.network_id,
 "network_name": self.network_name,
 "timestamp": int(time.time()),
 "node_count": len(self.nodes),
 "metrics_summary": {
 k: round(v, 4) for k, v in network_state["metrics"].items()
 },
 "consensus_value": self.consensus_history[-1]["consensus_value"] if self.consensus_history else 0,
 "active_allocations": len(self.allocations),
 "verification_hash": self.spiral.get_current_hash(),
 "previous_hash": self.spiral.hash_chain[-2] if len(self.spiral.hash_chain) > 1 else None,
 "tru_alpha_signature": hashlib.sha256(f"{self.network_id}-{self.spiral.get_current_hash()}".encode()).hexdigest()
 }

 logger.info(f"Generated IPFS record for network {self.network_id}")

 return ipfs_record


# Example usage
if __name__ == "__main__":
 # Create a decentralized resource allocation system
 network = DecentralizedResourceAllocation(network_name="Global-AI-Compute-Network")

 # Create and add some nodes
 nodes = [
 ResourceNode(
 node_id=f"node-{i}",
 capacity={
 "CPU": 64.0 + (i % 3) * 16.0,
 "GPU": 8.0 + (i % 5) * 2.0,
 "RAM": 256.0 + (i % 4) * 64.0,
 "Storage": 2048.0 + (i % 3) * 512.0
 },
 location=["us-east", "us-west", "eu-central", "ap-southeast", "sa-east"][i % 5],
 node_type=["compute", "storage", "specialized"][i % 3]
 )
 for i in range(10)
 ]

 for node in nodes:
 network.add_node(node)

 # Make some allocation requests
 allocation_requests = [
 {
 "request_id": f"req-{i}",
 "resources": {
 "CPU": 8.0 + (i % 4) * 4.0,
 "GPU": 1.0 + (i % 3),
 "RAM": 32.0 + (i % 3) * 16.0,
 "Storage": 128.0 + (i % 4) * 64.0
 },
 "location_preference": ["us-east", "eu-central", None, None, "ap-southeast"][i % 5],
 "node_type_preference": ["compute", None, "specialized"][i % 3],
 "priority": 1 + (i % 10)
 }
 for i in range(20)
 ]

 # Process allocation requests
 for request in allocation_requests:
 result = network.allocate_resources(request)
 print(f"Allocation request {request['request_id']}: {result['status']}")

 # Reach consensus and optimize network
 consensus_result = network.reach_consensus()
 print(f"Consensus reached: {consensus_result['consensus_reached']} with value {consensus_result['consensus_value']:.4f}")

 optimization_result = network.optimize_network()
 print(f"Network optimization completed with {len(optimization_result['actions_taken'])} actions")

 # Generate IPFS record
 ipfs_record = network.generate_ipfs_record()
 print("IPFS Record:", json.dumps(ipfs_record, indent=2))