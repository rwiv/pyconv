cd ..
set IMG=dockerpy:latest
set DOCKERFILE=./docker/Dockerfile

docker rmi %IMG%
docker build -t %IMG% -f %DOCKERFILE% .
pause