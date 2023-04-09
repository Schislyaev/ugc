#!/bin/bash

set -e

clickhouse client -n <<-EOSQL

  CREATE DATABASE IF NOT EXISTS $CH_DB;
  CREATE TABLE IF NOT EXISTS $CH_DB.$CH_TABLE (user_id UUID, movie_id UUID, event_time DateTime64) ENGINE = MergeTree() ORDER BY user_id;

EOSQL