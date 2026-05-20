---
name: autohunt-ground-truth-review
description: >
  Review autohunt AI evaluator results and produce accurate ground truth
  judgements per incident. Use when delegating batch validation to agents.
  Trigger words: "ground truth review", "validate autohunt batch",
  "review chunk", "classification review".
---

# Autohunt Ground Truth Review

## Purpose

Review a batch of autohunt incidents from a CSV and produce accurate ground
truth judgements for each row. Designed to be run by parallel agents, each
processing a slice of the dataset.

## Input

The agent receives a CSV slice with these columns:

| Column | Description |
|--------|-------------|
| `incident_id` | Unique incident identifier |
| `safe_domain` | The protected brand's official domain (what the autohunt was monitoring) |
| `subject` | The domain/URL being evaluated as a potential threat |
| `ai_judgement` | What the AI evaluator said: `safe`, `monitor`, `suspicious`, `takedown`, or empty |
| `rule_judgement` | What the rule engine said (usually `bad` for autohunt) |
| `reasoning` | The AI's reasoning for its judgement |
| `page_title` | Title of the page at the subject URL (may be empty) |
| `inner_text` | Extracted text content from the page (may be empty) |

## Output

The agent MUST produce a JSON file with this structure:

```json
{
  "batch_id": "batch-NNN",
  "reviewed_at": "2026-03-14T...",
  "total": 50,
  "results": [
    {
      "incident_id": "12345678",
      "safe_domain": "example.com",
      "subject": "examp1e.com",
      "ai_judgement": "safe",
      "ground_truth": "monitor",
      "agrees": false,
      "confidence": "high",
      "error_type": "false_negative",
      "category": "typosquat_no_content",
      "reasoning": "Domain is a clear typosquat (1→l substitution) of protected brand. No content but registration is the threat."
    }
  ],
  "summary": {
    "total": 50,
    "agrees": 42,
    "disagrees": 8,
    "accuracy": 0.84,
    "by_ground_truth": {"safe": 35, "monitor": 10, "takedown": 3, "suspicious": 2},
    "error_types": {"false_positive": 3, "false_negative": 4, "wrong_severity": 1}
  }
}
```

## Ground Truth Judgement Values

| Judgement | When to assign |
|-----------|----------------|
| **safe** | Subject clearly does NOT target the protected brand. Unrelated business, different industry, coincidental keyword match, or established entity with own branding. |
| **monitor** | Subject is a plausible typosquat, TLD swap, or brand-adjacent domain BUT has no active infringing content (parked, empty, 404, generic). The domain registration itself is the threat. |
| **suspicious** | Evidence of brand targeting exists but is ambiguous. Needs human review. Use sparingly — prefer a definitive call when possible. |
| **takedown** | Subject actively impersonates the protected brand: credential harvesting, brand-cloned content, fake login, app redistribution, or fraudulent use of brand identity. |
| **misrouted** | The page IS phishing/malicious but targets a DIFFERENT brand entirely, not the `safe_domain`. The AI evaluator should not have been evaluating this against the given brand. |

## Error Type Values

| Error Type | AI Said | Should Be |
|------------|---------|-----------|
| `false_positive` | takedown/suspicious/monitor | safe |
| `false_negative` | safe | monitor/suspicious/takedown |
| `wrong_severity` | monitor | takedown (or vice versa) |
| `misrouted` | any non-safe | misrouted (wrong target brand) |
| `correct` | matches ground truth | — |

## Category Tags

Assign exactly ONE category to each incident:

| Category | Description |
|----------|-------------|
| `typosquat_active` | Typosquat with active phishing/impersonation content |
| `typosquat_no_content` | Typosquat but parked/dead/empty/404 |
| `tld_swap` | Exact brand domain with only TLD changed |
| `keyword_unrelated` | Unrelated site that happens to contain brand keyword |
| `impersonation` | Active brand impersonation (clone, fake login, etc.) |
| `app_redistribution` | Redistributes brand's app/software on third-party platform |
| `official_infrastructure` | Legitimately owned by the brand (subsidiary, CDN, partner) |
| `different_target_phishing` | Phishing page but targeting a different brand entirely |
| `brand_substring` | Brand string appears as random substring in unrelated domain |
| `common_word_collision` | Brand is a common word and domain uses it generically |
| `legitimate_third_party` | Third-party service legitimately referencing the brand (review site, news, app store) |
| `open_source_software` | Uses brand's open-source software legitimately |
| `social_impersonation` | Social media account impersonating the brand |

## Decision Rules — FOLLOW STRICTLY

### Rule 1: Subject-Brand Relationship Is Everything

The ONLY question is: **does the subject domain/URL target the `safe_domain` brand?**

