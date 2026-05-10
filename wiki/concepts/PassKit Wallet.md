---
title: PassKit 与 Wallet
type: concept
tags: [ios, mature]
sources: [raw/iPhone/]
created: 2026-05-05
updated: 2026-05-05
summary: PassKit 是 iOS 中"票券、登机牌、会员卡、优惠券、活动门票"的统一容器框架,Wallet 是其前端 App,通过 .pkpass 文件标准化 + 推送更新机制提供位置感知与时间感知的票卡体验。
---

# PassKit 与 Wallet

## 定义

**PassKit** 是 iOS 中处理**票券类对象**(Passes)的开发者框架,**Wallet** 是其面向用户的前端 App。它把登机牌、电影票、会员卡、活动门票、优惠券、忠诚度卡等异构票据统一为 `.pkpass` 文件标准,提供锁屏唤起、位置感知、商家推送更新等能力。Apple Pay 也基于 PassKit 体系。

## 核心要点

**Pass 类型**

PassKit 定义了五大票券类型:
1. **Boarding Pass**(登机牌):机票、火车票、船票
2. **Coupon**(优惠券):打折券、积分券
3. **Event Ticket**(活动门票):演唱会、电影、体育赛事
4. **Generic Pass**(通用):课程证、入场券
5. **Store Card**(会员/储值卡):咖啡店积分卡、礼品卡

不同类型有不同的**字段布局**(主字段、次字段、辅助字段、背面字段)。

**.pkpass 文件结构**

`.pkpass` 是 ZIP 容器,内含:
- `pass.json`:元数据、字段、风格、相关位置
- `manifest.json`:文件清单与 SHA1
- `signature`:开发者证书签名
- 图片资源(logo、icon、strip、背景)

**位置感知与时间感知**

Pass 可声明**最多 10 个相关位置**(经纬度 + 半径 + 描述),设备靠近时锁屏自动浮现。也支持时间触发(登机牌起飞前几小时自动浮现)。

**推送更新机制**

商家可通过 APNs 向 Pass 推送更新:
- 用户安装 Pass 后,设备向商家服务器注册一个 push token
- 商家有变更(航班延误、登机口变化)时调用 PassKit Web Service 接口
- 服务器推送通知,Wallet 拉取最新 `.pkpass` 替换本地

**Apple Pay 的特殊地位**

Apple Pay 信用卡/借记卡 是 PassKit 的特殊 Pass 类型,但**不可被开发者直接创建**——必须银行通过与 Apple 的合约接入。普通开发者只能创建非支付类 Pass。

**集成方式**

App 创建 / 更新 Pass 的方式:
- 服务器端生成 `.pkpass`(需开发者证书签名)
- App 调用 `PKAddPassesViewController` 弹窗让用户加入 Wallet
- 或用户通过邮件、Web 链接、扫码点 `.pkpass` 加入

**可访问性与共享**

- AirDrop 可分享 Pass(航司给同行人)
- iMessage 可发送 Pass
- 共享后接收者可加入自己 Wallet

## 与其他概念的关系

PassKit 是 [[iOS应用扩展]] 之外另一种 App 与系统级界面深度集成的方式。其支付层延伸到 [[Apple Pay]];位置触发依赖 [[iOS隐私机制]] 的位置权限。许多商家通过 [[APNs推送通知]] 实现 Pass 实时更新。

## 高频陷阱

- `.pkpass` 必须开发者证书签名,自签 / 修改后失效
- iCloud 不会自动同步 Pass(2024 起部分商家加入)
- 信用卡型 Pass 由发卡行管控,不能任意开发
- 位置感知会消耗少量电量,数量过多影响续航
- 旧 Pass 用户已删除后,服务器还应能识别"已注销"状态,避免推送到不存在的卡

## 参考源

- raw/iPhone/(PassKit / Wallet 章节)
- 相关:[[Apple Pay]]、[[iOS应用扩展]]、[[APNs推送通知]]、[[iOS隐私机制]]
