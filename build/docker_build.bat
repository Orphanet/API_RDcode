set "ver=0.0.1";

rem Build with:
docker build -t api_rdcode:%ver% . --label api_rdcode:%ver%

rem Export with:
docker save api_rdcode:%ver% -o ./api_rdcode_%ver%

rem Load with:
echo docker load -i {path}\api_rdcode_%ver%

rem Run with:
echo docker run -p 8080:8080 --name api_rdcode_%ver% api_rdcode:%ver%