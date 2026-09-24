# Vireo Audio Support Desk — Decision Memo

**To:** Priya Raman, Head of Customer Experience  
**From:** Support Analytics Project  
**Date:** 24 September 2026  
**Subject:** Support volume, categorisation and headcount decision

## Executive summary

The 18-month support dataset contains [TOTAL TICKETS] tickets from January 2025 through June 2026.

For Q2 2026, the desk handled [Q2 TICKETS] tickets. The largest team by ticket volume was [LARGEST TEAM], with [TEAM TICKETS] tickets.

The analysis also identified [TRANSFER EVENTS] transfer events in Q2, representing a transfer cost of approximately Rs [TRANSFER COST] using the policy planning rate of Rs 305 per transfer.

The AI categorisation workflow classified tickets into 11 categories and flagged [Q2 REVIEW] Q2 tickets for human review ([REVIEW RATE]%).

## What the data shows

### Team workload

The Q2 team volumes were:

- [TEAM 1]&#58; [VOLUME]
- [TEAM 2]&#58; [VOLUME]
- [TEAM 3]&#58; [VOLUME]
- [TEAM 4]&#58; [VOLUME]

The largest queue should therefore be considered alongside transfer activity and resolution performance before treating ticket count alone as evidence of additional permanent capacity.

### Category workload

The largest Q2 categories were:

- [CATEGORY 1]&#58; [VOLUME]
- [CATEGORY 2]&#58; [VOLUME]
- [CATEGORY 3]&#58; [VOLUME]

Monthly analysis is included in the accompanying dashboard and separates category volume from team volume.

## Process opportunity

The transfer data provides a measurable process-cost opportunity.

Each internal team transfer is costed at Rs 305 under the support policy. Reducing unnecessary hand-offs would therefore reduce re-handling and administration cost without requiring additional headcount.

The recommended operating metric is:

**Transfer rate = tickets with one or more transfers / total tickets.**

This should be monitored monthly by originating team and category.

## AI categorisation

The AI-assisted workflow produces a category, confidence score and human-review flag.

Q2 2026 review rate: **[REVIEW RATE]%**

Validation sample:

- Records reviewed: [VALIDATED]
- Correct classifications: [CORRECT]
- Incorrect classifications: [INCORRECT]
- Observed accuracy: [ACCURACY]%

Low-confidence cases remain in the human-review queue rather than being treated as automatically correct.

## Business goal

**Reduce the Q2 transfer rate from [CURRENT RATE]% to [TARGET RATE]% by the end of Q4 2026, while maintaining the validated AI categorisation accuracy at or above [ACCURACY]% .**

At Q2 volume, this would avoid approximately [AVOIDED TRANSFERS] transfer events per quarter, equivalent to approximately **Rs [QUARTERLY SAVING] per quarter** at the policy rate of Rs 305 per transfer.

## Recommendation for operating decision

Use the monthly team/category dashboard as the headcount input, but review it together with:

1. transfer rate,
2. resolution time,
3. SLA performance, and
4. repeat contacts.

The dashboard is designed to make those measures visible before the next staffing review.

## Scope and limitations

The analysis uses the supplied ticket, roster, customer, order and product exports. Legacy records have missing transfer values because transfers were not captured in the previous helpdesk.

The AI categorisation should therefore be treated as decision support, with low-confidence cases routed for human review.

The project prioritised the requested monthly volume analysis, transparent categorisation, validation and quantified process-cost opportunity rather than building a larger production support platform.