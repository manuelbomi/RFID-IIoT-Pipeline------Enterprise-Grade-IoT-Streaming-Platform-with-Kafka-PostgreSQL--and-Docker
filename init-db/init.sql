-- Create temperature reads table
CREATE TABLE IF NOT EXISTS temperature_reads (
    id BIGSERIAL PRIMARY KEY,
    event TEXT NOT NULL,
    epc TEXT NOT NULL,
    temperature DECIMAL(5,2) NOT NULL,
    unit TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create price lookups table
CREATE TABLE IF NOT EXISTS price_lookups (
    id BIGSERIAL PRIMARY KEY,
    event TEXT NOT NULL,
    epc TEXT NOT NULL,
    item_name TEXT NOT NULL,
    sku TEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    currency TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_temperature_epc ON temperature_reads (epc);
CREATE INDEX IF NOT EXISTS idx_temperature_timestamp ON temperature_reads (timestamp);
CREATE INDEX IF NOT EXISTS idx_temperature_created ON temperature_reads (created_at);

CREATE INDEX IF NOT EXISTS idx_price_epc ON price_lookups (epc);
CREATE INDEX IF NOT EXISTS idx_price_timestamp ON price_lookups (timestamp);
CREATE INDEX IF NOT EXISTS idx_price_sku ON price_lookups (sku);
CREATE INDEX IF NOT EXISTS idx_price_created ON price_lookups (created_at);

-- Create hypertables for TimescaleDB (if using TimescaleDB extension)
-- CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
-- SELECT create_hypertable('temperature_reads', 'timestamp');
-- SELECT create_hypertable('price_lookups', 'timestamp');