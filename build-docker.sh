docker build -f Dockerfile -t upyun-logger/latest .
docker run --name=UPYUN-Logger \
           --mount type=bind,source="$(pwd)"/data,target=/app/data \
           --mount type=bind,source="$(pwd)"/config.json,target=/app/config.json \
           --restart always upyun-logger/latest
