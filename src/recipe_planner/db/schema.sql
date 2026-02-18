-- Recipe Planner Database Schema

CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS recipes (
    id TEXT PRIMARY KEY,
    version INTEGER NOT NULL DEFAULT 1,
    title TEXT NOT NULL,
    cuisine TEXT NOT NULL DEFAULT '',
    ingredients TEXT NOT NULL DEFAULT '[]',       -- JSON array
    instructions TEXT NOT NULL DEFAULT '[]',      -- JSON array
    prep_time TEXT,
    cook_time TEXT,
    tags TEXT NOT NULL DEFAULT '[]',              -- JSON array
    confidence_notes TEXT NOT NULL DEFAULT '[]',  -- JSON array
    date_added TEXT NOT NULL,
    date_modified TEXT NOT NULL,
    last_used_in_meal_plan TEXT,
    times_used INTEGER NOT NULL DEFAULT 0,
    original_values TEXT NOT NULL DEFAULT '{}',   -- JSON object
    edited_fields TEXT NOT NULL DEFAULT '[]',     -- JSON array
    version_history TEXT NOT NULL DEFAULT '[]',   -- JSON array of version entries
    change_highlights TEXT NOT NULL DEFAULT '{}'  -- JSON object
);

CREATE INDEX IF NOT EXISTS idx_recipes_title ON recipes(title);
CREATE INDEX IF NOT EXISTS idx_recipes_cuisine ON recipes(cuisine);
CREATE INDEX IF NOT EXISTS idx_recipes_date_added ON recipes(date_added);

CREATE TABLE IF NOT EXISTS meal_plans (
    id TEXT PRIMARY KEY,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    days TEXT NOT NULL DEFAULT '{}',              -- JSON object
    recipes_used TEXT NOT NULL DEFAULT '[]',      -- JSON array
    metadata TEXT NOT NULL DEFAULT '{}'           -- JSON object
);

CREATE INDEX IF NOT EXISTS idx_meal_plans_dates ON meal_plans(start_date, end_date);

CREATE TABLE IF NOT EXISTS shopping_lists (
    id TEXT PRIMARY KEY,
    meal_plan_id TEXT,
    categories TEXT NOT NULL DEFAULT '{}',        -- JSON object
    raw_items TEXT NOT NULL DEFAULT '[]',         -- JSON array
    metadata TEXT NOT NULL DEFAULT '{}',          -- JSON object
    FOREIGN KEY (meal_plan_id) REFERENCES meal_plans(id)
);
