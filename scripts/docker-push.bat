cd ..
set IMG1=dockerpy:0.1.0
set IMG2=ghcr.io/rwiv/dockerpy:0.1.0
set DOCKERFILE=./Dockerfile

docker rmi %IMG1%
docker rmi %IMG2%

docker build -t %IMG1% -f %DOCKERFILE% .

docker tag %IMG1% %IMG2%
docker push %IMG2%

docker rmi %IMG1%
docker rmi %IMG2%
pause