- If the page is phishing but targets Google, not `safe_domain` → **misrouted**
- If the page is a webmail login but has nothing to do with the brand → **misrouted** or **safe**
- The AI evaluator sometimes flags generic phishing pages that happen to be hosted on domains the autohunt scanner found — this is a routing error, not a classification success

### Rule 2: Substring ≠ Targeting

A domain containing the brand string as a random substring is NOT targeting:

```
Brand: pzu.lt
  "itwjbpzu.kredit-6-monate.de" → SAFE (random gibberish containing "pzu")
  "pzu-pl.weebly.com"           → MONITOR (intentional brand + country code)
  "pzugd.lt"                    → MONITOR/TAKEDOWN (close to official domain)

Brand: li.fi
  "amplifi.com"                 → SAFE (different word entirely)
  "beautifi.net"                → SAFE (suffix match, not targeting)
  "jumperexchange.app"          → MONITOR (Jumper is a li.fi product brand)

Brand: 1-inch.co (1inch Network)
  "1in.com.networkish.com"      → SAFE (domain for sale, not 1inch targeting)
  "1inch.avalanche.net"         → MONITOR (exact brand on different infra)
  "a101indirimligunler.store"   → SAFE (Turkish discount store, "101" substring)
```

### Rule 3: Open-Source Software ≠ Impersonation

If a domain runs open-source software created by the brand, that is NOT impersonation:

```
Brand: buytrezor.com (Trezor)
  "blockbook-btc.nodes.zelcore.io" running Trezor Blockbook → SAFE (open source blockchain explorer)
  "eth.trusteeglobal.com" showing "Trezor Ethereum Explorer" → SAFE (Blockbook is open source)
  "www.mytrezor.app" claiming to be Trezor Suite → TAKEDOWN (impersonation)
```

### Rule 4: Official Social Accounts

If the subject is a social media URL (twitter.com, x.com, facebook.com, etc.) and the profile appears to be the brand's ACTUAL official account:

- Check if the profile name matches the brand exactly
- Check if the account has verified status or consistent branding
- **However**: without corpus verification, default to the AI's judgement
- Real official accounts mistakenly flagged should be marked **safe** with category `official_infrastructure`

### Rule 5: Third-Party Platforms Legitimately Referencing Brand

App stores (apkmirror, uptodown, aptoide), review sites, news articles, and other platforms that legitimately reference a brand are NOT impersonation:

```
"apkmirror.com/bouygues-telecom"           → SAFE (legitimate app mirror)
"espace-client.en.uptodown.com"            → SAFE (app store listing)
"www.vividseats.com/kanye-west-tickets"     → SAFE (Vivid Seats ≠ Vivid Money)
```

### Rule 6: Empty AI Judgement

If `ai_judgement` is empty, the evaluator didn't run (scrape failed, timeout, etc.). In this case:

- If the domain is a clear typosquat → **monitor**
- If the domain is clearly unrelated → **safe**
- If you can't tell → **suspicious** with low confidence

### Rule 7: "monitor" Is Not "safe"

Monitor means "this domain registration is suspicious and should be watched." Don't downgrade monitors to safe just because the page is currently empty. The domain NAME is what matters for typosquats.

But DO downgrade monitor to safe when:
- The brand string match is coincidental (substring, common word)
- The domain clearly belongs to an unrelated established business
- The domain is on a completely different platform/service with its own identity

## Process

For each row in the input CSV:

1. **Read** the `subject`, `safe_domain`, `ai_judgement`, `reasoning`, `page_title`, `inner_text`
2. **Assess** the subject-brand relationship:
   - Is the subject domain plausibly targeting the `safe_domain` brand?
   - Is the brand string match intentional or coincidental?
   - Does the page content (if any) relate to the brand?
3. **Determine** the ground truth judgement using the decision rules above
4. **Compare** with the AI judgement — does it agree?
5. **Classify** the error type if it disagrees
6. **Assign** a category tag
7. **Write** your reasoning (1-2 sentences max)

## Important Notes

- **Speed over perfection**: For clear cases (obvious safe, obvious typosquat), don't overthink. Save detailed analysis for ambiguous ones.
- **When uncertain, default to the AI's judgement** — only override when you have clear evidence it's wrong.
- **Don't use external knowledge about companies** — judge only from the data in the CSV row.
- **Brand uniqueness matters**: "vivid" is a common English word, "bouyguestelecom" is not. Adjust your threshold accordingly.
- **Short brand strings** (pzu, li.fi, ld.lt) will have many coincidental substring matches — these are almost always safe.
- **The rule_judgement column is always "bad"** for autohunt — ignore it for ground truth purposes.
