---
title: AWS 核心服务
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: AWS 是 Amazon 在 2006 年起推出的云服务市场领导者,EC2/S3/Lambda/RDS/VPC 等核心服务定义了"云计算"行业语言,占据全球公有云 30%+ 市场份额,是云原生架构的事实参考。
---

# AWS 核心服务

## 定义

**Amazon Web Services(AWS)** 是 Amazon 在 2006 年起推出的云计算服务平台。它的成立改变了 IT 基础设施模式——从"自建机房"转向"按需付费的云服务"。S3(2006)、EC2(2006)是开山之作,后衍生 200+ 服务,覆盖计算、存储、网络、数据库、AI、IoT 等全部领域。

AWS 占公有云市场份额最大(2024 约 31%),GCP 约 12%,Azure 约 25%。中国市场被阿里云、腾讯云主导,但全球语境"云"几乎默认 AWS。

## 计算服务

**EC2(Elastic Compute Cloud)**

虚拟机(Instance):
- 实例类型:t/c/m/r/g/p 系列(通用/计算/内存/GPU)
- 按秒计费
- 自动扩缩(Auto Scaling Group)
- AMI(Amazon Machine Image)启动模板
- 关键概念:Region(地区)、AZ(可用区)、VPC、Security Group

EC2 是云的基础——租虚拟机的标杆。

**Lambda**

Serverless 函数:
- 上传代码(Python / Node / Java / Go / Rust 等)
- 事件触发(API Gateway / S3 / SQS / EventBridge)
- 按调用计费(冷启动 100ms-2s)
- 最长 15 分钟单次运行
- 适合:轻量后端、ETL、事件处理

催生了"无服务器架构"概念,与 [[Cloudflare Workers]]、Vercel Functions 共同代表。

**ECS / EKS / Fargate**

容器:
- ECS:AWS 自家容器编排
- EKS:[[Kubernetes]] 托管
- Fargate:Serverless 容器(无服务器管理)

**Lightsail**

简化 VPS,固定价格、面向开发者。

## 存储服务

**S3(Simple Storage Service)**

对象存储(2006 首发):
- 几乎无限容量
- 11 个 9 持久性
- 静态网站、备份、数据湖
- 对象级权限(ACL、Bucket Policy)
- 存储类:Standard / IA / Glacier 等
- API 是事实标准(MinIO、阿里云 OSS 都兼容)

S3 是云存储设计的标杆——简单 PUT/GET、几乎无限扩展、按用量付费。

**EBS(Elastic Block Store)**

EC2 的硬盘(Block Storage):
- 类型:gp3 / io2 / st1(吞吐)
- 快照备份
- 跨 AZ 不共享(单 AZ 限定)

**EFS(Elastic File System)**

NFS 类共享文件系统,跨多 EC2 共享。

**FSx**

Windows / Lustre / NetApp 专用文件系统。

**Glacier**

冷存储(归档)。低成本但取数据慢(分钟到小时)。

## 数据库

**RDS(Relational Database Service)**

托管关系型数据库:
- MySQL / PostgreSQL / MariaDB / SQL Server / Oracle
- Aurora(AWS 自研,MySQL/PostgreSQL 兼容,3-5 倍性能)
- 自动备份、Failover、读写分离

**DynamoDB**

托管 NoSQL(键值 + 文档):
- Serverless,毫秒级延迟
- Provisioned 或 On-Demand 计费
- 全球表(多 Region 复制)
- Stream(变更捕获)

**ElastiCache**

托管 Redis / Memcached。

**Redshift**

数据仓库(PostgreSQL 风),Snowflake 主要竞争对手。

**Neptune**

图数据库(SPARQL / Gremlin)。

**TimeStream**

时序数据库。

## 网络

**VPC(Virtual Private Cloud)**

私有网络:
- Subnet(子网,关联 AZ)
- Route Table、Internet Gateway
- NAT Gateway
- VPC Peering、Transit Gateway(跨 VPC 连通)

**Route 53**

DNS 服务,支持健康检查、地理路由。

**CloudFront**

CDN([[CDN]])全球节点,与 S3 / EC2 / API Gateway 集成。

**API Gateway**

[[API网关]]托管:
- REST、WebSocket、HTTP API
- 限流、认证、缓存
- 与 Lambda 紧密(常用组合)

**ELB / ALB / NLB**

负载均衡器:
- ALB(Application,L7 HTTP)
- NLB(Network,L4 TCP)
- ELB(经典,旧)

## 身份与安全

**IAM(Identity and Access Management)**

权限模型:
- User / Group / Role / Policy
- 极细粒度(JSON 策略)
- 跨账号 Role Assumption
- 复杂度高,误配置是常见漏洞

**KMS(Key Management Service)**

密钥管理:
- 客户主密钥(CMK)
- 加解密 API
- 与 S3、EBS、RDS 自动加密集成

**Secrets Manager / Parameter Store**

存数据库密码、API Key 等。

**Cognito**

用户身份服务:
- User Pool(用户库)
- Identity Pool(联合身份)
- 与 OAuth、SAML 集成

**WAF(Web Application Firewall)**

L7 防火墙,防 [[OWASP Top 10]] 攻击。

**Shield**

DDoS 防护(标准免费,Advanced 收费)。

