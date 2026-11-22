# 每次从主站数据重新生成 README 并推送到 GitHub / Gitee
# 用法：.\tools\update.ps1            （只更新 README 并本地提交）
#       .\tools\update.ps1 -Push      （再 push 到远端）

param([switch]$Push)

$ErrorActionPreference = "Stop"
$repo = Split-Path $PSScriptRoot -Parent
Set-Location $repo

python ".\tools\make_readme.py"

git add README.md data/courses.json
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    git commit -m "chore: 更新课程编号对照表 $(Get-Date -Format yyyy-MM-dd)"
    Write-Host "已提交"
} else {
    Write-Host "无变化，跳过提交"
}

if ($Push) {
    git push origin HEAD
    if (Test-Path .git\gitee-remote) { git push gitee HEAD }
    Write-Host "已推送"
}
