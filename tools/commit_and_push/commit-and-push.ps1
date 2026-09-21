param(
  [string]$Message = "chore: update",
  [switch]$All = $true,
  [switch]$Force = $false
)

Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Path) -ErrorAction SilentlyContinue
# Move to repo root
$repoRoot = (git rev-parse --show-toplevel) 2>$null
if ($LASTEXITCODE -ne 0) {
  Write-Error "Not inside a git repository."
  exit 1
}
Set-Location $repoRoot

if ($All) { git add -A }

# If there is nothing to commit, exit gracefully
$diff = git status --porcelain
if (-not $diff) {
  Write-Output "No changes to commit."
} else {
  if ($Force) {
    git commit --no-verify -m $Message
  } else {
    git commit -m $Message
  }
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }
}

# Push current branch
$branch = git rev-parse --abbrev-ref HEAD
if ($branch) {
  if ($Force) { git push -u origin $branch --force }
  else { git push -u origin $branch }
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }
} else {
  Write-Error "Could not determine current branch."
  exit 1
}
