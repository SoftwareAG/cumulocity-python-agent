docker-compose up -d --scale agent=$1
echo "ID"
docker stats --no-stream --format "{{.Container}}"
