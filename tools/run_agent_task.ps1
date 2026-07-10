# Local entry point for the autonomous task runner (Windows Task Scheduler).
# Registers as: every 20 minutes; exits in seconds when the inbox is empty.
# See ops/BRAIN-SETUP.md for the schtasks registration command.

$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo

# Make Node (git hooks/site), Python 3.12 (validators) and fcc-claude reachable
$env:Path = "C:\Program Files\nodejs;$env:LOCALAPPDATA\Programs\Python\Python312;$env:LOCALAPPDATA\Programs\Python\Python312\Scripts;$env:USERPROFILE\.local\bin;$env:Path"

$py = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"
& $py "$repo\tools\run_agent_task.py" --runner local @args
exit $LASTEXITCODE
