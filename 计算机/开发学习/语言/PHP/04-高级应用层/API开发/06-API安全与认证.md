# API安全与认证

## 🎯 学习目标
- 掌握API安全的基本概念和威胁模型
- 理解各种认证和授权机制
- 学会实现API安全防护措施
- 了解API安全的最佳实践和监控策略

## 📚 核心概念

### API安全架构

```mermaid
graph TD
    A[客户端] --> B[API网关]
    B --> C[认证服务]
    B --> D[授权服务]
    B --> E[API服务]
    
    F[安全威胁] --> G[身份伪造]
    F --> H[数据泄露]
    F --> I[权限提升]
    F --> J[拒绝服务]
    
    K[防护措施] --> L[身份认证]
    K --> M[访问控制]
    K --> N[数据加密]
    K --> O[安全监控]
```

### 认证方式对比

| 认证方式 | 描述 | 优点 | 缺点 | 适用场景 |
|----------|------|------|------|----------|
| API Key | 简单的密钥认证 | 实现简单 | 安全性较低 | 内部服务 |
| Basic Auth | HTTP基本认证 | 标准协议 | 传输明文 | 简单应用 |
| Bearer Token | 令牌认证 | 灵活性高 | 需要管理 | 现代应用 |
| JWT | JSON Web Token | 无状态 | 难以撤销 | 分布式系统 |
| OAuth 2.0 | 授权框架 | 标准化 | 复杂度高 | 第三方集成 |

## 🔧 API安全实现

