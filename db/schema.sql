-- ============================================
-- NEEL Database Schema (v1)
-- ============================================

-- Safety: use explicit schema
CREATE SCHEMA IF NOT EXISTS neel;
SET search_path TO neel;

-- ============================================
-- 1. USERS TABLE
-- Stores stable user identity & goals
-- ============================================

CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,

    education TEXT,
    primary_goal TEXT,
    priority TEXT,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 2. SESSIONS TABLE
-- Each invocation of NEEL = one session
-- ============================================

CREATE TABLE IF NOT EXISTS sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,

    supervisor_confidence TEXT CHECK (
        supervisor_confidence IN ('LOW', 'MEDIUM', 'HIGH')
    ),

    supervisor_status TEXT CHECK (
        supervisor_status IN ('ALLOW', 'BLOCK')
    ),

    reflection_decision TEXT CHECK (
        reflection_decision IN ('PASS', 'SOFTEN', 'REJECT')
    ),

    final_response TEXT,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 3. MEMORY SNAPSHOTS TABLE
-- Stores summarized, reflective memory
-- ============================================

CREATE TABLE IF NOT EXISTS memory_snapshots (
    memory_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,

    short_term_summary JSONB,
    reflective_summary TEXT,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- END OF SCHEMA
-- ============================================
