---
Authors: assad
Date: 2026-07-12
Summary: 折腾了一台联通 VN007+ 5G CPE，因为用的是流量卡，总担心超额，于是用 C# / .NET 8 / Windows Forms 写了个常驻任务栏的小工具：FiveGTrafficMonitor。除了实时显示本月已用流量，还顺手把路由器的短信收发也做进去了，附带一个本机 Web 短信中心和 HTTP API。本文介绍项目背景、功能、编译与使用方式。
Title: 用 C# 给 5G CPE 写一个任务栏流量监控 + 短信收发小工具
seo_description: 介绍 FiveGTrafficMonitor，一个基于 C# / .NET 8 / Windows Forms 的 5G CPE 任务栏流量监控与短信收发小工具，支持联通 VN007+，包含 Web 短信中心与 HTTP API。讲解项目背景、功能特性、编译与使用方法。
seo_keywords: 5G CPE, VN007+, 流量监控, C#, .NET 8, Windows Forms, 短信收发, 任务栏, 托盘程序
---

## 起因

家里用了一张流量卡插在 5G CPE 上网，设备型号是 VN007+。流量卡这种东西，最让人焦虑的就是「到底用了多少」「会不会悄悄超额」。虽然路由器后台能查，但每次都要开浏览器、登录、点菜单，实在太麻烦。

而这台 CPE 除了上网，还带短信收发功能--流量卡收到的验证码、运营商通知全在它身上。手机又收不到，得专门去后台翻，更麻烦。

于是干脆写个小工具常驻任务栏：一眼看到本月用了多少流量，顺便把短信也收发做了。这就是 FiveGTrafficMonitor。

