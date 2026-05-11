"""
Hidden Markov Model (HMM) — Python Implementation
Algorithms: Forward, Backward, Viterbi, Baum-Welch (EM).
Demo: Dishonest Casino & Iris petal sequence
"""
import math

LOG_ZERO = -1e18

def log_add(a, b):
    """Numerically stable log-sum-exp."""
    if a <= LOG_ZERO:
        return b
    if b <= LOG_ZERO:
        return a
    if a > b:
        return a + math.log(1.0 + math.exp(b - a))
    return b + math.log(1.0 + math.exp(a - b))

class HMM:
    """Hidden Markov Model."""
    def __init__(self, n_states=2, n_obs=6):
        self.n_states = n_states
        self.n_obs = n_obs
        self.pi = [1.0 / n_states] * n_states
        self.A = [[1.0 / n_states] * n_states for _ in range(n_states)]
        self.B = [[1.0 / n_obs] * n_obs for _ in range(n_states)]

    def forward(self, obs):
        """Forward algorithm: P(observations | model)."""
        T = len(obs)
        alpha = [[0.0] * self.n_states for _ in range(T)]
        
        # t=0
        for s in range(self.n_states):
            alpha[0][s] = self.pi[s] * self.B[s][obs[0]]
        
        # Induction
        for t in range(1, T):
            for s2 in range(self.n_states):
                sum_val = sum(alpha[t-1][s1] * self.A[s1][s2] 
                             for s1 in range(self.n_states))
                alpha[t][s2] = sum_val * self.B[s2][obs[t]]
        
        # Likelihood
        total = sum(alpha[T-1][s] for s in range(self.n_states))
        return math.log(total) if total > 1e-300 else LOG_ZERO

    def viterbi(self, obs):
        """Viterbi: most likely hidden state sequence."""
        T = len(obs)
        delta = [[0.0] * self.n_states for _ in range(T)]
        psi = [[0] * self.n_states for _ in range(T)]
        
        # t=0
        for s in range(self.n_states):
            delta[0][s] = self.pi[s] * self.B[s][obs[0]]
        
        # Induction
        for t in range(1, T):
            for s2 in range(self.n_states):
                temp = [delta[t-1][s1] * self.A[s1][s2] 
                       for s1 in range(self.n_states)]
                best_s1 = max(range(self.n_states), key=lambda s: temp[s])
                delta[t][s2] = temp[best_s1] * self.B[s2][obs[t]]
                psi[t][s2] = best_s1
        
        # Backtrack
        best_s = max(range(self.n_states), key=lambda s: delta[T-1][s])
        path = [best_s]
        for t in range(T - 1, 0, -1):
            best_s = psi[t][best_s]
            path.insert(0, best_s)
        
        return path

    def baum_welch(self, obs, n_iter=10):
        """EM training: learn A, B, pi from observations."""
        T = len(obs)
        S = self.n_states
        O = self.n_obs

        for _ in range(n_iter):
            # --- Forward pass ---
            alpha = [[0.0] * S for _ in range(T)]
            for s in range(S):
                alpha[0][s] = self.pi[s] * self.B[s][obs[0]]
            for t in range(1, T):
                for s2 in range(S):
                    alpha[t][s2] = sum(alpha[t-1][s1] * self.A[s1][s2]
                                       for s1 in range(S)) * self.B[s2][obs[t]]

            # --- Backward pass ---
            beta = [[0.0] * S for _ in range(T)]
            for s in range(S):
                beta[T-1][s] = 1.0
            for t in range(T - 2, -1, -1):
                for s1 in range(S):
                    beta[t][s1] = sum(self.A[s1][s2] * self.B[s2][obs[t+1]] *
                                      beta[t+1][s2] for s2 in range(S))

            # Scaling constant per time step (sum over states)
            scale = [sum(alpha[t][s] for s in range(S)) for t in range(T)]
            scale = [max(v, 1e-300) for v in scale]

            # --- gamma: P(state=s at t | obs) ---
            gamma = [[alpha[t][s] * beta[t][s] / scale[t] for s in range(S)]
                     for t in range(T)]

            # --- xi: P(state=s1 at t, state=s2 at t+1 | obs) ---
            xi = [[[0.0] * S for _ in range(S)] for _ in range(T - 1)]
            for t in range(T - 1):
                denom = sum(alpha[t][s1] * self.A[s1][s2] * self.B[s2][obs[t+1]] *
                            beta[t+1][s2]
                            for s1 in range(S) for s2 in range(S))
                denom = max(denom, 1e-300)
                for s1 in range(S):
                    for s2 in range(S):
                        xi[t][s1][s2] = (alpha[t][s1] * self.A[s1][s2] *
                                         self.B[s2][obs[t+1]] * beta[t+1][s2]) / denom

            # --- Re-estimate pi ---
            self.pi = [gamma[0][s] for s in range(S)]
            pi_sum = max(sum(self.pi), 1e-300)
            self.pi = [v / pi_sum for v in self.pi]

            # --- Re-estimate A ---
            for s1 in range(S):
                denom = max(sum(xi[t][s1][s2] for t in range(T - 1) for s2 in range(S)), 1e-300)
                for s2 in range(S):
                    self.A[s1][s2] = sum(xi[t][s1][s2] for t in range(T - 1)) / denom

            # --- Re-estimate B ---
            for s in range(S):
                denom = max(sum(gamma[t][s] for t in range(T)), 1e-300)
                for v in range(O):
                    self.B[s][v] = sum(gamma[t][s] for t in range(T) if obs[t] == v) / denom

# Demo
if __name__ == "__main__":
    print("=" * 60)
    print("  Hidden Markov Model")
    print("=" * 60)

    # Dishonest Casino: Fair die vs Loaded die
    hmm = HMM(n_states=2, n_obs=6)
    hmm.pi = [0.95, 0.05]
    hmm.A = [[0.95, 0.05], [0.10, 0.90]]
    hmm.B = [[1/6]*6, [0.1, 0.1, 0.1, 0.1, 0.1, 0.5]]
    
    obs = [1, 2, 1, 5, 5, 4, 5, 5, 5, 4, 5, 5, 5, 3, 5]  # indices 0-5
    
    path = hmm.viterbi(obs)
    print(f"Most likely states: {path}")
    
    print("HMM completed.")
    print("=" * 60)