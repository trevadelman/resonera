# System Architecture Document

## 1. System Overview

### 1.1 Architecture Principles
- Safety-First Design: All components prioritize user safety
- Real-Time Processing: Minimize latency in audio generation and delivery
- Simplicity: Start with minimal components for POC
- Maintainable: Easy to understand and modify
- Upgradeable: Clear path to production architecture

### 1.2 High-Level Architecture

#### Proof of Concept Architecture
```mermaid
graph TB
    Client[Basic Web Client]
    Flask[Flask Server]
    Auth[JWT Auth]
    AudioGen[Audio Generator]
    Safety[Safety Monitor]
    SQLite[(SQLite DB)]
    Files[Local Files]
    
    Client --> Flask
    Flask --> Auth
    Flask --> AudioGen
    AudioGen --> Safety
    Flask --> SQLite
    AudioGen --> Files
```

#### Production Architecture (Future)
```mermaid
graph TB
    Client[Client Applications]
    API[API Gateway]
    Auth[Authentication Service]
    UserMgmt[User Management]
    AudioGen[Audio Generation Engine]
    Safety[Safety Monitor]
    Storage[Audio Storage]
    Analytics[Analytics Engine]
    
    Client --> API
    API --> Auth
    API --> UserMgmt
    API --> AudioGen
    AudioGen --> Safety
    AudioGen --> Storage
    Safety --> Analytics
```

## 2. Component Architecture

### 2.1 Core Services

#### POC Implementation

##### Flask Server
```python
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required

app = Flask(__name__)
jwt = JWTManager(app)

class BasicServer:
    def __init__(self):
        self.audio_gen = AudioGenerator()
        self.safety = SafetyMonitor()
        
    @jwt_required()
    def generate_audio(self):
        """
        Basic audio generation endpoint.
        """
        params = request.get_json()
        audio = self.audio_gen.generate(params)
        if self.safety.validate(audio):
            return jsonify({"status": "success", "file": "audio.wav"})
```

##### Audio Generation Engine
```python
class AudioGenerator:
    """Generates neural entrainment audio using binaural beats and isochronic tones."""
    
    def __init__(self):
        self.sample_rate = 44100
        self.carrier_frequency = 440
        self.transition = FrequencyTransition(sample_rate=self.sample_rate)
        self.harmonic_generator = HarmonicOvertoneGenerator(sample_rate=self.sample_rate)
        
    def generate(self, frequency: float, duration: float,
                volume: float = 0.7, transition_type: str = 'sigmoid') -> str:
        """
        Generate complete neural entrainment audio file.
        
        Args:
            frequency: Target frequency in Hz
            duration: Duration in seconds
            volume: Volume level (0-1)
            transition_type: Type of frequency transition
            
        Returns:
            str: Path to generated audio file
        """
        try:
            # Generate binaural beats with harmonics
            left_channel, right_channel = self.generate_binaural_beat(
                frequency, duration, volume * 0.5
            )
            
            # Generate isochronic tones with harmonics
            isochronic = self.generate_isochronic_tone(
                frequency, duration, volume * 0.5
            )
            
            # Combine and process
            left_channel += isochronic
            right_channel += isochronic
            
            # Apply fades and normalize
            left_channel = self.apply_fade(left_channel)
            right_channel = self.apply_fade(right_channel)
            
            # Save to file
            stereo_audio = np.vstack((left_channel, right_channel)).T
            audio_16bit = (stereo_audio * 32767).astype(np.int16)
            
            temp_file = NamedTemporaryFile(suffix='.wav', delete=False)
            wavfile.write(temp_file.name, self.sample_rate, audio_16bit)
            
            return temp_file.name
            
        except Exception as e:
            self.handle_generation_error(e)
```

##### Safety Monitoring Service
```python
class BasicSafetyMonitor:
    def __init__(self):
        self.frequency_validator = FrequencyValidator()
        self.volume_checker = VolumeChecker()
        
    async def monitor_session(self, session_id: str) -> SafetyStatus:
        """
        Monitor active session safety.
        """
        status = await self.monitors['real_time'].check(session_id)
        if not status.is_safe:
            await self.handle_safety_violation(status)
        return status
```

### 2.2 Supporting Services

##### User Management
```python
class BasicUserManager:
    def __init__(self):
        self.db = SQLiteDatabase('users.db')
        
    def create_user(self, username, password):
        """Simple user creation with password hashing."""
        hashed = self.hash_password(password)
        return self.db.execute(
            'INSERT INTO users (username, password) VALUES (?, ?)',
            (username, hashed)
        )
        
    async def get_user_profile(self, user_id: str) -> UserProfile:
        """
        Retrieve user profile with safety preferences.
        """
        profile = await self.user_store.get_profile(user_id)
        safety_settings = await self.profile_manager.get_safety_settings(user_id)
        return UserProfile(profile, safety_settings)
```

##### Basic Analytics
```python
class BasicAnalytics:
    def __init__(self):
        self.db = SQLiteDatabase('analytics.db')
        
    def log_session(self, user_id, session_data):
        """Simple session logging."""
        return self.db.execute(
            'INSERT INTO sessions (user_id, data) VALUES (?, ?)',
            (user_id, json.dumps(session_data))
        )
        
    async def analyze_session(self, session_data: SessionData) -> Analysis:
        """
        Analyze session effectiveness and safety.
        """
        metrics = await self.metrics_collector.collect(session_data)
        return await self.analysis_engine.analyze(metrics)
```

## 3. Data Flow Architecture

### 3.1 Audio Generation Pipeline

