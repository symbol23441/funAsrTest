# SenseVoice 本地语音转文字工具

基于 FunASR + SenseVoice 实现的本地离线语音识别工具。

支持：

* 单个音频文件转写
* 目录递归批量转写
* 自动识别音频时长
* 长音频自动启用 VAD
* 保持目录结构输出
* 本地运行，无需上传云端
* Apple Silicon（M1/M2/M3/M4）支持

---

# 项目依赖

## FunASR

GitHub：

https://github.com/modelscope/FunASR

官方文档：

https://github.com/modelscope/FunASR/blob/main/README.md

## SenseVoice

GitHub：

https://github.com/FunAudioLLM/SenseVoice

论文：

https://arxiv.org/abs/2407.05642

---

# 环境准备

推荐：

* macOS
* Apple Silicon（M1/M2/M3/M4）
* Python 3.10

## 创建 Conda 环境

```bash
conda create --name funASR python=3.10
```

激活环境：

```bash
conda activate funASR
```

---

# 安装依赖

安装 FunASR：

```bash
pip install -U funasr
```

安装 PyTorch：

```bash
pip install torch torchaudio
```

安装 ffmpeg：

```bash
brew install ffmpeg
```

验证：

```bash
ffmpeg -version
ffprobe -version
```

---

# 项目目录

```text
funASR/
├── asr.py
├── README.md
└── out/
```

创建项目目录：

```bash
mkdir funASR
cd funASR
```

使用 VSCode 打开：

```bash
code .
```

---

# 使用方法

## 转写单个文件

```bash
python asr.py audio.mp3
```

示例：

```bash
python asr.py lecture.mp3
```

输出：

```text
out/
└── lecture.txt
```

---

## 转写整个目录

```bash
python asr.py ./audio
```

示例：

```bash
python asr.py /Users/shenbo/Downloads/Bilidown_download
```

输出：

```text
out/
├── video1.txt
├── video2.txt
└── subdir/
    └── video3.txt
```

目录结构会自动保持一致。

---

# 自动模式说明

脚本会自动检测音频时长。

## 短音频（≤ 5分钟）

使用：

```python
SenseVoiceSmall
```

特点：

* 启动速度快
* 资源占用低

---

## 长音频（> 5分钟）

使用：

```python
SenseVoiceSmall + fsmn-vad
```

特点：

* 自动静音检测
* 自动语音分段
* 长录音识别更稳定

适用于：

* 会议录音
* 播客
* 在线课程
* 视频字幕生成

---

# 输出结果

SenseVoice 默认会输出元标签：

```text
<|zh|><|NEUTRAL|><|Speech|><|withitn|>
大家好
```

脚本已自动清理：

```text
大家好
```

仅保留最终识别文字。

---

# 常见标签说明

| 标签 | 含义       |    |      |
| -- | -------- | -- | ---- |
| `< | zh       | >` | 中文   |
| `< | en       | >` | 英文   |
| `< | ja       | >` | 日文   |
| `< | Speech   | >` | 普通语音 |
| `< | BGM      | >` | 背景音乐 |
| `< | Applause | >` | 掌声   |
| `< | Laughter | >` | 笑声   |
| `< | NEUTRAL  | >` | 中性情绪 |
| `< | HAPPY    | >` | 开心   |
| `< | SAD      | >` | 悲伤   |

当前脚本会自动移除这些标签。

---

# 实际安装记录

```bash
conda create --name funASR python=3.10

conda activate funASR

pip install -U funasr

pip install torch torchaudio

mkdir funASR

cd funASR

vim transcribe.py

code .

python asr.py /Users/shenbo/Downloads/Bilidown_download
```

---

# 后续优化方向

可扩展：

* 输出 SRT 字幕
* 输出 JSON 时间戳
* 自动生成会议纪要
* 自动章节划分
* 对接 Ollama 本地大模型
* 批量总结课程内容

---

# License

本项目依赖：

* FunASR
* SenseVoice

请遵循其官方开源许可证使用。
