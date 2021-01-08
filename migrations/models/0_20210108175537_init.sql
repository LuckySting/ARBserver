-- upgrade --
CREATE TABLE IF NOT EXISTS "file" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "path" VARCHAR(1000) NOT NULL
);
COMMENT ON COLUMN "file"."id" IS 'Identifier field';
COMMENT ON COLUMN "file"."created_at" IS 'Datetime of creation of object';
COMMENT ON COLUMN "file"."updated_at" IS 'Datetime of last update of object';
COMMENT ON COLUMN "file"."path" IS 'Path to file';
CREATE TABLE IF NOT EXISTS "restaurant" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(50) NOT NULL,
    "description" TEXT NOT NULL,
    "confirmed" BOOL NOT NULL  DEFAULT False,
    "image_id" INT NOT NULL REFERENCES "file" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "restaurant"."id" IS 'Identifier field';
COMMENT ON COLUMN "restaurant"."created_at" IS 'Datetime of creation of object';
COMMENT ON COLUMN "restaurant"."updated_at" IS 'Datetime of last update of object';
COMMENT ON COLUMN "restaurant"."name" IS 'Name of the restaurant';
COMMENT ON COLUMN "restaurant"."description" IS 'Description of the restaurant';
COMMENT ON COLUMN "restaurant"."confirmed" IS 'Is restaurant is validated by moderator';
COMMENT ON TABLE "restaurant" IS 'Represents restaurant';
CREATE TABLE IF NOT EXISTS "dish" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(200) NOT NULL,
    "price" DOUBLE PRECISION NOT NULL,
    "sale" BOOL NOT NULL  DEFAULT False,
    "sale_price" DOUBLE PRECISION NOT NULL  DEFAULT 0,
    "restaurant_id" INT NOT NULL REFERENCES "restaurant" ("id") ON DELETE CASCADE,
    "image_id" INT NOT NULL REFERENCES "file" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "dish"."id" IS 'Identifier field';
COMMENT ON COLUMN "dish"."created_at" IS 'Datetime of creation of object';
COMMENT ON COLUMN "dish"."updated_at" IS 'Datetime of last update of object';
COMMENT ON COLUMN "dish"."name" IS 'Name of the dish';
COMMENT ON COLUMN "dish"."price" IS 'Price of the dish';
COMMENT ON COLUMN "dish"."sale" IS 'Is on sale';
COMMENT ON COLUMN "dish"."sale_price" IS 'Sale price of the dish';
COMMENT ON TABLE "dish" IS 'Represents dish';
CREATE TABLE IF NOT EXISTS "place" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "address" VARCHAR(300) NOT NULL,
    "longitude" DOUBLE PRECISION NOT NULL,
    "latitude" DOUBLE PRECISION NOT NULL,
    "work_time" VARCHAR(100) NOT NULL,
    "preorder" BOOL NOT NULL  DEFAULT False,
    "restaurant_id" INT NOT NULL REFERENCES "restaurant" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "place"."id" IS 'Identifier field';
COMMENT ON COLUMN "place"."created_at" IS 'Datetime of creation of object';
COMMENT ON COLUMN "place"."updated_at" IS 'Datetime of last update of object';
COMMENT ON COLUMN "place"."address" IS 'Address of the place';
COMMENT ON COLUMN "place"."longitude" IS 'Longitude of the place';
COMMENT ON COLUMN "place"."latitude" IS 'Latitude of the place';
COMMENT ON COLUMN "place"."work_time" IS 'Place work time';
COMMENT ON COLUMN "place"."preorder" IS 'Preorder is allowed';
COMMENT ON TABLE "place" IS 'Represents place';
CREATE TABLE IF NOT EXISTS "placegallery" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "place_id" INT NOT NULL REFERENCES "place" ("id") ON DELETE CASCADE,
    "file_id" INT NOT NULL REFERENCES "file" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "table" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(200) NOT NULL,
    "available" BOOL NOT NULL  DEFAULT True,
    "capacity" INT NOT NULL,
    "smoking" BOOL NOT NULL  DEFAULT False,
    "description" VARCHAR(1000) NOT NULL  DEFAULT '',
    "place_id" INT NOT NULL REFERENCES "place" ("id") ON DELETE CASCADE,
    "image_id" INT NOT NULL REFERENCES "file" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "table"."id" IS 'Identifier field';
COMMENT ON COLUMN "table"."created_at" IS 'Datetime of creation of object';
COMMENT ON COLUMN "table"."updated_at" IS 'Datetime of last update of object';
COMMENT ON TABLE "table" IS 'Represents table';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" TEXT NOT NULL
);