*任务栏图标直接显示紧凑数值，鼠标悬停看精确 MB*
![托盘图标效果](https://ittechren.oss-cn-beijing.aliyuncs.com/posts/images/2026/07/11/1648/tuopan.png)

## 为什么用 C#

Windows 11 已经不再正式支持传统任务栏 DeskBand，最稳的做法是用系统托盘（通知区域）。C# 对 `NotifyIcon`、注册表自启动、DPAPI 加密、单文件发布支持都很直接，不用额外装 Python 运行环境，分发给别人也省心。再加上 GDI+ 画图标很方便，整体方案干净利落。

## 都有哪些功能

### 流量监控

- 自动登录 CPE，自动维护会话，过期自动重连。
- 任务栏图标动态显示 `823M`、`2.2G` 这种紧凑数值；悬停和右键菜单显示精确 MB。
- 使用率 <70% 绿色，70%–90% 橙色，>90% 红色，一眼看出还剩多少额度。
- 阈值告警：到设定比例弹托盘气泡；支持开机自启、刷新间隔自定义（10–3600 秒）、手动刷新。

### 桌面流量条

右键托盘勾选「显示流量条」，桌面右下角会浮出一张深色卡片，这是我最常用的面板。它分完整模式和紧凑模式两种：

- **主数值**：本月已用流量，`12.34 G` 这种两位小数的大字，下面跟一行 `12.34 G / 12345.67 M` 的换算。
- **剩余与进度**：有套餐上限时显示 `剩余 87.66 G（12.3%）`；没设上限就显示 `未设置流量上限`。
- **预估**：`约可用 9 天 · 本月剩 18 天`，按当前消耗速率估个大概。
- **实时速度**：每秒刷新 `↓ 3.21 MB/s` `↑ 256 KB/s`，单位自动切换。
- **今日峰值**：完整模式下额外显示当天上下行峰值。

卡片整体是圆角渐变 + 主题色辉光，主题色随流量状态变（绿/橙/红）。左键单击立即刷新，左键拖动能挪到任意屏幕位置，松开自动记住坐标。读取出错时主题色变红、数值显示 `--`，并提示去检查路由器连接。

> ![桌面流量条完整模式](https://ittechren.oss-cn-beijing.aliyuncs.com/posts/images/2026/07/11/1648/llt.png)
>
> *完整模式：已用 / 剩余 / 预估天数 / 实时速度 / 今日峰值*

> ![桌面流量条紧凑模式](https://ittechren.oss-cn-beijing.aliyuncs.com/posts/images/2026/07/11/1648/minillt.png)
>
> *紧凑模式：省略峰值，体积更小，适合角落常驻*

### 短信收发

每次刷新周期顺带轮询收件箱，收到新短信会有两层提醒：

- **托盘气泡**：单条显示 `号码：正文预览`，多条显示 `收到 N 条新短信，最新来自 号码`。
- **桌面通知面板**：右下角弹出一个深色圆角窗口，显示发件人、日期、正文（字数提示 `xx / 140 字`），底部直接带回复框，输完点「发送」即可，单条上限 70 字。

通知面板为无边框置顶窗口，可拖动；点 × 关闭只隐藏不销毁，下次复用。发送按钮会变色反馈：发送中变 `发送中…`，成功变绿色 `✓ 短信已发送`，失败变红色 `✕ 发送失败`。已通知过的短信按索引去重，不会反复弹窗。

> ![新短信通知面板](https://ittechren.oss-cn-beijing.aliyuncs.com/posts/images/2026/07/11/1648/recvsms.png)
>
> *收到新短信弹出的通知面板，可直接回复*

### Web 短信中心

内嵌 HTTP 服务，浏览器访问 `http://localhost:8800/` 就是一个「5G 短信中心」单页应用：

- 支持密码登录、列表 / 对话两种视图、发送短信、改密码、暗色 / 亮色主题切换，登录后每 5 秒自动刷新。
- 列表视图按索引降序展示所有短信（收件箱 + 发件箱），未读带绿色徽标。
- 对话视图按联系人分组，气泡式展示收发记录，可在此直接回复。
- 右侧「发送短信」卡片填收件人和内容即可发送，支持 `+86` 开头号码。
- 仅监听 `localhost` / `127.0.0.1`，不对外网开放。

> ![Web 短信中心列表视图](https://ittechren.oss-cn-beijing.aliyuncs.com/posts/images/2026/07/11/1648/webui_smslist.png)
>
> *列表视图：所有短信按索引降序，未读带绿色徽标*

> ![Web 短信中心对话视图](https://ittechren.oss-cn-beijing.aliyuncs.com/posts/images/2026/07/11/1648/webui_smslist1.png)
>
> *对话视图：按联系人分组，气泡式展示，可直接回复*

### HTTP API

顺带提供 REST 接口给本机脚本调用，支持 `X-API-Key` 请求头免密鉴权，API Key 每次启动自动重新生成。常用接口：

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/api/auth/login` | 登录，请求体 `{ "password": "..." }` |
| GET | `/api/sms/list` | 返回所有短信（需鉴权） |
| POST | `/api/sms/send` | 发送短信，请求体 `{ "phoneNo": "...", "content": "..." }` |
| GET | `/api/info` | 返回 API Key、端口、调用示例 |

本机调用示例：

```python
import requests

resp = requests.post(
    "http://127.0.0.1:8800/api/sms/send",
    json={"phoneNo": "10086", "content": "你好"},
    headers={"X-API-Key": "<在设置窗口或 /api/info 查看的 Key>"},
)
print(resp.json())
```

### 安全

- 路由器密码用 Windows DPAPI 加密，绑定当前用户，换机器需重输。
- Web 密码明文存储，默认 `admin888`，建议首次用完就改。

## 设置窗口

右键托盘 -> 「设置」打开设置窗口。窗口不大，但把所有可调项都塞进去了，分几块：

- **连接**：路由器地址、用户名、密码（掩码输入），底部「测试连接」按钮会真的登录一次并读流量，成功显示 `连接成功：本月已使用 12.34 G`。
- **基础**：刷新间隔、开机启动、显示流量条、预警阈值（`例如 70, 80, 90；留空则关闭`）。
- **显示**：测速网卡下拉、托盘图标显示模式（已用流量 / 剩余流量 / 使用百分比 / 实时下载速度）、流量条透明度与字体缩放、紧凑模式、始终置顶。
- **短信 / Web**：短信通知开关、Web 服务开关与端口、API Key（只读）、Web 密码（带显示 / 隐藏切换）。

> ![设置窗口-连接](https://ittechren.oss-cn-beijing.aliyuncs.com/posts/images/2026/07/11/1648/setting.png)
>
> *连接设置：地址 / 用户名 / 密码 + 测试连接*

> ![设置窗口-显示与 Web](https://ittechren.oss-cn-beijing.aliyuncs.com/posts/images/2026/07/11/1648/set_webui.png)
>
> *显示与 Web 设置：托盘模式、流量条外观、短信与 Web 服务*

## 怎么编译

1. 装 [.NET 8 SDK](https://dotnet.microsoft.com/download/dotnet/8.0)（仅 Windows 可构建运行）。
2. 项目目录开 PowerShell。

快速验证编译：

```powershell
dotnet build FiveGTrafficMonitor.csproj -c Debug
```

发布（先放行脚本）：

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\publish.ps1            # 单文件、框架依赖，目标机需装 .NET 8 Desktop Runtime
.\publish-offline.ps1    # 多文件、框架依赖，不下载运行时包，适合离线/NU1100 场景
```

产物是 `publish\FiveGTrafficMonitor.exe`，依赖 .NET 8 Desktop Runtime x64，体积比自包含小不少。

> 小坑：发布时若报 `NU1100`（解析不了 `win-x64` 运行时包），别动项目里的 `NuGet.Config`--它专门用 `<clear/>` 清掉上级源只留官方 nuget.org 来解决这个问题。网络不通就改用 `publish-offline.ps1`。

## 怎么用

1. 运行 `FiveGTrafficMonitor.exe`，任务栏出现图标。首次启动没配过密码会自动弹设置窗口。
2. 填路由器地址、用户名、**明文密码**，点「测试连接」，成功后保存。
3. 勾选「显示流量条」，拖到顺手的位置，单击即可手动刷新。
4. 想用 Web 短信中心：浏览器开 `http://localhost:8800/`，用 Web 密码登录（默认 `admin888`，可在设置里查改）。

配置文件在 `%LOCALAPPDATA%\FiveGTrafficMonitor\config.json`，常用项都能在设置窗口改，不细列了。

## 技术上怎么跟 CPE 对话

VN007+ 的 Web 后台本质是往 `/cgi-bin/http.cgi` POST 一堆 `cmd=xxx` 的表单，流程和它前端 `login.js` 对齐：

1. `cmd=232` 取一次性 `token`；
2. `cmd=100` 登录，`passwd = SHA256(token + 明文密码)`，输出 64 位小写十六进制；
3. `cmd=337` 查流量，读 `mon_download_flow`（本月用量 MB）、`limitSwitch`/`limitSize`（套餐上限）、`startDate`（周期起始日）；
4. `cmd=12` 查短信（收件箱 / 发件箱），响应是逗号分隔的 Base64 列表；
5. `cmd=13` 发短信，正文做 Base64(UTF8) 编码。

`HttpClient` 关掉自动 Cookie，`sessionId` 手动塞 `Cookie` 头；会话过期就捕获异常自动重登重试一次。固件升级导致登录算法变了的话，基本只改 `RouterClient.LoginAsync` 就行。

## 一点感想

写这个工具的初衷很朴素--少开一次浏览器、少点几次菜单。但顺手把短信和 Web 接口都做上之后，这台 CPE 才真正像个「能用的设备」：验证码不用再翻后台，本机脚本也能通过 HTTP API 自动发短信。

项目纯框架依赖、零 NuGet 包，结构按 Domain / Application / Infrastructure / UI 分层，单 `.csproj` 走到底，整体很轻。如果你也在用类似的 5G CPE，欢迎拿去改改试试。