### 认证和授权系统
```php
<?php
// 1. 认证管理器
class AuthenticationManager {
    private $strategies;
    private $userRepository;
    private $tokenManager;
    
    public function __construct() {
        $this->strategies = [];
        $this->userRepository = new UserRepository();
        $this->tokenManager = new TokenManager();
    }
    
    // 注册认证策略
    public function registerStrategy($name, $strategy) {
        $this->strategies[$name] = $strategy;
    }
    
    // 认证用户
    public function authenticate($request) {
        $authHeader = $request['headers']['Authorization'] ?? '';
        
        if (empty($authHeader)) {
            return $this->createAuthResult(false, 'Authorization header required');
        }
        
        // 解析认证头
        $authParts = explode(' ', $authHeader, 2);
        if (count($authParts) !== 2) {
            return $this->createAuthResult(false, 'Invalid authorization header format');
        }
        
        $authType = strtolower($authParts[0]);
        $authValue = $authParts[1];
        
        // 根据认证类型选择策略
        if (isset($this->strategies[$authType])) {
            return $this->strategies[$authType]->authenticate($authValue, $request);
        }
        
        return $this->createAuthResult(false, 'Unsupported authentication type');
    }
    
    // 创建认证结果
    private function createAuthResult($success, $message, $user = null) {
        return [
            'success' => $success,
            'message' => $message,
            'user' => $user
        ];
    }
}

// 2. JWT认证策略
class JWTAuthenticationStrategy {
    private $secretKey;
    private $algorithm;
    private $userRepository;
    
    public function __construct($secretKey, $algorithm = 'HS256') {
        $this->secretKey = $secretKey;
        $this->algorithm = $algorithm;
        $this->userRepository = new UserRepository();
    }
    
    // 认证JWT令牌
    public function authenticate($token, $request) {
        try {
            // 验证JWT令牌
            $payload = $this->verifyToken($token);
            
            if (!$payload) {
                return ['success' => false, 'message' => 'Invalid token'];
            }
            
            // 检查令牌是否过期
            if (isset($payload['exp']) && $payload['exp'] < time()) {
                return ['success' => false, 'message' => 'Token expired'];
            }
            
            // 获取用户信息
            $user = $this->userRepository->findById($payload['user_id']);
            
            if (!$user) {
                return ['success' => false, 'message' => 'User not found'];
            }
            
            return [
                'success' => true,
                'message' => 'Authentication successful',
                'user' => $user,
                'payload' => $payload
            ];
            
        } catch (Exception $e) {
            return ['success' => false, 'message' => 'Token verification failed'];
        }
    }
    
    // 验证JWT令牌
    private function verifyToken($token) {
        $parts = explode('.', $token);
        
        if (count($parts) !== 3) {
            return false;
        }
        
        list($header, $payload, $signature) = $parts;
        
        // 验证签名
        $expectedSignature = $this->sign($header . '.' . $payload);
        
        if (!hash_equals($expectedSignature, $signature)) {
            return false;
        }
        
        // 解码载荷
        $decodedPayload = json_decode(base64_decode($payload), true);
        
        return $decodedPayload;
    }
    
    // 生成签名
    private function sign($data) {
        return base64_encode(hash_hmac('sha256', $data, $this->secretKey, true));
    }
    
    // 生成JWT令牌
    public function generateToken($user, $expiration = 3600) {
        $header = json_encode(['typ' => 'JWT', 'alg' => $this->algorithm]);
        $payload = json_encode([
            'user_id' => $user['id'],
            'username' => $user['username'],
            'exp' => time() + $expiration,
            'iat' => time()
        ]);
        
        $headerEncoded = base64_encode($header);
        $payloadEncoded = base64_encode($payload);
        
        $signature = $this->sign($headerEncoded . '.' . $payloadEncoded);
        
        return $headerEncoded . '.' . $payloadEncoded . '.' . $signature;
    }
}

// 3. API Key认证策略
class APIKeyAuthenticationStrategy {
    private $apiKeyRepository;
    
    public function __construct() {
        $this->apiKeyRepository = new APIKeyRepository();
    }
    
    // 认证API Key
    public function authenticate($apiKey, $request) {
        $keyInfo = $this->apiKeyRepository->findByKey($apiKey);
        
        if (!$keyInfo) {
            return ['success' => false, 'message' => 'Invalid API key'];
        }
        
        // 检查API Key是否过期
        if ($keyInfo['expires_at'] && strtotime($keyInfo['expires_at']) < time()) {
            return ['success' => false, 'message' => 'API key expired'];
        }
        
        // 检查API Key是否被禁用
        if (!$keyInfo['is_active']) {
            return ['success' => false, 'message' => 'API key disabled'];
        }
        
        // 更新最后使用时间
        $this->apiKeyRepository->updateLastUsed($apiKey);
        
        return [
            'success' => true,
            'message' => 'Authentication successful',
            'user' => $keyInfo['user'],
            'api_key' => $keyInfo
        ];
    }
}

// 4. 授权管理器
class AuthorizationManager {
    private $permissions;
    private $roles;
    
    public function __construct() {
        $this->permissions = [];
        $this->roles = [];
        $this->loadPermissions();
        $this->loadRoles();
    }
    
    // 检查权限
    public function checkPermission($user, $resource, $action) {
        // 检查用户角色
        $userRoles = $user['roles'] ?? [];
        
        foreach ($userRoles as $role) {
            if ($this->hasRolePermission($role, $resource, $action)) {
                return true;
            }
        }
        
        // 检查用户直接权限
        return $this->hasUserPermission($user['id'], $resource, $action);
    }
    
    // 检查角色权限
    private function hasRolePermission($role, $resource, $action) {
        if (!isset($this->roles[$role])) {
            return false;
        }
        
        $rolePermissions = $this->roles[$role]['permissions'] ?? [];
        
        foreach ($rolePermissions as $permission) {
            if ($this->matchPermission($permission, $resource, $action)) {
                return true;
            }
        }
        
        return false;
    }
    
    // 检查用户权限
    private function hasUserPermission($userId, $resource, $action) {
        $userPermissions = $this->permissions[$userId] ?? [];
        
        foreach ($userPermissions as $permission) {
            if ($this->matchPermission($permission, $resource, $action)) {
                return true;
            }
        }
        
        return false;
    }
    
    // 匹配权限
    private function matchPermission($permission, $resource, $action) {
        $permissionParts = explode(':', $permission);
        
        if (count($permissionParts) !== 2) {
            return false;
        }
        
        $permissionResource = $permissionParts[0];
        $permissionAction = $permissionParts[1];
        
        // 支持通配符匹配
        $resourceMatch = $permissionResource === '*' || $permissionResource === $resource;
        $actionMatch = $permissionAction === '*' || $permissionAction === $action;
        
        return $resourceMatch && $actionMatch;
    }
    
    // 加载权限配置
    private function loadPermissions() {
        $this->permissions = [
            '1' => ['users:read', 'users:write'],
            '2' => ['orders:read']
        ];
    }
    
    // 加载角色配置
    private function loadRoles() {
        $this->roles = [
            'admin' => [
                'permissions' => ['*:*']
            ],
            'user' => [
                'permissions' => ['users:read', 'orders:read', 'orders:write']
            ],
            'guest' => [
                'permissions' => ['users:read']
            ]
        ];
    }
}

// 5. 安全中间件
class SecurityMiddleware {
    private $authManager;
    private $authzManager;
    private $rateLimiter;
    private $logger;
    
    public function __construct() {
        $this->authManager = new AuthenticationManager();
        $this->authzManager = new AuthorizationManager();
        $this->rateLimiter = new RateLimiter();
        $this->logger = new SecurityLogger();
    }
    
    // 认证中间件
    public function authentication($request) {
        $authResult = $this->authManager->authenticate($request);
        
        if (!$authResult['success']) {
            $this->logger->logAuthFailure($request, $authResult['message']);
            return $this->createErrorResponse(401, $authResult['message']);
        }
        
        $request['user'] = $authResult['user'];
        return true;
    }
    
    // 授权中间件
    public function authorization($request, $resource, $action) {
        if (!isset($request['user'])) {
            return $this->createErrorResponse(401, 'Authentication required');
        }
        
        $user = $request['user'];
        
        if (!$this->authzManager->checkPermission($user, $resource, $action)) {
            $this->logger->logAuthzFailure($request, $resource, $action);
            return $this->createErrorResponse(403, 'Insufficient permissions');
        }
        
        return true;
    }
    
    // 速率限制中间件
    public function rateLimit($request, $limit = 100, $window = 3600) {
        $clientId = $this->getClientId($request);
        
        if (!$this->rateLimiter->checkLimit($clientId, $limit, $window)) {
            $this->logger->logRateLimitExceeded($request, $limit, $window);
            return $this->createErrorResponse(429, 'Rate limit exceeded');
        }
        
        return true;
    }
    
    // 获取客户端ID
    private function getClientId($request) {
        // 优先使用用户ID
        if (isset($request['user']['id'])) {
            return 'user:' . $request['user']['id'];
        }
        
        // 使用IP地址
        return 'ip:' . ($request['ip'] ?? 'unknown');
    }
    
    // 创建错误响应
    private function createErrorResponse($statusCode, $message) {
        return [
            'status_code' => $statusCode,
            'headers' => ['Content-Type' => 'application/json'],
            'body' => json_encode(['error' => $message, 'status_code' => $statusCode])
        ];
    }
}

// 6. 安全监控器
class SecurityMonitor {
    private $logger;
    private $alerts;
    private $metrics;
    
    public function __construct() {
        $this->logger = new SecurityLogger();
        $this->alerts = [];
        $this->metrics = [
            'auth_failures' => 0,
            'authz_failures' => 0,
            'rate_limit_hits' => 0,
            'suspicious_requests' => 0
        ];
    }
    
    // 记录认证失败
    public function recordAuthFailure($request, $reason) {
        $this->metrics['auth_failures']++;
        
        $this->logger->logAuthFailure($request, $reason);
        
        // 检查是否需要告警
        if ($this->metrics['auth_failures'] > 10) {
            $this->triggerAlert('HIGH_AUTH_FAILURES', [
                'count' => $this->metrics['auth_failures'],
                'time_window' => '1 hour'
            ]);
        }
    }
    
    // 记录授权失败
    public function recordAuthzFailure($request, $resource, $action) {
        $this->metrics['authz_failures']++;
        
        $this->logger->logAuthzFailure($request, $resource, $action);
        
        // 检查权限提升尝试
        if ($this->isPrivilegeEscalationAttempt($request, $resource, $action)) {
            $this->triggerAlert('PRIVILEGE_ESCALATION', [
                'user' => $request['user']['id'],
                'resource' => $resource,
                'action' => $action
            ]);
        }
    }
    
    // 记录速率限制
    public function recordRateLimit($request, $limit, $window) {
        $this->metrics['rate_limit_hits']++;
        
        $this->logger->logRateLimitExceeded($request, $limit, $window);
        
        // 检查DDoS攻击
        if ($this->metrics['rate_limit_hits'] > 100) {
            $this->triggerAlert('POSSIBLE_DDOS', [
                'rate_limit_hits' => $this->metrics['rate_limit_hits'],
                'time_window' => '1 hour'
            ]);
        }
    }
    
    // 检查权限提升尝试
    private function isPrivilegeEscalationAttempt($request, $resource, $action) {
        // 简化的权限提升检测逻辑
        $sensitiveResources = ['admin', 'system', 'config'];
        $sensitiveActions = ['delete', 'admin', 'system'];
        
        return in_array($resource, $sensitiveResources) || in_array($action, $sensitiveActions);
    }
    
    // 触发告警
    private function triggerAlert($type, $data) {
        $alert = [
            'type' => $type,
            'timestamp' => time(),
            'data' => $data
        ];
        
        $this->alerts[] = $alert;
        $this->logger->logAlert($alert);
        
        // 发送通知
        $this->sendNotification($alert);
    }
    
    // 发送通知
    private function sendNotification($alert) {
        // 实现通知发送逻辑
        echo "Security Alert: {$alert['type']} - " . json_encode($alert['data']) . "\n";
    }
    
    // 获取安全指标
    public function getSecurityMetrics() {
        return $this->metrics;
    }
    
    // 获取告警
    public function getAlerts($limit = 100) {
        return array_slice($this->alerts, -$limit);
    }
}

// 使用示例
echo "=== API安全与认证示例 ===\n";

try {
    // 创建认证管理器
    $authManager = new AuthenticationManager();
    
    // 注册认证策略
    $authManager->registerStrategy('bearer', new JWTAuthenticationStrategy('your-secret-key'));
    $authManager->registerStrategy('apikey', new APIKeyAuthenticationStrategy());
    
    // 创建授权管理器
    $authzManager = new AuthorizationManager();
    
    // 创建安全中间件
    $securityMiddleware = new SecurityMiddleware();
    
    // 创建安全监控器
    $securityMonitor = new SecurityMonitor();
    
    // 模拟请求
    $request = [
        'method' => 'GET',
        'path' => '/users/123',
        'headers' => [
            'Authorization' => 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImpvaG4iLCJleHAiOjE2MDAwMDAwMDB9.signature'
        ],
        'ip' => '192.168.1.100'
    ];
    
    // 测试认证
    $authResult = $authManager->authenticate($request);
    echo "认证结果: " . json_encode($authResult) . "\n";
    
    // 测试授权
    if ($authResult['success']) {
        $request['user'] = $authResult['user'];
        $authzResult = $authzManager->checkPermission($request['user'], 'users', 'read');
        echo "授权结果: " . ($authzResult ? '允许' : '拒绝') . "\n";
    }
    
    // 测试安全监控
    $securityMonitor->recordAuthFailure($request, 'Invalid token');
    $securityMonitor->recordAuthzFailure($request, 'admin', 'delete');
    $securityMonitor->recordRateLimit($request, 100, 3600);
    
    // 获取安全指标
    $metrics = $securityMonitor->getSecurityMetrics();
    echo "安全指标: " . json_encode($metrics) . "\n";
    
    // 获取告警
    $alerts = $securityMonitor->getAlerts();
    echo "安全告警数量: " . count($alerts) . "\n";
    
} catch (Exception $e) {
    echo "错误: " . $e->getMessage() . "\n";
}
?>
```

