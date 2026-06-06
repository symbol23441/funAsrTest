#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SenseVoice 批量 ASR 转写工具

安装:
    pip install -U funasr torch torchaudio
    brew install ffmpeg

使用:
    python asr.py audio.mp3
    python asr.py ./audio_dir

功能:
    - 单文件或目录递归转写
    - 输出到当前目录 out/
    - 保持目录结构
    - 自动判断时长
    - <=5分钟: 普通模型
    - >5分钟: VAD模型
"""

import argparse
import re
import subprocess
from pathlib import Path

from funasr import AutoModel

SUPPORTED_EXTS = {
    ".wav",
    ".mp3",
    ".m4a",
    ".aac",
    ".flac",
    ".ogg",
    ".wma",
    ".opus",
}

SHORT_AUDIO_THRESHOLD = 300  # 5分钟


def clean_text(text: str) -> str:
    """
    清理 SenseVoice 元标签
    """

    # 删除标签
    text = re.sub(
        r"<\|.*?\|>",
        "",
        text,
    )

    # 合并多余空白
    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def get_audio_duration(audio_file: str) -> float:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        audio_file,
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True,
    )

    return float(result.stdout.strip())


def format_duration(seconds: float) -> str:
    total = int(seconds)
    hours = total // 3600
    minutes = (total % 3600) // 60
    seconds = total % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def get_audio_files(path: Path):
    if path.is_file():
        return [path]

    files = []

    for ext in SUPPORTED_EXTS:
        files.extend(path.rglob(f"*{ext}"))
        files.extend(path.rglob(f"*{ext.upper()}"))

    return sorted(files)


def main():
    parser = argparse.ArgumentParser(
        description="SenseVoice 批量 ASR 转写工具"
    )

    parser.add_argument(
        "input_path",
        help="音频文件或目录"
    )

    args = parser.parse_args()

    input_path = Path(args.input_path).expanduser().resolve()

    if not input_path.exists():
        raise FileNotFoundError(f"路径不存在: {input_path}")

    out_root = Path.cwd() / "out"
    out_root.mkdir(exist_ok=True)

    print("=" * 60)
    print("加载 SenseVoice 普通模型...")
    print("=" * 60)

    normal_model = AutoModel(
        model="iic/SenseVoiceSmall",
        trust_remote_code=True,
    )

    print("=" * 60)
    print("加载 SenseVoice VAD 模型...")
    print("=" * 60)

    vad_model = AutoModel(
        model="iic/SenseVoiceSmall",
        vad_model="fsmn-vad",
        trust_remote_code=True,
    )

    audio_files = get_audio_files(input_path)

    if not audio_files:
        print("未发现音频文件")
        return

    total = len(audio_files)

    print(f"\n发现 {total} 个音频文件\n")

    success_count = 0
    fail_count = 0

    for idx, audio_file in enumerate(audio_files, start=1):
        try:
            duration = get_audio_duration(str(audio_file))

            if duration > SHORT_AUDIO_THRESHOLD:
                model = vad_model
                mode = "VAD"
            else:
                model = normal_model
                mode = "NORMAL"

            print("-" * 60)
            print(f"[{idx}/{total}] {audio_file.name}")
            print(f"时长: {format_duration(duration)}")
            print(f"模式: {mode}")

            result = model.generate(
                input=str(audio_file),
                language="auto",
                use_itn=True,
            )

            raw_text = result[0]["text"]

            text = clean_text(raw_text)

            if input_path.is_file():
                relative_path = Path(audio_file.stem + ".txt")
            else:
                relative_path = (
                    audio_file.relative_to(input_path)
                    .with_suffix(".txt")
                )

            output_file = out_root / relative_path

            output_file.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            output_file.write_text(
                text,
                encoding="utf-8",
            )

            print(f"输出: {output_file}")
            success_count += 1

        except Exception as e:
            fail_count += 1
            print(f"失败: {audio_file}")
            print(e)

    print("\n" + "=" * 60)
    print("处理完成")
    print("=" * 60)
    print(f"成功: {success_count}")
    print(f"失败: {fail_count}")
    print(f"输出目录: {out_root}")
    print("=" * 60)


if __name__ == "__main__":
    main()
