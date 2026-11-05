"""BGE-M3 环境探测：确认模型能加载、维度正确、速度可接受。

用法：python probe.py
模型已下载完成，之后完全走本地缓存，不会再联网。
"""

import os
import time

# 模型缓存在 D 盘（之前下载的位置）。必须在 import sentence_transformers 之前设。
os.environ.setdefault("HF_HOME", "D:/cache/huggingface")
# 只用本地缓存，不走网络。模型已经下完了，不需要再联网；
# 顺便避开镜像限流(429)和代理问题(502)。
os.environ.setdefault("HF_HUB_OFFLINE", "1")
# 关掉那句 "Could not reach the Hub" 的提示噪声
os.environ.setdefault("HF_HUB_VERBOSITY", "error")

from sentence_transformers import SentenceTransformer

t0 = time.time()
# use_safetensors=False：只读已下好的 pytorch_model.bin，
# 否则 transformers 会优先找 safetensors，发现没有就重下 2.27GB。
model = SentenceTransformer("BAAI/bge-m3", model_kwargs={"use_safetensors": False})
print("加载耗时 %.1f 秒" % (time.time() - t0))

t0 = time.time()
vecs = model.encode(["show ip route 命令的作用是什么"])
print("向量维度", len(vecs[0]))
print("单句耗时 %d ms" % ((time.time() - t0) * 1000))

t0 = time.time()
model.encode(["OSPF 邻居状态有哪些"] * 20, batch_size=8)
print("20 句批量 %.1f 秒" % (time.time() - t0))
