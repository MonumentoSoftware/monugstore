# Security

## Reporting

If you find a vulnerability, email **pedro@monumentosoftware.com.br**.

Do not open a public GitHub issue for:

- Service-account keys or other credentials
- Ways to make buckets or objects public by accident
- Dependency or supply-chain issues that are still unpatched

Include the affected version (or commit), a reproduction, and impact.

## Scope

This library wraps Google Cloud Storage. Please also check whether the issue belongs in [google-cloud-storage](https://github.com/googleapis/python-storage/security) or another dependency before reporting it here.

`mgs-dump-key` prints a service-account JSON string to stdout. Treat that output as secret.
