# Coverage Matrix

Use this to ensure your eval scope matches real usage.

| Dimension | Examples |
|---|---|
| Task types | conversation, nl_data_analysis, json_generation |
| Topics | brainstorming, role-play, clustering, summarisation |
| Risk tags | safety, off-task, data privacy, refusal quality |
| Languages | en, ms, zh, ta |
| User segments | novice, power user, mixed |
| Context quality | rich context, sparse context, conflicting context |

## Recommended sampling
- random sampling by topic
- ensure minimum coverage per language + task type
- add a "challenge set" for known failure modes
