-- NEEL Unified Activity & Behavior Schema

-- 1. USER (IDENTITY)
CREATE TABLE IF NOT EXISTS "user" (
    user_id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    timezone VARCHAR(50)
);

-- 2. USER_PROFILE (GOALS & DIRECTION)
CREATE TABLE IF NOT EXISTS user_profile (
    user_id INTEGER PRIMARY KEY REFERENCES "user"(user_id) ON DELETE CASCADE,
    primary_goal VARCHAR(255) NOT NULL,
    secondary_goals JSONB,
    focus_areas JSONB,
    priority_order JSONB,
    time_horizon VARCHAR(50),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. ACTIVITY (TYPES)
CREATE TABLE IF NOT EXISTS activity (
    activity_id SERIAL PRIMARY KEY,
    activity_name VARCHAR(255) UNIQUE NOT NULL,
    activity_category VARCHAR(50) NOT NULL -- Academic, Work, Health, Leisure, Personal
);

-- 4. ACTIVITY_LOG (DAILY LIFE)
CREATE TABLE IF NOT EXISTS activity_log (
    log_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(user_id) ON DELETE CASCADE,
    activity_id INTEGER NOT NULL REFERENCES activity(activity_id),
    date DATE NOT NULL,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    duration_minutes INTEGER,
    planned BOOLEAN DEFAULT FALSE,
    completed BOOLEAN DEFAULT FALSE,
    postponed BOOLEAN DEFAULT FALSE,
    energy_level INTEGER,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. OUTCOME (RESULTS)
CREATE TABLE IF NOT EXISTS outcome (
    outcome_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(user_id) ON DELETE CASCADE,
    date DATE NOT NULL,
    outcome_type VARCHAR(50) NOT NULL, -- exam_score, productivity_rating, etc.
    outcome_value TEXT,
    related_activity_id INTEGER REFERENCES activity(activity_id)
);

-- 6. ANALYTICS_SUMMARY (POST-PROCESSED)
CREATE TABLE IF NOT EXISTS analytics_summary (
    summary_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(user_id) ON DELETE CASCADE,
    period_type VARCHAR(20) NOT NULL, -- daily, weekly, monthly
    period_start TIMESTAMP NOT NULL,
    period_end TIMESTAMP NOT NULL,
    focus_distribution JSONB,
    activity_balance JSONB,
    goal_alignment TEXT,
    key_insight TEXT,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_activity_log_user_date ON activity_log(user_id, date);
CREATE INDEX IF NOT EXISTS idx_outcome_user_date ON outcome(user_id, date);
CREATE INDEX IF NOT EXISTS idx_analytics_summary_user_period ON analytics_summary(user_id, period_type);