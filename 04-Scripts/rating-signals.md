# Rating Signals: Real Claims vs. Garbage

Framework for scoring leads, calls, and claims. Derived from patterns across 2,800+ calls — what separates the claims CW successfully works from the ones that waste back-office hours.

---

## Hard Disqualifiers (Instant No)

These kill the claim immediately. Don't waste time.

| Signal | Why It's a Disqualifier |
|--------|------------------------|
| **Renter, not homeowner** | Cannot file property insurance claims on a rental |
| **No insurance policy** | Nothing to claim against |
| **Claim outside statute of limitations** | Typically 2 years for property claims (varies by state) — no legal standing |
| **Already signed with another PA and won't cancel** | Cannot have two PAs on same claim |
| **Used insurance-preferred contractor for full rebuild** | CW "can't help anymore" with the rebuild portion — no room to negotiate |
| **Claim value clearly under $10k** | Below CW's minimum threshold — cost to work exceeds recovery |

---

## Lead Rating Signals (1-10)

**Is this person worth pursuing?**

### Strong Lead (8-10)
- Homeowner (name on policy) ✓
- Has an active, open claim ✓
- Frustrated with insurance company (motivated to act) ✓
- Has documentation (photos, estimates, denial letter) ✓
- Claim is recent (within 6 months) ✓
- Engages on the call — asks questions, provides info ✓
- Ready to sign or close to it ✓
- Has a contractor estimate showing gap vs. insurance offer ✓

### Medium Lead (5-7)
- Homeowner but claim details unclear
- Interested but "needs to think about it" or consult spouse
- Has some documentation but not complete
- Claim is 6-18 months old
- Cooperative but passive — needs follow-up to close
- Insurance hasn't formally denied yet (unclear status)

### Weak Lead (1-4)
- Unclear if they're the policyholder
- Very old claim (18+ months, approaching statute)
- No documentation and no willingness to gather it
- Shopping around, asking about competitors
- Hostile or uncooperative tone
- Claim value appears very low
- Already started or completed repairs with no photos
- "I'll think about it" with no specific follow-up commitment

---

## Call Rating Signals (1-10)

**Was this call productive?**

