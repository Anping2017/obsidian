---
title: 企业 MDM
type: concept
tags: [ios, mature]
sources: [raw/iPhone/]
created: 2026-05-05
updated: 2026-05-05
summary: MDM(Mobile Device Management)是企业管理员通过 Apple Push 通道向员工 iOS 设备下发配置、应用、限制策略的标准协议,与 ABM/Apple Configurator 配合实现规模化设备生命周期管理。
---

# 企业 MDM

## 定义

**移动设备管理(Mobile Device Management, MDM)** 是 Apple 提供的、让企业 / 教育机构 IT 管理员**远程管理 iPhone / iPad / Mac**的协议与平台。管理员通过 MDM 服务器(Jamf、Microsoft Intune、Mosyle、JumpCloud 等)向员工设备**下发配置文件、应用、限制策略、监控指令**,并接收设备状态回报。它是企业批量部署 Apple 设备的标准方案。

## 核心要点

**MDM 能做什么**

1. **配置下发**:Wi-Fi、VPN、邮件、CalDAV、CardDAV、证书、Web Clip
2. **应用管理**:推送 App Store / 企业内部 App、强制安装 / 移除
3. **限制策略**:禁用相机、AirDrop、iCloud 备份、App Store、Safari、特定网址
4. **设备状态查询**:序列号、IMEI、电池健康、可用空间、已安装应用
5. **远程命令**:锁定、清除、改密码、重启、定位(Lost Mode)
6. **监督模式(Supervised)**:更深限制权限,适用于公司/学校发设备

**关键服务体系**

1. **APNs 通道**:MDM 服务器通过 Apple Push 把指令"叫醒"设备,设备主动连服务器拉指令
2. **DEP / ABM(Apple Business Manager)**:开机即纳入 MDM 的"零接触"部署
3. **VPP(Volume Purchase Program)**:批量采购 App 许可分发给员工
4. **Apple School Manager**:教育版同等体系
5. **Apple Configurator**:Mac 上的本地批量配置工具,USB 直连

**标准 MDM vs 监督模式**

- **标准 MDM**:用户自愿加入(BYOD 场景),管理员能力受限
- **监督模式 Supervised**:必须通过 ABM 或 Configurator 注册,管理员有更深权限(如阻止抹除设备、过滤网址、单 App 模式)

监督模式开启后可:
- 阻止用户绕过 MDM
- 强制特定主屏布局
- 单 App 锁定模式(如售点设备只跑收银 App)
- 禁用 Activation Lock,丢失后能完全清除

**注册流程**

1. 管理员在 ABM 创建组织,关联 DEP / VPP
2. 设备从 Apple 直接采购或注册到 ABM
3. 设备激活时自动检测 ABM 归属,弹出"远程管理"提示,用户接受后注册到组织 MDM
4. MDM 推送策略 / 应用,设备开始受管

**隐私边界**

iOS 的 MDM 严格区分"工作 / 个人":
- 用户注册(BYOD)模式:管理员看不到用户数据、不能远程清除整机(只能清除工作账户)
- 监督模式(公司发):管理员可全设备清除,但不可读用户消息内容
- 用户 *设置 > 通用 > VPN与设备管理* 可看到当前 MDM 的权限范围

**第三方 MDM 平台**

主流:Jamf Pro(企业)、Jamf School(教育)、Microsoft Intune(混合 Apple/Windows)、Mosyle(中小企业)、Cisco Meraki SM、JumpCloud。Apple 官方协议开放,但 UI 和管理体验差异巨大。

## 与其他概念的关系

MDM 与 [[Apple生态系统]] 战略中"企业市场"扩展直接相关,涉及 [[APNs推送通知]] 通道、[[iOS沙盒]] 的工作账户隔离、[[iOS隐私机制]] 的边界。与开发流程上的 [[TestFlight]]、[[Xcode开发工具]] 互为补充——开发者验证 App 后通过 MDM 大规模分发。

## 高频陷阱

- MDM 不能监控用户私人 iMessage / Safari 历史(隐私边界)
- 监督模式必须重置设备并通过 ABM 注册才能启用,不可后置改造
- iOS 17+ 的"账户管理"权限分离让 MDM 不能再控制 Apple ID 行为
- 同一设备只能注册一个 MDM 服务器
- 用户在 BYOD 模式下可随时退出 MDM(管理员无法阻止)

## 参考源

- raw/iPhone/(MDM 章节)
- 相关:[[APNs推送通知]]、[[Apple生态系统]]、[[iOS沙盒]]、[[iOS隐私机制]]、[[TestFlight]]、[[Xcode开发工具]]
