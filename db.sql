CREATE TABLE product (
    product_id int AUTO_INCREMENT PRIMARY KEY,
    name varchar(64) NOT NULL,
    price decimal(10, 2) NOT NULL,
    additional_info JSON
