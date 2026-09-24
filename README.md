# Vireo Audio — Support Ticket Intelligence

AI-assisted support-ticket categorisation and workload analysis for Vireo Audio.

## Project objective

Analyse 18 months of Vireo Audio support tickets and provide:

- AI-assisted ticket categorisation
- Confidence and human-review flagging
- Monthly ticket volume by category
- Monthly ticket volume by team
- Team and category workload analysis
- Transfer-cost analysis
- AI classification validation
- Business decision support for staffing and process improvement

## Dataset

The project uses the supplied Vireo Audio data pack:

- `data/tickets.csv`
- `data/agents.csv`
- `data/orders.csv`
- `data/customers.csv`
- `data/products.csv`
- `support-policy.pdf`
- `email-thread.txt`

The ticket data covers January 2025 through June 2026.

## Requirements

- Python 3.11+
- Windows, macOS or Linux
- Internet connection only if installing Python packages

## Installation

Create a virtual environment.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1