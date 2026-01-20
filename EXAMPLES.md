# AI Prompt Vault - Examples

This document provides real-world examples of using AI Prompt Vault in various scenarios.

---

## Table of Contents

1. [Basic Operations](#basic-operations)
2. [Developer Workflows](#developer-workflows)
3. [Content Creation](#content-creation)
4. [Team Collaboration](#team-collaboration)
5. [Advanced Usage](#advanced-usage)
6. [Integration Examples](#integration-examples)
7. [Troubleshooting Examples](#troubleshooting-examples)
8. [Automation Examples](#automation-examples)
9. [Best Practices](#best-practices)
10. [Real-World Scenarios](#real-world-scenarios)

---

## Example 1: Basic Operations

### Adding Your First Prompt

```bash
# Simple add
python prompt_vault.py add "code-review" "Review this code for bugs, performance issues, and best practices. Provide specific suggestions for improvement."

# Output:
✓ Added prompt 'code-review' [general]
```

### Adding with Category and Tags

```bash
python prompt_vault.py add "debug-python" \
  -c debugging \
  -t python,error,traceback \
  -d "Python debugging helper" \
  "Help me debug this Python error. Here's the traceback: [PASTE_TRACEBACK]"

# Output:
✓ Added prompt 'debug-python' [debugging]
```

### Using a Prompt

```bash
python prompt_vault.py use "code-review"

# Output:
✓ Copied 'code-review' to clipboard!

Review this code for bugs, performance issues, and best practices. Provide specific suggestions for improvement.
```

---

## Example 2: Developer Workflows

### Morning Standup Prompt

```bash
python prompt_vault.py add "standup" \
  -c productivity \
  -t team,daily \
  "Generate a concise standup update based on my git commits and calendar for today. Format:
- What I did yesterday: [GIT_COMMITS]
- What I'm doing today: [CALENDAR_EVENTS]
- Blockers: [IF_ANY]"
```

### Code Review Checklist

```bash
python prompt_vault.py add "review-checklist" \
  -c coding \
  -t review,quality \
  "Review this pull request for:
1. Code correctness and logic
2. Performance implications
3. Security vulnerabilities
4. Test coverage
5. Documentation updates
6. Breaking changes
7. Edge cases handled
8. Code style compliance

PR: [PR_LINK]"
```

### Bug Report Generator

```bash
python prompt_vault.py add "bug-report" \
  -c debugging \
  -t bug,template \
  "Help me write a detailed bug report:

**Bug Description:**
[DESCRIBE_ISSUE]

**Steps to Reproduce:**
1. [STEP_1]
2. [STEP_2]
3. [STEP_3]

**Expected Behavior:**
[WHAT_SHOULD_HAPPEN]

**Actual Behavior:**
[WHAT_ACTUALLY_HAPPENS]

**Environment:**
- OS: [OS]
- Version: [VERSION]
- Browser: [IF_APPLICABLE]

**Logs/Screenshots:**
[ATTACH_HERE]"
```

---

## Example 3: Content Creation

### Blog Post Outline

```bash
python prompt_vault.py add "blog-outline" \
  -c writing \
  -t content,blog \
  "Create a blog post outline for: [TOPIC]

Include:
- Catchy title (3 options)
- Introduction hook
- 5-7 main sections with subpoints
- Conclusion with call-to-action
- SEO keywords
- Target audience: [AUDIENCE]
- Tone: [PROFESSIONAL/CASUAL/TECHNICAL]"
```

### Social Media Thread

```bash
python prompt_vault.py add "twitter-thread" \
  -c writing \
  -t social,twitter \
  "Create a Twitter thread about [TOPIC]:
- 8-10 tweets
- Start with a hook
- Include data/facts
- End with engagement question
- Add relevant hashtags
- Make it shareable"
```

---

## Example 4: Team Collaboration

### Exporting Team Prompts

```bash
# Export all coding prompts for the team
python prompt_vault.py export team-coding-prompts.json -c coding

# Output:
✓ Exported 12 prompts to team-coding-prompts.json
```

### Sharing via Email

```bash
# Export and prepare for email
python prompt_vault.py export shared-prompts.json

# Then attach shared-prompts.json to email
```

### Importing Team Prompts

```bash
# Team member imports shared prompts
python prompt_vault.py import team-coding-prompts.json

# Output:
✓ Imported 12 prompts (0 skipped)
```

### Selective Import

```bash
# Import only debugging prompts from a larger collection
python prompt_vault.py import all-prompts.json
python prompt_vault.py list -c debugging

# Then use grep/filter to work with just debugging prompts
```

---

## Example 5: Advanced Usage

### Creating a Prompt Chain

```bash
# React component workflow
python prompt_vault.py add "react-1-component" \
  -c coding \
  -t react,component \
  "Create a React component: [COMPONENT_NAME]
Props: [LIST_PROPS]
State: [LIST_STATE]
Include TypeScript types."

python prompt_vault.py add "react-2-tests" \
  -c testing \
  -t react,jest \
  "Write Jest tests for the [COMPONENT_NAME] component.
Test: rendering, props, user interactions, edge cases."

python prompt_vault.py add "react-3-docs" \
  -c documentation \
  -t react,storybook \
  "Create Storybook documentation for [COMPONENT_NAME].
Include: default state, all props, interaction examples."
```

### Using Prompt Chains

```bash
# Step 1: Create component
python prompt_vault.py use "react-1-component"
# [Paste result into editor, build component]

# Step 2: Generate tests
python prompt_vault.py use "react-2-tests"
# [Create test file]

# Step 3: Document
python prompt_vault.py use "react-3-docs"
# [Add to Storybook]
```

### Interactive Mode for Complex Prompts

```bash
python prompt_vault.py interactive

# Follow prompts:
Name: api-design-review
Category [general]: coding
Tags (comma-separated): api,rest,design
Description (optional): REST API design review checklist
Enter prompt content (end with a line containing only '---'):
Review this REST API design:

1. Resource naming (RESTful?)
2. HTTP methods appropriate?
3. Status codes correct?
4. Pagination strategy?
5. Authentication/Authorization?
6. Rate limiting?
7. Versioning strategy?
8. Error response format?
9. Documentation (OpenAPI)?
10. Performance considerations?

API Spec: [PASTE_SPEC]
---

# Output:
✓ Added prompt 'api-design-review' [coding]
```

---

## Example 6: Integration Examples

### Shell Script Integration

```bash
#!/bin/bash
# quick-prompt.sh - Quick access to prompts

PROMPT_NAME=$1

if [ -z "$PROMPT_NAME" ]; then
    echo "Usage: ./quick-prompt.sh <prompt-name>"
    exit 1
fi

python ~/prompt-vault/prompt_vault.py use "$PROMPT_NAME" --no-copy
```

### Git Hook Integration

```bash
# .git/hooks/prepare-commit-msg
#!/bin/bash

# Get conventional commit prompt
COMMIT_TEMPLATE=$(python ~/prompt-vault/prompt_vault.py use "git-commit" --no-copy)

# Append to commit message
echo "$COMMIT_TEMPLATE" > "$1"
```

### VS Code Task Integration

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Get Code Review Prompt",
            "type": "shell",
            "command": "python",
            "args": [
                "~/prompt-vault/prompt_vault.py",
                "use",
                "code-review"
            ],
            "problemMatcher": []
        }
    ]
}
```

---

## Example 7: Troubleshooting Examples

### Finding a Prompt You Don't Remember

```bash
# Search by keyword
python prompt_vault.py search "debug"

# Output:
ID         Name                      Category        Uses   Tags
────────────────────────────────────────────────────────────────────────────────
abc12345   debug-python              debugging       5      python, error
def67890   debug-js                  debugging       2      javascript, console

Total: 2 prompts
```

### Updating an Old Prompt

```bash
# View current prompt
python prompt_vault.py get "old-prompt"

# Update content
python prompt_vault.py update "old-prompt" \
  -c coding \
  -t updated,improved

# Or update from file
echo "New improved content" > new-content.txt
python prompt_vault.py update "old-prompt" -f new-content.txt
```

### Recovering from Accidental Delete

```bash
# Export regularly to backup
python prompt_vault.py export backup-$(date +%Y%m%d).json

# To restore:
python prompt_vault.py import backup-20260120.json
```

---

## Example 8: Automation Examples

### Daily Backup Script

```bash
#!/bin/bash
# backup-prompts.sh

BACKUP_DIR=~/Dropbox/prompt-vault-backups
DATE=$(date +%Y-%m-%d)

python ~/prompt-vault/prompt_vault.py export "$BACKUP_DIR/prompts-$DATE.json"

# Keep only last 30 days
find "$BACKUP_DIR" -name "prompts-*.json" -mtime +30 -delete

echo "✓ Backed up prompts to $BACKUP_DIR/prompts-$DATE.json"
```

### Most Used Prompts Report

```bash
#!/bin/bash
# weekly-report.sh

python ~/prompt-vault/prompt_vault.py stats > weekly-prompt-stats.txt

# Email the report
mail -s "Weekly Prompt Stats" you@example.com < weekly-prompt-stats.txt
```

### Auto-categorize New Prompts

```bash
#!/bin/bash
# categorize.sh

# Get uncategorized prompts
python prompt_vault.py list -c general | grep "test" | while read line; do
    NAME=$(echo $line | awk '{print $2}')
    python prompt_vault.py update "$NAME" -c testing
done
```

---

## Example 9: Best Practices

### Template Prompts with Placeholders

**Good:**
```bash
python prompt_vault.py add "explain-code" \
  "Explain this [LANGUAGE] code in simple terms:
[CODE_HERE]

Focus on:
- What it does
- Why it's written this way
- Potential improvements"
```

**Why:** Clear placeholders make prompts reusable

### Naming Conventions

**Good:**
```bash
python-debug-error
python-debug-performance
python-debug-memory
```

**Why:** Prefix-based naming helps with search and organization

### Regular Maintenance

```bash
# Monthly cleanup
python prompt_vault.py stats

# Review unused prompts
python prompt_vault.py list | sort -k5 -n

# Delete unused
python prompt_vault.py delete "never-used-prompt" -y
```

---

## Example 10: Real-World Scenarios

### Scenario: New Developer Onboarding

```bash
# Create onboarding prompt collection
python prompt_vault.py add "onboard-1-setup" \
  -c onboarding \
  "Help me set up my development environment:
- Install [LANGUAGES/TOOLS]
- Configure [IDE]
- Set up [VCS]
- Install [DEPENDENCIES]"

python prompt_vault.py add "onboard-2-codebase" \
  -c onboarding \
  "Help me understand this codebase:
- Main entry point?
- Project structure?
- Key dependencies?
- Common patterns used?
Repo: [REPO_URL]"

python prompt_vault.py add "onboard-3-first-pr" \
  -c onboarding \
  "Help me find a good first issue:
- Label: good-first-issue
- Not too complex
- Well-documented
- Review requirements?"

# Export for new devs
python prompt_vault.py export onboarding-pack.json -c onboarding
```

### Scenario: Code Review Workflow

```bash
# Morning: Review PRs
python prompt_vault.py use "pr-review-checklist"
# [Review each PR using the checklist]

# Track reviews
python prompt_vault.py use "pr-review-checklist"  # increments counter

# End of week: See stats
python prompt_vault.py stats
# Most used: pr-review-checklist (23 uses)
```

### Scenario: Content Creator Pipeline

```bash
# 1. Generate topic ideas
python prompt_vault.py use "content-ideation"

# 2. Create outline
python prompt_vault.py use "blog-outline"

# 3. Write introduction
python prompt_vault.py use "engaging-intro"

# 4. Create social posts
python prompt_vault.py use "twitter-thread"
python prompt_vault.py use "linkedin-post"

# 5. SEO optimization
python prompt_vault.py use "seo-review"

# Check workflow usage
python prompt_vault.py list -t content
```

---

## Output Examples

### Stats Output

```bash
$ python prompt_vault.py stats

📊 Vault Statistics
────────────────────────────────────────
  Total prompts:  42
  Total uses:     156
  Most used:      code-review (28 uses)

  By category:
    coding: 18
    debugging: 8
    writing: 6
    testing: 5
    documentation: 3
    general: 2
```

### List Output with Filters

```bash
$ python prompt_vault.py list -c coding -t python

ID         Name                      Category        Uses   Tags
────────────────────────────────────────────────────────────────────────────────
a1b2c3d4   python-debug-error        coding          12     python, debug, error
e5f6g7h8   python-optimize           coding          8      python, performance
i9j0k1l2   python-type-hints         coding          5      python, types, mypy

Total: 3 prompts
```

### Search Output

```bash
$ python prompt_vault.py search "api"

ID         Name                      Category        Uses   Tags
────────────────────────────────────────────────────────────────────────────────
m3n4o5p6   api-design-review         coding          15     api, rest, design
q7r8s9t0   api-documentation         documentation   7      api, docs, openapi
u1v2w3x4   test-api-endpoints        testing         9      api, testing, jest

Total: 3 prompts
```

---

## Tips for Maximum Productivity

1. **Use Short Names**: `pr-review` is better than `pull-request-review-checklist-v2`
2. **Tag Liberally**: Tags make search easier
3. **Update Regularly**: Improve prompts based on what works
4. **Export Weekly**: Backup your vault
5. **Share Winners**: Export and share your best prompts with the team
6. **Track Usage**: Use stats to see what's actually helpful
7. **Create Templates**: Use placeholders like [TOPIC] for reusability
8. **Chain Prompts**: Create workflows with numbered prefixes
9. **Categorize Well**: Makes filtering much easier
10. **Clean Up**: Delete prompts you never use

---

## Common Patterns

### The "Improve" Pattern

```bash
# Original version
python prompt_vault.py add "v1-prompt" "Basic content"

# After using it a few times, improve it
python prompt_vault.py update "v1-prompt" \
  -n "improved-prompt" \
  "Enhanced content with better structure and examples"
```

### The "Collection" Pattern

```bash
# Create themed collections
python prompt_vault.py add "sec-1-owasp" -c security -t owasp ...
python prompt_vault.py add "sec-2-dependencies" -c security -t deps ...
python prompt_vault.py add "sec-3-auth" -c security -t auth ...

# Export as a collection
python prompt_vault.py export security-pack.json -c security
```

### The "Workflow" Pattern

```bash
# Number prompts in sequence
python prompt_vault.py add "deploy-1-test" ...
python prompt_vault.py add "deploy-2-build" ...
python prompt_vault.py add "deploy-3-staging" ...
python prompt_vault.py add "deploy-4-prod" ...

# Use sequentially for consistent process
```

---

## Getting Help

```bash
# General help
python prompt_vault.py --help

# Command-specific help
python prompt_vault.py add --help
python prompt_vault.py export --help
```

---

**Pro Tip:** Start with 5-10 prompts you use daily. Build from there. Quality > Quantity!