### 数据加密和安全传输
```php
<?php
// 1. 数据加密器
class DataEncryptor {
    private $algorithm;
    private $key;
    private $iv;
    
    public function __construct($key, $algorithm = 'AES-256-CBC') {
        $this->algorithm = $algorithm;
        $this->key = $key;
        $this->iv = random_bytes(16);
    }
    
    // 加密数据
    public function encrypt($data) {
        $encrypted = openssl_encrypt($data, $this->algorithm, $this->key, 0, $this->iv);
        
        if ($encrypted === false) {
            throw new Exception('Encryption failed');
        }
        
        return base64_encode($this->iv . $encrypted);
    }
    
    // 解密数据
    public function decrypt($encryptedData) {
        $data = base64_decode($encryptedData);
        
        if ($data === false) {
            throw new Exception('Invalid encrypted data');
        }
        
        $iv = substr($data, 0, 16);
        $encrypted = substr($data, 16);
        
        $decrypted = openssl_decrypt($encrypted, $this->algorithm, $this->key, 0, $iv);
        
        if ($decrypted === false) {
            throw new Exception('Decryption failed');
        }
        
        return $decrypted;
    }
    
    // 生成随机密钥
    public static function generateKey($length = 32) {
        return random_bytes($length);
    }
}

// 2. 密码哈希器
class PasswordHasher {
    private $algorithm;
    private $options;
    
    public function __construct($algorithm = PASSWORD_ARGON2ID, $options = []) {
        $this->algorithm = $algorithm;
        $this->options = array_merge([
            'memory_cost' => 65536,
            'time_cost' => 4,
            'threads' => 3
        ], $options);
    }
    
    // 哈希密码
    public function hash($password) {
        return password_hash($password, $this->algorithm, $this->options);
    }
    
    // 验证密码
    public function verify($password, $hash) {
        return password_verify($password, $hash);
    }
    
    // 检查密码是否需要重新哈希
    public function needsRehash($hash) {
        return password_needs_rehash($hash, $this->algorithm, $this->options);
    }
}

// 3. 安全传输管理器
class SecureTransportManager {
    private $encryptor;
    private $signer;
    
    public function __construct($encryptionKey, $signingKey) {
        $this->encryptor = new DataEncryptor($encryptionKey);
        $this->signer = new DataSigner($signingKey);
    }
    
    // 安全发送数据
    public function sendSecureData($data, $recipient) {
        // 加密数据
        $encryptedData = $this->encryptor->encrypt(json_encode($data));
        
        // 签名数据
        $signature = $this->signer->sign($encryptedData);
        
        // 创建安全消息
        $secureMessage = [
            'data' => $encryptedData,
            'signature' => $signature,
            'timestamp' => time(),
            'recipient' => $recipient
        ];
        
        return $secureMessage;
    }
    
    // 安全接收数据
    public function receiveSecureData($secureMessage) {
        // 验证签名
        if (!$this->signer->verify($secureMessage['data'], $secureMessage['signature'])) {
            throw new Exception('Invalid signature');
        }
        
        // 检查时间戳
        if (time() - $secureMessage['timestamp'] > 300) { // 5分钟过期
            throw new Exception('Message expired');
        }
        
        // 解密数据
        $decryptedData = $this->encryptor->decrypt($secureMessage['data']);
        
        return json_decode($decryptedData, true);
    }
}

// 4. 数据签名器
class DataSigner {
    private $privateKey;
    private $publicKey;
    
    public function __construct($privateKey, $publicKey = null) {
        $this->privateKey = $privateKey;
        $this->publicKey = $publicKey;
    }
    
    // 签名数据
    public function sign($data) {
        $signature = '';
        
        if (openssl_sign($data, $signature, $this->privateKey, OPENSSL_ALGO_SHA256)) {
            return base64_encode($signature);
        }
        
        throw new Exception('Signing failed');
    }
    
    // 验证签名
    public function verify($data, $signature) {
        $signature = base64_decode($signature);
        
        if ($signature === false) {
            return false;
        }
        
        $result = openssl_verify($data, $signature, $this->publicKey, OPENSSL_ALGO_SHA256);
        
        return $result === 1;
    }
    
    // 生成密钥对
    public static function generateKeyPair() {
        $config = [
            'digest_alg' => 'sha256',
            'private_key_bits' => 2048,
            'private_key_type' => OPENSSL_KEYTYPE_RSA
        ];
        
        $resource = openssl_pkey_new($config);
        
        if ($resource === false) {
            throw new Exception('Key generation failed');
        }
        
        openssl_pkey_export($resource, $privateKey);
        $publicKey = openssl_pkey_get_details($resource)['key'];
        
        return [
            'private_key' => $privateKey,
            'public_key' => $publicKey
        ];
    }
}

// 5. 安全配置管理器
class SecurityConfigManager {
    private $config;
    private $encryptor;
    
    public function __construct($encryptionKey) {
        $this->encryptor = new DataEncryptor($encryptionKey);
        $this->config = [];
    }
    
    // 设置安全配置
    public function setSecureConfig($key, $value) {
        $encryptedValue = $this->encryptor->encrypt(json_encode($value));
        $this->config[$key] = $encryptedValue;
    }
    
    // 获取安全配置
    public function getSecureConfig($key) {
        if (!isset($this->config[$key])) {
            return null;
        }
        
        $decryptedValue = $this->encryptor->decrypt($this->config[$key]);
        return json_decode($decryptedValue, true);
    }
    
    // 加载配置
    public function loadConfig($configFile) {
        if (file_exists($configFile)) {
            $configData = json_decode(file_get_contents($configFile), true);
            
            foreach ($configData as $key => $value) {
                $this->setSecureConfig($key, $value);
            }
        }
    }
    
    // 保存配置
    public function saveConfig($configFile) {
        $configData = [];
        
        foreach ($this->config as $key => $encryptedValue) {
            $configData[$key] = $encryptedValue;
        }
        
        file_put_contents($configFile, json_encode($configData, JSON_PRETTY_PRINT));
    }
}

// 使用示例
echo "=== 数据加密和安全传输示例 ===\n";

try {
    // 创建数据加密器
    $encryptionKey = DataEncryptor::generateKey();
    $encryptor = new DataEncryptor($encryptionKey);
    
    // 测试加密解密
    $originalData = 'Sensitive data that needs to be encrypted';
    $encryptedData = $encryptor->encrypt($originalData);
    $decryptedData = $encryptor->decrypt($encryptedData);
    
    echo "原始数据: $originalData\n";
    echo "加密数据: $encryptedData\n";
    echo "解密数据: $decryptedData\n";
    echo "加密解密成功: " . ($originalData === $decryptedData ? '是' : '否') . "\n\n";
    
    // 创建密码哈希器
    $passwordHasher = new PasswordHasher();
    
    // 测试密码哈希
    $password = 'user123';
    $hash = $passwordHasher->hash($password);
    $isValid = $passwordHasher->verify($password, $hash);
    
    echo "密码: $password\n";
    echo "哈希值: $hash\n";
    echo "验证结果: " . ($isValid ? '有效' : '无效') . "\n\n";
    
    // 创建数据签名器
    $keyPair = DataSigner::generateKeyPair();
    $signer = new DataSigner($keyPair['private_key'], $keyPair['public_key']);
    
    // 测试数据签名
    $data = 'Data to be signed';
    $signature = $signer->sign($data);
    $isValidSignature = $signer->verify($data, $signature);
    
    echo "数据: $data\n";
    echo "签名: $signature\n";
    echo "签名验证: " . ($isValidSignature ? '有效' : '无效') . "\n\n";
    
    // 创建安全传输管理器
    $secureTransport = new SecureTransportManager($encryptionKey, $keyPair['private_key']);
    
    // 测试安全传输
    $messageData = ['user_id' => 123, 'action' => 'login', 'timestamp' => time()];
    $secureMessage = $secureTransport->sendSecureData($messageData, 'user-service');
    $receivedData = $secureTransport->receiveSecureData($secureMessage);
    
    echo "原始消息: " . json_encode($messageData) . "\n";
    echo "安全消息: " . json_encode($secureMessage) . "\n";
    echo "接收数据: " . json_encode($receivedData) . "\n";
    echo "传输成功: " . (json_encode($messageData) === json_encode($receivedData) ? '是' : '否') . "\n\n";
    
    // 创建安全配置管理器
    $securityConfig = new SecurityConfigManager($encryptionKey);
    
    // 测试安全配置
    $securityConfig->setSecureConfig('database.password', 'secret123');
    $securityConfig->setSecureConfig('api.secret', 'api-secret-key');
    
    $dbPassword = $securityConfig->getSecureConfig('database.password');
    $apiSecret = $securityConfig->getSecureConfig('api.secret');
    
    echo "数据库密码: $dbPassword\n";
    echo "API密钥: $apiSecret\n";
    
} catch (Exception $e) {
    echo "错误: " . $e->getMessage() . "\n";
}
?>
```