### High-Quality Call (8-10)
- All key information collected (policy #, claim #, DOL, insurance co, address, email)
- Claim type and status identified
- Value estimate established (customer estimate or contractor quote)
- Objections raised AND resolved
- Clear next step established (contract sent, follow-up scheduled)
- Customer emotional state improved during call (frustrated → hopeful/committed)
- Close attempted — whether successful or not

### Medium Call (5-7)
- Some information collected but gaps remain
- Claim type identified but status unclear
- Objections raised, some unresolved
- Customer engaged but not committed
- Follow-up needed to complete intake
- No close attempted (document collection call, status update)

### Low-Quality Call (1-4)
- Minimal information gathered
- Customer disengaged or hostile throughout
- Major objections unresolved (trust, cost)
- No clear next step
- Customer explicitly declined or went cold
- Technical issues (bad connection, wrong number, voicemail)

---

## Claim Rating Signals (1-10)

**Is this claim viable and worth pursuing?**

### High-Value Claim (8-10)

**Water**:
- Sudden pipe burst or appliance overflow (clearly covered event)
- Multiple rooms affected, mold present
- Customer displaced (ALE recovery opportunity)
- Insurance offered $10-20k but contractor quotes $50-100k+
- Plumber's report confirming sudden cause
- Photos before and after remediation

**Roof**:
- Documented storm/hail event in the area
- Roof is 15+ years old with discontinued materials (full replacement argument)
- Insurance claims "wear and tear" but damage is clearly storm-related
- Interior damage present (expands claim beyond just roof)
- Contractor estimates $40-60k+ for full replacement
- Insurance offered patch repair or low ACV

**Fire**:
- Total or near-total loss (policy limits in play)
- Contents list started with high-value items
- Customer displaced with documented ALE expenses
- Fire department report available
- Rebuild estimate exceeds $100k
- Insurance using preferred vendor doing cheap work

**Misc**:
- Clear cause of loss with documentation (police report, engineer report)
- High-value property or commercial property
- Insurance miscategorized the claim (fight the category = easy win)
- Business income loss with clean tax records

### Medium Claim (5-7)
- Damage is real but value is moderate ($20-50k range)
- Some documentation gaps but recoverable
- Insurance has paid something but clearly underpaid
- Claim is somewhat old (6-12 months) but within statute
- Customer has done some repairs but has photos
- Verbal denial only (easier to challenge than written)

### Low-Value/Risky Claim (1-4)
- Damage appears minimal or cosmetic
- No documentation and repairs already done
- Insurance denial appears well-founded (pre-existing, maintenance)
- Claim value likely under $20k total
- Customer unreliable — can't provide basic info, doesn't follow through
- Slow leak or gradual damage (hard to prove sudden event)
- Multiple prior adjusters/attorneys who couldn't move it

---

## Dollar Amount Estimation Signals

Don't give a single number. Give a range based on these indicators:

### Value Amplifiers (multiply contractor quote by 2-3x)
- Insurance company's initial offer is dramatically lower than contractor quotes
- Multiple types of damage (structural + contents + ALE)
- Discontinued materials requiring full replacement
- Policy limits are high relative to damage
- Customer has strong documentation
- Claim is clean — no complications, no prior adjusters

### Value Reducers (stay closer to 1-1.5x contractor quote)
- Insurance has already paid a reasonable amount
- Damage is limited in scope
- Cash value policy (not replacement cost)
- Repairs already completed
- Missing documentation for key items
- Claim is old (less leverage)

### Value Ranges by Type (from actual calls)
| Type | Insurance Typically Offers | CW Typically Targets | Recovery Range |
|------|--------------------------|---------------------|---------------|
| Water | $7,000 - $20,000 | $30,000 - $100,000+ | 2-4x insurer offer |
| Roof | $2,800 - $16,000 | $40,000 - $60,000 | 2-3x insurer offer |
| Fire | $10,000 - $45,000 | $100,000 - $500,000 | 3-10x insurer offer |
| Misc | $1,000 - $7,000 | $25,000 - $78,000 | 3-10x insurer offer |

---

## Action Summary Decision Tree

After rating, every call should produce one of these actions:

```
Is the customer a homeowner with active insurance?
  ├─ NO → Disqualify. Log reason. End call politely.
  └─ YES → Is the claim value likely $20k+?
              ├─ NO → Disqualify. "This claim is too small for our firm." Refer if possible.
              └─ YES → Is the customer ready to sign?
                          ├─ YES → Send contract NOW. Walk through DocuSign on the call.
                          ├─ MAYBE → Schedule specific follow-up within 48 hours.
                          │           Send info they asked for (reviews, license, contract preview).
                          └─ NO → Tag for nurture sequence by claim type.
                                   Set 7-day follow-up reminder.
```

---

## Red Flag → Action Mapping

| Red Flag | Severity | Action |
|----------|----------|--------|
| Renter | Fatal | Disqualify immediately |
| Claim too old (>2 years) | Fatal | Disqualify — check exact statute first |
| Already has PA who won't release | Fatal | Can't proceed — explain they need to cancel first |
| Under $10k claim | Fatal | Decline politely |
| No photos + repairs done | High | Proceed with caution — may not be viable |
| Verbal denial only | Low | Good sign — easier to challenge than written |
| Mortgage on property | Low | Not a problem — just complicates payment |
| Missing some docs | Low | CW helps collect — very manageable |
| Old claim (1-2 years) | Medium | Proceed with urgency |
| Prior bad experience with another PA | Medium | Empathize, differentiate CW, be transparent |
| Customer consulting spouse/attorney | Medium | Offer 3-way call, set specific follow-up |
| Insurance-referred contractor | Medium | Explain bias, recommend independent contractor |

---

## Source

Synthesized from 28 batch reports covering 2,800+ successful Claim Warriors sales calls. Value ranges from actual customer and rep discussions in call transcripts.
