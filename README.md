# Multi-Agent Development Template

[![Multi-Agent](https://img.shields.io/badge/development-multi--agent-blue)](https://github.com/your-org/multi-agent-template)
[![Orchestration](https://img.shields.io/badge/orchestration-autonomous-green)](https://claude.ai/code)
[![Logging](https://img.shields.io/badge/logging-YAML-orange)](./logs/agent-activity.yaml)

This is a template repository for multi-agent software development using Claude Code's orchestration capabilities.

## ## Multi-Agent Architecture Multi-Agent Architecture

This template includes 7 specialized agents:

- **orchestrator** - Coordinates all agents and manages workflow
- **developer** - Implementation and coding tasks
- **qa** - Testing, validation, and quality assurance  
- **devops** - CI/CD, deployment, and git workflow management
- **infrastructure** - Monitoring, documentation, and operations
- **innovation** - Suggests new features and improvements
- **cleanup** - Refactoring and technical debt management

## ## Quick Start Quick Start

1. **Copy this template** to your new project directory
2. **Update CLAUDE.md** with your project-specific instructions
3. **Customize development_checklist.yaml** for your project phases
4. **Run the orchestrator** with `/orchestrator` in Claude Code

```bash
# Initialize the multi-agent system
./scripts/setup-multiagent.sh

# Scan existing codebase
python scripts/scan-codebase.py

# View activity logs
python scripts/log-agent-activity.py --stats

# Generate workflow flowchart
python scripts/generate-flowchart.py --condensed
```

## ## Activity Tracking Activity Tracking

All agent activities are tracked in YAML format with:
- Running averages for cleanup optimization
- Programmatic analysis capabilities  
- Mermaid flowchart generation
- Terminal-friendly statistics

## ## Template Structure Template Structure

```
+-- .claude/
|   +-- commands/          # Agent command definitions
|   +-- settings.local.json
+-- logs/
|   +-- agent-activity.yaml    # Main activity log
|   +-- *.py                   # Analysis scripts
+-- suggestions/
|   +-- features.md            # Innovation agent output
|   +-- cleanup-tracker.yaml   # Cleanup tracking
+-- scripts/
|   +-- log-agent-activity.py  # Activity logging
|   +-- scan-codebase.py       # Codebase scanning
|   +-- generate-flowchart.py  # Mermaid generation
+-- docs/                      # Documentation
```

## ## Customization Customization

1. **Edit CLAUDE.md** - Add project-specific context and requirements
2. **Update development_checklist.yaml** - Define your project phases
3. **Configure agents** - Modify agent commands in `.claude/commands/`
4. **Set thresholds** - Adjust cleanup and monitoring thresholds

## ## Monitoring Monitoring

- **Agent Activity**: View in `logs/agent-activity.yaml`
- **Cleanup Status**: Track in `suggestions/cleanup-tracker.yaml`  
- **Feature Suggestions**: Review in `suggestions/features.md`
- **Flowcharts**: Generate with `scripts/generate-flowchart.py`

## ## Example Usage Example Usage

```bash
# Log an agent activity
python scripts/log-agent-activity.py \
  --agent developer \
  --agent-type implementation \
  --instruction "Add user authentication" \
  --result "JWT auth system implemented" \
  --duration 1800 \
  --lines-added 245 \
  --files-modified 5

# Scan for cleanup opportunities  
python scripts/scan-codebase.py

# Generate workflow visualization
python scripts/generate-flowchart.py --condensed --output workflow.mmd
```

## ## Contributing Contributing

This template is designed to evolve. Suggestions for new agents, improved tracking, or better visualization are welcome!

---

**Built with [Claude Code](https://claude.ai/code) Multi-Agent Orchestration**