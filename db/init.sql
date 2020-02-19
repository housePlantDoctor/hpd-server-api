CREATE DATABASE plants_db;
use plants_db;

CREATE TABLE plants (
  plant_id MEDIUMINT NOT NULL AUTO_INCREMENT,
  plant_name VARCHAR(30),
  plant_information VARCHAR(500),
  PRIMARY KEY (plant_id)
);

CREATE TABLE diseases (
  disease_id MEDIUMINT NOT NULL AUTO_INCREMENT,
  disease_name VARCHAR(30),
  plant_name VARCHAR(30),
  disease_symptoms VARCHAR(500),
  disease_treatment VARCHAR(500),
  PRIMARY KEY (disease_id)
);

CREATE TABLE results (
  result_id MEDIUMINT NOT NULL AUTO_INCREMENT,
  plant_name VARCHAR(30),
  disease_name VARCHAR(30),
  file_name VARCHAR(30),
  PRIMARY KEY (result_id)
);

INSERT INTO plants (plant_name, plant_information) VALUES ("hello", "world" )
