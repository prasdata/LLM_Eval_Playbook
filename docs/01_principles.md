# Principles for LLM Evaluation (AI Product Management)

This document outlines the core principles for evaluating LLM features in production. These principles ensure evaluations are scalable, reliable, and aligned with real-world product needs.

## 1. Bulk Testing Over Anecdotes

- **Scale**: Evaluate across hundreds of de-identified cases from production logs to capture representative usage patterns.
- **Coverage**: Include typical flows, edge cases, and high-risk scenarios to ensure comprehensive assessment.
- **Regression Tracking**: Monitor performance across iterations to catch declines early.

## 2. Pass/Fail Rubrics for Speed and Clarity

- **Efficiency**: Use binary pass/fail criteria that enable quick interpretation and automation.
- **Release Gating**: Set clear thresholds for deployment decisions, reducing ambiguity in go/no-go calls.
- **Definition of Success**: Force teams to explicitly define what "good" means for each feature.

## 3. LLM-as-Judge with Human Calibration

- **Scalability**: Leverage LLMs as judges to evaluate outputs at scale without manual review for every case.
- **Human Oversight**: Maintain integrity through:
  - Human-defined evaluation criteria
  - Sampled human review of judge outputs
  - Continuous adjustment of rubrics based on judge performance and drift
- **Balanced Approach**: Combine automation with human expertise to ensure accuracy and fairness.

## 4. Multi-Judge Setup to Reduce Bias

- **Bias Mitigation**: Use two or more judges to minimize single-model biases and inconsistencies.
- **Ambiguity Detection**: Surface cases where judges disagree, highlighting areas needing clearer criteria.
- **Prioritization**: Flag disagreed-upon cases for human review, optimizing limited human resources.
