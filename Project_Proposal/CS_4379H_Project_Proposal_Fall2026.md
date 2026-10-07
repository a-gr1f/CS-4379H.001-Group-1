# Project Proposal

**Paper Title:** Accelerating SLH-DSA by Two Orders of Magnitude with a Single Hash Unit (2nd paper on recommended list)

**Group Members:**
| Full Name | GitHub nickname |
| -------------- | --------------- |
| Tina Carter | a-gr1f |
| Adiyat Abubakirov | adiyat-abubakirov |
| Justin Williams | SeidaSecurity |


**Reviewer:**

## Task 1 (10 points)

Write your own high-level overview (like a summary) of the key contributions of the paper that your team has picked (7 pts), then complete the AI Review Disagreement Table below against your review of your paper (3 pts). Write your review before reading the AI review.

### Overview

In this paper, the authors present a high efficiency open-source hash-signature-verification accelerator hardware and firmware/hardware system, tailored to the FIPS 205 SLH-DSA (post-quantum hash-based signature) standard. The paper focuses on the target application of value in constrained Root-of-Trust (RoT) and embedded environments such as Open Titan and Caliptra. The authors have identified that generic hash accelerators successfully increase the SLH-DSA acceleration by about an order of magnitude, yet do not fully utilize the core hash accelerator unit due to tight firmware timeline and message formatting overhead. The authors propose an algorithm-hardware co-design approach where the SLH-DSA specific computation, such as the Winternitz chain iteration, automatic padding, and domain separation (ADRS) formatting, are offloaded onto the hardware.

These results demonstrate an order-of-magnitude improvements in the performance of the verification step: in the highest performance case, SLotH outperforms an unaccelerated microcontroller by up to a factor of 100, and outperforms a generic hash accelerator by a factor of 10. In addition, the paper provides a thorough security analysis, which demonstrates experimentally that implementations of CPU-based SLH-DSA are susceptible to rapid side-channel leakage of the master secret SK.seed, which is reused in numerous PRF invocations, and proposes a Threshold Implementation (TI) of the Keccak core and verifies it using a 100,000-trace TVLA analysis. Overall, the paper shows that, with acceleration via hardware improvement, SLH-DSA "s" (small) parameters would outperform ECDSA and Dilithium for signature verification, making them very attractive for post-quantum secure boot.

### Intellectual Merit

- Algorithm-Hardware Co-design is Critical for Post-Quantum Cryptography: The results imply that just dropping a general-purpose high-performance hash core into a system is not enough for hash-based signature systems. At least orders of magnitude (perhaps 100x) better performance is obtained by exposing the details of the algorithm, such as Winternitz chaining, and by doing iterative padding and key-management at the silicon level.

- Serious Software Side-Channel Attack: The results provide significant experimental results and demonstrate that the software SNH-DSA is severely affected in a malicious physical environment. Due to the high frequency of the master key (SK.seed) reuse in the call to the pseudorandom function (PRF), it will be quickly exposed to the CPU. And it can conclude that hardware key isolation and masking are no more than optional requirements.

- Challenging perceptions of Secure Boot: Quantitative evidence indicates accelerated SLH-DSA "s" variants are likely to be faster at signature verification than comparably-sized ECDSA or Dilithium accelerators. This runs counter to public perception, and provides strong evidence that "conservative" hash-based signatures are suitable for latency-sensitive firmware verification.

- SLH-DSA'S Fault Resilience: The authors admit a major flaw in SLH-DSA signing is its exposure to fault injection. A faulty signature could be validated by leaking enough information to allow future signatures to be forged. This is especially valuable to hardware designers as it shows that simple post-signature validation is not sufficient and that hardware duplication and redundancy is an upgrade.

## AI Review Disagreement Table (3 pts)

_Compare your review with the AI-generated review of your paper. List at least three specific points of comparison._


