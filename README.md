# Nail Art Try-On (MVP)

本仓库包含：
- FastAPI 后端（素材提取 + 试戴合成 + 异步任务）
- 微信小程序前端

## 目录结构
```
repo/
  backend/
    app/
      __init__.py
      main.py
      core/
        config.py
        logging.py
      db/
        base.py
        models.py
        session.py
        init_db.py
      api/
        deps.py
        routes/
          health.py
          assets.py
          jobs.py
          extract.py
          tryon.py
      services/
        storage.py
        image_io.py
        mediapipe_hand.py
        nail_geometry.py
        extraction_pipeline.py
        tryon_pipeline.py
        blending.py
      workers/
        worker.py
        tasks.py
      schemas/
        asset.py
        job.py
        common.py
      utils/
        ids.py
        errors.py
        time.py
    tests/
      assets/
        sample_hand.jpg
        sample_nail.jpg
      test_health.py
      test_assets.py
      test_jobs.py
      test_pipelines_smoke.py
    requirements.txt
    docker-compose.yml
    Dockerfile
    README.md
    data/
      uploads/original/
      outputs/extract/
      outputs/tryon/
      assets/
      presets/

  miniprogram/
    project.config.json
    app.js
    app.json
    app.wxss
    env.example.js
    utils/
      api.js
      upload.js
      poll.js
    pages/
      extract/
        index.js
        index.wxml
        index.wxss
      library/
        index.js
        index.wxml
        index.wxss
      tryon/
        index.js
        index.wxml
        index.wxss
    components/
      asset-card/
        index.js
        index.wxml
        index.wxss
    README.md
```

## 后端运行
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Redis（二选一）
docker-compose up -d
# 或：redis-server

python -m app.db.init_db
uvicorn app.main:app --reload --port 8000

# 另开终端启动 worker
python -m app.workers.worker
# 或：rq worker -u redis://localhost:6379/0 nail_jobs
```

## 小程序运行
1. 复制 `miniprogram/env.example.js` 为 `miniprogram/env.js`，修改 `BASE_URL` 指向后端地址（手机真机访问需内网 IP）。
2. 用微信开发者工具打开 `miniprogram/`。
3. 运行流程：
   - 打开“素材提取”页上传成品美甲图 -> 保存素材
   - 进入素材库 -> 选择素材进入试戴页 -> 上传手部无美甲照片

## 常见问题
- **MediaPipe 安装失败**：确保 Python 3.11，必要时升级 pip，并安装系统依赖（Linux 缺少 `libgl1` 时需要安装）。
- **OpenCV 报错**：确保安装 `opencv-python` 而非 `opencv-python-headless`，或者补齐系统 GUI 依赖。
- **真机访问本地服务**：需要把 `BASE_URL` 改成电脑内网 IP（如 `http://192.168.x.x:8000`），并保证手机/电脑同一局域网。

## 验收要点
- `GET /v1/health` 返回 `{"status":"ok"}`
- extract 任务生成 preview + 5 个贴片
- tryon 任务生成 result/debug
- 小程序可轮询任务并展示结果
