# Resonera API Documentation

## Overview
The resonera API provides programmatic access to neural entrainment audio generation, user management, and session tracking. This RESTful API uses JSON for request and response payloads and JWT for authentication.

## Base URL
```
Production: https://api.resonera.com/v1
Development: http://localhost:8000/v1
```

## Authentication
All API requests must include a JWT token in the header:
```http
Authorization: Bearer <token>
```

## Rate Limiting
- Free tier: 60 requests per hour
- Premium tier: 1000 requests per hour
- Headers included in response:
  - X-RateLimit-Limit
  - X-RateLimit-Remaining
  - X-RateLimit-Reset

## Endpoints

### Authentication

#### Register New User
```http
POST /auth/register
Content-Type: application/json

Request:
{
    "email": "user@example.com",
    "phone_number": "+1234567890",
    "password": "securePassword123",
    "time_zone": "America/New_York"
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

### Neural Profile Management

#### Create Neural Profile
```http
POST /profiles
Content-Type: application/json
Authorization: Bearer <token>

Request:
{
    "sensitivity_level": 7,
    "contraindications": ["epilepsy", "migraines"],
    "preferred_states": {
        "alpha": {
            "min": 8.0,
            "max": 12.0
        },
        "theta": {
            "min": 4.0,
            "max": 8.0
        }
    },
    "optimal_transition_time": 300
}

Response: 201 Created
{
    "profile_id": "550e8400-e29b-41d4-a716-446655440000",
    "created_at": "2024-01-27T10:30:00Z",
    "status": "active"
}
```

### Audio Generation

#### Generate Entrainment Audio
```http
POST /audio/generate
Content-Type: application/json
Authorization: Bearer <token>

Request:
{
    "session_type": "meditation",
    "base_frequency": 200,
    "target_frequency": 10,
    "duration": 1200,
    "transitions": [
        {
            "time": 0,
            "frequency": 8,
            "duration": 300
        },
        {
            "time": 300,
            "frequency": 10,
            "duration": 600
        }
    ],
    "background": {
        "type": "nature",
        "volume": 0.3
    },
    "voice": {
        "type": "female",
        "script_id": "meditation_basic_01"
    }
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

#### Create Session
```http
POST /sessions
Content-Type: application/json
Authorization: Bearer <token>

Request:
{
    "session_type": "morning",
    "target_state": "alpha",
    "duration": 1200,
    "preferences": {
        "voice_type": "female",
        "background": "nature",
        "volume": 75
    }
}

Response: 201 Created
{
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "audio_url": "https://storage.resonera.com/audio/{file_id}",
    "duration": 1200,
    "start_time": "2024-01-27T10:30:00Z"
}
```

#### Record Session Feedback
```http
POST /sessions/{session_id}/feedback
Content-Type: application/json
Authorization: Bearer <token>

Request:
{
    "rating": 4,
    "physical_effects": {
        "relaxation": 8,
        "drowsiness": 3
    },
    "mental_effects": {
        "clarity": 7,
        "focus": 8
    },
    "notes": "Felt very relaxed and focused after the session"
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

## WebSocket API

### Real-time Session Monitoring
```javascript
// Connect to WebSocket
ws://api.resonera.com/v1/sessions/{session_id}/monitor

// Message Format
{
    "type": "brainwave_data",
    "timestamp": "2024-01-27T10:30:00Z",
    "data": {
        "current_frequency": 10.2,
        "target_frequency": 10.0,
        "coherence_level": 0.95
    }
}
```

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