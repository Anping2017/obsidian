---
title: iOS 辅助功能
type: concept
tags: [iphone, ios, mature]
sources: [raw/iPhone/iPhone知识体系/03-功能特性层/用户体验/04-可访问性功能.md]
created: 2026-05-05
updated: 2026-05-05
summary: iOS 辅助功能(Accessibility)是面向视觉、听觉、运动、认知障碍用户的系统级支持工具集,涵盖 VoiceOver、动态文字、AssistiveTouch、Live Captions、Voice Control 等数十项功能。
---

# iOS 辅助功能

## 定义

iOS 辅助功能(Accessibility)是 Apple 内置的一整套面向身心障碍用户的系统级支持,使盲人、低视力、听障、运动障碍、认知障碍、自闭症谱系等用户都能独立使用 iPhone。它是 Apple 长期投资且引以为豪的产品领域,2009 年首次完整推出,至今持续扩展。

辅助功能不是"一组特殊功能",而是一种产品哲学——iOS 设计中处处考虑可达性(WCAG 标准),从字体、对比度到交互逻辑都让大多数用户受益。

## 五大类别

**1. 视觉(Vision)**

- **VoiceOver**:屏幕阅读器,把屏幕内容转语音读出,触摸时朗读元素,双击激活。盲用户的核心入口。
- **缩放(Zoom)**:全屏或区域放大,3 指三击触发
- **显示与文字大小**:动态文字、加粗、提高对比度、智能反色、降低透明度
- **亮度与配色**:经典反色、智能反色、色彩滤镜(色盲)
- **朗读屏幕(Speak Screen)**:从顶部下拉双指唤起朗读
- **大文字/动态字体**:文字大小可调
- **指针/光标**:外接鼠标时光标可调

**2. 听觉(Hearing)**

- **MFi 助听器**:与 iPhone 直连,助听器音量、模式直接 iPhone 控制
- **Live Listen**:把 iPhone 当成远端麦克风,声音传到 AirPods/MFi 助听器
- **实时字幕(Live Captions)**:任何 App 或电话中的语音实时转文字(部分语言,iOS 16+)
- **声音识别**:门铃、警报、宝宝哭等环境声触发通知(听障用户重要)
- **单声道音频/左右平衡**

**3. 运动(Mobility)**

- **AssistiveTouch**:屏幕悬浮触控菜单,代替物理按键(主屏键、Siri、屏幕截图)
- **辅助控制**:外接开关(switch control)、头部追踪(Vision Pro 端)
- **Voice Control(语音控制)**:用语音操作整个 iPhone,精确到点击屏幕坐标(iOS 13+)
- **触觉/触感反馈、点击辅助**:按键延迟、点击锁定时间可调
- **背部点击(Back Tap)**:双击/三击 iPhone 背部触发自定义动作

**4. 认知(Cognitive)**

- **辅助访问(Assistive Access)**:iOS 17+ 推出的极简模式,把 iPhone 简化为大图标的几个核心 App(电话、消息、相机),适合认知障碍或老人
- **引导式访问(Guided Access)**:把 iPhone 锁在一个 App,防止意外切换(自闭症儿童、博物馆展示用)
- **背景声音**:雨声、海浪、白噪音帮助专注
- **Safari Reader**:剥离干扰,纯净阅读

**5. 通用(General)**

- **辅助快捷键**:三击侧键唤起特定辅助功能
- **手电筒、放大器**:相机增强为放大镜

## 标志性功能

**VoiceOver**

iPhone 与 iPad 上完全免费的屏幕阅读器,与 Mac 上的 VoiceOver 一脉相承。盲用户可独立使用所有 iOS 内置 App 和大部分第三方 App(只要开发者遵循 Accessibility API)。多语言支持极强,中文支持完整。

**Live Captions**

任何 App 中的音频(电话、视频通话、视频播放)实时转文字气泡显示在屏幕上方,处理在端侧完成,隐私不外泄。彻底改变听障用户的电话与会议体验。

**Personal Voice / Live Speech**(iOS 17+)

- Personal Voice:用户用 iPhone 录制 15 分钟样本,iPhone 用机器学习生成"个人语音克隆",在失声前预先录入
- Live Speech:打字 iPhone 朗读,可使用 Personal Voice
- 面向 ALS 患者等可能失声的用户

**门检测、人物检测**(iPhone Pro 系列 LiDAR)

通过 LiDAR 检测附近门、人物、距离,语音播报,辅助盲人导航。

## 商业与社会意义

**Apple 价值观体现**

辅助功能在每场 WWDC、产品发布会都获得显著时间,Tim Cook 多次强调"Accessibility is a fundamental human right"。

**全球意义**

WHO 估计全球约 16% 人口有某种残障。辅助功能让 iOS 成为这部分用户首选(iPhone 用户残障比例高于市场平均)。

**反向受益**

许多原本为残障用户设计的功能,被普通用户广泛使用——背景声音(专注)、Live Captions(嘈杂环境)、放大器(看小字)。这是"通用设计(Universal Design)"原则的体现。

**开发者 API**

iOS Accessibility API 让开发者用很少代码就能让 App 可达性升级(动态字体、VoiceOver 标签、对比度自适应),是 Apple 对开发者的隐性要求。

## 参考源

- raw/iPhone/iPhone知识体系/03-功能特性层/用户体验/04-可访问性功能.md
- 相关:[[iOS隐私机制]]、[[Apple生态系统]]、[[Siri与Apple Intelligence]]