## 📊 最佳实践

### API安全最佳实践
```php
<?php
// API安全最佳实践

class APISecurityBestPractices {
    // 1. 认证安全
    public static function getAuthenticationSecurityPractices() {
        return [
            '令牌管理' => [
                'JWT安全' => '使用强密钥，设置合理过期时间',
                '令牌撤销' => '实现令牌撤销机制',
                '令牌刷新' => '实现令牌刷新机制',
                '令牌存储' => '安全存储令牌'
            ],
            '密码安全' => [
                '密码策略' => '实施强密码策略',
                '密码哈希' => '使用安全的密码哈希算法',
                '密码重置' => '实现安全的密码重置流程',
                '多因素认证' => '实施多因素认证'
            ],
            '会话管理' => [
                '会话超时' => '设置合理的会话超时时间',
                '会话固定' => '防止会话固定攻击',
                '会话劫持' => '防止会话劫持攻击',
                '会话注销' => '实现安全的会话注销'
            ]
        ];
    }
    
    // 2. 授权安全
    public static function getAuthorizationSecurityPractices() {
        return [
            '权限控制' => [
                '最小权限' => '实施最小权限原则',
                '角色分离' => '分离不同角色的权限',
                '权限继承' => '合理设计权限继承关系',
                '权限审计' => '定期审计权限分配'
            ],
            '访问控制' => [
                '资源保护' => '保护敏感资源',
                '操作控制' => '控制敏感操作',
                '数据过滤' => '根据权限过滤数据',
                'API限制' => '限制API访问范围'
            ],
            '权限管理' => [
                '权限分配' => '自动化权限分配',
                '权限回收' => '及时回收不需要的权限',
                '权限监控' => '监控权限使用情况',
                '权限报告' => '生成权限使用报告'
            ]
        ];
    }
    
    // 3. 数据安全
    public static function getDataSecurityPractices() {
        return [
            '数据加密' => [
                '传输加密' => '使用HTTPS加密传输',
                '存储加密' => '加密敏感数据存储',
                '密钥管理' => '安全管理加密密钥',
                '加密算法' => '使用强加密算法'
            ],
            '数据保护' => [
                '数据脱敏' => '对敏感数据进行脱敏',
                '数据备份' => '定期备份重要数据',
                '数据恢复' => '实现数据恢复机制',
                '数据销毁' => '安全销毁不需要的数据'
            ],
            '数据访问' => [
                '访问日志' => '记录数据访问日志',
                '访问控制' => '控制数据访问权限',
                '数据审计' => '审计数据访问行为',
                '异常检测' => '检测异常数据访问'
            ]
        ];
    }
    
    // 4. 网络安全
    public static function getNetworkSecurityPractices() {
        return [
            '传输安全' => [
                'HTTPS强制' => '强制使用HTTPS',
                '证书管理' => '管理SSL证书',
                '协议安全' => '使用安全协议',
                '传输监控' => '监控传输安全'
            ],
            '网络防护' => [
                '防火墙' => '配置网络防火墙',
                'DDoS防护' => '实施DDoS防护',
                '入侵检测' => '部署入侵检测系统',
                '网络隔离' => '实施网络隔离'
            ],
            'API防护' => [
                '速率限制' => '实施API速率限制',
                '请求验证' => '验证API请求',
                '响应过滤' => '过滤敏感响应数据',
                '错误处理' => '安全处理错误信息'
            ]
        ];
    }
}

// 使用示例
echo "=== API安全最佳实践示例 ===\n";

try {
    // 认证安全
    $authenticationSecurity = APISecurityBestPractices::getAuthenticationSecurityPractices();
    echo "认证安全:\n";
    foreach ($authenticationSecurity as $category => $practices) {
        echo "  $category:\n";
        foreach ($practices as $practice => $description) {
            echo "    - $practice: $description\n";
        }
        echo "\n";
    }
    
    // 授权安全
    $authorizationSecurity = APISecurityBestPractices::getAuthorizationSecurityPractices();
    echo "授权安全:\n";
    foreach ($authorizationSecurity as $category => $practices) {
        echo "  $category:\n";
        foreach ($practices as $practice => $description) {
            echo "    - $practice: $description\n";
        }
        echo "\n";
    }
    
    // 数据安全
    $dataSecurity = APISecurityBestPractices::getDataSecurityPractices();
    echo "数据安全:\n";
    foreach ($dataSecurity as $category => $practices) {
        echo "  $category:\n";
        foreach ($practices as $practice => $description) {
            echo "    - $practice: $description\n";
        }
        echo "\n";
    }
    
    // 网络安全
    $networkSecurity = APISecurityBestPractices::getNetworkSecurityPractices();
    echo "网络安全:\n";
    foreach ($networkSecurity as $category => $practices) {
        echo "  $category:\n";
        foreach ($practices as $practice => $description) {
            echo "    - $practice: $description\n";
        }
        echo "\n";
    }
    
} catch (Exception $e) {
    echo "错误: " . $e->getMessage() . "\n";
}
?>
```

## 🎓 学习建议

### 费曼学习法应用
1. **选择概念**: 选择API安全中的核心概念
2. **简化解释**: 用简单语言解释API安全的重要性
3. **识别盲点**: 发现理解不深入的地方
4. **重新学习**: 针对盲点进行深入学习

### 刻意练习重点
1. **认证机制**: 掌握各种认证机制的实现
2. **授权控制**: 学会实现细粒度授权控制
3. **数据保护**: 理解数据加密和保护方法
4. **安全监控**: 建立完善的安全监控机制

## 🔗 相关链接
- [[01-RESTful API设计|RESTful API设计]]
- [[02-GraphQL API|GraphQL API]]
- [[03-API文档编写|API文档编写]]
- [[04-API版本控制|API版本控制]]
- [[05-微服务架构|微服务架构]]
- [[07-API性能优化|API性能优化]]
