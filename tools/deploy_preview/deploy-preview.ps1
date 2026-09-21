param(
  [string]$SourceRef = "",
  [string]$PreviewRepository = "gitmaruneko/yuban-preview",
  [string]$Workflow = "deploy-preview.yml",
  [string]$PreviewUrl = "https://gitmaruneko.github.io/yuban-preview/",
  [string]$ExpectedText = ""
)

$ErrorActionPreference = "Stop"
Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Path)
$repoRoot = (git rev-parse --show-toplevel) 2>$null
if ($LASTEXITCODE -ne 0) {
  throw "Not inside a git repository."
}
Set-Location $repoRoot

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
  throw "GitHub CLI (gh) is required."
}

if (-not $SourceRef) {
  $SourceRef = (git branch --show-current).Trim()
}
if (-not $SourceRef) {
  throw "Could not determine the source ref."
}

if ($SourceRef -match '^[0-9a-fA-F]{40}$') {
  $sourceSha = $SourceRef.ToLowerInvariant()
} else {
  $remoteRef = "refs/heads/$SourceRef"
  $remoteLine = (git ls-remote origin $remoteRef).Trim()
  if ($LASTEXITCODE -ne 0 -or -not $remoteLine) {
    throw "Source ref '$SourceRef' was not found on origin. Push it before deploying a preview."
  }
  $sourceSha = ($remoteLine -split '\s+')[0]
}

if ($sourceSha -notmatch '^[0-9a-fA-F]{40}$') {
  throw "Could not resolve '$SourceRef' to a full commit SHA."
}

Write-Output "Deploying $SourceRef ($sourceSha) to $PreviewRepository"
$dispatchOutput = gh workflow run $Workflow --repo $PreviewRepository --ref main -f "source_ref=$sourceSha" 2>&1 | Out-String
if ($LASTEXITCODE -ne 0) {
  throw $dispatchOutput.Trim()
}

$runIdMatch = [regex]::Match($dispatchOutput, '/actions/runs/(\d+)')
if (-not $runIdMatch.Success) {
  throw "The workflow was dispatched, but its run ID could not be determined.`n$dispatchOutput"
}
$runId = $runIdMatch.Groups[1].Value
$runUrl = "https://github.com/$PreviewRepository/actions/runs/$runId"
Write-Output "Workflow: $runUrl"

gh run watch $runId --repo $PreviewRepository --exit-status
if ($LASTEXITCODE -ne 0) {
  throw "Preview workflow failed: $runUrl"
}

$cacheBust = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
$refUrl = "$PreviewUrl`preview-ref.txt?verify=$cacheBust"
$versionUrl = "$PreviewUrl`preview-version.txt?verify=$cacheBust"
$pageUrl = "$PreviewUrl`learning-materials/index.html?verify=$cacheBust"
$publishedRef = (Invoke-WebRequest -UseBasicParsing $refUrl).Content.Trim()
$publishedSha = (Invoke-WebRequest -UseBasicParsing $versionUrl).Content.Trim()
$page = (Invoke-WebRequest -UseBasicParsing $pageUrl).Content

if ($publishedSha -ne $sourceSha) {
  throw "Preview SHA mismatch. Expected $sourceSha, received $publishedSha."
}
if ($publishedRef -ne $SourceRef -and $publishedRef -ne $sourceSha) {
  throw "Preview ref mismatch. Expected $SourceRef or $sourceSha, received $publishedRef."
}
if ($ExpectedText -and -not $page.Contains($ExpectedText)) {
  throw "Preview page does not contain expected text: $ExpectedText"
}

[pscustomobject]@{
  Workflow = $runUrl
  SourceRef = $SourceRef
  SourceSha = $sourceSha
  PublishedRef = $publishedRef
  PublishedSha = $publishedSha
  PreviewUrl = $PreviewUrl
  ExpectedTextFound = [bool]$ExpectedText -and $page.Contains($ExpectedText)
}
