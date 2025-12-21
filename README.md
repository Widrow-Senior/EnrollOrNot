# EnrollOrNot

**Rule-based, explainable eligibility screening for clinical trials and real-world evidence (RWE) studies.**

This solution enables transparent, auditable, and traceable patient eligibility assessment — without black-box models or hidden logic.

Built for the **Xplore Intelligence Hackathon**, it demonstrates how explicit rules + structured data extraction can replace opaque AI in high-stakes clinical decision support.

---

## ✅ Key Features

- **Fully rule-based engine** — eligibility logic defined in human-readable YAML
- **End-to-end traceability** — every decision links to source data and original clinical text
- **Two-block support**:
  - **Block 1**: DAPA-HF & SIGIR-20141 (structured notes + expert labels)
  - **Block 2**: Study W01 & W02 (real-world EHR-like data with missing fields)
- **Handles uncertainty** — clearly flags "not enough information" with missing criteria
- **Zero hallucination risk** — no LLMs, no probabilistic guesses

---

## 🛠️ How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/Widrow-Senior/EnrollOrNot.git
   cd EnrollOrNot

  ## Team

  **Olga Vederinkova**  
  Role: ML Engineer / Project Lead  
  GitHub: [@Widrow-Senior](https://github.com/Widrow-Senior)

  **Anastasia Kulik**
  Role: ML Engineer
  GitHub: https://github.com/akukulik
  
