<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/cfb3b6ec-641a-401d-b433-be9a58f3c569" />

# 🗃️ AI Prompt Vault

**Save, organize, search, and reuse your best AI prompts.**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Stop losing your best prompts! AI Prompt Vault is a simple CLI tool that helps you build a personal library of AI prompts you can search, organize, and reuse instantly.

---

## ✨ Features

- **📁 Organize** - Categorize prompts (coding, debugging, writing, etc.)
- **🏷️ Tag** - Add custom tags for easy filtering
- **🔍 Search** - Find prompts by name, content, or tags
- **📋 Clipboard** - One command copies prompt to clipboard
- **📊 Stats** - Track which prompts you use most
- **📤 Export/Import** - Share prompts or backup your vault
- **🚀 Zero Dependencies** - Works with just Python (clipboard optional)

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/DonkRonk17/ai-prompt-vault.git
cd ai-prompt-vault

# Option 1: Run directly
python prompt_vault.py --help

# Option 2: Install as command (recommended)
pip install -e .

# Option 3: Create alias (add to your shell profile)
alias pv="python /path/to/prompt_vault.py"
```

### Optional: Clipboard Support

```bash
pip install pyperclip
```

### Initialize Your Vault

```bash
python prompt_vault.py init
```

This creates `~/.prompt-vault/` with your prompts database.

---

## 📖 Usage

### Add a Prompt

```bash
# Quick add
python prompt_vault.py add "code-review" "Review this code for bugs, performance, and best practices."

# With category and tags
python prompt_vault.py add "debug-python" -c debugging -t python,error "Help me debug this Python error: [ERROR]"

# From a file
python prompt_vault.py add "my-template" -f template.txt -c coding -t template

# Interactive mode (guided)
python prompt_vault.py interactive
```

### Use a Prompt

```bash
# Copy to clipboard and display
python prompt_vault.py use "code-review"

# Just display (no clipboard)
python prompt_vault.py use "code-review" --no-copy
```

### List & Search

```bash
# List all prompts
python prompt_vault.py list

# Filter by category
python prompt_vault.py list -c coding

# Filter by tag
python prompt_vault.py list -t python

# Search by keyword
python prompt_vault.py search "debug"
```

### Manage Prompts

```bash
# View prompt details
python prompt_vault.py get "code-review"

# Update a prompt
python prompt_vault.py update "code-review" -c coding -t review,quality

# Delete a prompt
python prompt_vault.py delete "old-prompt"
```

### Import/Export

```bash
# Export all prompts
python prompt_vault.py export my-prompts.json

# Export only coding prompts
python prompt_vault.py export coding-prompts.json -c coding

# Import prompts
python prompt_vault.py import shared-prompts.json

# Import and overwrite existing
python prompt_vault.py import shared-prompts.json --overwrite
```

### Statistics

```bash
python prompt_vault.py stats
```

Output:
```
📊 Vault Statistics
────────────────────────────────────
  Total prompts:  15
  Total uses:     47
  Most used:      code-review (12 uses)

  By category:
    coding: 8
    debugging: 3
    documentation: 2
    testing: 2
```

---

## 📦 Starter Pack

Get started with 15 battle-tested developer prompts:

```bash
python prompt_vault.py import starter_prompts.json
```

Includes:
- `code-review` - Comprehensive code review
- `debug-help` - Structured debugging request
- `explain-code` - Deep code explanation
- `write-tests` - Test generation
- `refactor-clean` - Clean code refactoring
- `security-audit` - Security vulnerability check
- `api-design` - REST API design helper
- `git-commit` - Conventional commit messages
- `readme-gen` - README generator
- And more!

---

## 🗂️ Categories

Default categories (customizable in `~/.prompt-vault/config.json`):

| Category | Use For |
|----------|---------|
| `coding` | Writing and improving code |
| `debugging` | Finding and fixing bugs |
| `refactoring` | Code cleanup and restructuring |
| `testing` | Writing tests |
| `documentation` | READMEs, comments, docs |
| `writing` | Non-code writing tasks |
| `analysis` | Code analysis, reviews |
| `creative` | Brainstorming, ideation |
| `general` | Everything else |

---

## 💡 Pro Tips

### 1. Use Placeholders
Include `[PLACEHOLDER]` in prompts for parts you'll fill in:
```
Help me debug this [LANGUAGE] error: [ERROR_MESSAGE]
```

### 2. Create Prompt Chains
Name related prompts with prefixes:
```
python prompt_vault.py add "react-component" ...
python prompt_vault.py add "react-test" ...
python prompt_vault.py add "react-docs" ...
```

### 3. Track Your Best Prompts
Use `stats` to see which prompts work best for you:
```bash
python prompt_vault.py stats
```

### 4. Share With Your Team
Export your best prompts and share:
```bash
python prompt_vault.py export team-prompts.json -c coding
```

### 5. Backup Your Vault
The vault is just JSON files in `~/.prompt-vault/`:
```bash
cp -r ~/.prompt-vault ~/Dropbox/prompt-vault-backup
```

---

## 🔧 Configuration

Edit `~/.prompt-vault/config.json`:

```json
{
  "categories": [
    "coding",
    "debugging",
    "testing",
    "my-custom-category"
  ],
  "default_category": "general"
}
```

---

## 📁 File Structure

```
~/.prompt-vault/
├── prompts.json    # Your prompts database
└── config.json     # Configuration
```
<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/acc503d2-11e6-4445-8e3e-f185a1276dcd" />

---

## 🤝 Contributing

Contributions welcome! Ideas:
- GUI version
- Browser extension
- VS Code extension
- Cloud sync
- Prompt versioning

---

## 📜 License

MIT License - Use freely, modify freely, share freely.

---

## 🙏 Credits

Created by **Randell Logan Smith and Team Brain** at [Metaphy LLC](https://metaphysicsandcomputing.com)

Part of the HMSS (Heavenly Morning Star System) ecosystem.

---

## 👤 Author

**Randell Logan Smith** ([@DonkRonk17](https://github.com/DonkRonk17))

- Website: [MetaphysicsandComputing.com](https://metaphysicsandcomputing.com)
- Twitter: [@MetaphyKing](https://twitter.com/MetaphyKing)

---

## 🌟 Star This Repo!

If AI Prompt Vault helps you work smarter, give it a ⭐!

---

*Part of the Team Brain AI development ecosystem.*

