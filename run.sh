#!/bin/bash
# 啟動 Docker container 並執行資料庫建構主程式

set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 建立 docker network（若不存在）
docker network create db_network 2>/dev/null || true

# 啟動 MySQL DB Server
docker compose -f "${SCRIPT_DIR}/docker/TwDatabase.yaml" up -d

# 等待 MySQL healthcheck 通過
echo "等待 MySQL 啟動..."
until docker inspect --format='{{.State.Health.Status}}' tw_stock_database 2>/dev/null | grep -q "healthy"; do
  sleep 5
done
echo "MySQL 已就緒"

# 執行 DBmaker 建立資料庫
docker run --rm --network db_network nk7260ynpa/dbmaker:1.0.0
