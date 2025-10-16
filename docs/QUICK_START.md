# 快速使用指南 - 自动对话模式

## 🚀 快速开始

1. **直接启动应用**
   ```bash
   python3 main.py
   ```

2. **等待连接建立** (约3-5秒)
   ```
   看到 "已自动启动对话模式" 日志消息
   ```

3. **开始语音对话** 🎤
   ```
   直接说话，无需按任何按键
   例如: "今天天气怎么样？"
   ```

## ✨ 主要特性

- ✅ **零操作启动**: 启动后自动进入对话状态
- ✅ **即说即用**: 无需按键或唤醒词
- ✅ **智能音频**: 根据设备自动选择最佳模式
- ✅ **语音提示**: 支持MP3唤醒提示音
- ✅ **快捷控制**: 保留所有手动控制选项

## 🎯 使用场景

### 场景 1: 日常对话助手
```bash
启动应用 → 直接询问问题 → 获得回答
```

### 场景 2: 语音唤醒模式
```bash
启动应用 → 说"你好小智" → 听到提示音 → 开始对话
```

### 场景 3: 手动控制
```bash
启动应用 → 按Ctrl+J → 说话 → 松开按键
```

## ⚙️ 自定义配置

### 禁用自动模式
```json
// config/config.json
{
  "SYSTEM_OPTIONS": {
    "AUTO_START_CONVERSATION": false
  }
}
```

### 启用音频增强 (更好体验)
```json
{
  "AEC_OPTIONS": {
    "ENABLED": true
  }
}
```

### 自定义语音唤醒
```json
{
  "WAKE_WORD_OPTIONS": {
    "USE_WAKE_WORD": true,
    "PLAY_BEEP_ON_WAKE": true,
    "USE_MP3_SOUND": true
  }
}
```

## 🔧 故障排除

### 问题 1: 启动后无法对话
**解决方案:**
1. 检查麦克风权限
2. 确认音频设备正常
3. 查看日志: `tail -f logs/app.log`

### 问题 2: 连接失败
**解决方案:**
1. 检查网络连接
2. 确认配置文件中的服务器地址
3. 尝试: `python3 main.py --skip-activation`

### 问题 3: 自动模式太敏感
**解决方案:**
1. 设置 `"AUTO_START_CONVERSATION": false`
2. 使用语音唤醒: "你好小智"
3. 或手动控制: `Ctrl+K`

## 📱 快捷键参考

- **`Ctrl+K`**: 切换自动对话
- **`Ctrl+J`**: 按住说话
- **`Ctrl+Q`**: 中断对话
- **`Ctrl+W`**: 显示/隐藏界面

## 🎵 音频体验优化

### 推荐设置
```json
{
  "SYSTEM_OPTIONS": {
    "AUTO_START_CONVERSATION": true
  },
  "AEC_OPTIONS": {
    "ENABLED": false  // 简单设备使用
  },
  "WAKE_WORD_OPTIONS": {
    "USE_WAKE_WORD": true,
    "USE_MP3_SOUND": true
  }
}
```

### 高级设置 (更好设备)
```json
{
  "AEC_OPTIONS": {
    "ENABLED": true  // 支持打断对话
  }
}
```

## 📋 常用命令

```bash
# 标准启动
python3 main.py

# 调试模式
python3 main.py --skip-activation

# CLI模式
python3 main.py --mode cli

# 测试配置
python3 scripts/test_auto_conversation.py

# 测试提示音
python3 scripts/test_wake_up_sound.py
```

## 💡 使用技巧

1. **首次使用**: 建议先启用自动模式，熟悉后可调整
2. **音频质量**: 在安静环境下使用效果更佳
3. **网络稳定**: 确保网络连接稳定以获得最佳体验
4. **权限设置**: 首次运行需要授予麦克风权限
5. **配置调优**: 根据实际使用情况调整配置参数

---

**享受与小智AI的智能对话体验！** 🤖✨