# AI_AUDIT — Team AI Verification Log

CS 4379H Cryptography, Fall 2026

**Group #: 1**
| Full Name | GitHub nickname |
| -------------- | --------------- |
| Tina Carter | a-gr1f |
| Adiyat Abubakirov | adiyat-abubakirov |
| Justin Williams | SeidaSecurity |


**Paper:** Accelerating SLH-DSA by Two Orders of Magnitude with a Single Hash Unit (2nd paper on recommended list)

**AI assistant(s) used (name and version, e.g., "ChatGPT (GPT-5), Claude (Sonnet 5)"):** Qwen3.7-Plus Deep Think, Copilot Deep Think, GPT-5.6 Sol Deep Think, Deepseek Deep Think.

## How to use this log

AI use in this project is required, not banned. Every AI output your team relies on (a claim you repeat, a citation you include, code you commit, an idea you adopt) must appear here as one row, whether or not it turned out to be correct. You do not need to log throwaway drafts or outputs you discarded without using.

One log per team, kept in the root of your GitHub repository and updated as you work, not reconstructed at the end. Commit history should show it growing over the semester. The completeness and honesty of this log is graded under Project Code; catching an AI error earns credit, hiding one costs it.

## Categories

| Code | Category |
|------|----------|
| FC | Fabricated citation (paper, author, or venue that does not exist or does not say what was claimed) |
| NA | Nonexistent API or function (library, method, flag, or parameter that does not exist) |
| MR | Misstated result (real source, but the number, finding, or claim is wrong) |
| CW | Code runs but is wrong (executes without error, output is incorrect) |
| OC | Overclaim (true in a narrow case, stated as general) |
| OK | Verified correct (the output survived verification) |

## Log

*Role is one of: Reviewer, Archaeologist, Student Researcher, Reproducibility Checker, Quanta Correspondent. Add rows as needed.*

| # | Date | Role | What the AI claimed or produced (short quote or summary) | Category | Verified? (yes / no / partially) | How you checked it (source, test, experiment) | Team member |
|---|------|------|----------------------------------------------------------|----------|----------------------------------|------------------------------------------------|-------------|
| 1 | 10/04 | Reviewer | Accelerating hash functions alone is insufficient and that optimizing SLH-DSA-specific operations can produce much greater performance improvements. | OK | yes | The top-line on this page summarizes the main point of the paper. The first part of the paper (Section 1.1) explicitly states "It seems probable that in hardware a general-purpose hash accelerator can rapidly increase the performance of an SLH-DSA implementation (by about a factor of 10)." And, there is good reason to believe that a "second order of magnitude" (100) speed-up can be achieved by offloading the SLH-DSA-specific Winternitz iteration. | Adiyat Abubakirov |
| 2 | 10/04 | Reviewer | Highlight "300x faster than unaccelerated microcontrollers" as the primary performance achievement. | OC | yes | The central comparative argument of the paper might not be addressed by the AI. Abstract and Section 1.1 both suggest generic hash accelerators usually yield a tenfold speedup. But the main academic contribution seems to be achieving a second order of magnitude (100x) speedup over other RoT hash accelerators through algorithm-hardware co-design and the claim in Section 7 that SLH-DSA "s" verification outperforms ECDSA/Dilithium. | Adiyat Abubakirov |
| 3 | 10/04 | Reviewer | Protection against fault-injection attacks remains necessary future work. | FC | yes | Like Copilot, it is also a superficial reading. While the Authors acknowledge the potential project of FI protection in Section 6.5, the AI seems to fail to contextualize it at least in terms of architecture. The authors list out a complete plan of how this can be achieved by instantiate two or more copies of SLotH redundantly and the small size of the system makes this anticipated mitigation plausible. | Adiyat Abubakirov |
| 4 | 10/04 | Reviewer | The lack of fault-injection countermeasures is an important limitation that should be addressed before the accelerator is used in security-critical environments. | OC | yes | Probably the AI interprets it as a benign "missing feature" defect, but as Section 6.5 clarifies in no uncertain terms, SLH-DSA is vulnerable to faults - a faulted signature still proves correct, so naive safeguards do not suffice. This is correctly recognised by the authors: traditional protection requires duplicate (or redundant) hardware, which is entirely feasible for the 155KGE area of SLotH, and has just been planned as future work, rather than omitted. | Adiyat Abubakirov |
| 5 | 10/04 | Student Researcher | Software Simulation of Fault-Tolerant SLH-DSA Signing | FC | yes | Additionally, software cannot reliably emulate physical fault attack techniques, such as instruction skipping or voltage glitches. Clearly, the document states that basic post-signing verification won't work for such hardware faults. | Adiyat Abubakirov |
| 6 | 10/04 | Student Researcher | Secure Boot Simulator Using SLH-DSA | OK | yes | For this reason, this software project is both useful and feasible, by simply using the core use case illustrated in the paper with open-source SLH-DSA implementations without the required hardware. | Adiyat Abubakirov|
| 7 | 10/04 | Student Researcher | Comparing SLH-DSA Parameter Sets | OK | yes | All 12 parameter sets' performance, key sizes, and signature sizes are all explicitly compared in the paper with a detailed quantitative analysis and tables, making a software dashboard more of a data visualization than a total new dataset. | Adiyat Abubakirov |
| 8 |10/7 |Image |images for quantum correspondent presentation | OK |Yes (verified) | visual conformation related to the prompt | Justin |
| 9 | | | | | | | |
| 10 | | | | | | | |

## End-of-semester summary (fill in before the final demo)

- Total AI outputs logged: ______
- Verified correct: ______
- Failed verification: ______

### The two most consequential AI failures (present these in Task 6, lessons learned)

**Failure 1:**

**Failure 2:**

### Which verification habit saved your team the most time?
