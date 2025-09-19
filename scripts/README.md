# Utility Scripts

Helpers for working with the Hills draw feed outside the scheduled Lambda.

- `get-draw.py` — runs the calendar generation flow locally and pushes results to S3 using the same logic as the Lambda function.
- `extract-calendar.py` — small example showing how to create `.ics` files with custom events, useful when prototyping calendar tweaks.

Run these with your preferred virtualenv activated, e.g.:

```bash
python scripts/get-draw.py
```
