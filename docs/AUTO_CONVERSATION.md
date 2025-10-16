# 自动对话模式

小智AI客户端现在支持启动后自动进入对话模式，用户无需手动激活即可开始语音对话。

## 功能特性

- **自动启动**: 应用启动后自动进入对话监听状态
- **即用性**: 无需按快捷键或等待唤醒词即可开始对话
- **可配置**: 通过配置文件灵活控制是否启用自动模式
- **智能回退**: 如果自动启动失败，会回退到基础监听状态

## 配置方式

在 `config/config.json` 文件中配置：

```json
{
  "SYSTEM_OPTIONS": {
    "AUTO_START_CONVERSATION": true
  }
}
```

### 配置选项说明

- **`AUTO_START_CONVERSATION: true`**: 启用自动对话模式
- **`AUTO_START_CONVERSATION: false`**: 禁用自动对话模式，需要手动激活

## 工作流程

### 启用自动模式时 (推荐)

1. 启动应用 `python3 main.py`
2. 等待协议连接建立
3. **自动进入对话模式** ✨
4. 直接开始语音对话

### 禁用自动模式时

1. 启动应用 `python3 main.py`
2. 等待协议连接建立
3. 应用进入待机状态
4. 需要手动激活对话：
   - 按 `Ctrl+K` 切换自动对话
   - 按住 `Ctrl+J` 说话
   - 说出唤醒词 "你好小智"

## 对话模式说明

应用会根据音频配置自动选择最佳对话模式：

### 实时模式 (REALTIME)
- **启用条件**: `AEC_OPTIONS.ENABLED = true`
- **特点**: 支持双工对话，可以打断AI回答
- **用途**: 更自然的对话体验

### 自动停止模式 (AUTO_STOP)
- **启用条件**: `AEC_OPTIONS.ENABLED = false`
- **特点**: 单轮对话，等AI回答完成后再次监听
- **用途**: 适合音频设备较简单的环境

## 快捷键控制

即使启用了自动模式，所有快捷键仍然可用：

- **`Ctrl+K`**: 切换自动对话 (开启/关闭)
- **`Ctrl+J`**: 按住说话 (手动模式)
- **`Ctrl+Q`**: 中断当前对话
- **`Ctrl+M`**: 切换对话模式
- **`Ctrl+W`**: 显示/隐藏界面

## 语音唤醒集成

自动对话模式与语音唤醒功能完美集成：

- 自动模式下，唤醒词会触发打断和重新开始
- 手动模式下，唤醒词会激活自动对话
- 唤醒成功会播放提示音确认

## 使用建议

### 推荐设置 (开箱即用)

```json
{
  "SYSTEM_OPTIONS": {
    "AUTO_START_CONVERSATION": true
  },
  "AEC_OPTIONS": {
    "ENABLED": false
  },
  "WAKE_WORD_OPTIONS": {
    "USE_WAKE_WORD": true,
    "PLAY_BEEP_ON_WAKE": true,
    "USE_MP3_SOUND": true
  }
}
```

### 高级用户设置

```json
{
  "SYSTEM_OPTIONS": {
    "AUTO_START_CONVERSATION": true
  },
  "AEC_OPTIONS": {
    "ENABLED": true
  }
}
```

## 故障排除

### 常见问题

1. **自动模式无法启动**
   - 检查音频设备是否正常
   - 确认麦克风权限已授予
   - 查看日志: `tail -f logs/app.log`

2. **连接建立但无法对话**
   - 检查网络连接
   - 确认配置中的服务器地址正确
   - 尝试手动激活: `Ctrl+K`

3. **想要禁用自动模式**
   - 设置 `"AUTO_START_CONVERSATION": false`
   - 重启应用

### 调试模式

启动时添加调试信息：

```bash
# 查看详细启动日志
python3 main.py --skip-activation

# 查看实时日志
tail -f logs/app.log | grep -i "conversation\|listening\|auto"
```

## 命令行选项

```bash
# 标准启动 (推荐)
python3 main.py

# 跳过激活流程 (调试用)
python3 main.py --skip-activation

# CLI模式
python3 main.py --mode cli

# 使用MQTT协议
python3 main.py --protocol mqtt
```

## 与其他功能的关系

- **语音唤醒**: 自动模式下增强体验，手动模式下提供激活方式
- **快捷键**: 始终可用，提供额外控制选项
- **音频增强**: 影响对话模式选择 (实时 vs 自动停止)
- **界面模式**: GUI和CLI模式都支持自动对话

## 版本说明

- **v1.0**: 基础自动对话功能
- **配置项**: `AUTO_START_CONVERSATION`
- **支持模式**: GUI, CLI
- **支持协议**: WebSocket, MQTT