| AI review | Your assessment (right / shallow / wrong / fabricated) | Evidence from the paper |
| --------------- | --------------- | --------------- |
| Copilot: "The lack of fault-injection countermeasures is an important limitation that should be addressed before the accelerator is used in security-critical environments." | shallow | Probably the AI interprets it as a benign "missing feature" defect, but as Section 6.5 clarifies in no uncertain terms, SLH-DSA is vulnerable to faults - a faulted signature still proves correct, so naive safeguards do not suffice. This is correctly recognised by the authors: traditional protection requires duplicate (or redundant) hardware, which is entirely feasible for the 155KGE area of SLotH, and has just been planned as future work, rather than omitted. |
| GPT-5.6 Sol Think: "Accelerating hash functions alone is insufficient" and that "optimizing SLH-DSA-specific operations can produce much greater performance improvements." | right | The top-line on this page summarizes the main point of the paper. The first part of the paper (Section 1.1) explicitly states "It seems probable that in hardware a general-purpose hash accelerator can rapidly increase the performance of an SLH-DSA implementation (by about a factor of 10)." And, there is good reason to believe that a "second order of magnitude" (100) speed-up can be achieved by offloading the SLH-DSA-specific Winternitz iteration. |
| GPT-5.6 Sol Think: "Protection against fault-injection attacks remains necessary future work." | shallow | Like Copilot, it is also a superficial reading. While the Authors acknowledge the potential project of FI protection in Section 6.5, the AI seems to fail to contextualize it at least in terms of architecture. The authors list out a complete plan of how this can be achieved by instantiate two or more copies of SLotH redundantly and the small size of the system makes this anticipated mitigation plausible. |
| Both Copilot & GPT: Highlight "300x faster than unaccelerated microcontrollers" as the primary performance achievement. | shallow | The central comparative argument of the paper might not be addressed by the AI. Abstract and Section 1.1 both suggest generic hash accelerators usually yield a tenfold speedup. But the main academic contribution seems to be achieving a second order of magnitude (100x) speedup over other RoT hash accelerators through algorithm-hardware co-design and the claim in Section 7 that SLH-DSA "s" verification outperforms ECDSA/Dilithium. |



---

## Task 2 & 3

## Proposed Work and Methodology

**<Student Researcher>**

### Task 2 (5 pts)

**Describe which specific topic from the paper you are investigating in further detail over the next two months and why you picked that topic? Describe how it ties to the topics that we have covered in the class? Which application areas can the idea that you have chosen to be applied to? Complete the AI Idea Appendix below and state whether your chosen topic came from your team or from the AI.**

Over the next two months, our team will be investigating Side-Channel Attack (SCA) Resistance and Threshold Implementation (TI) in Post-Quantum Hash-Based Signatures (specifically SLH-DSA), as detailed in the SLotH paper. 

**Why We Picked This Topic:**
We chose this topic because it exemplifies the most important challenge in the practical implementation of PQC. The SLotH paper explicitly states that their SLH-DSA is perfectly secure in theory, but standard CPU software implementations would almost certainly be insecure in the hands of an attacker in the physical world. The master secret (SK.seed) is used in many calls to the Pseudorandom Function (PRF) and has been shown to exhibit power consumption side-channel leakage in under 1,000 traces. The exploration of how to mitigate this by hardware TI, which splits the secret in Boolean shares and refreshes them in order to prevent leakage, is a fascinating intersection of cryptography and hardware design. It moves the question from "does the math work?" to "can it withstand a physical attack?", which we take to be the hallmark of a solid cryptosystem.

**Connection to class notes:** 
This investigation connects to several foundational concepts we have covered during class:
    - Digital Signatures & Hash Functions (Lecture 2): The SLH-DSA is a digital signature scheme completely constructed from the security properties of cryptographic hash functions (SHA-2 and SHAKE/Keccak). In order to understand the reasoning behind the structure of SLH-DSA, an in-depth prior understanding of a hash function's innate properties (pre-image and collision resistance) is needed. This denotes how significantly hash functions feature to the cornerstone of the SLH-DSA scheme.
    - Abstract Algebra & Finite Fields (Lecture 3 & 4): Threshold schemes are implementable primarily because of secret sharing in a finite field – in this case, GF(2) (where addition is actually an XOR operation). The modular arithmetic and group properties outlined in lectures form the rigorous mathematical foundation that allow a secret key to be divided into shares, such as K = K1 ⊕ K2 ⊕ K_3, and have their various operations maintained without revealing the original value.
    - Pseudorandomness and PRFs (Lecture 6): The signing operation in SLH-DSA relies on a Pseudo-Random Function to stretch the SK.seed into deterministic streams for use in a Winternitz chain; conceptually analogous to the Pseudo-Random Number Generators, and keystreams of symmetric stream ciphers. In particular, the cryptographic needs of a secure PRF seem to be crucial for the proof of the devastating effects of seed leakage.

