---
name: Cluster brand is human/LLM assigned, not derived from columns
description: SSDeep cluster brand field is set by LLM suggestion or human override during labeling — never derived from ASN, composition, or any other data column
type: feedback
---

Cluster brand is a LABEL assigned during the labeling workflow (LLM suggest or human override). It is NOT derived from dominant_asn, composition, or any structural data field.

**Why:** The entire point of the cluster library is to browse LABELED data — dispositions, categories, and brands that humans/LLM have assigned. Suggesting that brand should be "Cloudflare" because the ASN is Cloudflare misunderstands the labeling model. A non-content Cloudflare error page cluster might have brand=NULL because it's generic infrastructure noise, or it might have brand="Cloudflare" if a human decided that's meaningful for routing/GTM. The brand field reflects a classification decision, not a data extraction.

**How to apply:** When working with cluster labels (disposition, category, brand), treat them as curated human decisions. Don't propose replacing or deriving them from raw enrichment data. When building views for labeled data, show the labels as-is and provide filtering/grouping on the label values, not on the underlying enrichment columns.
