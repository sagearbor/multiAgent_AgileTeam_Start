#!/usr/bin/env python3
"""
Multi-Agent Development System Setup Script

Installs the Claude Code multi-agent system into an existing git repository.
Validates target directory and safely copies all required files with conflict detection.
"""

import os
import sys
import shutil
import argparse
from pathlib import Path


def is_git_repository(path):
    """Check if path is a git repository (has .git directory)."""
    git_path = Path(path) / '.git'
    return git_path.exists() and git_path.is_dir()


def find_file_conflicts(source_dir, target_dir):
    """Find all files that would be overwritten, with detailed analysis."""
    conflicts = []
    
    items_to_copy = ['.claude', 'scripts', 'logs', 'suggestions']
    
    for item in items_to_copy:
        source_path = Path(source_dir) / item
        target_path = Path(target_dir) / item
        
        if not source_path.exists():
            continue
            
        if source_path.is_file():
            if target_path.exists():
                conflicts.append({
                    'type': 'file',
                    'path': str(target_path.relative_to(target_dir)),
                    'full_path': str(target_path),
                    'category': 'direct_overwrite'
                })
        elif source_path.is_dir():
            if target_path.exists() and target_path.is_dir():
                # Check for file conflicts within directories
                for source_file in source_path.rglob('*'):
                    if source_file.is_file():
                        relative_path = source_file.relative_to(source_path)
                        target_file = target_path / relative_path
                        
                        if target_file.exists():
                            # Categorize the conflict
                            category = 'unknown'
                            if 'commands/' in str(relative_path) and str(relative_path).endswith('.md'):
                                category = 'claude_agent'
                            elif str(relative_path).endswith('.py'):
                                category = 'script'
                            elif str(relative_path).endswith('.yaml'):
                                category = 'config'
                            elif str(relative_path).endswith('.md'):
                                category = 'documentation'
                            
                            conflicts.append({
                                'type': 'file',
                                'path': f"{item}/{relative_path}",
                                'full_path': str(target_file),
                                'category': category
                            })
    
    return conflicts


def display_conflict_analysis(conflicts):
    """Display detailed conflict analysis with recommendations."""
    if not conflicts:
        print("✅ No conflicts detected - safe to install!")
        return True
    
    print(f"\n⚠️  CONFLICTS DETECTED: {len(conflicts)} files would be overwritten")
    print("=" * 60)
    
    # Group conflicts by category
    by_category = {}
    for conflict in conflicts:
        category = conflict['category']
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(conflict)
    
    # Display by category with explanations
    critical_conflicts = 0
    
    for category, items in by_category.items():
        if category == 'claude_agent':
            print(f"\n🤖 CLAUDE AGENTS ({len(items)} conflicts):")
            print("   ⚠️  CRITICAL: These would overwrite your existing Claude agents!")
            critical_conflicts += len(items)
            for item in items:
                agent_name = Path(item['path']).stem
                print(f"   ❌ {item['path']} - Your existing '{agent_name}' agent would be replaced")
        
        elif category == 'script':
            print(f"\n📜 SCRIPTS ({len(items)} conflicts):")
            print("   ⚠️  These would overwrite your existing scripts:")
            for item in items:
                print(f"   ❌ {item['path']}")
        
        elif category == 'config':
            print(f"\n⚙️  CONFIG FILES ({len(items)} conflicts):")
            print("   ℹ️  These contain activity logs and settings:")
            for item in items:
                print(f"   ⚠️  {item['path']} - existing data would be lost")
        
        elif category == 'documentation':
            print(f"\n📄 DOCUMENTATION ({len(items)} conflicts):")
            for item in items:
                print(f"   ⚠️  {item['path']}")
        
        else:
            print(f"\n❓ OTHER FILES ({len(items)} conflicts):")
            for item in items:
                print(f"   ❌ {item['path']}")
    
    # Provide recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    
    if critical_conflicts > 0:
        print(f"   🚨 CRITICAL: {critical_conflicts} Claude agent conflicts detected!")
        print(f"   📋 You have existing agents that would be overwritten.")
        print(f"   🤔 Consider:")
        print(f"      • Backup your existing .claude/commands/ directory first")
        print(f"      • Review which agents you actually need")
        print(f"      • Manually merge agent functionality if needed")
    
    print(f"   🔧 Options:")
    print(f"      • Use --force to proceed anyway (creates backups)")
    print(f"      • Exit now and manually resolve conflicts")
    print(f"      • Use --backup to create timestamped backups first")
    
    return False


