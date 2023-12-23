# meta_llm_leaderboard
Meta leaderboard combines data from multiple different leaderboards about LLMs.
The focus is primarily on Open LLMs.

Todo:
- Need to figure out why flagged models showing up in HF leaderboard. Need to not filter flagged models in HF clone
- If a model is present on non HF boards and score high, but is not on models.json make sure to flag it
- LMSYS - many models need to have Sizes.(Add non open models?)
- LMSYS Arena  plot needs name positioned.
- allenai/tulu-2-dpo-70b - check what this model is about.. flagged?
- Add to automated change tracker for AgentBench - checkout repo see if a new file is present?
  - Few updates or none.. until see at least one update hold off.
- Track which models are pre-trained. Make HF graph for pretrained models.
- Update rescoring with new weights for Open LLM HF. 
- Open compass diagram 13B messed up. 

Ideas:
- Create across everything chart. Show model that has been evaluated on all leaderboards.
- Add a runner-up (commercial permissible) license to HF best models.
- Work on Supernatural Instruction
- Take another look at HELM (They hardly evaluate recent open models. Not even bother with finetunes)
- https://gpt4all.io/index.html is that Test set worth it?
- https://github.com/defog-ai/sqlcoder sqlcode.. not a leaderboard but nice evaluation
- https://github.com/HazyResearch/legalbench/ Tasks relevant to legal profession.