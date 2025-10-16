# 语音唤醒提示音功能

本功能为小智AI客户端提供语音唤醒后的音频提示，帮助用户确认语音唤醒已成功激活。

## 功能特性

- **MP3提示音播放**：支持播放自定义MP3文件作为唤醒提示音
- **Beep音生成**：内置beep音生成器，支持单音和双音提示
- **灵活配置**：通过配置文件轻松开启/关闭和自定义提示音
- **多后端支持**：自动检测可用的音频播放后端（pygame、系统播放器等）

## 配置选项

在 `config/config.json` 的 `WAKE_WORD_OPTIONS` 部分配置：

```json
{
  "WAKE_WORD_OPTIONS": {
    "PLAY_BEEP_ON_WAKE": true,          // 是否启用唤醒提示音
    "USE_MP3_SOUND": true,              // 优先使用MP3提示音
    "MP3_FILENAME": "wake_up.mp3",      // MP3文件名（位于assets/audio/目录）
    "USE_DOUBLE_BEEP": false,           // 使用双音beep（当MP3不可用时）
    "BEEP_FREQUENCY": 800.0,            // Beep音频率（Hz）
    "BEEP_DURATION": 0.3,               // Beep音持续时间（秒）
    "BEEP_VOLUME": 0.3                  // Beep音音量（0.0-1.0）
  }
}
```

### 配置说明

- **PLAY_BEEP_ON_WAKE**: 总开关，设为 `false` 禁用所有提示音
- **USE_MP3_SOUND**: 优先级设置，`true` 时优先播放MP3，失败则回退到beep
- **MP3_FILENAME**: MP3文件名，文件应放在 `assets/audio/` 目录下
- **USE_DOUBLE_BEEP**: 当不使用MP3时，是否播放双音beep（更清晰的提示）
- **BEEP_FREQUENCY/DURATION/VOLUME**: beep音的音频参数

## 音频文件管理

### 内置提示音

项目已包含一个默认的 `wake_up.mp3` 提示音文件。

### 自定义提示音

1. **添加自己的MP3文件**：
   ```bash
   cp your_sound.mp3 assets/audio/
   ```

2. **更新配置**：
   ```json
   "MP3_FILENAME": "your_sound.mp3"
   ```

3. **重新生成提示音**（可选）：
   ```bash
   python3 scripts/generate_wake_up_sound.py
   ```

### 支持的音频格式

- **MP3**: 推荐格式，兼容性最好
- **WAV**: 作为中间格式，可自动转换为MP3
- **其他格式**: 取决于系统安装的播放器

## 依赖要求

### Python包

```bash
# 基础音频处理（必需）
pip install numpy sounddevice

# MP3播放支持（推荐）
pip install pygame

# 音频转换（可选，用于生成MP3）
# 系统需要安装 ffmpeg
```

### 系统依赖

- **Linux**: `mpg123`, `mpv`, 或 `ffplay`（任选其一）
- **macOS**: 内置 `afplay`
- **Windows**: 内置支持

#### Linux安装播放器

```bash
# Ubuntu/Debian
sudo apt install mpg123
# 或
sudo apt install mpv

# CentOS/RHEL
sudo yum install mpg123
# 或
sudo yum install mpv
```

## 使用方法

### 正常使用

启动应用后，当语音唤醒词被检测到时，会自动播放配置的提示音。

### 测试功能

运行测试脚本验证提示音功能：

```bash
python3 scripts/test_wake_up_sound.py
```

### 生成自定义提示音

使用内置脚本生成新的提示音：

```bash
python3 scripts/generate_wake_up_sound.py
```

## 故障排除

### 常见问题

1. **ALSA警告信息**（Linux）
   ```
   ALSA lib pcm.c:xxxx:(snd_pcm_recover) underrun occurred
   ```
   - 这是常见的Linux音频警告，不影响功能
   - 可以忽略，或通过安装/配置音频驱动解决

2. **MP3播放失败**
   - 检查 `pygame` 是否安装：`pip install pygame`
   - 确认MP3文件存在：`ls assets/audio/`
   - 系统会自动回退到beep音

3. **完全无声音**
   - 检查系统音量设置
   - 确认音频设备正常工作
   - 检查配置中 `PLAY_BEEP_ON_WAKE` 是否为 `true`

4. **提示音太响/太小**
   - 调整 `BEEP_VOLUME` 参数（0.0-1.0）
   - 或在系统音量控制中调整

### 调试模式

启用调试日志查看详细信息：

```bash
# 查看详细日志
tail -f logs/app.log | grep -i "beep\|mp3\|wake"
```

## 扩展开发

### 添加新的音频后端

在 `src/utils/beep_generator.py` 中添加新的播放方法：

```python
async def _play_mp3_with_custom_backend(self, mp3_path: str):
    # 实现自定义播放逻辑
    pass
```

### 集成到其他插件

```python
from src.utils.beep_generator import get_beep_generator

# 获取生成器实例
generator = get_beep_generator()

# 播放MP3
await generator.play_wake_up_mp3("custom.mp3")

# 播放beep
await generator.play_beep_tone(frequency=1000, duration=0.5)
```

## 版本历史

- **v1.0**: 基础MP3播放和beep音生成功能
- **支持的提示音格式**: MP3, WAV
- **支持的平台**: Linux, macOS, Windows