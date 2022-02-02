#!/bin/bash

sudo -u postgres psql postgres;

#create database
sudo -u postgres bash -c "psql -c\"CREATE DATABASE weatherbot-dev;\""

#create user 
sudo -u postgres bash -c "psql -c \"CREATE USER weather_admin WITH PASSWORD 'weather?';\""
sudo -u postgres bash -c "psql -c \"ALTER ROLE weather_admin set client_encoding to 'utf8';\""
#sudo -u postgres bash -c "psql -c \"ALTER ROLE weather_admin set default_transaction_isolation to 'read committed';\""

sudo -u postgres bash -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE weatherbot-dev to weather_admin;\""

