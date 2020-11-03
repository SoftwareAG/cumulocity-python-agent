docker-compose up -d --scale agent=$1
docker stats --no-stream --format "{{.Container}}"
