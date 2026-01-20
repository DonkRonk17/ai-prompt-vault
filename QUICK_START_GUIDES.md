# AI Prompt Vault - Quick Start Guides

Agent-specific and role-specific quick start guides.

## For Team Brain Agents

### FORGE (Autonomous Builder)
1. Install: `python prompt_vault.py init`
2. Add code templates: `pv add 'forge-review' 'Review code for: bugs, performance, security'`
3. Use: `pv use 'forge-review'` before code reviews

### ATLAS (Q-Mode Architect)
1. Install: `python prompt_vault.py init`
2. Add planning templates: `pv add 'atlas-plan' 'Architecture review checklist'`
3. Export for team: `pv export atlas-prompts.json`

### CLIO (Memory Historian)
1. Install: `python prompt_vault.py init`
2. Add documentation templates
3. Use for consistent session logs

### NEXUS (Network Coordinator)
1. Install: `python prompt_vault.py init`
2. Add communication templates
3. Share with all agents

### BOLT (Rapid Prototyper)
1. Install: `python prompt_vault.py init`
2. Add quick iteration prompts
3. Use for fast prototyping

## For Developers

### 5-Minute Setup
1. `git clone https://github.com/DonkRonk17/AI-Prompt-Vault.git`
2. `cd AI-Prompt-Vault`
3. `python prompt_vault.py init`
4. `python prompt_vault.py import starter_prompts.json`
5. `alias pv='python ~/AI-Prompt-Vault/prompt_vault.py'`

### Daily Workflow
1. Morning: `pv use 'standup'` for daily update
2. Code review: `pv use 'code-review'`
3. Debug: `pv use 'debug-helper'`
4. Tests: `pv use 'test-gen'`
5. Commit: `pv use 'git-commit'`

### Team Setup
1. Create team repo
2. `pv export team-prompts.json`
3. Commit to repo
4. Team imports with `pv import team-prompts.json`

## Common Patterns

### Adding Prompts with Placeholders
`pv add 'template' 'Content with [PLACEHOLDER]'`

### Search & Filter
`pv search 'keyword'`
`pv list -c coding -t python`

### Backup
`pv export backup-.json`

## Troubleshooting

### Can't find prompt
`pv list` or `pv search 'keyword'`

### Clipboard not working
`pip install pyperclip`

### Import failed
Check JSON format, ensure valid structure

---

**Version:** 1.0  
**For:** All Team Brain agents and external developers  
**Last Updated:** January 2026
