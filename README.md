# email-distribution

CLI utility to send a newsletter to recipients listed in an Excel (`.xlsx`) file.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Recipients Excel format

The first row must contain headers. By default these headers are expected:

- `email` (required)
- `name` (optional)

## Usage

```bash
python newsletter_distribution.py recipients.xlsx "Monthly newsletter" newsletter.txt \
  --smtp-host smtp.example.com \
  --smtp-port 587 \
  --smtp-user your-user \
  --smtp-password your-password \
  --sender newsletter@example.com
```

### Dry run

```bash
python newsletter_distribution.py recipients.xlsx "Monthly newsletter" newsletter.txt \
  --smtp-host smtp.example.com \
  --smtp-user your-user \
  --smtp-password your-password \
  --sender newsletter@example.com \
  --dry-run
```

`newsletter.txt` supports `{name}` and `{email}` placeholders.
