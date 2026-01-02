-- Supabase Database Setup Script
-- Run this in your Supabase SQL Editor

-- Create messages table
CREATE TABLE IF NOT EXISTS messages (
    id BIGSERIAL PRIMARY KEY,
    data JSONB NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    phone VARCHAR(20) UNIQUE NOT NULL,
    parent_name VARCHAR(255) NOT NULL,
    child_name VARCHAR(255) NOT NULL,
    wishlist JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index on phone for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_phone ON users(phone);

-- Create index on timestamp for messages
CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp);

-- Create menu_items table
CREATE TABLE IF NOT EXISTS menu_items (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index on display_order for sorting
CREATE INDEX IF NOT EXISTS idx_menu_items_display_order ON menu_items(display_order);

-- Insert default menu items
INSERT INTO menu_items (id, title, display_order) VALUES
    ('ADD', '➕ Add to Wishlist', 1),
    ('VIEW', '📄 View Wishlist', 2),
    ('REMOVE', '❌ Remove from Wishlist', 3)
ON CONFLICT (id) DO NOTHING;

-- Create primary_input_field table
CREATE TABLE IF NOT EXISTS primary_input_field (
    no INTEGER PRIMARY KEY,
    field_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Insert sample data
INSERT INTO primary_input_field (no, field_name, created_at) VALUES
    (1, 'parent_01', NOW()),
    (2, 'child_01', NOW()),
    (3, 'child_02', NOW())
ON CONFLICT (no) DO NOTHING;

-- Enable Row Level Security (RLS) - Optional
-- ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE users ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE menu_items ENABLE ROW LEVEL SECURITY;

-- Create policies if using RLS (adjust as needed)
-- Policy to allow all operations (for API key access)
-- CREATE POLICY "Allow all operations" ON messages FOR ALL USING (true);
-- CREATE POLICY "Allow all operations" ON users FOR ALL USING (true);
-- CREATE POLICY "Allow all operations" ON menu_items FOR ALL USING (true);

