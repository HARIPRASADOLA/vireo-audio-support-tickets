# AI Usage Disclosure

## AI tools used

AI assistance was used during development for:

* Python and Streamlit development support
* Debugging and troubleshooting
* Data-analysis workflow design
* AI-assisted ticket categorisation approach
* Validation and error-analysis workflow
* Documentation and README preparation
* Reviewing the final project structure and reproducibility

The submitted application and analysis were run against the supplied Vireo Audio data and checked through the project's validation and application testing workflow.

## Cost

**External AI/API cost: Rs 0**

No paid external AI API was required for the submitted prototype.

## What was discarded

Because the assignment was time-boxed, the following were deliberately not implemented:

* Production deployment infrastructure
* Authentication and user management
* Production database architecture
* Automatic helpdesk ticket write-back
* Full production model-serving infrastructure
* Additional automation outside the requested analysis workflow

These items were excluded to prioritise a working prototype, measurable validation, business analysis and reproducibility.

## Important limitation

The existing helpdesk category was not treated as perfect ground truth. The AI-assisted categorisation therefore includes a confidence/review mechanism so lower-confidence cases can be reviewed by a human.

Legacy transfer blanks were also treated separately from confirmed zero transfers because the transfer field was not available in the legacy helpdesk data.