#### POC Pipeline
```mermaid
sequenceDiagram
    participant Client
    participant Flask
    participant AudioGen
    participant Safety
    participant Files
    
    Client->>Flask: Request Audio
    Flask->>Safety: Basic Validation
    Safety-->>Flask: Validation Result
    Flask->>AudioGen: Generate Audio
    AudioGen->>Safety: Safety Check
    Safety-->>AudioGen: Safety Result
    AudioGen->>Files: Save Locally
    Files-->>Flask: File Path
    Flask-->>Client: Audio Response
```

#### Production Pipeline (Future)
```mermaid
sequenceDiagram
    participant Client
    participant API
    participant AudioGen
    participant Safety
    participant Storage
    
    Client->>API: Request Audio
    API->>Safety: Validate Request
    Safety-->>API: Validation Result
    API->>AudioGen: Generate Audio
    AudioGen->>Safety: Safety Check
    Safety-->>AudioGen: Safety Result
    AudioGen->>Storage: Store Audio
    Storage-->>API: Audio URL
    API-->>Client: Audio Response
```

### 3.2 Real-Time Monitoring Flow
```python
class RealTimeMonitor:
    def __init__(self):
        self.active_sessions = {}
        self.safety_thresholds = SafetyThresholds()
        
    async def monitor_metrics(self, session_id: str, metrics: SessionMetrics):
        """
        Monitor real-time session metrics.
        """
        if self.detect_anomaly(metrics):
            await self.trigger_safety_protocol(session_id)
```

## 4. Security Architecture

### 4.1 Authentication Flow
```python
class AuthenticationService:
    def __init__(self):
        self.token_manager = TokenManager()
        self.user_validator = UserValidator()
        
    async def authenticate(self, credentials: Credentials) -> AuthToken:
        """
        Authenticate user and generate session token.
        """
        user = await self.user_validator.validate(credentials)
        return await self.token_manager.generate_token(user)
```

### 4.2 Data Protection
```python
class DataProtectionService:
    def __init__(self):
        self.encryption = EncryptionManager()
        self.access_control = AccessControl()
        
    async def protect_user_data(self, data: UserData) -> ProtectedData:
        """
        Encrypt and protect user data.
        """
        encrypted_data = await self.encryption.encrypt(data)
        return await self.access_control.apply_policies(encrypted_data)
```

## 5. Scalability Architecture

### 5.1 Load Balancing
```python
class LoadBalancer:
    def __init__(self):
        self.service_registry = ServiceRegistry()
        self.health_checker = HealthChecker()
        
    async def route_request(self, request: Request) -> Response:
        """
        Route request to appropriate service instance.
        """
        available_services = await self.health_checker.get_healthy_services()
        selected_service = await self.select_optimal_service(available_services)
        return await self.forward_request(request, selected_service)
```

### 5.2 Caching Strategy
```python
class CacheManager:
    def __init__(self):
        self.audio_cache = AudioCache()
        self.user_cache = UserCache()
        
    async def cache_audio(self, audio_id: str, audio_data: AudioData):
        """
        Cache generated audio for quick retrieval.
        """
        cache_key = self.generate_cache_key(audio_id)
        await self.audio_cache.set(cache_key, audio_data)
```

## 6. Error Handling

### 6.1 Error Recovery
```python
class ErrorRecoveryService:
    def __init__(self):
        self.error_handler = ErrorHandler()
        self.recovery_strategies = RecoveryStrategies()
        
    async def handle_error(self, error: SystemError) -> RecoveryResult:
        """
        Handle system errors and attempt recovery.
        """
        strategy = await self.select_recovery_strategy(error)
        return await strategy.execute()
```

### 6.2 Failover Systems
```python
class FailoverSystem:
    def __init__(self):
        self.health_monitor = HealthMonitor()
        self.backup_systems = BackupSystems()
        
    async def handle_failure(self, service_id: str):
        """
        Handle service failure and activate backup.
        """
        backup_service = await self.backup_systems.activate(service_id)
        await self.health_monitor.verify_backup(backup_service)
```

## 7. Deployment Architecture

### 7.1 Container Organization
```yaml
# docker-compose.yml
version: '3.8'
services:
  api_gateway:
    image: resonera/api_gateway
    ports:
      - "8000:8000"
    
  audio_generator:
    image: resonera/audio_generator
    volumes:
      - audio_data:/data
      
  safety_monitor:
    image: resonera/safety_monitor
    depends_on:
      - audio_generator
      
  analytics:
    image: resonera/analytics
    volumes:
      - analytics_data:/data
```

### 7.2 Scaling Configuration
```python
class ScalingManager:
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.scaling_rules = ScalingRules()
        
    async def adjust_capacity(self, metrics: SystemMetrics):
        """
        Adjust system capacity based on load.
        """
        if await self.needs_scaling(metrics):
            await self.scale_services(metrics)
```

## 8. Monitoring Architecture

### 8.1 System Monitoring
```python
class SystemMonitor:
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.alert_manager = AlertManager()
        
    async def monitor_system_health(self):
        """
        Monitor overall system health.
        """
        metrics = await self.metrics_collector.collect_system_metrics()
        if await self.detect_issues(metrics):
            await self.alert_manager.trigger_alert(metrics)
```

### 8.2 Performance Monitoring
```python
class PerformanceMonitor:
    def __init__(self):
        self.performance_metrics = PerformanceMetrics()
        self.threshold_manager = ThresholdManager()
        
    async def monitor_performance(self):
        """
        Monitor system performance metrics.
        """
        metrics = await self.performance_metrics.collect()
        if await self.threshold_manager.check_thresholds(metrics):
            await self.handle_performance_issue(metrics)
```
