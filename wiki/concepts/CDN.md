---
title: CDN
type: concept
tags: [cs, distributed, mature]
sources: [raw/计算机/开发学习/系统/Wordpress/04-精通创新层/02-性能优化/CDN配置.md]
created: 2026-05-05
updated: 2026-05-05
summary: CDN 通过全球分布的边缘节点缓存内容,让用户从最近节点获取资源,显著降低延迟、节省带宽,是网站性能与高可用的标配基础设施。
---

# CDN

## 定义

**CDN(Content Delivery Network,内容分发网络)** 是部署在全球各地的边缘节点网络,通过把网站静态资源(图片、视频、JS、CSS)缓存到离用户最近的节点,显著降低延迟、节省源站带宽、提升可用性。是现代 Web 站点、视频平台、API 服务的标配基础设施。

## 核心要点

- **核心价值**
  - **降低延迟**:用户从最近节点取数据,RTT 从几百 ms 降到几十 ms
  - **节省带宽**:源站只需向 CDN 节点回源,边缘节点服务用户
  - **承载突发流量**:CDN 节点群天然分摊大流量,源站不挂
  - **DDoS 防护**:边缘节点过滤攻击流量,源站隐藏
  - **全球可用**:跨大洲访问质量提升
- **核心组件**
  - **边缘节点(POP, Point of Presence)**:全球数百节点,缓存内容
  - **回源(Origin Pull)**:首次未命中时从源站拉取
  - **DNS 调度**:基于用户 IP 解析到最近节点
  - **Anycast IP**:全球同一 IP,BGP 路由就近(Cloudflare、Google)
- **路由原理**
  - 用户访问 cdn.example.com
  - DNS 服务器根据用户 IP 返回最近 / 最优节点 IP
  - 用户向该节点发请求
  - 节点缓存命中 → 直接返回
  - 未命中 → 回源拉取并缓存
- **缓存策略**
  - **Cache-Control / Expires**:HTTP 头控制 TTL
  - **基于路径**:静态资源(.js/.png)长缓存,API 短缓存或不缓存
  - **基于 Vary**:按 Accept-Encoding / User-Agent 区分缓存
  - **强制刷新(Purge)**:发布新版本时手动清除缓存
  - **预热(Preload)**:活动开始前主动让 CDN 拉取热门资源
- **缓存命中率**
  - 命中率高 → 性能好,源站压力低
  - 影响因素:URL 一致性、缓存键设计、TTL 长度、内容更新频率
- **静态 vs 动态加速**
  - **静态加速**:缓存资源,经典用途
  - **动态加速**:不缓存内容,但优化路由(DSA - Dynamic Site Acceleration)
    - 节点间用专线 / 优化路径
    - 适合 API、登录、个性化内容
- **CDN 缓存层级**
  - L1 边缘节点(用户最近)
  - L2 / 中间层(区域汇聚)
  - 源站(Origin)
  - 减少源站回源,提升整体命中率
- **CDN 应用场景**
  - **网站静态资源**:图片、视频、CSS/JS
  - **视频点播 / 直播**:HLS / DASH 切片分发
  - **软件下载**:大文件分发
  - **API 缓存**:GET 接口缓存,提升 QPS
  - **边缘计算**:运行 Worker 函数,见 [[边缘计算]]
- **现代趋势:边缘计算 + Serverless**
  - **Cloudflare Workers / Vercel Edge / AWS Lambda@Edge**:在 CDN 边缘运行代码
  - 用例:A/B 实验、个性化、AI 推理、API 路由
  - 把"动态内容"也下沉到边缘
- **典型 CDN 服务商**
  - **国际**:Cloudflare、AWS CloudFront、Akamai、Fastly、Google Cloud CDN
  - **国内**:阿里云 CDN、腾讯云 CDN、网宿、华为云、百度智能云
- **关键指标**
  - **命中率**:命中 / 总请求
  - **回源率**:1 - 命中率
  - **平均响应时间**:用户感知性能
  - **带宽**:计费基础
- **常见坑**
  - **缓存穿透**:请求不存在的 URL,每次都回源,需缓存空响应
  - **缓存击穿**:热门 key 失效瞬间高并发回源,需互斥锁 + 提前刷新
  - **缓存雪崩**:大量 key 同时过期,源站被压垮,需 TTL 错峰
  - **私有信息缓存**:用户专属内容被缓存到 CDN,需 Vary / Cache-Control: private
  - **HTTP / HTTPS 区分**:不同协议不同缓存键

## 和其他概念的关系

CDN 是 [[缓存]] 在地理分布式场景的特殊化:边缘节点 + 全球 DNS 调度。

与 [[负载均衡]] 协作:用户先到 CDN,CDN 未命中再到源站 LB。

与 [[TLS]] 配合:HTTPS 内容也可缓存,需要 SSL 证书部署到 CDN。

与 [[Web安全]] 结合:CDN 是 DDoS 防护、WAF、Bot 防护的天然部署点(Cloudflare、AWS CloudFront 都内置)。

[[边缘计算]] 把 CDN 进一步演进为可执行代码的"分布式 Serverless 平台",见 raw 中"边缘计算 + 云融合"。

[[微服务]] 中的全球部署架构常用 CDN 做静态资源 + 边缘 API 缓存,源站集中部署降低复杂度。

## 参考源

- raw/计算机/开发学习/系统/Wordpress/04-精通创新层/02-性能优化/CDN配置.md(CDN 配置)
- raw/计算机/运维知识/云服务/云服务器知识地图.md(CDN 章节)
- raw/计算机/运维知识/云服务/边缘计算 + 云融合.md(边缘 + CDN 联动)
