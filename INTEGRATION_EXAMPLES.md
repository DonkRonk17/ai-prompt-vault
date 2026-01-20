# AI Prompt Vault - Integration Examples

Real code examples for integrating with other systems.

## Python API Integration

### Basic Integration
```python
import prompt_vault

# Initialize
prompt_vault.init_vault()

# Add prompt
prompt_vault.add_prompt('test', 'content', category='testing')

# Use prompt
content = prompt_vault.use_prompt('test', copy_to_clipboard=False)
print(content)
```

### Flask Integration
```python
from flask import Flask
import prompt_vault

app = Flask(__name__)

@app.route('/prompts/<name>')
def get_prompt(name):
    prompt = prompt_vault.get_prompt(name)
    return prompt['content'] if prompt else 'Not found', 404
```

### FastAPI Integration
```python
from fastapi import FastAPI
import prompt_vault

app = FastAPI()

@app.get('/prompts/{name}')
async def get_prompt(name: str):
    prompt = prompt_vault.get_prompt(name)
    if prompt:
        return {
            'name': prompt['name'],
            'content': prompt['content'],
            'category': prompt['category']
        }
    return {'error': 'Not found'}, 404
```

## CLI Integration

### Shell Script
```bash
#!/bin/bash
# quick-prompt.sh

PROMPT_NAME=\
python ~/AI-Prompt-Vault/prompt_vault.py use "\" --no-copy
```

### Git Hook
```bash
# .git/hooks/prepare-commit-msg
#!/bin/bash
python ~/AI-Prompt-Vault/prompt_vault.py use 'commit-template' --no-copy >> "\"
```

## Team Brain Integration

### With SynapseLink
```python
import prompt_vault
from synapselink import quick_send

# Get prompt for agent communication
msg_template = prompt_vault.get_prompt('synapse-notification')

# Send to agents
quick_send('FORGE,ATLAS', 'Update', msg_template['content'])
```

### With MemoryBridge
```python
import prompt_vault
from memorybridge import MemoryBridge

# Get memory query template
query_template = prompt_vault.get_prompt('memory-search')

# Query memory
bridge = MemoryBridge()
results = bridge.query(query_template['content'])
```

### With TaskQueuePro
```python
import prompt_vault
from taskqueuepro import TaskQueuePro

# Get task template
task_template = prompt_vault.get_prompt('high-priority-task')

# Create task
queue = TaskQueuePro()
queue.add_task(task_template['content'], priority='high')
```

## IDE Integration

### VS Code Task
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Get Code Review Prompt",
      "type": "shell",
      "command": "python",
      "args": ["~/AI-Prompt-Vault/prompt_vault.py", "use", "code-review"]
    }
  ]
}
```

### VS Code Snippet
```json
{
  "AI Prompt Vault Get": {
    "prefix": "pv",
    "body": [
      "python ~/AI-Prompt-Vault/prompt_vault.py use '\'"
    ],
    "description": "Get prompt from vault"
  }
}
```

## Automation Examples

### Cron Backup
```bash
# Crontab entry
0 0 * * * python ~/AI-Prompt-Vault/prompt_vault.py export ~/backups/prompts-.json
```

### Weekly Stats Email
```bash
#!/bin/bash
python ~/AI-Prompt-Vault/prompt_vault.py stats > /tmp/stats.txt
mail -s 'Weekly Prompt Stats' you@example.com < /tmp/stats.txt
```

## Advanced Integration

### Custom Prompt Manager
```python
class TeamPromptManager:
    def __init__(self):
        prompt_vault.init_vault()
    
    def get_agent_prompt(self, agent: str, task: str) -> str:
        prompt_name = f'{agent.lower()}-{task}'
        prompt = prompt_vault.get_prompt(prompt_name)
        return prompt['content'] if prompt else None
    
    def sync_team_prompts(self, repo_path: str):
        import subprocess
        subprocess.run(['git', 'pull'], cwd=repo_path)
        prompt_vault.import_prompts(f'{repo_path}/team-prompts.json', overwrite=True)
```

---

**Version:** 1.0  
**Last Updated:** January 2026  
**For:** Integration developers and Team Brain agents