def create_backups(conflicts, target_dir):
    """Create timestamped backups of conflicting files."""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(target_dir) / f".multiagent_backup_{timestamp}"
    
    print(f"\n💾 Creating backups in: {backup_dir}")
    backup_dir.mkdir(exist_ok=True)
    
    backed_up = []
    for conflict in conflicts:
        source_file = Path(conflict['full_path'])
        if source_file.exists():
            # Preserve directory structure in backup
            rel_path = Path(conflict['path'])
            backup_file = backup_dir / rel_path
            backup_file.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.copy2(source_file, backup_file)
            backed_up.append(conflict['path'])
            print(f"   ✅ Backed up: {conflict['path']}")
    
    print(f"   📁 {len(backed_up)} files backed up to: {backup_dir}")
    return backup_dir


def copy_multiagent_system(template_dir, target_dir, dry_run=False, force=False, create_backup=False):
    """Copy the multi-agent system files to target directory."""
    
    # Items to copy
    items_to_copy = ['.claude', 'scripts', 'logs', 'suggestions']
    
    print(f"\n📋 Installation Plan:")
    print(f"   Source: {template_dir}")
    print(f"   Target: {target_dir}")
    
    # Detect conflicts
    conflicts = find_file_conflicts(template_dir, target_dir)
    
    # Display conflict analysis
    safe_to_proceed = display_conflict_analysis(conflicts)
    
    if not safe_to_proceed and not force:
        if not dry_run:
            print(f"\n❌ Installation aborted due to conflicts.")
            print(f"   Use --force to proceed anyway, or --backup to create backups first.")
        return False
    
    if dry_run:
        print(f"\n🧪 DRY RUN - No files would be copied")
        if conflicts:
            print(f"   ⚠️  {len(conflicts)} conflicts detected (shown above)")
        return True
    
    # Create backups if requested or if there are critical conflicts
    backup_dir = None
    if create_backup or (conflicts and force):
        backup_dir = create_backups(conflicts, target_dir)
    
    # Perform the copy
    print(f"\n📂 Installing multi-agent system...")
    copied_items = []
    
    for item in items_to_copy:
        source_path = Path(template_dir) / item
        target_path = Path(target_dir) / item
        
        if not source_path.exists():
            print(f"   ⚠️  Skipping {item} - not found in template")
            continue
        
        try:
            if source_path.is_dir():
                if target_path.exists():
                    print(f"   🔄 Merging {item}/")
                    # Copy contents, preserving existing files not in source
                    for sub_item in source_path.rglob('*'):
                        if sub_item.is_file():
                            rel_path = sub_item.relative_to(source_path)
                            dest_file = target_path / rel_path
                            dest_file.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(sub_item, dest_file)
                else:
                    print(f"   📁 Creating {item}/")
                    shutil.copytree(source_path, target_path)
            else:
                print(f"   📄 Copying {item}")
                shutil.copy2(source_path, target_path)
            
            copied_items.append(item)
            
        except Exception as e:
            print(f"   ❌ Failed to copy {item}: {e}")
            return False
    
    print(f"\n✅ Successfully installed: {', '.join(copied_items)}")
    
    if backup_dir:
        print(f"💾 Backups created in: {backup_dir}")
        print(f"   You can restore files from there if needed")
    
    return True


def check_dependencies():
    """Check if required dependencies are available."""
    print(f"\n🔍 Checking dependencies...")
    
    try:
        import yaml
        print(f"   ✅ PyYAML - available")
        return True
    except ImportError:
        print(f"   ❌ PyYAML - missing")
        print(f"   Install with: pip install pyyaml")
        return False


