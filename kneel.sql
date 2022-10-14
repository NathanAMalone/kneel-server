CREATE TABLE `Metals`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `metal` NVARCHAR(160) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

CREATE TABLE `Orders`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `metal_id` INTEGER NOT NULL,
    `size_id` INTEGER NOT NULL,
    `style_id` INTEGER NOT NULL,
    `timestamp` NUMERIC(50) NOT NULL,
    FOREIGN KEY(`metal_id`) REFERENCES `Metals` (`id`),
    FOREIGN KEY(`size_id`) REFERENCES `Sizes` (`id`),
    FOREIGN KEY(`style_id`) REFERENCES `Styles` (`id`)
);


CREATE TABLE `Sizes`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `carets` NUMERIC(3,2) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

CREATE TABLE `Styles`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `style` NVARCHAR(160) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

DROP TABLE `Styles`

INSERT INTO `Metals` VALUES (null, 'Sterling Silver', 12.42);
INSERT INTO `Metals` VALUES (null, '14k Gold', 736.4);
INSERT INTO `Metals` VALUES (null, '24k Gold', 1258.9);
INSERT INTO `Metals` VALUES (null, 'Platinum', 795.45);
INSERT INTO `Metals` VALUES (null, 'Palladium', 1241.0);

INSERT INTO `Orders` VALUES (null, 3, 2, 3, 1614659931693);
INSERT INTO `Orders` VALUES (null, 2, 5, 2, 1614659931793);
INSERT INTO `Orders` VALUES (null, 1, 4, 1, 1614659931993);
INSERT INTO `Orders` VALUES (null, 4, 1, 3, 1614659932693);

INSERT INTO `SIZES` VALUES (null, 0.5, 405);
INSERT INTO `SIZES` VALUES (null, 0.75, 782);
INSERT INTO `SIZES` VALUES (null, 1, 1470);
INSERT INTO `SIZES` VALUES (null, 1.5, 1997);
INSERT INTO `SIZES` VALUES (null, 2, 3638);

INSERT INTO `STYLES` VALUES (null, 'Classic', 500);
INSERT INTO `STYLES` VALUES (null, 'Modern', 710);
INSERT INTO `STYLES` VALUES (null, 'Vintage', 965);

SELECT * FROM Orders

SELECT
    o.id,
    o.metal_id,
    o.size_id,
    o.style_id,
    o.timestamp
FROM Orders o

SELECT
    o.id,
    o.metal_id,
    o.size_id,
    o.style_id,
    o.timestamp
FROM Orders o
WHERE o.id = 2

SELECT * FROM Styles

SELECT
    o.timestamp,
    o.size_id,
    o.style_id,
    o.metal_id,
    m.metal metals_metal,
    m.price metals_price,
    st.style styles_style,
    st.price styles_price,
    si.carets sizes_carets,
    si.price sizes_price
FROM `Orders` o
JOIN Metals m ON m.id = o.metal_id
JOIN Styles st ON st.id = o.style_id
JOIN Sizes si ON si.id = o.size_id