**Applicaiton Areas:** 
- Root-of-Trust (RoT) SoC secure boot and firmware verify Open Titan and Caliptra System-on-Chip (SoC) system designs that require low area and power budgets while having high security requirements.
- Cyber-Physical Systems (CPS): Connected autonomous vehicles, medical equipment, and IoT infrastructure require lightweight, quantum-resistant security solutions as described in the course intro. These will probably be needed to prevent catastrophic physical failure due to corrupt firmware.
- Post-Quantum Infrastructure: Combining current evaluations by the Market Top on new investment schemes as well as the COVID-19 responses, and the technology common basis of the 2 considerations, the research study of legacy PKI & code-signing certificates requires upgrading through SLH-DSA as well as resilience to classical side-channel assaults with TI (threshold implementation).

**Origin of Our Topic:** 
Our topic originated from our findings. AI tools were utilized to provide summaries of the paper and to help discover potential links to the lecture content. The group chose the paper's focus on the vulnerability to SCA/TI and the implications for the actual real-world RoT (Root of Trust), as this was the key takeaway from a security perspective.

### AI Idea Appendix (required)

_Ask an approved AI assistant for three follow-up project ideas based on your paper, then label and justify each._
| AI-suggested idea | Label (feasible / already published / technically flawed) | One-sentence justification |
| --------------- | --------------- | --------------- |
| Secure Boot Simulator Using SLH-DSA | feasible | By using the core use case illustrated in the paper with open-source SLH-DSA implementations without the required hardware, this software project is both useful and feasible. |
| Comparing SLH-DSA Parameter Sets | already published | All 12 parameter sets' performance, key sizes, and signature sizes are all explicitly compared in the paper with a detailed quantitative analysis and tables, making a software dashboard more of a data visualization than a total new dataset. |
| Software Simulation of Fault-Tolerant SLH-DSA Signing | technically flawed | Software cannot reliably emulate physical fault attack techniques, such as instruction skipping or voltage glitches. Clearly, the document states that basic post-signing verification won't work for such hardware faults. |


---

**<Reproducibility Checker>**

### Task 3 (5 pts)

**As part of the final presentation, you will be required to demonstrate software for one idea presented in the paper or a new idea that you may have based on what you learned from the paper? For the project proposal phase, describe which idea you will be picking and how you plan on approaching this task? Name the AI coding assistant your team will use and describe how you will verify its output. Create your team’s AI_AUDIT (template provided) in your GitHub repository.**

For the final presentation, the team plans to present a Software-Based Side-Channel Leakage Simulator for SLH-DSA PRF Operations. This work is motivated by the key results shown in the SLotH paper, which hypothesizes that CPU-based implementations of the SLH-DSA algorithm will leak the SK.seed in as few as 1,000 power traces, since the key is used across thousands of PRF calls (see the second example in Section 6.1, Figure 6).

**Idea:** 

Instead of the physical FPGA hardware and an oscilloscope (which are not available), a simulator will be provided in Python to simulate the information leakage during SLH-DSA signing at the algorithmic level. The proposed tool will:

