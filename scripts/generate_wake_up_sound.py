#!/usr/bin/env python3
"""
生成语音唤醒提示音MP3文件的脚本
"""

import numpy as np
from pathlib import Path
import wave
import tempfile
import os

def generate_wake_up_tone(output_path: str, duration: float = 1.0, sample_rate: int = 44100):
    """生成语音唤醒提示音并保存为WAV（可转换为MP3）"""
    
    # 生成时间序列
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # 创建复合音调：基础频率 + 和弦
    base_freq = 523.25  # C5
    harmony_freq = 659.25  # E5
    
    # 生成双音调和弦
    tone1 = 0.6 * np.sin(2 * np.pi * base_freq * t)
    tone2 = 0.4 * np.sin(2 * np.pi * harmony_freq * t)
    combined = tone1 + tone2
    
    # 添加包络（渐变效果）
    envelope = np.exp(-t * 2)  # 指数衰减
    combined *= envelope
    
    # 标准化到合适的音量
    combined = combined * 0.3
    
    # 转换为16位整数
    audio_data = (combined * 32767).astype(np.int16)
    
    # 保存为WAV文件
    with wave.open(output_path, 'w') as wav_file:
        wav_file.setnchannels(1)  # 单声道
        wav_file.setsampwidth(2)  # 16位
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())
    
    print(f"生成WAV文件: {output_path}")

def convert_wav_to_mp3(wav_path: str, mp3_path: str):
    """尝试将WAV转换为MP3"""
    try:
        import subprocess
        
        # 尝试使用ffmpeg转换
        result = subprocess.run([
            'ffmpeg', '-i', wav_path, '-codec:a', 'mp3', '-b:a', '128k', 
            '-y', mp3_path
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"转换成功: {mp3_path}")
            return True
        else:
            print(f"ffmpeg转换失败: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("ffmpeg未安装，无法转换为MP3")
        return False
    except Exception as e:
        print(f"转换失败: {e}")
        return False

def main():
    # 确保输出目录存在
    assets_audio_dir = Path(__file__).parent.parent / "assets" / "audio"
    assets_audio_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成WAV文件
    wav_path = assets_audio_dir / "wake_up.wav"
    generate_wake_up_tone(str(wav_path))
    
    # 尝试转换为MP3
    mp3_path = assets_audio_dir / "wake_up.mp3"
    if convert_wav_to_mp3(str(wav_path), str(mp3_path)):
        # 转换成功，删除WAV文件
        try:
            os.remove(wav_path)
            print("已删除临时WAV文件")
        except:
            pass
    else:
        print(f"保留WAV文件: {wav_path}")
        print("提示：安装ffmpeg可以生成MP3文件")
    
    print("\n提示音文件生成完成！")
    print(f"输出目录: {assets_audio_dir}")
    
    # 列出生成的文件
    audio_files = list(assets_audio_dir.glob("wake_up.*"))
    for file in audio_files:
        print(f"  - {file.name}")

if __name__ == "__main__":
    main()