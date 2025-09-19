# Infrastructure

This directory holds deployment assets for the Hills Draw calendar service.

- `template.yaml` — AWS SAM template describing the scheduled Lambda.
- `samconfig.toml` — saved deploy defaults for `sam deploy`.
- `website-bucket.yaml` — CloudFormation template for the public S3 website bucket and Route 53 alias.
- `events/` — sample payloads for local `sam local invoke` runs.

## Deploying the Lambda

```bash
sam build --template-file infra/template.yaml
sam deploy --template-file infra/template.yaml --config-file infra/samconfig.toml
```

Adjust or override the `sam deploy` parameters as required for your AWS account.
