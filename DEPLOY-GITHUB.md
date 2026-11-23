# 用 GitHub 发布公共网站（5 分钟）

项目目录：`C:\Users\roqian\Desktop\Test for Cursor\apac-policy-monitor`  
本地已 `git init`，分支 `main`，首次提交已完成。

## 第一步：在网页上新建仓库

1. 打开 https://github.com/new  
2. **Repository name**：`apac-policy-monitor`（或你喜欢的名字）  
3. 选 **Public**  
4. **不要**勾选 “Add a README”（仓库要空的）  
5. 点 **Create repository**

## 第二步：推送代码（PowerShell）

把下面命令里的 `你的用户名` 换成你的 GitHub 用户名：

```powershell
cd "C:\Users\roqian\Desktop\Test for Cursor\apac-policy-monitor"
git remote add origin https://github.com/你的用户名/apac-policy-monitor.git
git push -u origin main
```

若提示登录，用浏览器完成 GitHub 验证（或 Personal Access Token 当密码）。

如果已经添加过 `origin` 且地址不对：

```powershell
git remote set-url origin https://github.com/你的用户名/apac-policy-monitor.git
git push -u origin main
```

## 第三步：开启 GitHub Pages

1. 打开仓库 → **Settings** → 左侧 **Pages**  
2. **Build and deployment** → **Source** 选 **GitHub Actions**（不要选 Branch）  
3. 打开 **Actions** 标签，等 **Deploy GitHub Pages** 变绿（约 1–2 分钟）  
   - 若没有自动跑：Actions → **Deploy GitHub Pages** → **Run workflow**

## 第四步：打开公网地址

地址一般为：

```text
https://你的用户名.github.io/apac-policy-monitor/
```

手机浏览器或发给别人用这个 **https** 链接即可。

## 自动更新

- **Deploy GitHub Pages**：`web/` 有改动就重新发布  
- **biweekly-crawl**：每月 1 日、15 日（UTC）自动抓取政策并提交 JSON，随后会自动触发部署  

可手动抓一次：Actions → **biweekly-crawl** → **Run workflow**

## 第一次部署前若仓库缺 Pages 权限

Settings → Pages 若提示配置失败，到 Settings → Actions → General，  
**Workflow permissions** 选 **Read and write permissions**，保存后再跑一次 Deploy。

## Authorize 按钮点不了？（常见：公司账号 / SSO）

设备码页里 **Authorize GitHub CLI** 灰色不可点时，不要用网页授权，改用 **Token**：

1. 浏览器打开：https://github.com/settings/tokens  
   - 个人项目：用 **Fine-grained token** 或 **Tokens (classic)**  
   - 若页面顶部有 **「Configure SSO」/「Enable SSO」**，必须先对你的组织点 **Authorize**（否则 Token 也不能推代码）
2. 新建 Token，至少勾选：**repo**（或 fine-grained 对该仓库 Read and write）
3. 复制 Token（只显示一次）

PowerShell（把 `ghp_xxxx` 换成你的 Token，不要发给任何人）：

```powershell
@'
ghp_你的Token粘贴在这里
'@ | & "$env:ProgramFiles\GitHub CLI\gh.exe" auth login --with-token
& "$env:ProgramFiles\GitHub CLI\gh.exe" auth status
cd "C:\Users\roqian\Desktop\Test for Cursor\apac-policy-monitor"
.\publish-github.ps1
```

若公司策略禁止 PAT，只能：用**个人 GitHub 账号**建公开仓，或让 IT 放行 GitHub CLI OAuth。

### 浏览器仍异常时

- 无痕窗口打开 https://github.com/login/device  
- 确认登录的是**要用来放仓库**的那个账号（不是另一个）  
- 暂时关闭广告拦截插件后再试设备码

## 可选：安装 GitHub CLI（以后一条命令建库）

```powershell
winget install --id GitHub.cli
gh auth login
cd "C:\Users\roqian\Desktop\Test for Cursor\apac-policy-monitor"
gh repo create apac-policy-monitor --public --source=. --push
```

然后在 Settings → Pages 选 **GitHub Actions** 即可。