def test_installation(target_dir):
    """Test that the installation works."""
    print(f"\n🧪 Testing installation...")
    
    # Check that key files exist
    required_files = [
        '.claude/commands/orchestrator.md',
        'scripts/log-agent-activity.py',
        'scripts/generate-flowchart.py', 
        'logs/agent-activity.yaml',
        'suggestions/cleanup-tracker.yaml'
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = Path(target_dir) / file_path
        if not full_path.exists():
            missing_files.append(file_path)
        else:
            print(f"   ✅ {file_path}")
    
    if missing_files:
        print(f"   ❌ Missing files: {', '.join(missing_files)}")
        return False
    
    # Test running the stats command
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, 'scripts/log-agent-activity.py', '--stats'
        ], cwd=target_dir, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print(f"   ✅ Scripts working - stats command succeeded")
            return True
        else:
            print(f"   ❌ Scripts failed - stats command returned {result.returncode}")
            print(f"       Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ⚠️  Could not test scripts: {e}")
        return True  # Don't fail installation for test issues


def main():
    parser = argparse.ArgumentParser(
        description="Install Claude Code Multi-Agent Development System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python setup_multiagent.py /path/to/my/existing/repo
  python setup_multiagent.py . --dry-run
  python setup_multiagent.py ../my-project --force --backup
        """
    )
    
    parser.add_argument('target_repo', 
                       help='Path to existing git repository to install multi-agent system into')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be copied and detect conflicts without actually copying')
    parser.add_argument('--force', action='store_true', 
                       help='Proceed with installation even if conflicts are detected')
    parser.add_argument('--backup', action='store_true',
                       help='Create timestamped backups of any files that would be overwritten')
    parser.add_argument('--skip-git-check', action='store_true',
                       help='Skip git repository validation (use with caution)')
    parser.add_argument('--skip-deps', action='store_true',
                       help='Skip dependency checking')
    parser.add_argument('--skip-test', action='store_true', 
                       help='Skip testing installation')
    
    args = parser.parse_args()
    
    # Get absolute paths
    template_dir = Path(__file__).parent.absolute()
    target_dir = Path(args.target_repo).absolute()
    
    print(f"🤖 Multi-Agent Development System Setup")
    print(f"=" * 50)
    
    # Validate template directory
    if not template_dir.exists():
        print(f"❌ Template directory not found: {template_dir}")
        return 1
    
    # Validate target directory
    if not target_dir.exists():
        print(f"❌ Target directory does not exist: {target_dir}")
        return 1
    
    if not target_dir.is_dir():
        print(f"❌ Target is not a directory: {target_dir}")
        return 1
    
    # Check if target is a git repository
    if not args.skip_git_check and not is_git_repository(target_dir):
        print(f"❌ Target directory is not a git repository: {target_dir}")
        print(f"   Use --skip-git-check to override this validation")
        return 1
    
    print(f"✅ Target directory validated: {target_dir}")
    
    # Check dependencies
    if not args.skip_deps and not check_dependencies():
        print(f"\n💡 Install missing dependencies first:")
        print(f"   pip install pyyaml")
        return 1
    
    # Copy the multi-agent system
    if not copy_multiagent_system(template_dir, target_dir, args.dry_run, args.force, args.backup):
        print(f"\n❌ Installation failed or cancelled")
        return 1
    
    if args.dry_run:
        print(f"\n✅ Dry run completed")
        print(f"   Use without --dry-run to perform actual installation")
        print(f"   Add --force to proceed despite conflicts")
        print(f"   Add --backup to create safety backups")
        return 0
    
    # Test installation
    if not args.skip_test and not test_installation(target_dir):
        print(f"\n⚠️  Installation completed but tests failed")
        print(f"   The system may still work - try running manually:")
        print(f"   cd {target_dir}")
        print(f"   python scripts/log-agent-activity.py --stats")
        return 1
    
    # Success!
    print(f"\n🎉 Multi-Agent Development System installed successfully!")
    print(f"\n📋 Next steps:")
    print(f"   1. cd {target_dir}")
    print(f"   2. Review any overwritten files (check backups if created)")
    print(f"   3. Customize agents in .claude/commands/ for your project")
    print(f"   4. Test: python scripts/log-agent-activity.py --stats")
    print(f"   5. Start using agents with /orchestrator in Claude Code")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())