**GuardDuty / Inspector / Macie**

威胁检测、漏洞扫描、敏感数据发现。

## 数据与 AI

**Glue**

托管 [[ETL与ELT]] 服务,Spark + 数据目录。

**EMR**

托管 Hadoop / Spark 集群。

**Athena**

S3 上的 SQL 查询(Presto-based),按扫描量计费。

**Kinesis**

类似 [[Kafka]] 的流处理:
- Streams(原始流)
- Data Firehose(自动批量到 S3)
- Analytics(SQL 流分析)

**SageMaker**

机器学习平台:训练、部署、Feature Store、Pipelines。

**Bedrock**

LLM API 服务:Anthropic Claude、Mistral、Meta Llama 等。

**Lex / Polly / Transcribe / Translate / Comprehend**

NLP 服务集合。

## 应用集成

**SQS(Simple Queue Service)**

[[消息队列]],FIFO / 标准:
- 标准:At-Least-Once,顺序不保证
- FIFO:严格顺序、Exactly-Once

**SNS(Simple Notification Service)**

发布订阅,推送到 SMS、邮件、Lambda、SQS。

**EventBridge**

事件总线,与 200+ AWS 服务和第三方 SaaS 集成。

**Step Functions**

工作流编排([[Saga模式]] 实现选项),与 Lambda、ECS 集成。

## DevOps

**CloudFormation**

基础设施即代码(IaC):
- YAML / JSON 模板
- 与 AWS 服务深度耦合
- 现代多用 Terraform 替代

**CDK(Cloud Development Kit)**

用 TypeScript / Python / Java 写 CloudFormation。

**CodePipeline / CodeBuild / CodeDeploy**

[[CI_CD流水线]] 全套(竞争 GitHub Actions、GitLab CI)。

**Systems Manager**

服务器管理、Patch、Run Command。

## 监控

**CloudWatch**

指标、日志、告警:
- Metric(自动收集 EC2/Lambda/RDS)
- Logs(集中存储)
- Alarms(阈值告警)
- Insights(日志查询)

**X-Ray**

[[分布式追踪]],与 OpenTelemetry 互通。

## 全球分布

**Region**

物理地区:
- us-east-1(弗吉尼亚)是最老的
- 中国:北京(BJS,与西云联营)、宁夏(ZHY,与光环新网联营)——独立账号
- 全球 30+ Region

**Availability Zone(AZ)**

Region 内多个独立机房,毫秒级延迟。HA 架构必须跨 AZ。

**Edge Locations**

CloudFront / Lambda@Edge / Global Accelerator,400+ 节点。

## 云成本管理

**Cost Explorer**

可视化账单分析。

**Budgets**

预算告警。

**Savings Plans / Reserved Instances**

预付折扣。Compute Savings Plans 可省 60-72%。

**Spot Instances**

剩余产能拍卖,价格便宜 70-90%,但可能被回收。

## AWS 与竞争对手对比

| 功能 | AWS | GCP | Azure |
|---|---|---|---|
| VM | EC2 | Compute Engine | VM |
| Serverless 函数 | Lambda | Cloud Functions | Azure Functions |
| 对象存储 | S3 | Cloud Storage | Blob Storage |
| K8s | EKS | GKE | AKS |
| 数据仓库 | Redshift | BigQuery | Synapse |
| AI | SageMaker / Bedrock | Vertex AI | Azure ML / OpenAI |
| 全球网络 | 最广 | 强 | 强 |

## 局限与批评

- **复杂度爆炸**:200+ 服务,文档浩瀚
- **账单意外**:细粒度计费,易超预算
- **Vendor Lock-in**:Lambda、DynamoDB 等专有 API
- **客服**:基础免费(回复慢)
- **学习曲线**:认证(SAA、SAP、DOP)是市场必需
- **Region 独立计费 / 数据出域费**

## 工程实践

**1. 多账号架构**

按环境(dev / staging / prod)、按团队拆账号,用 AWS Organizations 集中管理。

**2. IaC 必备**

Terraform / CloudFormation / CDK,人工 Console 操作仅作探索。

**3. 标签(Tag)规范**

每个资源加 owner、env、cost-center,后期账单分析依赖。

**4. 监控基线**

CloudWatch Dashboard + Alarms 是最低要求,生产应有 [[Datadog]] / [[Grafana]] 等更强工具。

## 和其他概念的关系

AWS 是 [[云计算]] 服务的事实定义者,与 [[Vercel]]、[[Cloudflare Workers]]、[[Netlify]] 等"应用层 PaaS"形成"基础设施 vs 开发者体验"两层。它的服务是 [[微服务]] / [[Kubernetes]] / [[CI_CD流水线]] 等实践的常见承载平台。

S3 API 是对象存储的事实标准,与 [[ELK Stack]]、[[Apache Spark]] / [[Apache Airflow]]、Lakehouse([[ETL与ELT]])架构紧密配合,是数据工程基础。

Lambda 等 Serverless 服务推动 [[Serverless]] 范式普及,与 [[Cloudflare Workers]] 共同代表"无服务器化"工程趋势。

## 参考源

- raw/计算机/
- 相关:[[云计算]]、[[Serverless]]、[[Vercel]]
