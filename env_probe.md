# 环境探测结果（2026-11-05）

## BGE-M3（已确认可用，离线跑）

| 项 | 实测值 | 说明 |
|---|---|---|
| 向量维度 | **1024** | 与设计一致，后续代码按 1024 写 |
| 单句编码 | **213 ms** | 每次提问的固定延迟 |
| 20 句批量 | **0.6 s** | 推算 5000 块建库约 2.5 分钟 |
| 模型加载 | **2.5 s** | 每次启动服务一次 |

**结论**：本地跑 BGE-M3 没问题，不需要降级到 small 版。

## 关键配置（写死在代码里，别改）

```python
os.environ.setdefault("HF_HOME", "D:/cache/huggingface")
os.environ.setdefault("HF_HUB_OFFLINE", "1")      # 只用本地缓存，不走网络
model = SentenceTransformer("BAAI/bge-m3", model_kwargs={"use_safetensors": False})
```

- `HF_HOME=D:/cache/huggingface`：模型实体在 D 盘
- `use_safetensors=False`：只读 `pytorch_model.bin`（2.27 GB，已完整下载）
  不加这个参数，transformers 会认为"缺 safetensors"，重新下载 2.27 GB
- `HF_HUB_OFFLINE=1`：完全不联网。模型已在本地，联网只会带来 429/502 这类问题

## 镜像（仅下载时需要，运行时不需要）

```bash
export HF_ENDPOINT=https://hf-mirror.com
export HF_HUB_DISABLE_XET=1
```

`HF_HUB_DISABLE_XET=1` 是必须的——hf 新的 Xet 传输后端在镜像环境下会报
`CAS Client Error / xethub.hf.co`，导致大文件下到一半失败。

## 踩过的坑（按发生顺序）

| 现象 | 原因 | 解决 |
|---|---|---|
| `WinError 10060` 连不上 huggingface.co | 国内网络 | 设 `HF_ENDPOINT=https://hf-mirror.com` |
| `CAS Client Error ... xethub.hf.co` | Xet 后端在镜像上不稳 | 设 `HF_HUB_DISABLE_XET=1` |
| `HTTP 429 Too Many Requests` | 重复下载触发限流 | 停止重跑，等 5 分钟 |
| `OSError: Can't load the model ... pytorch_model.bin` | 当时 bin 只有半截 | 下完后删掉 `.incomplete` 文件 |
| 每次启动都要重下 safetensors | 默认优先 safetensors | `model_kwargs={"use_safetensors": False}` |

## 待办

- [ ] DeepSeek API（需要 key + 充值）
- [ ] 演示方式（云服务器 / 内网穿透 / 本机+录屏）
