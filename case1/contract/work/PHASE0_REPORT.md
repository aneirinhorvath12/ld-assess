# Phase 0 — Extraction and inventory

Source: `source/project_agreement.pdf`, 236 pp., SHA-256 `83f24d4e…df20cc` (identical to the PDF at the repository root). Schedules from `olrt_source_documents.zip` → `source/schedules/` (10 files).

## 0. Headline finding: the source is the 2019 Amended and Restated agreement

The PDF is not the agreement as signed on 12 February 2013. It is the **Amended and Restated** version, which includes the 2017–2019 Stage 2 amendments (recitals H–L, s. 1.5 "Ring Fencing Principle", DB Co interface provisions, Belfast MSF Expansion, Stage 2 Additional Vehicles). These amendments are spread through the body, not only in the sections you listed. Two consequences:

* Removing them shrinks the body by about **14–16%**, which breaks the ±10% length rule if it's measured against this PDF (see §4.6).
* Section 1.5(b) says the pre-amendment text of the changed definitions is preserved in **Schedule 1, Appendix 8 ("Original Defined Terms")**. That gives an authoritative way to restore the as-signed definitions instead of guessing (§4.3).

## 1. Extraction and word count

`checks/extract_source.py` runs `pdftotext -layout` and then:

* strips running headers and footers: "Amended and Restated Project Agreement", "Ottawa Light Rail Transit Project … REDACTED Execution Version", "Schedule N to Project Agreement", `BD-#…`, `CAN: …`, `CAN_DMS: …`, `TOR01: …`, `OTT01: …`, "CONFIDENTIAL AND PROPRIETARY", page numbers and "Signature Page";
* rebuilds paragraphs, joins paragraphs split by a page break, keeps list labels, and renders Articles as `##` and Sections as `###`;
* keeps tables (the Schedule list and the signature blocks) line by line.

All 370 TOC entries resolve to headings. One source quirk: s. 9.10 is a heading in the body but is missing from the source TOC.

Line-end hyphenation is negligible (2 cases, both genuine: "non-", "Co-"). Cleaned text is in `work/source_clean/`.

| Measure | Words |
|---|---:|
| Whole document (cover, TOC, body, signature blocks) | **95,872** |
| Cover + TOC + Schedule list | 1,985 |
| Operative body (from "THIS PROJECT AGREEMENT is made" to "IN WITNESS WHEREOF") | **93,784** |
| Signature blocks | 103 |
| Raw `pdftotext` output, before furniture strip | 100,630 |

Supplied schedules, cleaned: S1 48,766 · S2 4,917 · S6 13,184 · S10 21,450 · S14 2,750 · S15-1 15,433 · S20 16,512 · S22 6,718 · S27 8,650 · S33 1,146.

## 2. Schedules referenced in the body

Counts are references in the operative body and include the one entry in the s. 1.1(b) list. Schedule 15-1 appears in the list only as "15-1", so it counts 0.

