# 小智设备远程控制 (Xiaozhi API)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

Home Assistant 自定义集成，用于远程控制小智系列智能设备。

## 兼容性

| 设备 | 固件版本 | 状态 |
|------|----------|------|
| 无名科技 星智1.54(WIFI) | 星智官网 2.0.44 | ✅ 测试通过 |
| 星智系列其他型号 | - | 应该通用 |
| 其他设备 | - | 未知 |

## 功能

- 发送聊天消息
- 音乐控制（播放/暂停/上一曲/下一曲）
- 播放模式设置（顺序/随机/列表循环/单曲循环）
- 音量调节 (0-100)
- 亮度调节 (0-100)
- 主题切换（浅色/深色）
- 待机命令

## 安装

### HACS 安装（推荐）

1. 打开 HACS
2. 点击右上角三个点，选择 **自定义存储库**
3. 添加存储库地址：`https://github.com/JochenZhou/xiaozhi_api`
4. 类别选择：**Integration**
5. 点击添加，然后搜索 "小智" 安装

### 手动安装

1. 下载此仓库
2. 将 `custom_components/xiaozhi_api` 文件夹复制到 Home Assistant 的 `custom_components` 目录
3. 重启 Home Assistant

## 配置

1. 进入 **设置 → 设备与服务 → 添加集成**
2. 搜索 "小智" 或 "Xiaozhi"
3. 填写配置信息：
   - **API地址**: 默认为 `http://101.35.234.159/Xiaozhi`
   - **API密钥**: 从星智官网获取的 API Key
   - **设备MAC地址**: 设备的 MAC 地址
   - **设备名称**: 可选，用于在 Home Assistant 中显示

## 实体

配置完成后，每个设备会创建以下实体：

| 类型 | 实体 | 说明 |
|------|------|------|
| Button | 待机 | 发送待机命令 |
| Button | 停止播放 | 停止音乐播放 |
| Button | 恢复播放 | 恢复音乐播放 |
| Button | 上一曲 | 播放上一首 |
| Button | 下一曲 | 播放下一首 |
| Number | 音量 | 音量控制 (0-100) |
| Number | 亮度 | 亮度控制 (0-100) |
| Select | 播放模式 | 顺序/随机/列表循环/单曲循环 |
| Select | 主题 | 浅色/深色 |
| Text | 发送消息 | 发送聊天消息 |
| Text | 播放音乐 | 搜索并播放音乐 |

## 服务

集成提供以下服务：

- `xiaozhi_api.send_chat_message` - 发送聊天消息
- `xiaozhi_api.play_music` - 播放音乐
- `xiaozhi_api.set_volume` - 设置音量
- `xiaozhi_api.set_brightness` - 设置亮度
- `xiaozhi_api.set_player_mode` - 设置播放模式
- `xiaozhi_api.set_theme` - 设置主题

## 多设备支持

支持添加多个设备，每个设备使用不同的 MAC 地址进行区分。重复添加集成即可配置多个设备。

## 许可证

MIT License
