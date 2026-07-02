# 一键启动 Flask 博客开发服务器
# 用法：在项目根目录下运行 .\start.ps1

$ErrorActionPreference = "Stop"

# 切换到脚本所在目录（项目根目录）
Set-Location -LiteralPath $PSScriptRoot

# 虚拟环境路径
$venvActivate = Join-Path $PSScriptRoot ".venv\Scripts\Activate.ps1"

# 如果虚拟环境不存在则创建并安装依赖
if (-not (Test-Path -LiteralPath $venvActivate)) {
    Write-Host "未检测到虚拟环境，正在创建 .venv ..." -ForegroundColor Yellow
    python -m venv .venv
    & $venvActivate
    Write-Host "正在安装依赖 ..." -ForegroundColor Yellow
    pip install -e ".[dev,server]"
} else {
    # 激活已有虚拟环境
    & $venvActivate
}

# 站点地址
$url = "http://127.0.0.1:5000"

# 后台等待服务器就绪后自动打开浏览器
Start-Job -ScriptBlock {
    param($u)
    # 轮询直到端口可访问
    for ($i = 0; $i -lt 30; $i++) {
        try {
            Invoke-WebRequest -Uri $u -UseBasicParsing -TimeoutSec 2 | Out-Null
            Start-Process $u
            break
        } catch {
            Start-Sleep -Milliseconds 500
        }
    }
} -ArgumentList $url | Out-Null

# 启动开发服务器
Write-Host "启动 Flask 开发服务器 ..." -ForegroundColor Green
flask --app blog:create_app --debug run
