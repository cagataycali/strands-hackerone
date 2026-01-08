# Strands HackerOne

HackerOne API tool for [Strands Agents](https://github.com/strands-agents). Automate bug bounty research, program monitoring, and report management with AI.

## Installation

```bash
pip install strands-hackerone
```

## Setup

Get API credentials from [HackerOne Settings](https://hackerone.com/settings/api_token):

```bash
export HACKERONE_USERNAME="your_username"
export HACKERONE_API_KEY="your_api_key"
```

## Usage

### Standalone

```python
from strands_hackerone import hackerone

# List programs
hackerone(action="programs", limit=10)

# Check hacktivity
hackerone(action="hacktivity", query="severity:critical")

# View balance
hackerone(action="balance")
```

### With Strands Agent

```python
from strands import Agent
from strands_hackerone import hackerone

agent = Agent(tools=[hackerone])
agent("Find high-paying programs accepting XSS vulnerabilities")
```

## Actions

| Action | Description | Parameters |
|--------|-------------|------------|
| `programs` | List bug bounty programs | `page`, `limit` |
| `program_info` | Get program details | `program_handle` |
| `program_scope` | View program scope | `program_handle`, `page`, `limit` |
| `program_weaknesses` | List accepted vulnerability types | `program_handle`, `page`, `limit` |
| `hacktivity` | Browse public disclosures | `query`, `page`, `limit` |
| `my_reports` | List your reports | `page`, `limit` |
| `report_details` | Get report details | `report_id` |
| `balance` | Check current balance | - |
| `earnings` | View earnings history | `page`, `limit` |
| `payouts` | View payout history | `page`, `limit` |

## Examples

### Search hacktivity

```python
# Critical vulnerabilities
hackerone(action="hacktivity", query="severity:critical")

# High bounties
hackerone(action="hacktivity", query="bounty:>5000")

# Specific program
hackerone(action="hacktivity", query="program:security")
```

### Get program info

```python
hackerone(action="program_info", program_handle="security")
hackerone(action="program_scope", program_handle="github")
hackerone(action="program_weaknesses", program_handle="security")
```

### Track your activity

```python
hackerone(action="my_reports", limit=25)
hackerone(action="report_details", report_id="274387")
hackerone(action="balance")
hackerone(action="earnings", page=1, limit=50)
```

## AI Agent Examples

### Research Assistant

```python
agent = Agent(
    tools=[hackerone],
    system_prompt="Bug bounty research assistant"
)

agent("Find programs with web apps in scope that offer fast payments")
```

### Monitor

```python
agent = Agent(
    tools=[hackerone],
    system_prompt="Monitor HackerOne for important events"
)

agent("Check for new critical disclosures in the last 24 hours")
```

## Output Format

All actions return:

```python
{
    "status": "success" | "error",
    "content": [{"text": "formatted_output"}]
}
```

Example output:

```
🔥 HackerOne Hacktivity (Page 1)

🎯 Stored XSS in Profile Editor
   Program: gitlab
   Severity: high
   Bounty: $3,500

🎯 SQL Injection in API Endpoint
   Program: shopify
   Severity: critical
   Bounty: $10,000
```

## Troubleshooting

**401 Unauthorized**  
Check `HACKERONE_USERNAME` and `HACKERONE_API_KEY`

**403 Forbidden**  
You must be enrolled in the program

**Rate Limited**  
Reduce request frequency, use pagination, cache results

## Development

```bash
git clone https://github.com/cagataycali/strands-hackerone.git
cd strands-hackerone
pip install -e .
python test_hackerone.py
```

## Resources

- [HackerOne API Docs](https://api.hackeone.com/docs/v1)
- [Strands Agents](https://github.com/strands-agents)

## License

MIT

## Author

[@cagataycali](https://github.com/cagataycali)
