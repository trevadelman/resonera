# Resonera API Documentation

## Overview
The Resonera API provides programmatic access to neural entrainment audio generation, user management, and session tracking. This RESTful API uses JSON for request and response payloads and JWT for authentication.

### Implementation Stages

#### Proof of Concept
- Simple Flask-based API
- Basic JWT authentication
- Local file storage
- SQLite database
- Core functionality only

#### Production (Future)
- Full FastAPI implementation
- Advanced authentication
- Cloud storage integration
- PostgreSQL database
- Extended feature set

## Base URL
```
POC: http://localhost:5000/api
Production (Future): https://api.resonera.com/v1
```

## Authentication
### POC Authentication
Basic JWT authentication:
```http
Authorization: Bearer <token>
```

### Production Authentication (Future)
- Enhanced JWT with refresh tokens
- Rate limiting:
  - Free tier: 60 requests per hour
  - Premium tier: 1000 requests per hour
- Advanced monitoring and security

## Endpoints

### Authentication

#### POC: Register User
```http
POST /auth/register
Content-Type: application/json

Request:
{
    "email": "user@example.com",
    "password": "securePassword123"
}

Response: 201 Created
{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "expires_in": 3600
}

Error Response: 400 Bad Request
{
    "error": "validation_error",
    "message": "Invalid email format",
    "fields": {
        "email": "Must be a valid email address"
    }
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

Request:
{
    "email": "user@example.com",
    "password": "securePassword123"
}

Response: 200 OK
{
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "expires_in": 3600,
    "user": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "user@example.com",
        "subscription_tier": "premium"
    }
}

Error Response: 401 Unauthorized
{
    "error": "authentication_failed",
    "message": "Invalid credentials"
}
```

### User Preferences

#### POC: Set User Preferences
```http
POST /preferences
Content-Type: application/json
Authorization: Bearer <token>

Request:
{
    "voice_preference": "female",
    "background_sound": "nature",
    "session_duration": 300
}

Response: 201 Created
{
    "profile_id": "550e8400-e29b-41d4-a716-446655440000",
    "created_at": "2024-01-27T10:30:00Z",
    "status": "active"
}
```

### Audio Generation

#### POC: Generate Basic Audio
```http
POST /audio/generate
Content-Type: application/json
Authorization: Bearer <token>

Request:
{
    "session_type": "relaxation",
    "target_frequency": 10,  # Alpha state
    "duration": 300,
    "background": "nature"
}

Response: 202 Accepted
{
    "audio_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "processing",
    "estimated_completion": "2024-01-27T10:35:00Z",
    "status_url": "/audio/550e8400-e29b-41d4-a716-446655440000/status"
}
```

#### Check Audio Generation Status
```http
GET /audio/{audio_id}/status
Authorization: Bearer <token>

Response: 200 OK
{
    "status": "completed",
    "download_url": "https://storage.resonera.com/audio/{file_id}",
    "duration": 1200,
    "format": "mp3",
    "size_bytes": 15000000,
    "frequency_data": {
        "base": 200,
        "target": 10,
        "transition_points": [
            {
                "time": 0,
                "frequency": 8
            },
            {
                "time": 300,
                "frequency": 10
            }
        ]
    }
}
```

### Session Management

#### POC: Create Session
```http
POST /sessions
Content-Type: application/json
Authorization: Bearer <token>

Request:
{
    "session_type": "morning",
    "duration": 300,
    "target_state": "alpha"
}

Response: 201 Created
{
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "audio_url": "https://storage.resonera.com/audio/{file_id}",
    "duration": 1200,
    "start_time": "2024-01-27T10:30:00Z"
}
```

#### POC: Record Session Feedback
```http
POST /sessions/{session_id}/feedback
Content-Type: application/json
Authorization: Bearer <token>

Request:
{
    "rating": 4,  # 1-5 scale
    "effectiveness": 4,  # 1-5 scale
    "notes": "Felt relaxed after the session"
}

Response: 200 OK
{
    "feedback_id": "550e8400-e29b-41d4-a716-446655440000",
    "received_at": "2024-01-27T11:30:00Z",
    "status": "processed",
    "next_session_adjustments": {
        "frequency_adjustment": -0.5,
        "transition_time_adjustment": 30
    }
}
```

## Error Handling

### Error Response Format
```json
{
    "error": "error_code",
    "message": "Human-readable error message",
    "details": {
        "field": "Additional error context"
    }
}
```

### Common Error Codes
- `validation_error`: Invalid request parameters
- `authentication_error`: Invalid or missing authentication
- `rate_limit_exceeded`: Too many requests
- `resource_not_found`: Requested resource doesn't exist
- `processing_error`: Audio generation failed
- `storage_error`: File storage/retrieval error

## Future Enhancements

### Production Features
- WebSocket support for real-time monitoring
- Advanced neural profile management
- Complex audio generation options
- Detailed session analytics
- Enhanced error handling and monitoring

## Appendix

### Frequency Ranges
- Delta: 0.5-4 Hz
- Theta: 4-8 Hz
- Alpha: 8-14 Hz
- Beta: 14-30 Hz
- Gamma: 30-100 Hz

### Safety Limits
- Maximum volume: 85 dB
- Maximum frequency transition rate: 2 Hz/second
- Minimum session duration: 60 seconds
- Maximum session duration: 7200 seconds
