# 🐛 Strands HackerOne: When AI Meets Bug Bounty

**Picture this:** It's 3 AM. You're hunting bugs across 50 programs. Manually checking scope. Tracking reports. Missing critical disclosures. Your coffee's cold, and you're wondering—*there has to be a better way*.

There is. Welcome to **Strands HackerOne**—where AI agents hunt alongside you.

## 🎯 The Problem

Bug bounty hunting is overwhelming:
- 📊 **2,000+ programs** to monitor
- 🔥 **Critical vulns** disclosed while you sleep  
- 📋 **Reports scattered** across your dashboard
- 💰 **Earnings buried** in payment histories

Traditional approach? Manual. Time-consuming. **Exhausting.**

## ⚡ The Solution

An AI-powered HackerOne tool that works while you code:

```python
from strands import Agent
from strands_hackerone import hackerone

# Your AI bug bounty assistant
agent = Agent(tools=[hackerone])

# Natural language → API magic
agent("Find high-paying programs accepting XSS that launched this month")
```

**That's it.** Your AI handles the REST API complexity.

## 🚀 Installation: 30 Seconds

```bash
pip install strands-hackerone

export HACKERONE_USERNAME="your_username"
export HACKERONE_API_KEY="your_api_key"
```

Get credentials: [HackerOne Settings](https://hackerone.com/settings/api_token) → API Tokens

## 💡 Real-World Scenarios

### Scenario 1: Morning Intelligence Brief
```python
# What happened while you slept?
agent("Show me critical severity disclosures from the last 12 hours")
```

**Result:** Instant brief of overnight activity. No manual scrolling.

### Scenario 2: Target Acquisition
```python
# Find your next target
agent("List programs offering bounties with web apps in scope, sorted by fast payments")
```

**Result:** Curated program list matching your hunting style.

### Scenario 3: Research Before Reporting
```python
# Avoid duplicates
agent("Search hacktivity for similar XSS vulnerabilities in the GitHub program")
```

**Result:** Historical context preventing duplicate reports.

## 🛠️ Core Actions

Every action returns clean, formatted results:

| Action | Purpose | Example |
|--------|---------|---------|
| `programs` | List all programs | `hackerone(action="programs", limit=50)` |
| `program_info` | Deep-dive into one | `hackerone(action="program_info", program_handle="security")` |
| `program_scope` | View in-scope assets | `hackerone(action="program_scope", program_handle="github")` |
| `hacktivity` | Public disclosures | `hackerone(action="hacktivity", query="severity:critical")` |
| `my_reports` | Your submissions | `hackerone(action="my_reports")` |
| `balance` | Current earnings | `hackerone(action="balance")` |
| `earnings` | Payment history | `hackerone(action="earnings", limit=100)` |

## 🎨 Advanced Queries

The `hacktivity` action supports Lucene queries:

```python
# Critical vulns in a specific program
hackerone(action="hacktivity", query="program:security AND severity:critical")

# High-paying bounties (inspiration!)
hackerone(action="hacktivity", query="bounty:>5000")

# Recent XSS findings
hackerone(action="hacktivity", query="weakness:xss AND disclosed_at:>2024-01-01")
```

## 🤖 AI Agent Patterns

### Pattern 1: The Researcher
```python
researcher = Agent(
    tools=[hackerone],
    system_prompt="Research assistant specializing in vulnerability patterns"
)

researcher("""
Analyze the last 20 XSS disclosures. 
What patterns emerge? Which programs pay best?
""")
```

### Pattern 2: The Monitor
```python
monitor = Agent(
    tools=[hackerone],
    system_prompt="Alert on important HackerOne events"
)

# Run periodically (cron, scheduler, etc.)
monitor("Check for new critical disclosures or payment updates")
```

### Pattern 3: The Strategist
```python
strategist = Agent(
    tools=[hackerone],
    system_prompt="Bug bounty career advisor"
)

strategist("""
I specialize in web app security and have 6 months experience.
Which 5 programs should I focus on this quarter?
""")
```

## 🧪 Quick Test

```bash
git clone https://github.com/cagataycali/strands-hackerone.git
cd strands-hackerone
pip install -e .
python test_hackerone.py
```

Output shows all actions working:
```
✅ Hacktivity loaded
✅ Programs retrieved  
✅ Balance checked
```

## 📊 Example Output

**Hacktivity Feed:**
```
🔥 HackerOne Hacktivity (Page 1)

🎯 Stored XSS in Profile Editor
   Program: gitlab | Severity: high | Bounty: $3,500
   
🎯 SQL Injection in API Endpoint  
   Program: shopify | Severity: critical | Bounty: $10,000
```

**Program Info:**
```
🎯 Program: GitHub Security

💰 Bounties: Yes | ⚡ Fast Payments: Yes
📋 Policy: We appreciate security research...

✅ IN SCOPE:
- URL: github.com (Max: critical)
- API: api.github.com (Max: high)
```

## 🔧 Troubleshooting

**401 Unauthorized?**  
→ Verify `HACKERONE_USERNAME` and `HACKERONE_API_KEY`

**403 Forbidden?**  
→ You must be enrolled in the program to access details

**Rate Limited?**  
→ Slow down requests. Cache results. Use pagination smartly.

## 🏗️ Build Your Own Actions

Fork and extend:

```python
# In hackerone.py
elif action == "trending_programs":
    # Your custom logic
    programs = api.get("/programs", params={"trending": True})
    return {"status": "success", "content": [{"text": format_programs(programs)}]}
```

Submit PRs to add community features!

## 📚 Resources

- [HackerOne API Docs](https://api.hackerone.com/docs/v1)
- [Strands Agents Framework](https://github.com/cagataycali/strands-agents)  
- [Bug Bounty Programs Directory](https://hackerone.com/bug-bounty-programs)

## 🎯 The Vision

Imagine a world where:
- ✅ Your AI scouts programs while you sleep
- ✅ Disclosures trigger instant Slack notifications  
- ✅ Duplicate reports become impossible
- ✅ Research happens at machine speed

**That world exists now.** This is just the beginning.

## 🤝 Contributing

Bug bounty hunters + AI developers = **unstoppable**

1. Fork the repo
2. Add features (`git checkout -b feature/auto-recon`)
3. Test thoroughly  
4. Submit PR

Ideas:
- Integration with recon tools (Nuclei, ffuf, etc.)
- Auto-report drafting from findings
- Real-time webhook listeners
- Multi-platform aggregation (Bugcrowd, Intigriti, etc.)

## ⭐ Support the Hunt

- **Star** if this saves you time
- **Issue** if something breaks  
- **PR** if you make it better
- **Share** with fellow hunters

## 📜 License

MIT - Hunt freely, build openly.

---

**Built by bug bounty hunters, for bug bounty hunters.**  
[@cagataycali](https://github.com/cagataycali) | Powered by [Strands Agents](https://github.com/cagataycali/strands-agents)

*Now stop reading and start hunting.* 🐛🔍💰
