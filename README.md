# APAC Employer Policy Monitor（每两周自动抓取）

原静态页已改成：**公网可访问的 HTTPS 看板** + 后台每 14 天抓取各国劳工部门公开源，数据写在 `web/data/policies.json`。

本工具只读公开源，供 HR 监控参考，不构成法律意见。卡片链接请回到官网核对原文。

---

## 发布成公共网站（手机、发链接给别人都能打开）

推荐 **GitHub Pages**（免费 HTTPS，适合分享给同事和手机浏览器）。

### 1. 把项目推到 GitHub

在 PowerShell 中（把 `你的用户名` 换成自己的 GitHub 账号）：

```powershell
cd "C:\Users\roqian\Desktop\Test for Cursor\apac-policy-monitor"
git init
git add .
git commit -m "APAC policy monitor with public site"
gh repo create apac-policy-monitor --public --source=. --push
```

若没有安装 [GitHub CLI](https://cli.github.com/)，可在 GitHub 网页新建空仓库后：

```powershell
git remote add origin https://github.com/你的用户名/apac-policy-monitor.git
git branch -M main
git push -u origin main
```

### 2. 开启 GitHub Pages

1. 打开仓库 **Settings → Pages**
2. **Build and deployment** 里 **Source** 选 **GitHub Actions**（不要选 “Deploy from a branch”）
3. 等 **Actions** 里 **Deploy GitHub Pages** 跑绿（推送 `web/` 后会自动部署）

公网地址一般为：

`https://你的用户名.github.io/apac-policy-monitor/`

把该链接发到微信/邮件/手机浏览器即可打开。页面上有 **分享 / Share** 按钮（手机可调系统分享菜单）。

### 3. 自动更新（云端每两周抓取 + 自动重新发布）

- **biweekly-crawl**：每月 1 日、15 日 UTC 抓取并提交 JSON
- **deploy-pages**：`web/` 有变更时自动部署

也可在 **Actions → biweekly-crawl → Run workflow** 手动抓一次。

### 4. 自定义域名（可选）

在 `web/` 下放 `CNAME` 文件，内容为你的域名（如 `policy.example.com`），并在 DNS 添加 GitHub Pages 要求的记录。详见 [GitHub 文档](https://docs.github.com/pages/configuring-a-custom-domain-for-your-github-pages-site)。

### 不想用 GitHub？

- [Cloudflare Pages](https://pages.cloudflare.com/)：连接同一仓库，**Build output directory** 填 `web`
- [Netlify](https://www.netlify.com/)：拖拽 `web` 文件夹即可得临时公网链（无自动抓取，需自己定期上传 JSON）

---

## 本地预览（开发用）

```powershell
cd "C:\Users\roqian\Desktop\Test for Cursor\apac-policy-monitor"
python -m pip install -r requirements.txt
python scraper/crawl.py
python serve.py
```

浏览器打开 http://127.0.0.1:8765/  
仅在本机服务下显示 **立即抓取**；公网版由 GitHub Actions 更新数据。

## 本机每两周抓取（可选）

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\install_windows_task.ps1
```

## 覆盖市场

中国、日本、韩国、新加坡、香港、台湾、澳大利亚、新西兰、印度，以及越南/泰国/印尼/菲律宾/马来西亚（SE Asia）。