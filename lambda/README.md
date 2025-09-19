# Lambda Source

This package contains the code that runs on the scheduled AWS Lambda.

- `app.py` — entry point invoked by `lambda_handler`, responsible for crawling the Hills Hornets API, building team calendars, and uploading them to S3.
- `requirements.txt` — third-party dependencies bundled with the function during deployment.

To execute the handler locally without SAM, run:

```bash
python lambda/app.py
```

The module is designed for use with the SAM template in `infra/template.yaml`.
