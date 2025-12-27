#!/usr/bin/env python3
"""
AI Prompt Vault - Universal AI Prompt Manager
=============================================
Save, organize, search, and reuse your best AI prompts.

Author: Randell Logan Smith (DonkRonk17)
License: MIT
Repository: https://github.com/DonkRonk17/ai-prompt-vault
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
import hashlib

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

VAULT_DIR = Path.home() / ".prompt-vault"
VAULT_FILE = VAULT_DIR / "prompts.json"
CONFIG_FILE = VAULT_DIR / "config.json"

# Default categories
DEFAULT_CATEGORIES = [
    "coding",
    "writing", 
    "analysis",
    "creative",
    "debugging",
    "refactoring",
    "documentation",
    "testing",
    "general"
]

# ═══════════════════════════════════════════════════════════════════════════════
# VAULT OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════

def init_vault():
    """Initialize the vault directory and files."""
    VAULT_DIR.mkdir(exist_ok=True)
    
    if not VAULT_FILE.exists():
        VAULT_FILE.write_text(json.dumps({"prompts": [], "version": "1.0.0"}, indent=2))
        print(f"✓ Created vault at {VAULT_FILE}")
    
    if not CONFIG_FILE.exists():
        config = {
            "categories": DEFAULT_CATEGORIES,
            "default_category": "general",
            "created": datetime.now().isoformat()
        }
        CONFIG_FILE.write_text(json.dumps(config, indent=2))
        print(f"✓ Created config at {CONFIG_FILE}")
    
    return True


def load_vault():
    """Load the prompt vault."""
    if not VAULT_FILE.exists():
        init_vault()
    return json.loads(VAULT_FILE.read_text())


def save_vault(vault):
    """Save the prompt vault."""
    VAULT_FILE.write_text(json.dumps(vault, indent=2))


def load_config():
    """Load configuration."""
    if not CONFIG_FILE.exists():
        init_vault()
    return json.loads(CONFIG_FILE.read_text())


def generate_id(content):
    """Generate a short unique ID for a prompt."""
    return hashlib.md5(content.encode()).hexdigest()[:8]


# ═══════════════════════════════════════════════════════════════════════════════
# PROMPT MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

def add_prompt(name, content, category="general", tags=None, description=""):
    """Add a new prompt to the vault."""
    vault = load_vault()
    
    # Check for duplicate names
    for p in vault["prompts"]:
        if p["name"].lower() == name.lower():
            print(f"✗ Prompt '{name}' already exists. Use 'update' to modify.")
            return False
    
    prompt = {
        "id": generate_id(content + str(datetime.now())),
        "name": name,
        "content": content,
        "category": category,
        "tags": tags or [],
        "description": description,
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat(),
        "uses": 0
    }
    
    vault["prompts"].append(prompt)
    save_vault(vault)
    print(f"✓ Added prompt '{name}' [{category}]")
    return True


def get_prompt(name_or_id):
    """Get a prompt by name or ID."""
    vault = load_vault()
    
    for p in vault["prompts"]:
        if p["name"].lower() == name_or_id.lower() or p["id"] == name_or_id:
            return p
    return None


def use_prompt(name_or_id, copy_to_clipboard=True):
    """Get a prompt and optionally copy to clipboard."""
    vault = load_vault()
    
    for i, p in enumerate(vault["prompts"]):
        if p["name"].lower() == name_or_id.lower() or p["id"] == name_or_id:
            # Increment use counter
            vault["prompts"][i]["uses"] += 1
            save_vault(vault)
            
            content = p["content"]
            
            # Try to copy to clipboard
            if copy_to_clipboard:
                try:
                    import pyperclip
                    pyperclip.copy(content)
                    print(f"✓ Copied '{p['name']}' to clipboard!")
                except ImportError:
                    print("(Install pyperclip for clipboard support: pip install pyperclip)")
            
            return content
    
    print(f"✗ Prompt '{name_or_id}' not found")
    return None


def list_prompts(category=None, tag=None, search=None):
    """List prompts with optional filters."""
    vault = load_vault()
    prompts = vault["prompts"]
    
    # Apply filters
    if category:
        prompts = [p for p in prompts if p["category"].lower() == category.lower()]
    
    if tag:
        prompts = [p for p in prompts if tag.lower() in [t.lower() for t in p.get("tags", [])]]
    
    if search:
        search_lower = search.lower()
        prompts = [p for p in prompts if 
                   search_lower in p["name"].lower() or 
                   search_lower in p["content"].lower() or
                   search_lower in p.get("description", "").lower()]
    
    return prompts


def delete_prompt(name_or_id):
    """Delete a prompt."""
    vault = load_vault()
    
    for i, p in enumerate(vault["prompts"]):
        if p["name"].lower() == name_or_id.lower() or p["id"] == name_or_id:
            name = p["name"]
            del vault["prompts"][i]
            save_vault(vault)
            print(f"✓ Deleted prompt '{name}'")
            return True
    
    print(f"✗ Prompt '{name_or_id}' not found")
    return False


def update_prompt(name_or_id, new_content=None, new_name=None, new_category=None, new_tags=None):
    """Update an existing prompt."""
    vault = load_vault()
    
    for i, p in enumerate(vault["prompts"]):
        if p["name"].lower() == name_or_id.lower() or p["id"] == name_or_id:
            if new_content:
                vault["prompts"][i]["content"] = new_content
            if new_name:
                vault["prompts"][i]["name"] = new_name
            if new_category:
                vault["prompts"][i]["category"] = new_category
            if new_tags is not None:
                vault["prompts"][i]["tags"] = new_tags
            
            vault["prompts"][i]["updated"] = datetime.now().isoformat()
            save_vault(vault)
            print(f"✓ Updated prompt '{p['name']}'")
            return True
    
    print(f"✗ Prompt '{name_or_id}' not found")
    return False


# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT/EXPORT
# ═══════════════════════════════════════════════════════════════════════════════

def export_prompts(filepath, category=None):
    """Export prompts to a JSON file."""
    prompts = list_prompts(category=category)
    
    export_data = {
        "exported": datetime.now().isoformat(),
        "count": len(prompts),
        "prompts": prompts
    }
    
    Path(filepath).write_text(json.dumps(export_data, indent=2))
    print(f"✓ Exported {len(prompts)} prompts to {filepath}")
    return True


def import_prompts(filepath, overwrite=False):
    """Import prompts from a JSON file."""
    try:
        data = json.loads(Path(filepath).read_text())
        prompts = data.get("prompts", data) if isinstance(data, dict) else data
        
        if not isinstance(prompts, list):
            print("✗ Invalid import file format")
            return False
        
        imported = 0
        skipped = 0
        
        for p in prompts:
            if "name" not in p or "content" not in p:
                skipped += 1
                continue
            
            existing = get_prompt(p["name"])
            if existing and not overwrite:
                skipped += 1
                continue
            
            if existing:
                update_prompt(p["name"], new_content=p["content"], 
                            new_category=p.get("category", "general"),
                            new_tags=p.get("tags", []))
            else:
                add_prompt(p["name"], p["content"], 
                          p.get("category", "general"),
                          p.get("tags", []),
                          p.get("description", ""))
            imported += 1
        
        print(f"✓ Imported {imported} prompts ({skipped} skipped)")
        return True
        
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

def print_prompt_table(prompts):
    """Print prompts in a nice table format."""
    if not prompts:
        print("No prompts found.")
        return
    
    # Header
    print(f"\n{'ID':<10} {'Name':<25} {'Category':<15} {'Uses':<6} {'Tags'}")
    print("─" * 80)
    
    for p in sorted(prompts, key=lambda x: x.get("uses", 0), reverse=True):
        tags = ", ".join(p.get("tags", [])[:3])
        if len(p.get("tags", [])) > 3:
            tags += "..."
        print(f"{p['id']:<10} {p['name'][:24]:<25} {p['category']:<15} {p.get('uses', 0):<6} {tags}")
    
    print(f"\nTotal: {len(prompts)} prompts")


def print_prompt_detail(prompt):
    """Print detailed prompt information."""
    print(f"\n{'═' * 60}")
    print(f"  {prompt['name']}")
    print(f"{'═' * 60}")
    print(f"  ID:       {prompt['id']}")
    print(f"  Category: {prompt['category']}")
    print(f"  Tags:     {', '.join(prompt.get('tags', [])) or 'none'}")
    print(f"  Uses:     {prompt.get('uses', 0)}")
    print(f"  Created:  {prompt['created'][:10]}")
    print(f"  Updated:  {prompt['updated'][:10]}")
    if prompt.get('description'):
        print(f"  Desc:     {prompt['description']}")
    print(f"{'─' * 60}")
    print(f"\n{prompt['content']}\n")
    print(f"{'═' * 60}")


def interactive_add():
    """Interactive prompt addition."""
    print("\n📝 Add New Prompt")
    print("─" * 40)
    
    name = input("Name: ").strip()
    if not name:
        print("✗ Name is required")
        return
    
    config = load_config()
    print(f"Categories: {', '.join(config['categories'])}")
    category = input(f"Category [{config['default_category']}]: ").strip() or config['default_category']
    
    tags_input = input("Tags (comma-separated): ").strip()
    tags = [t.strip() for t in tags_input.split(",")] if tags_input else []
    
    description = input("Description (optional): ").strip()
    
    print("\nEnter prompt content (end with a line containing only '---'):")
    lines = []
    while True:
        line = input()
        if line.strip() == "---":
            break
        lines.append(line)
    
    content = "\n".join(lines)
    
    if content:
        add_prompt(name, content, category, tags, description)
    else:
        print("✗ Content is required")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AI Prompt Vault - Save, organize, and reuse your best AI prompts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  prompt-vault add "code-review" -c coding -t python,review
  prompt-vault use "code-review"
  prompt-vault list -c coding
  prompt-vault search "python"
  prompt-vault export my-prompts.json
  prompt-vault import shared-prompts.json
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Init command
    subparsers.add_parser("init", help="Initialize the vault")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new prompt")
    add_parser.add_argument("name", help="Prompt name")
    add_parser.add_argument("-c", "--category", default="general", help="Category")
    add_parser.add_argument("-t", "--tags", help="Comma-separated tags")
    add_parser.add_argument("-d", "--description", default="", help="Description")
    add_parser.add_argument("-f", "--file", help="Read content from file")
    add_parser.add_argument("content", nargs="?", help="Prompt content (or use -f)")
    
    # Use command
    use_parser = subparsers.add_parser("use", help="Use a prompt (copies to clipboard)")
    use_parser.add_argument("name", help="Prompt name or ID")
    use_parser.add_argument("--no-copy", action="store_true", help="Don't copy to clipboard")
    
    # Get command (show without incrementing uses)
    get_parser = subparsers.add_parser("get", help="Get prompt details")
    get_parser.add_argument("name", help="Prompt name or ID")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List prompts")
    list_parser.add_argument("-c", "--category", help="Filter by category")
    list_parser.add_argument("-t", "--tag", help="Filter by tag")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search prompts")
    search_parser.add_argument("query", help="Search query")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a prompt")
    delete_parser.add_argument("name", help="Prompt name or ID")
    delete_parser.add_argument("-y", "--yes", action="store_true", help="Skip confirmation")
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update a prompt")
    update_parser.add_argument("name", help="Prompt name or ID")
    update_parser.add_argument("-c", "--category", help="New category")
    update_parser.add_argument("-t", "--tags", help="New tags (comma-separated)")
    update_parser.add_argument("-n", "--new-name", help="New name")
    update_parser.add_argument("-f", "--file", help="Read new content from file")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export prompts")
    export_parser.add_argument("file", help="Output file path")
    export_parser.add_argument("-c", "--category", help="Export only this category")
    
    # Import command
    import_parser = subparsers.add_parser("import", help="Import prompts")
    import_parser.add_argument("file", help="Input file path")
    import_parser.add_argument("--overwrite", action="store_true", help="Overwrite existing")
    
    # Categories command
    subparsers.add_parser("categories", help="List categories")
    
    # Stats command
    subparsers.add_parser("stats", help="Show vault statistics")
    
    # Interactive command
    subparsers.add_parser("interactive", help="Interactive mode")
    
    args = parser.parse_args()
    
    # Initialize vault on first run
    if not VAULT_DIR.exists():
        init_vault()
    
    # Handle commands
    if args.command == "init":
        init_vault()
        print("✓ Vault initialized!")
        
    elif args.command == "add":
        content = args.content
        if args.file:
            content = Path(args.file).read_text()
        if not content:
            print("✗ Content required. Use -f FILE or provide content as argument")
            sys.exit(1)
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
        add_prompt(args.name, content, args.category, tags, args.description)
        
    elif args.command == "use":
        content = use_prompt(args.name, copy_to_clipboard=not args.no_copy)
        if content:
            print(f"\n{content}\n")
            
    elif args.command == "get":
        prompt = get_prompt(args.name)
        if prompt:
            print_prompt_detail(prompt)
        else:
            print(f"✗ Prompt '{args.name}' not found")
            
    elif args.command == "list":
        prompts = list_prompts(category=args.category, tag=args.tag)
        print_prompt_table(prompts)
        
    elif args.command == "search":
        prompts = list_prompts(search=args.query)
        print_prompt_table(prompts)
        
    elif args.command == "delete":
        if not args.yes:
            confirm = input(f"Delete '{args.name}'? [y/N]: ")
            if confirm.lower() != 'y':
                print("Cancelled")
                return
        delete_prompt(args.name)
        
    elif args.command == "update":
        new_content = None
        if args.file:
            new_content = Path(args.file).read_text()
        new_tags = [t.strip() for t in args.tags.split(",")] if args.tags else None
        update_prompt(args.name, new_content, args.new_name, args.category, new_tags)
        
    elif args.command == "export":
        export_prompts(args.file, args.category)
        
    elif args.command == "import":
        import_prompts(args.file, args.overwrite)
        
    elif args.command == "categories":
        config = load_config()
        print("\nCategories:")
        for cat in config["categories"]:
            count = len(list_prompts(category=cat))
            print(f"  • {cat} ({count} prompts)")
            
    elif args.command == "stats":
        vault = load_vault()
        prompts = vault["prompts"]
        print("\n📊 Vault Statistics")
        print("─" * 40)
        print(f"  Total prompts:  {len(prompts)}")
        print(f"  Total uses:     {sum(p.get('uses', 0) for p in prompts)}")
        if prompts:
            most_used = max(prompts, key=lambda x: x.get('uses', 0))
            print(f"  Most used:      {most_used['name']} ({most_used.get('uses', 0)} uses)")
            
            # Category breakdown
            categories = {}
            for p in prompts:
                cat = p.get('category', 'general')
                categories[cat] = categories.get(cat, 0) + 1
            print("\n  By category:")
            for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
                print(f"    {cat}: {count}")
                
    elif args.command == "interactive":
        interactive_add()
        
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

