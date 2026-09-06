# Railway 部署

Railway 使用根目录 `Dockerfile`，通过 Nginx 提供图谱网页。无需数据库、持久化磁盘、npm 安装或模型 API 密钥。

1. 在 Railway 新建项目，选择 GitHub 仓库 `yuweiwan/world-model-mapping`。
2. 在服务 Settings → Source 中选择默认分支 `main`，根目录保持仓库根目录。
3. 保留默认 Dockerfile 构建方式，不设置额外的 Build Command 或 Start Command。
4. 部署成功后，在 Settings → Networking 中点击 Generate Domain。默认目标端口为 `8080`；如设置了 `PORT` 环境变量，目标端口须使用相同值。
5. 打开生成的 HTTPS 地址，确认图谱和论文筛选可用。`/healthz` 应返回 `ok`。

`railway.json` 配置了健康检查和失败重启。Nginx 会监听 Railway 提供的 `PORT`，未设置时使用 `8080`。部署镜像只包含网页及其 JavaScript 文件。

启用 GitHub 自动部署后，向 `main` 推送更新会触发重新部署。网页发布的是仓库中已审核并导出的 `paper-data.js`。

论文采集与人工审核仍使用原有 Python 流水线和 GitHub Actions。部署网页不会启动定时采集；GitHub 的定时工作流需位于默认分支才会自动执行。

参考：[Railway 静态网站部署](https://docs.railway.com/guides/static-hosting)、[Dockerfile 部署](https://docs.railway.com/builds/dockerfiles)。
