# Database Schema and Data Architecture

## Implementation Stages

### Proof of Concept (SQLite)
```sql
-- Basic user management
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    account_status TEXT DEFAULT 'active'
);

-- Essential user preferences
CREATE TABLE user_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    voice_preference TEXT,  -- 'male', 'female', 'neutral'
    background_sound TEXT,  -- 'nature', 'white_noise', 'ambient'
    session_duration INTEGER,  -- in minutes
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Basic session tracking
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    session_type TEXT,  -- 'morning', 'evening'
    frequency REAL,
    effectiveness INTEGER CHECK (effectiveness BETWEEN 1 AND 5),
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Simple feedback storage
CREATE TABLE session_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    feedback_text TEXT,
    FOREIGN KEY(session_id) REFERENCES sessions(id)
);
```

### Migration to Production
When ready to scale, migrate to PostgreSQL with full features:

## Production Tables (PostgreSQL)

### Users
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE,
    account_status VARCHAR(20) DEFAULT 'active',
    subscription_tier VARCHAR(20) DEFAULT 'free'
);

-- Index for quick user lookups
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_phone ON users(phone_number);
```

### Neural Profiles
```sql
CREATE TABLE neural_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    base_frequency_response JSONB,  -- Stores frequency sensitivity data
    optimal_transition_time INTEGER,  -- In seconds
    contraindications TEXT[],  -- Array of medical conditions
    sensitivity_level INTEGER CHECK (sensitivity_level BETWEEN 1 AND 10),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Preferred ranges for different states
    alpha_range NUMRANGE,  -- e.g., [8.0, 12.0]
    theta_range NUMRANGE,
    delta_range NUMRANGE,
    gamma_range NUMRANGE,
    
    CONSTRAINT fk_user
        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);
```

### Sessions
```sql
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    start_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP WITH TIME ZONE,
    session_type VARCHAR(50),  -- 'morning', 'evening', 'custom'
    initial_state VARCHAR(20),
    target_state VARCHAR(20),
    effectiveness_rating INTEGER CHECK (effectiveness_rating BETWEEN 1 AND 10),
    side_effects JSONB,
    
    -- Session configuration
    base_frequency NUMERIC(7,2),
    target_frequency NUMERIC(7,2),
    volume_level INTEGER CHECK (volume_level BETWEEN 0 AND 100),
    
    CONSTRAINT fk_user
        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_start_time ON sessions(start_time);
```

### Audio Files
```sql
CREATE TABLE audio_files (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES sessions(id),
    file_path VARCHAR(255) NOT NULL,
    duration INTEGER NOT NULL,  -- In seconds
    format VARCHAR(10),
    size_bytes BIGINT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Audio specifications
    sample_rate INTEGER DEFAULT 44100,
    bit_depth INTEGER DEFAULT 24,
    channels INTEGER DEFAULT 2,
    
    -- Frequency data
    frequency_data JSONB,  -- Stores frequency analysis results
    
    CONSTRAINT fk_session
        FOREIGN KEY(session_id)
        REFERENCES sessions(id)
        ON DELETE CASCADE
);
```

### User Preferences
```sql
CREATE TABLE user_preferences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    voice_preference VARCHAR(20),  -- 'male', 'female', 'neutral'
    background_sound_type VARCHAR(50),  -- 'nature', 'white_noise', 'ambient'
    preferred_duration INTEGER,  -- session length in minutes
    notification_preferences JSONB,  -- stores complex notification settings
    morning_routine_time TIME,
    evening_routine_time TIME,
    
    CONSTRAINT fk_user
        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);
```

### Progress Tracking
```sql
CREATE TABLE progress_tracking (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    date DATE DEFAULT CURRENT_DATE,
    metrics JSONB,  -- Stores various progress metrics
    notes TEXT,
    sleep_quality INTEGER CHECK (sleep_quality BETWEEN 1 AND 10),
    stress_level INTEGER CHECK (stress_level BETWEEN 1 AND 10),
    focus_score INTEGER CHECK (focus_score BETWEEN 1 AND 10),
    
    CONSTRAINT fk_user
        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE INDEX idx_progress_user_date ON progress_tracking(user_id, date);
```

## Junction Tables

### Session_Feedback
```sql
CREATE TABLE session_feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES sessions(id),
    user_id UUID REFERENCES users(id),
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    feedback_text TEXT,
    physical_effects JSONB,
    mental_effects JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_session
        FOREIGN KEY(session_id)
        REFERENCES sessions(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_user
        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);
```

## Views

### User_Progress_Summary
```sql
CREATE VIEW user_progress_summary AS
SELECT 
    u.id as user_id,
    u.email,
    COUNT(s.id) as total_sessions,
    AVG(s.effectiveness_rating) as avg_effectiveness,
    AVG(pt.sleep_quality) as avg_sleep_quality,
    AVG(pt.focus_score) as avg_focus_score
FROM users u
LEFT JOIN sessions s ON u.id = s.user_id
LEFT JOIN progress_tracking pt ON u.id = pt.user_id
GROUP BY u.id, u.email;
```

### Recent_Session_Analysis
```sql
CREATE VIEW recent_session_analysis AS
SELECT 
    s.user_id,
    s.session_type,
    s.effectiveness_rating,
    sf.physical_effects,
    sf.mental_effects,
    s.start_time,
    s.end_time,
    af.duration
FROM sessions s
JOIN session_feedback sf ON s.id = sf.session_id
JOIN audio_files af ON s.id = af.session_id
WHERE s.start_time > CURRENT_DATE - INTERVAL '30 days'
ORDER BY s.start_time DESC;
```

## Functions

### Update User Neural Profile
```sql
CREATE OR REPLACE FUNCTION update_neural_profile()
RETURNS TRIGGER AS $$
BEGIN
    -- Update neural profile based on session feedback
    -- Implementation here
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_session_feedback
    AFTER INSERT ON session_feedback
    FOR EACH ROW
    EXECUTE FUNCTION update_neural_profile();
```

## Indexes and Optimizations

### Performance Indexes
```sql
-- Frequently accessed user data
CREATE INDEX idx_users_subscription ON users(subscription_tier);

-- Session analysis
CREATE INDEX idx_sessions_effectiveness ON sessions(effectiveness_rating);
CREATE INDEX idx_sessions_type_time ON sessions(session_type, start_time);

-- Progress tracking
CREATE INDEX idx_progress_metrics ON progress_tracking USING GIN (metrics);
```

### Partitioning Strategy
```sql
-- Partition sessions table by month
CREATE TABLE sessions_partition OF sessions
PARTITION BY RANGE (start_time);

-- Create monthly partitions
CREATE TABLE sessions_y2024m01 PARTITION OF sessions_partition
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

## Data Retention Policy
```sql
-- Automated cleanup of old sessions
CREATE OR REPLACE FUNCTION cleanup_old_sessions()
RETURNS void AS $$
BEGIN
    DELETE FROM sessions 
    WHERE start_time < CURRENT_DATE - INTERVAL '1 year'
    AND user_id NOT IN (
        SELECT id FROM users 
        WHERE subscription_tier = 'premium'
    );
END;
$$ LANGUAGE plpgsql;
```

## Security Considerations
- All sensitive data is encrypted at rest
- Passwords are hashed using Argon2
- Regular security audits
- Compliance with GDPR and HIPAA requirements
