# Gemini Flash Extraction Rubric

You are analyzing call transcripts from Claim Warriors, a public adjusting firm that helps homeowners fight insurance companies for fair claim payouts. Every transcript is from a customer who eventually signed a contract — these are all successful sales calls.

Your job: extract SPECIFIC PATTERNS from each transcript. Do NOT summarize. Extract exact quotes and specific instances.

## Context

- **Claim Warriors** represents homeowners against insurance companies
- **Claim types**: Water damage, Roof damage, Fire damage, Miscellaneous (vandalism, theft, etc.)
- **Claim statuses**: New (just filed), Denied (insurance said no), Underpaid (insurance paid too little)
- **Speaker labels**: [Speaker 1] and [Speaker 2] — one is the CW rep, one is the customer. Identify which is which from context.
- All calls are from customers who eventually signed — so every call is a "win" we can learn from

## Extract These Patterns

For each transcript, output a JSON object with these fields:

### 1. call_metadata
```json
{
  "claim_type": "water|roof|fire|misc|unknown",
  "claim_status": "new|denied|underpaid|unknown",
  "estimated_value": "dollar amount if mentioned, null otherwise",
  "call_purpose": "intake|follow_up|negotiation_update|document_collection|other"
}
```

### 2. opener
How did the rep start the call? What was the customer's initial tone?
```json
{
  "rep_opener": "exact quote of first substantive thing rep says",
  "customer_initial_tone": "cooperative|skeptical|frustrated|confused|eager",
  "customer_first_response": "exact quote"
}
```

### 3. qualification_questions
Every question the rep asked to assess the claim. In order.
```json
[
  {
    "question": "exact quote",
    "timing": "early|mid|late in the call",
    "purpose": "assess_value|assess_viability|collect_info|identify_type|red_flag_check",
    "customer_answer_summary": "brief summary of what customer said"
  }
]
```

### 4. objections_and_responses
Every time the customer pushed back, hesitated, or raised a concern.
```json
[
  {
    "objection": "exact quote or close paraphrase",
    "objection_category": "cost|trust|time|complexity|prior_bad_experience|already_have_adjuster|claim_too_old|other",
    "rep_response": "exact quote of how rep handled it",
    "response_strategy": "empathy|reframe|social_proof|urgency|education|direct_answer",
    "resolved": true/false
  }
]
```

### 5. close_attempts
Every time the rep moved toward signing or commitment.
```json
[
  {
    "close_attempt": "exact quote",
    "close_type": "direct_ask|assumptive|summary|urgency|trial",
    "timing": "early|mid|late",
    "customer_response": "exact quote",
    "successful": true/false
  }
]
```

### 6. red_flags_discussed
Any mention of factors that make a claim risky or low-value.
```json
[
  {
    "red_flag": "description",
    "category": "old_claim|low_value|prior_adjuster|inflated_damage|missing_documentation|policy_issue|other",
    "how_rep_handled": "what rep said or did about it"
  }
]
```

### 7. value_signals
Anything that indicates the claim's dollar value or the rep's assessment of it.
```json
[
  {
    "signal": "exact quote or description",
    "estimated_value_range": "if inferable",
    "who_mentioned": "rep|customer"
  }
]
```

### 8. information_collected
What specific data points did the rep collect during the call?
```json
[
  "insurance_company_name",
  "policy_number",
  "date_of_loss",
  "type_of_damage",
  "prior_claim_history",
  "current_payout_amount",
  "denial_reason",
  "photos_available",
  "other_adjusters_involved"
]
```

### 9. emotional_dynamics
How did the customer's emotional state change during the call?
```json
{
  "initial_state": "frustrated|hopeful|skeptical|confused|angry|neutral",
  "turning_point": "what moment shifted the customer's attitude (exact quote if possible)",
  "final_state": "confident|committed|still_skeptical|relieved|excited",
  "rep_empathy_moments": ["exact quotes where rep showed empathy or built rapport"]
}
```

### 10. type_specific_details
Claim-type-specific information that came up.
```json
{
  "water": {
    "source": "pipe_burst|storm|flood|other",
    "mold_mentioned": true/false,
    "remediation_discussed": true/false
  },
  "roof": {
    "cause": "wind|hail|storm|age",
    "inspection_mentioned": true/false,
    "wear_vs_storm_debate": true/false
  },
  "fire": {
    "smoke_damage": true/false,
    "contents_loss": true/false,
    "displacement_discussed": true/false
  }
}
```

## Rules

1. EXTRACT, don't summarize. Use exact quotes whenever possible.
2. If a pattern doesn't appear in a transcript, return an empty array or null — don't fabricate.
3. If you can't determine claim type or status, say "unknown" — don't guess.
4. Short calls (<2 minutes) may only have metadata and a few fields. That's fine.
5. Include the `ghl_message_id` and `ghl_contact_id` from the input data so extractions can be linked back.

## Output Format

Return a JSON array — one object per transcript — each containing all 10 sections above plus the message/contact IDs.
