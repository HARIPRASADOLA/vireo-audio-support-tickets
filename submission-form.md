Write-Host "`n=== 1. APPLICATION ==="
Test-Path "app\app.py"

Write-Host "`n=== 2. BUSINESS MEMO ==="
Test-Path "docs\memo_priya_raman.md"

Write-Host "`n=== 3. VALIDATION ==="
Test-Path "output\ai_categorised_tickets.csv"

Write-Host "`n=== 4. README ==="
Test-Path "README.md"

Write-Host "`n=== 5. SUPPORT POLICY ==="
Test-Path "support-policy.pdf"

Write-Host "`n=== 6. SUBMISSION FORM ==="
Test-Path "submission-form.md"