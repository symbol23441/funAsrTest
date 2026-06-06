# SenseVoice 本地语音转文字工具

基于 FunASR + SenseVoice 的本地离线 ASR 转写脚本，支持单文件和目录批量转写。

## 功能

- 单个音频文件转写
- 目录递归批量转写
- 自动根据音频时长选择普通模型或 VAD 模型
- 输出目录可配置，默认 `out/`
- 目录输入时保持原目录结构
- 默认按句末标点换行，可手动关闭
- 自动清理 SenseVoice 元标签

## 环境准备

建议使用 Python 3.10。

```bash
conda create --name funASR python=3.10
conda activate funASR
pip install -U funasr torch torchaudio
brew install ffmpeg
```

验证 `ffmpeg` / `ffprobe`：

```bash
ffmpeg -version
ffprobe -version
```

## 使用方法

查看帮助：

```bash
python asr.py
python asr.py --help
```

转写单个文件：

```bash
python asr.py audio.mp3
```

转写目录：

```bash
python asr.py ./audio_dir
```

指定输出目录：

```bash
python asr.py ./audio_dir -o ./transcripts
python asr.py ./audio_dir --output-dir ./transcripts
```

关闭句末标点换行：

```bash
python asr.py audio.mp3 --no-period-newline
```

组合使用：

```bash
python asr.py ./audio_dir -o ./transcripts --no-period-newline
```

## 参数说明

```text
usage: asr.py [-h] [-o DIR] [--no-period-newline] INPUT

positional arguments:
  INPUT                      输入路径：音频文件或音频目录。目录会递归扫描支持格式。

options:
  -h, --help                 显示帮助信息并退出
  -o, --output-dir DIR       转写结果输出目录。默认: out
  --no-period-newline        关闭按句末标点换行。默认开启，支持标点: 。 . ！ ! ？ ?。
```

## 支持格式

`.wav` `.mp3` `.m4a` `.aac` `.flac` `.ogg` `.wma` `.opus`

## 输出说明

默认输出到 `out/`：

```text
out/
├── audio.txt
└── subdir/
    └── video.txt
```

输入为目录时，输出目录会保持输入目录下的相对结构。

## 模型选择

脚本会自动检测音频时长：

- `<= 5 分钟`：使用 SenseVoiceSmall 普通模型
- `> 5 分钟`：使用 SenseVoiceSmall + fsmn-vad

## 依赖项目

- [FunASR](https://github.com/modelscope/FunASR)
- [SenseVoice](https://github.com/FunAudioLLM/SenseVoice)
