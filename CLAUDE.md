# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

[CUSTOMIZE THIS SECTION FOR YOUR PROJECT]

This is a multi-agent development project using Claude Code's orchestration capabilities. The system uses 7 specialized agents that collaborate to implement features, ensure quality, and maintain code health.

## Multi-Agent Architecture

### Agent Roster
- **orchestrator** - Coordinates all agents and manages development workflow
- **developer** - Feature implementation, coding, and architecture decisions  
- **qa** - Testing, validation, and quality assurance
- **devops** - CI/CD, deployment, and git workflow management
- **infrastructure** - Documentation, monitoring, and external integrations
- **innovation** - Suggests new features and improvements
- **cleanup** - Refactoring and technical debt management

### Agent Communication
All agent activities are logged in `logs/agent-activity.yaml` with:
- Running statistics for optimization
- Flowchart generation capabilities
- Performance tracking and analysis

## Development Commands

[CUSTOMIZE THESE FOR YOUR PROJECT]

### Environment Setup
```bash
# Add your project-specific setup commands
pip install -r requirements.txt
```

### Running the Application  
```bash
# Add your project-specific run commands
python src/main.py
```

### Testing
```bash
# Add your project-specific test commands
pytest
```

## Project Structure

[CUSTOMIZE THIS FOR YOUR PROJECT]

- `src/` - Main source code
- `tests/` - Test files
- `docs/` - Documentation
- `scripts/` - Utility scripts
- `logs/` - Agent activity logs
- `suggestions/` - Agent suggestions and tracking

## Development Notes

### Multi-Agent Workflow
1. The **orchestrator** analyzes requirements and coordinates agents
2. **developer** implements features and core functionality
3. **qa** validates implementation with comprehensive testing
4. **devops** sets up CI/CD and deployment infrastructure
5. **infrastructure** adds monitoring, documentation, and operational support
6. **innovation** suggests improvements and new features
7. **cleanup** maintains code quality and reduces technical debt

### Activity Logging
Every agent action is logged with:
- Duration and impact metrics
- Files modified and lines changed
- Triggering relationships between agents
- Progress toward project completion

### Quality Gates
- All implementations must pass QA validation
- Cleanup agent maintains technical debt thresholds
- Innovation agent suggests improvements without bloat
- Infrastructure ensures production readiness

## Agent Instructions

### For Developer Agent
- Follow existing code patterns and architecture
- Use established libraries and frameworks
- Create comprehensive tests for all new features
- Document APIs and complex logic
- Update development checklist as tasks complete

### For QA Agent  
- Validate all functionality with automated tests
- Check edge cases and error handling
- Verify integration between components
- Ensure performance meets requirements
- Approve or reject implementations based on quality

### for DevOps Agent
- Set up CI/CD pipelines and automation
- Create deployment configurations
- Establish branching and release strategies
- Configure monitoring and alerting
- Document operational procedures

### For Infrastructure Agent
- Add monitoring and observability
- Create operational documentation  
- Set up external service integrations
- Establish backup and recovery procedures
- Ensure security and compliance

### For Innovation Agent
- Analyze current functionality for improvement opportunities
- Research new technologies and best practices
- Suggest features that add user value
- Avoid suggesting improvements for simple/complete code
- Write suggestions to `suggestions/features.md` with approval checkboxes

### For Cleanup Agent
- Scan codebase systematically for technical debt
- Remove code duplication and improve structure  
- Optimize performance bottlenecks
- Update dependencies and remove unused code
- Track cleanup activities in `suggestions/cleanup-tracker.yaml`
- Only suggest cleanup when beneficial (not for simple/clean code)

## Important Reminders

- **Activity Logging**: All agent actions must be logged via `scripts/log-agent-activity.py`
- **Running Statistics**: System tracks cleanup frequency and impact automatically
- **Incremental Cleanup**: Cleanup agent works in chunks over time, not all at once
- **Quality Focus**: Every change must maintain or improve code quality
- **Documentation**: Keep all documentation current and accurate

---

**Multi-Agent Development powered by [Claude Code](https://claude.ai/code)**