| Sch. | Title | Refs | Supplied? | Note |
|---|---|---:|---|---|
| 1 | Definitions and Interpretation | 14 | ✅ |  |
| 2 | Completion Documents | 8 | ✅ |  |
| 3 | Custody Agreement | 3 | — |  |
| 4 | Lenders’ Direct Agreement | 2 | — |  |
| 5 | Direct Agreements | 1 | — |  |
| 6 | Independent Certifier Agreement | 5 | ✅ |  |
| 7 | [Intentionally deleted] | 1 | — | Intentionally deleted: stays a one-line entry |
| 8 | Energy Matters | 6 | — |  |
| 9 | Key Individuals | 9 | — |  |
| 10 | Review Procedure | 26 | ✅ |  |
| 11 | Quality Management | 6 | — |  |
| 12 | [Intentionally deleted] | 1 | — | Intentionally deleted: stays a one-line entry |
| 13 | Project Co Proposal Extracts | 3 | — |  |
| 14 | Commissioning | 5 | ✅ |  |
| 15 | Output Specifications | 4 | — |  |
| 15-1 | Technical Definitions and Reference Documents | 0 | ✅ |  |
| 15-2 | Design and Construction Requirements | 8 | — |  |
| 15-3 | Maintenance and Rehabilitation Requirements | 7 | — |  |
| 15-4 | Regulatory Standards | 9 | — |  |
| 16 | Title Encumbrances | 1 | — |  |
| 17 | Environmental Obligations | 14 | — |  |
| 18 | Communications and Public Consultation Protocol | 8 | — |  |
| 19 | Milestone Payments | 3 | — |  |
| 20 | Payment Mechanism | 14 | ✅ |  |
| 21 | [Intentionally deleted] | 1 | — | Intentionally deleted: stays a one-line entry |
| 22 | Variation Procedure | 51 | ✅ |  |
| 23 | Compensation on Termination | 10 | — |  |
| 24 | Expiry Transition Procedure | 7 | — |  |
| 25 | Insurance and Performance Security Requirements | 6 | — |  |
| 26 | Record Provisions | 9 | — |  |
| 27 | Dispute Resolution Procedure | 50 | ✅ |  |
| 28 | Refinancing | 4 | — |  |
| 29 | Standby Letter of Credit | 3 | — |  |
| 30 | Insurance Trust Agreement | 3 | — |  |
| 31 | Project Co Information | 3 | — |  |
| 32 | Financial Model Extracts | 1 | — |  |
| 33 | Works Reports | 4 | ✅ |  |
| 34 | Vehicle and Fixed Equipment Warranties | 3 | — |  |
| 35 | Additional Vehicles | 5 | — |  |
| 36 | Milestones | 1 | — |  |
| 37 | Mobility Matters | 3 | — |  |
| 38 | Extension and Additional Phases | 4 | — |  |
| 39 | Operations Matters | 8 | — |  |
| 40 | Highway Work | 24 | — |  |
| 41 | Intellectual Property | 7 | — |  |
| 42 | [Intentionally deleted] | 1 | — | Intentionally deleted: stays a one-line entry |
| 43 | Procurement Support Services | 11 | — | Post-execution amendment: remove |
| 44 | Stage 2 Additional Vehicles | 4 | — | Post-execution amendment: remove |
| 45 | Belfast MSF Expansion | 8 | — | Post-execution amendment: remove |
| 46 | Stage 2 Interface and Design Management Services | 3 | — | Post-execution amendment: remove |

Totals: 50 schedule slots. 10 supplied, 4 intentionally deleted (7, 12, 21, 42), 4 to remove (43–46), **32 to draft** in Phase 3, counting Schedule 15 (the umbrella over 15-1 to 15-4) as one.

## 3. Defined terms

Full inventories, generated by `checks/inventory_terms.py`:

* `work/inventory/defined_terms_used.md` (and `.json`): every defined term used in the body, how often, and where it's defined.
* `work/inventory/undefined_capitalised.md`: capitalised phrases in the body that match no definition.

Summary:

* 1,416 definitions harvested from S1 (1,339 entries), the body, and S2, S6, S15-1 and S20.
* **526 distinct defined terms used in the body.** Where they are defined:
  * 499 in Schedule 1, of which 131 point back to a body Section or another Schedule ("has the meaning given in Section 26.7(c)");
  * 12 inline in the body;
  * 7 in Schedule 15-1;
  * 3 in Schedule 20;
  * 3 in Schedule 2;
  * 2 in Schedule 6.
* Schedule 1, Appendix 8 holds the 67 original definitions; 65 of those terms are used in the body.

Capitalised terms used in the body that aren't defined anywhere in the supplied materials. These are real gaps, so preserve them:

| Term | Uses | Comment |
|---|---:|---|
| Good Industry Practice | 23 | S1 defines only "Good Industry Practice (Highway)" and "(Works)"; the bare form is undefined. Keep as is. |
| Species-at-Risk | 13 | Probably defined in S17 (not supplied). Define it when drafting S17. |
| Warranty Request | 8 | Only in Stage 2 / DBF Defect text, so it goes with the removal. |
| Relevant Convictions | 5 | Probably in S1 under a different form, or undefined. Check in Phase 3. |
| Excise Tax | 5 | Statute short-name usage (*Excise Tax Act*). Maps to a fictional statute. |
| Railway Company | 3 | Undefined in the supplied materials. |
| Geotechnical Reliant Reports | 2 | Undefined; probably intended to be in S1 or S15-1. |
| Insurance Trust Account | 2 | Probably defined in S30 (not supplied). |
| DBF Warranty Period | 3 | Stage 2 only; goes with the removal. |
| Light Rail Transit, Downtown Core, WBS, PMBOK, EVM | ≤3 | Descriptive or industry usage. |

