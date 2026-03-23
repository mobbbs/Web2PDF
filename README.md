# URL to PDF for AI Reading

将网页 URL 转换为 AI 友好的 PDF。

## 功能

- API 模式：`POST /convert`
- 交互模式：终端输入网址后直接转换
- 支持 JS 动态页面渲染（Playwright）
- 正文抽取清洗（Readability）
- A4 PDF 输出（带页码）

## 一、源码模式（开发/本机运行）

### 1) 安装依赖

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install chromium
```

### 2) 交互式使用（推荐）

直接双击：

- `start-url2pdf.bat`

或者命令行运行：

```powershell
python -m app.interactive
```

运行后输入 URL，例如：

`https://learnopengl-cn.github.io/05%20Advanced%20Lighting/06%20HDR/`

转换完成后 PDF 在 `output/` 目录。

### 3) API 模式使用

启动服务：

```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

调用接口：

```powershell
curl -X POST "http://127.0.0.1:8000/convert" `
  -H "Content-Type: application/json" `
  -d "{\"url\":\"https://learnopengl-cn.github.io/05%20Advanced%20Lighting/06%20HDR/\"}"
```

## 二、Wheel 安装模式（`whl`）

安装：

```powershell
pip install .\dist\url2pdf_ai_reader-0.1.0-py3-none-any.whl
python -m playwright install chromium
```

使用：

```powershell
url2pdf-run
```

如果命令不在 PATH，可用：

```powershell
python -m app.interactive
```

## 三、Release 解压即用（推荐给最终用户）

从 GitHub Release 下载：

- `url2pdf-ai-reader-vX.Y.Z-windows-x64.zip`

使用步骤：

1. 解压 zip
2. 双击 `start-url2pdf.bat`
3. 在终端粘贴网址并回车
4. 等待生成 PDF（输出到 `output/`）

说明：

- Release 包内含 `url2pdf-run.exe` 和 Chromium 运行资源
- 不需要本机安装 Python

## 四、如何发布 Release

### 1) 本地准备版本

```powershell
.\scripts\release.ps1 -Version 0.1.1
```

此命令会自动：

- 更新版本号
- 创建 commit
- 创建 tag（`v0.1.1`）

### 2) 推送触发发布

```powershell
git push origin HEAD --tags
```

GitHub Actions（`.github/workflows/release.yml`）会自动：

- 构建 `sdist` / `wheel`
- 构建 Windows 便携包（可双击直接用）
- 创建 GitHub Release 并上传产物
