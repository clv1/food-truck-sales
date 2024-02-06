SET search_path = kevin_schema;

DROP TABLE IF EXISTS DIM_trucks CASCADE;
DROP TABLE IF EXISTS DIM_payments CASCADE;
DROP TABLE IF EXISTS FACT_transaction CASCADE;


CREATE TABLE IF NOT EXISTS DIM_trucks (
    truck_id INT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    has_card_reader BOOLEAN NOT NULL,
    fsa_rating_22 INT NOT NULL,
    PRIMARY KEY (truck_id),
    UNIQUE (name, description)
);

CREATE TABLE IF NOT EXISTS DIM_payment_type (
    payment_type_id INT GENERATED ALWAYS AS IDENTITY,
    payment_type VARCHAR(255) NOT NULL,
    PRIMARY KEY (payment_type_id),
    UNIQUE (payment_type)
);

CREATE TABLE IF NOT EXISTS FACT_transactions (
    transaction_id INT GENERATED ALWAYS AS IDENTITY,
    truck_id INT NOT NULL,
    time_stamp TIMESTAMP NOT NULL,
    payment_type_id INT NOT NULL,
    total DECIMAL(5,2) NOT NULL,
    PRIMARY KEY (transaction_id),
    FOREIGN KEY (truck_id) REFERENCES DIM_trucks(truck_id),
    FOREIGN KEY (payment_type_id) REFERENCES DIM_payment_type(payment_type_id)
);

--- seeding basic data ---

INSERT INTO DIM_trucks 
        (name, description, has_card_reader, fsa_rating_22)
    VALUES 
        ('Burrito Madness', 'An authentic taste of Mexico.', TRUE, 4),
        ('Kings of Kebabs', 'Locally-sourced meat cooked over a charcoal grill.', TRUE, 2),
        ('Cupcakes by Michelle', 'Handcrafted cupcakes made with high-quality, organic ingredients.', TRUE, 5),
        ('Hartmann''s Jellied Eels', 'A taste of history with this classic English dish.', TRUE, 4),
        ('Yoghurt Heaven', 'All the great tastes, but only some of the calories!', TRUE, 4),
        ('SuperSmoothie', 'Pick any fruit or vegetable, and we''ll make you a delicious, healthy, multi-vitamin shake. Live well; live wild.', FALSE, 3);


INSERT INTO DIM_payment_type 
        (payment_type)
    VALUES 
        ('card'),
        ('cash'),
        ('crypto');



-- --- sample data and commands --

-- -- Insert additional sample transactions
-- INSERT INTO FACT_transactions (truck_id, time_stamp, payment_type_id, total)
-- VALUES 
--     (2, '2023-11-21 13:45:00', 2, 20.50),
--     (3, '2023-11-22 09:15:00', 1, 10.75),
--     (1, '2023-11-22 14:30:00', 3, 25.00),
--     (4, '2023-11-23 11:00:00', 1, 18.99),
--     (5, '2023-11-23 17:45:00', 2, 12.25);

-- -- Select transactions
-- SELECT * FROM FACT_transactions;

-- -- Delete a specific transaction
-- DELETE FROM FACT_transactions WHERE transaction_id = 1;

-- -- Delete all transactions 
-- DELETE FROM FACT_transactions;