The rest of the undefined-phrase list is proper nouns, which feed Phase 1: Canada, Ontario, Province of Ontario, Her Majesty the Queen in Right of Canada, RTG / ACS RTG / SNC RTG / EllisDon RTG, Algonquins of Pikwakanangan, National Arts Centre, Amalgamated Transit Union, Canada Revenue Agency, Constellation Crescent, Bay Street, St-Laurent, Blair, Tunney's Pasture, and others. The list also includes statute short titles (*Bankruptcy and Insolvency Act*, *Companies' Creditors Arrangement Act*, *Income Tax Act*, *Construction Lien Act (Ontario)*, *Freedom of Information and Protection of Privacy Act*).

Also: **"2017 Readiness"** (and 2017 Readiness Date / Work, s. 22.3A, etc.) is an **original 2013 defined term**, not amendment content. It's an interim public-readiness milestone tied to a real anniversary year and a strong fingerprint, so it gets renamed in Phase 1.

## 4. Amendment-inserted content proposed for removal

Marker set: Stage 2, DB Co, Belfast (MSF Expansion), Expanded System, Procurement Support, Schedules 43–46, Ring Fencing / Timing Principle, Equivalent Project Relief, (DB Co) Interface Agreement, DBF…, Stage 2 Additional Vehicles Variation, City Trial Running, Post-Warranty Delay Period.

### 4.1 Whole provisions (about 7,200 words)

