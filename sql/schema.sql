-- Tabla dimensión listings (dim_listings)
CREATE TABLE IF NOT EXISTS dim_listings (
    id BIGINT NOT NULL,
    name VARCHAR(255),
    host_id BIGINT,
    host_name VARCHAR(255),     
    neighbourhood VARCHAR(255),
    room_type VARCHAR(50),           -- Agregado para análisis por tipo de habitación
    price DECIMAL(10,2),
    price_tier ENUM('low', 'medium', 'high'),
    calculated_host_listings_count INT,
    start_date DATE NOT NULL,
    end_date DATE DEFAULT NULL,
    current_flag BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id, start_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Tabla hechos reviews (fact_reviews)
CREATE TABLE IF NOT EXISTS fact_reviews (
    review_id BIGINT NOT NULL PRIMARY KEY,
    listing_id BIGINT NOT NULL,
    date DATE,
    rating DECIMAL(2,1),             -- Agregado para métricas de calificación
    response_time TIME,              -- Agregado para métricas de respuesta
    is_recent BOOLEAN,
    FOREIGN KEY (listing_id) REFERENCES dim_listings(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
