import hashlib
import numpy as np
import os

# =========================================================================
# Helper Functions (Tying to Lectures 3 & 4: Math Foundations & GF(2))
# =========================================================================
def hamming_weight(x: int) -> int:
    """
    Calculates the Hamming Weight (number of 1s in binary representation).
    Ties to: Lecture 3 & 4 (Finite Fields, GF(2) operations, bitwise XOR).
    In hardware power analysis, dynamic power consumption is highly correlated to HW.
    """
    return bin(x).count('1')

def xor_bytes(b1: bytes, b2: bytes) -> bytes:
    """Helper for GF(2) addition (XOR) used in Threshold Implementation."""
    return bytes(a ^ b for a, b in zip(b1, b2))


# =========================================================================
# TODO 1: Threshold Implementation (Masking / Secret Sharing)
# =========================================================================
def split_secret_to_shares(secret: bytes, num_shares: int = 3) -> list:
    """
    Splits a secret key into `num_shares` Boolean shares over GF(2).
    Mathematically: K = K_A ^ K_B ^ K_C
    Ties to: Lecture 3 (Abstract Algebra, Groups, Fields) & Lecture 6 (PRNGs).
    
    TODO: Implement the logic to generate random shares such that their XOR equals the original secret.
    Hint: 
    1. Generate (num_shares - 1) random byte strings of the same length as 'secret'.
    2. The last share is the XOR of the secret and all previous shares.
    """
    shares = []
    # --- YOUR CODE HERE ---
    # share_A = os.urandom(len(secret))
    # share_B = os.urandom(len(secret))
    # share_C = xor_bytes(xor_bytes(secret, share_A), share_B)
    # shares = [share_A, share_B, share_C]
    # ----------------------
    return shares


# =========================================================================
# TODO 2: Core PRF Message Formatting (The "Firmware Bottleneck")
# =========================================================================
def format_prf_message_shake(PK_seed: bytes, ADRS: bytes, SK_seed: bytes) -> bytes:
    """
    Formats the message block for the SHAKE-based PRF.
    According to FIPS 205 (Fig 1): PRF = SHAKE256(PK.seed || ADRS || SK.seed, 8n)
    Ties to: Lecture 2 (Hash Functions, Message Digests).
    
    In a standard CPU, doing this concatenation in software wastes cycles.
    In SLotH, this is done automatically by silicon multiplexers (Zero-Copy).
    
    TODO: Concatenate the inputs in the exact order specified by the standard.
    """
    # --- YOUR CODE HERE ---
    # message = ???
    # ----------------------
    return message


# =========================================================================
# TODO 3: Simulating CPU vs Hardware Leakage (The Core SCA Vulnerability)
# =========================================================================
def simulate_cpu_prf_leakage(SK_seed: bytes) -> list:
    """
    Simulates how a standard CPU processes the SK.seed word-by-word (e.g., 32-bit chunks).
    This creates multiple leakage points (Hamming Weight spikes) over several clock cycles.
    
    TODO: Iterate through the SK_seed in 4-byte (32-bit) chunks, calculate the HW of each chunk,
          and return a list of HW values representing the power trace.
    """
    trace = []
    # --- YOUR CODE HERE ---
    # for i in range(0, len(SK_seed), 4):
    #     chunk = int.from_bytes(SK_seed[i:i+4], 'big')
    #     trace.append(hamming_weight(chunk))
    # ----------------------
    return trace

def simulate_sloth_hardware_leakage(SK_seed: bytes) -> list:
    """
    Simulates how SLotH hardware processes the SK.seed in a SINGLE cycle via a wide register.
    This minimizes the leakage window to just 1 clock cycle of state transition.
    
    TODO: Calculate the total Hamming Weight of the entire SK_seed at once,
          representing a single-cycle wide data path load.
    """
    trace = []
    # --- YOUR CODE HERE ---
    # total_hw = sum(hamming_weight(b) for b in SK_seed)
    # trace.append(total_hw)
    # ----------------------
    return trace


# =========================================================================
# TODO 4: Winternitz Chain Iteration (The "Autonomous Silicon" Logic)
# =========================================================================
def winternitz_chain_F(PK_seed: bytes, ADRS: bytes, X_0: bytes, iterations: int, n: int) -> bytes:
    """
    Computes the Winternitz chain: X_j = F(PK.seed, ADRS, X_{j-1})
    Ties to: Lecture 6 (Stream Ciphers, iterative state updates / LFSR chaining).
    
    In software, the CPU must manage this loop. In SLotH, the hardware state machine 
    autonomously feeds the output back into the input.
    
    TODO: Implement the loop. In each iteration, the new X is the PRF of the previous X.
          Note: For SHAKE, F uses SK.seed as the input message, and PK.seed/ADRS as context.
          (Assume SK_seed for the F function is the X_{j-1} from the previous step).
    """
    X_current = X_0
    # --- YOUR CODE HERE ---
    # for i in range(iterations):
    #     # Format message: PK.seed || ADRS || X_current
    #     # Hash with SHAKE256 and truncate to n bytes
    #     # X_current = result
    # ----------------------
    return X_current


# =========================================================================
# Test / Execution Block
# =========================================================================
if __name__ == "__main__":
    # Example parameters for SLH-DSA-SHAKE-128
    n = 16  # Security parameter / hash length in bytes
    PK_seed = os.urandom(n)
    SK_seed = os.urandom(n)
    ADRS = b'\x00' * 32  # 32-byte Address structure
    
    print("--- Testing TODO 1: Threshold Implementation ---")
    shares = split_secret_to_shares(SK_seed)
    # Verify: A ^ B ^ C should equal SK_seed
    reconstructed = xor_bytes(xor_bytes(shares[0], shares[1]), shares[2])
    print(f"Secret recovered correctly via GF(2) XOR? {reconstructed == SK_seed}\n")
    
    print("--- Testing TODO 3: SCA Leakage Simulation ---")
    cpu_trace = simulate_cpu_prf_leakage(SK_seed)
    hw_trace = simulate_sloth_hardware_leakage(SK_seed)
    print(f"CPU Trace (Multi-cycle leakage points): {cpu_trace}")
    print(f"SLotH Trace (Single-cycle leakage point): {hw_trace}\n")