| Provision | Words | Why |
|---|---:|---|
| Recitals H–L | ~110 | Dated amendment recitals (2017, 2019) |
| s. 1.1(b): Schedule list entries 43–46 | ~20 | Amendment schedules |
| **1.5** Impact of Stage 2 Maintenance Services Variation | 1,201 | Inserted 16 Sep 2019 |
| **6.6** DB Co Originated Stage 2 Background Information | 86 | Stage 2 |
| **9.10–9.14** DB Co Interface Agreement; Enforcement of DB Co Works Agreement; Equivalent Project Relief; Enforcement by City of DB Co claims; DB Co-derived Claims | 4,347 | Stage 2. 9.10–9.14 come after 9.8/9.9, so they're trailing items |
| **16.1B** Acceptance of Stage 2 Site Condition | 590 | Stage 2 (load-bearing article; it's a separate lettered insert, so 16.1 and 16.1A are untouched) |
| **24.7** Belfast MSF Expansion Works Impacts on LEED Certification | 266 | Belfast MSF |
| **27.4** Price adjustment for Maintenance Services arising from Stage 2 Variations… | 331 | Stage 2 |
| **27.5** Impact of Trial Running | 307 | Stage 2 trial running / DB Co |
| Schedules 43, 44, 45, 46 | — | Not supplied; drop them from the list |

### 4.2 Clause-level surgery inside original sections (about 6,200–7,500 words)

These are original sections with Stage 2 sentences, sub-paragraphs or parentheticals added. I propose to remove only the marker-bearing sentences, items or parentheticals, for example:

* "In respect of the Stage 2 System, the City shall issue a Variation Enquiry…" in 23.1 and 24.3;
* "(subject to the amendments agreed … pursuant to the Belfast MSF Expansion Variation)" in 25.2;
* ", taking into account the Timing Principle" in 27.2;
* "(… not including DB Co or any DB Co Party)" in 35.5;
* 42.1(a)(xiii)–(xvii), (xix) and (xx), plus the "Post-Warranty Delay Period" definition, from Excusing Causes.

Bold = load-bearing Article under your rules. Each of these will be reviewed and logged individually in `CHANGELOG.md`:

| Section | Heading | Load-bearing? | Paragraphs affected | ~Words in affected sentences |
|---|---|---|---|---:|
| Recitals |  |  | ¶, ¶, ¶, ¶, ¶ | 122 |
| 1.1 | Definitions and Interpretation |  | ¶ | 284 |
| 6.1 | No Liability |  | (b) | 103 |
| 6.2 | No Warranty |  | (b), (i), (B), (C) | 126 |
| 6.3 | No Claims |  | (ii), (iv), (A), (B) | 150 |
| 6.4 | Technical Reports |  | (b), (i), (ii) | 129 |
| 9.4 | Project Co Permits, Licences and Approvals |  | (b1) | 66 |
| 9.7 | Additional Works/Third Party Works |  | (i), (i), (i), (ii), (i), (ii), ¶ | 378 |
| 12.2 | Function and Role |  | (b), (vi) | 70 |
| 14.1 | Licence to Lands |  | (a) | 94 |
| 14.2 | Non-exclusive Licence/Development of Lands |  | (a) | 76 |
| 15.1 | Title Encumbrances |  | (ii) | 38 |
| 16.2 | Contamination | **yes** | (a1), ¶, (A), (i), (iii), (B), (i), (ii) … | 428 |
| 16.3 | Items of Geological, Historical or Archaeological Inter | **yes** | (b) | 123 |
| 16.4 | Species-at-Risk | **yes** | (a1) | 45 |
| 16.5 | Latent Defects | **yes** | (a1), (i), (ii), (iii), (b), (c), (f), (g) … | 349 |
| 19 | COORDINATION AND NO DISRUPTION |  | (i), (ii), (i) | 190 |
| 21.1 | Access for City Parties |  | (i) | 155 |
| 21.5 | Access by Others |  | (a), (vi) | 218 |
| 21.6 | Public Use |  | (i) | 14 |
| 23.1 | Operations Provision |  | (a) | 167 |
| 24.3 | Energy Matters |  | (a) | 124 |
| 25.2 | Role of Independent Certifier | **yes** | (a) | 35 |
| 27.2 | Commencement of Maintenance Services |  | (a) | 33 |
| 35.5 | Taxes − General |  | (a) | 110 |
| 35.6 | Taxes − Indemnity |  | (b) | 49 |
| 38.4 | Changes to OLRT Regulations | **yes** | (b) | 49 |
| 41.1 | Definition | **yes** | (ii) | 77 |
| 42.1 | Definition | **yes** | (xiii), (xiv), (xv), (xvi), (xvii), (xix), (A), (B) … | 1348 |
| 42.2 | Consequences of an Excusing Cause | **yes** | (A), (B), (1), (2), (iii) | 201 |
| 43.1 | Definition | **yes** | (ix) | 50 |
| 44.1 | Definition | **yes** | (b) | 51 |
| 45.1 | Project Co Events of Default | **yes** | (xix) | 76 |
| 52.1 | Disclosure |  | (a), (d) | 182 |
| 56.1 | Project Co Indemnities to the City | **yes** | (a), (f) | 94 |
| 56.2 | City Indemnities to Project Co | **yes** | (i), (ii), (iii) | 114 |
| 62.1 | Emergency |  | (a), (b) | 135 |
| 64.18 | City Parties as Third Party Beneficiaries |  | (i), (b) | 169 |

### 4.3 Schedule 1 definitions

* **Remove** the 52 Stage 2 / DB Co / Belfast / Expanded System definitions, for example Stage 2 East System, Stage 2 MOU, Stage 2 Variation Schedules, DB Co Works Agreement, Belfast MSF Expansion Variation and Expanded System.
* **Restore** the original text of the 6 definitions the amendment changed, from Appendix 8:
  * Design and Construction Works ("Stage 1 System" → "System");
  * Fixed Facilities ("Expanded … MSFs" → "Maintenance Centre");
  * Output Specifications (drop "as amended by the Stage 2 Maintenance Services Variation");
  * System (drop the phased (a)/(b) Expanded System definition);
  * Work;
  * Advanced Environmental Reports (dash only).

  The other 61 Appendix 8 entries are word-for-word identical to the current text.
* **Delete Appendix 8** itself. It exists only because of the amendment.
* Remove "Stage 1", "Stage 1 System", "Stage 1 E&M" and "Stage 1 Fixed Facilities". Rename the 15 body uses back to the original terms ("System", "E&M", "Fixed Facilities").

### 4.4 Supplied schedules (Phase 3)

Stage 2 / DB Co text also appears in S20 (for example "City Trial Running" = "Trial Running" in the DB Co Works Agreement), S6, S10 and S22. I'll apply the same treatment and log each change.

### 4.5 Uncertain, to be logged rather than guessed

* **Amendments between 2013 and 2017 without Stage 2 wording.** The A&R restates everything to October 2017 and doesn't mark earlier non-Stage-2 amendments. I can't detect those from the text, so the body will be as of the "October 1, 2017 baseline" with Stage 2 stripped. I'll log this as a known limitation.
* 16.1A Highway Site Investigation – Concealed or Unknown Conditions; 6.5 Highway Work Document Review; 22.3A Acceleration of the 2017 Readiness Work. These have no Stage 2 markers and are ring-fenced in 1.5, so they existed by October 2017. **Proposed: keep.**
* 9.7 Additional Works / Third Party Works: the Belfast paragraphs come out, and the rest stays.
* 38.4 Changes to OLRT Regulations: the DB Co sentences come out; the regulation mechanism stays (the name gets anonymised).
* 20.13(d) Coventry Bridge Work "by March 31, 2014": original, and gets a date shift.

### 4.6 Decisions needed before Phase 1/2

1. **Length baseline.** After the removal, the body will be about 79–82k words against 93.8k in the source (−14% to −16%). Options:
   * (a) **Recommended:** measure ±10% against the *reconstructed as-executed source* (the A&R minus the amendment removals). I'd produce that as `work/source_as_executed.md`, so the transformation diff stays honest.
   * (b) Keep the PDF baseline and accept the failure as explained.

   Padding to hit the band would break "never add obligations", so I don't propose it.
2. **Numbering gaps.** For removed items in the *middle* of a sequence (42.1(a)(xiii)–(xvii), with (xviii) surviving), there are two options:
   * (a) **Recommended:** replace each with "[Intentionally deleted]". This keeps existing numbering and cross-references intact (for example any reference to 42.1(a)(xviii)), and matches the source's own convention, which already has 33.2, 34.12, 26.10 and 64.6 as "[Intentionally deleted]".
   * (b) Renumber, and fix the cross-references.

   Trailing removals (1.5, 6.6, 9.10–9.14, 27.4–27.5, 24.7) would simply be dropped, with no placeholder.
3. **The 26.7(e) blank.** The source reads "the Liquidated Damages … shall be the sum of $ following the New Required Revenue Service Availability Date to and including the reset New Required Revenue Service Availability Date". The grammar suggests the redaction may have removed a rate as well as the number. Options:
   * (a) **Recommended:** a single lump sum per missed reset date, consistent with 26.7(b) and your "per missed committed date" brief. Fill it as "$X" and leave the odd syntax untouched. That ambiguity is genuine and should stay.
   * (b) "$X per day for each day".
4. **Other blanks to fill from `parameters.yaml`.** These are the 11 body blanks; I'll also fill those in S1, S6 and S20 (about 65):
   * 2.2 Standby Letter of Credit amount;
   * 9.7 insurance minimums ×2;
   * 20.13 Civic Works cash allowances ×6 (Queen Street, Albert Street, Rock Stabilization, Coventry Bridge, Utilities, CSST);
   * 24.5(c) LEED liquidated damages;
   * 26.7(b) and 26.7(e) RSA liquidated damages;
   * 34.1(g) Highway Post Substantial Completion Maintenance payment;
   * 45.1 default threshold;
   * S1: Highway Milestone Payment;
   * S1: Revenue Service Availability Payment.

   The 57.4 cap ($50,000,000) and the 26.7(f) interest rate (2% p.a.) are not redacted, so they'll be scaled or kept per Phase 1.

Preview for Phase 1 (you asked for reasoning): I propose to **keep "Project Co"**. It's the standard defined term across Canadian, UK (PF2), Australian and NZ PPP templates, so on its own it identifies a template family, not this project. It's also used thousands of times, so renaming it would make the text read less like a real agreement. The fingerprints worth renaming are the IO-specific compound terms ("Revenue Service Availability", "Required Notification Date", "Minimum Subsequent Time", "2017 Readiness", and so on).