- First, the leakage of a 'leaky' CPU-based PRF execution in which SK.seed is processed word-by-word just like in a real CPU. It will simulate the hamming weight power leakage for each intermediate value similarly to the vulnerability illustrated in Figure 6 in \[29\].
- Secondly, it will mimic a 'protected' hardware-isolated PRF execution loading of SK.seed in one cycle loading, which can be performed with the KECC_SKSD register in SLotH. The number of leakage points should be drastically lower.
- Additionally, a simplified TVLA, which applies the Welch's t-test to the simulated traces, will be performed. It is anticipated that the test will statistically prove the CPU version leaks (the t-value is larger than the critical threshold) while the hardware-isolated version does not, following the 100,000-trace TVLA in section 6.2 of the paper.
- Optionally, the tool may also show Boolean secret sharing (Threshold Implementation) of (a variant of) the GF(2) implementation (but THE implementation) using the SK.seed split into `K = KA \oplus KB \oplus K_C` and operated on each share separately. This approach will probably remove any first-order leakage, and naturally uses the (sketch of the) mathematics of the Galois field division and XOR operation from Lecture 3 (Mathematical Foundations) and the PRNG/keystreams from Lecture 6 (Stream Ciphers).

**Our Approach:** 
Phase 1 (Weeks 1–3): Foundation & PRF Implementation:
The implementation of the proposed SLH-DSA Pseudo-Random Function (PRF) based on SHAKE256 can be performed in Python using the pycryptodome or pysha3 library, with careful observation of the exact message formatting described in Fig 1 of the paper. Also, the implementation of the iteration loop for Winternitz chain (X j = F(PK.seed, ADRS, X j-1)) should produce the same signing workload. It is recommended to perform this stage by using the hash function primitives mentioned in Lecture 2, i.e. pre-image resistance, deterministic hash output, and the digital signature pipeline.
Phase 2 (Weeks 4–5): Leakage Simulation Engine:
When building the Hamming weight leakage model, we find HW(intermediate_value) of every intermediate variable of PRF operations and add a Gaussian noise in order to simulate real power traces. In our CPU mode case, from literature, it can be modelled as key being loaded one byte at a time in more clock cycles, providing several leakage points during one PRF execution; meanwhile in our SLotH mode, from literature, it can be modelled as key being loaded in one single clock cycle, thus giving one leakage point in each PRF execution mainly determined by the Hamming distance of the state transition; interestingly this could be related to Lecture 6's discussion of when Linear Feedback Shift Register (LFSR) in stream ciphers is weak to known-plaintext attacks if part of the internal state is leaked, which could be extended to PRF internal state.
Phase 3 (Weeks 6–7): TVLA Analysis & Visualization:
In order to perform the empirical comparison of 'fixed key' versus 'random key' trace sets, the authors recommend that researchers perform Welch's t-test along the lines of Section 6.2 of the paper. In addition, the authors recommend producing plots showing the spikes in t-value for the CPU implementation, which is expected to break the critical value C 4.5 within about 1,000 traces (as opposed to the flat t-value plot for the SLotH-style implementation). Finally, if there is time, the authors recommend including the 3-share TI masking layer, which may be able to push the leakage below the visual level.
Phase 4 (Week 8): Demo & Presentation:
Create an interactive dashboard in which the user is able to change "CPU mode", "SLotH mode" and "TI-masked mode" using a matplotlib or streamlit application. The user should also be able to choose different numbers of simulated traces and watch how the TVLA t-statistics converge in real-time. The research demonstrated that roughly 1,000 simulated traces in CPU mode, SK.seed can be recovered, while the protected modes should be safe.

**Why this idea:** 
The reason why we chose this way instead of using just a 'secure boot simulator' or 'parameter set comparison tool' is that this implementation shows a real cryptographic security vulnerability which has been verified using measurements and subsequently eliminated - and not just a cryptographically functional implementation. In addition, Figure 6 of the study, which shows SK.seed leakage for 1000 traces, was the most interesting 'plot' for the team. Being able to make this figure reproducible in simulation, without a 500 dollar FPGA board and oscilloscope, will likely be the most 'hands-on' and secures-The-security-measure for the class. Furthermore, this would give us the chance to utilize abstract algebra (GF(2) secret sharing) and principles of pseudorandomness from the lecture in an interesting sense, in the setting of a real (post quantum) cryptography problem.

**AI coding assistant & Verification strategy:** 
Our team will use GPT-5.6 Sol (Copilot as fallback) as AI coding assistant & we are going to thoroughly test the functionality by analyzing the mechanism & concepts the AI uses for this simulation program. As well as thoroughly researching internet & paper for non-coding outputs.
