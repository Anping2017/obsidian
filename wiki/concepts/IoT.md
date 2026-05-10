---
title: IoT 物联网
type: concept
tags: [programming, mature]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: IoT 是把物理设备通过传感器、网络、云端连为一体的技术体系,涵盖消费、工业、城市三大场景,核心挑战是规模、能耗、安全。
---

# IoT 物联网

## 定义

**IoT(Internet of Things,物联网)** 指将物理世界的设备(传感器、执行器、家电、车辆、工业机械等)通过嵌入式计算 + 网络连接 + 云端数据平台连接为一体,实现远程感知、控制与自动化决策的技术体系。

概念由 Kevin Ashton 1999 年提出,2010 年代随着低成本 MCU、无线模组、云计算普及而爆发。今天 IoT 设备数量已远超人口,据 IoT Analytics 估计全球活跃 IoT 设备 2025 年突破 200 亿台。

## 核心要点

### 四层架构

```
应用层  : 业务应用、可视化、AI 分析
平台层  : 设备管理、数据中台、规则引擎、数字孪生
网络层  : 短距(WiFi/蓝牙/Zigbee)、广域(4G/5G/LoRa/NB-IoT)
感知层  : 传感器、MCU、执行器、嵌入式 OS
```

### 三大典型场景

- **消费 IoT(Consumer IoT)**:智能家居、可穿戴、车联网。
  - 代表:Apple HomeKit、Google Home、小米生态链、特斯拉。
- **工业 IoT(IIoT)**:智能制造、预测性维护、能源管理、供应链追踪。
  - 代表:GE Predix、西门子 MindSphere、PTC ThingWorx、华为 FusionPlant。
- **智慧城市 / 公共 IoT**:智能路灯、环境监测、智能交通、共享设备。
  - 代表:智慧水表、共享单车、城市大脑。

### 通信协议

| 类型 | 协议 | 适用 |
|---|---|---|
| 短距无线 | WiFi、蓝牙 BLE、Zigbee、Thread、Matter | 家居、可穿戴 |
| 蜂窝 | 4G、5G、Cat-M、NB-IoT | 广域低带宽 |
| LPWAN | LoRa、Sigfox | 表计、农业 |
| 应用层 | MQTT、CoAP、HTTP/REST、AMQP | 设备 ↔ 云 |
| 工业协议 | Modbus、OPC UA、PROFINET | 工厂车间 |

**MQTT** 是 IoT 应用层事实标准:发布/订阅、QoS 三档、轻量包头。

### 数据流通常态

边缘传感 → 边缘网关(预处理 / 过滤)→ MQTT/HTTP → 云端 IoT 平台(AWS IoT Core、Azure IoT Hub、阿里云物联网)→ 数据仓库 + 流处理(Kafka、Flink)→ AI 推理 / 业务系统 → 反向控制设备。

### 边缘计算

为降低延迟、节流量、保护隐私,大量推理与控制下沉到**边缘**:NVIDIA Jetson、树莓派 + Coral TPU、各种 SoC + NPU。与 [[微服务]]、Kubernetes(K3s/MicroK8s)思想结合,形成 IoT-Edge-Cloud 连续体。

### 数字孪生(Digital Twin)

把物理设备/产线/城市映射为云端虚拟模型,实时同步状态并支持仿真预测。是 IIoT 与智慧城市的高阶形态。

## 典型应用 / 主要工具

- **消费**:Apple HomeKit、Matter 标准、小米米家、华为鸿蒙智联。
- **工业**:Siemens MindSphere、PTC ThingWorx、AVEVA、华为 FusionPlant。
- **平台**:AWS IoT Core / Greengrass、Azure IoT Hub / Edge、Google Cloud IoT、阿里云物联网平台。
- **开源**:EMQX、Mosquitto(MQTT broker)、ThingsBoard、Node-RED、OpenHAB、Home Assistant。
- **硬件**:ESP32、STM32、树莓派、Arduino、NRF52、Particle。
- **协议**:Matter(智能家居跨厂商)、OPC UA(工业)、CoAP(受限设备)。

## 局限与陷阱

- **安全噩梦**:Mirai 等僵尸网络利用默认密码、固件漏洞,IoT 是 DDoS 重灾区。需固件签名、零信任、最小权限。
- **碎片化生态**:协议、平台、厂商林立,跨品牌互联难,Matter 试图统一智能家居。
- **能耗约束**:电池设备需深度睡眠 + 唤醒事件驱动,与"始终在线"逻辑天然冲突。
- **隐私争议**:摄像头、门铃、智能音箱采集大量隐私数据,合规复杂。涉及 [[GDPR]]、[[CCPA]]。
- **生命周期长**:工业设备 10—20 年,固件更新机制薄弱时埋下长期漏洞。
- **OTA 风险**:远程升级若推错固件可能"砖化"百万设备。
- **数据洪水**:海量小包数据带来存储、网络、隐私三重压力,需边缘预处理。

## 与其他概念的关系

- 设备生态:[[HomeKit智能家居]]、[[Apple生态系统]] 是 IoT 在消费场景的代表。
- 网络通信:依赖 [[TCP]]、UDP、MQTT 等协议;短距常用 [[AirDrop与无线协议]] 描述的同类无线协议族。
- 云架构:平台依赖 [[微服务]]、[[分布式系统]] 处理海量设备并发。
- 数据基础:与 [[Lambda架构]]、[[Lakehouse架构]] 协同处理流批数据。
- 安全合规:与 [[零信任架构]]、[[GDPR]]、[[CCPA]]、[[隐私优先时代]] 紧密关联。
- AI 融合:边缘 [[人工智能]] / TinyML 把模型部署到 IoT 终端,实现本地推理。

## 参考源

- Kevin Ashton (2009). *That 'Internet of Things' Thing*. RFID Journal.
- IoT Analytics 年度市场报告
- IETF / OASIS MQTT、CoAP 规范
