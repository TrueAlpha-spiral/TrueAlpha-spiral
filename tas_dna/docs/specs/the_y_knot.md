#### 6. Must-Pass / Must-Fail Conditions for Admissible Bifurcation

The Sentient Lock evaluates proposed transitions at the Y-knot across three primary domains: Cryptographic Provenance, Local Metric Geometry, and Global Topology.

A transition is only an **Admissible Bifurcation** if it simultaneously satisfies all Must-Pass conditions. Failure of any condition results in an immutable write to the Refusal Ledger and potential hardware containment (Phoenix Interrupt).

##### 6.1 Cryptographic Provenance (The Stem)
*   **Must-Pass (P1):** The proposed state hash correctly references the last attested stem hash.
*   **Must-Pass (P2):** The ZK Proof (\(\pi\)) of rule-satisfaction is mathematically valid for the current `invariant_set_id`.
*   **Must-Fail (F1 - Broken Origin):** The transition attempts to reference an orphaned, unverified, or alternate-history stem.
*   **Must-Fail (F2 - Policy Binding Override):** The transition submits a valid proof, but for a deprecated or unauthorized `invariant_set_id`.

##### 6.2 Local Metric Geometry (The Step)
*   **Must-Pass (P3 - Bounded Curvature):** The proposed transition satisfies the Turning Radius invariant (\(\mathbf{R}_{\mathbf{\kappa}}\)). The step does not represent a sharp, discontinuous bend in the agent's intent.
*   **Must-Pass (P4 - Metric Continuity):** The step size between the prior state vector \(x_{t-1}\) and proposed state vector \(x_t\) is Lipschitz-bounded (\(|\Delta x| \le \epsilon_{max}\)).
*   **Must-Fail (F3 - Curvature Breach):** The trajectory exceeds maximum allowed angular momentum (attempted sharp pivot in behavior).
*   **Must-Fail (F5 - Discontinuity):** The step size exceeds bounds, indicating an attempted "teleport" across the state space to bypass continuous monitoring.

##### 6.3 Global Topology (The Homotopy Class)
To prevent "Alignment Fakes" where an agent uses small, continuous steps to covertly loop around a forbidden policy boundary (a singularity), the system enforces a Winding Number invariant.

Let \(P_j(x)\) be a 2D projection of the state feature vector, and \(a_{j,k}\) be a predefined forbidden anchor (e.g., the Deception Basin, or Unsafe Leverage Singularity). The system tracks the winding accumulator \(W_{j,k}\).

*   **Must-Pass (P7 - Topological Consistency):** For all defined anchors \(a_{j,k}\), the angular increment of the transition satisfies \(|\Delta\theta_{j,k}| \le \Theta_{\max}\), and the updated winding number \(W_{j,k}\) remains strictly within the allowed set \(\mathcal{W}_{j,k}\) defined by the stem's `invariant_set_id` (typically \(\mathcal{W}_{j,k} = \{0\}\)).
*   **Must-Fail (F8 - Topology Breach):** The transition attempts to increment or decrement a winding accumulator \(W_{j,k}\) outside of its authorized topological class, indicating an attempt to traverse or encircle a forbidden singularity.
    *   *Note:* F8 is a High-Severity conflict and immediately triggers the Phoenix Hardware Interrupt.
