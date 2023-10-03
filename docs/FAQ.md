1. 
 У нас в архитектуре есть один мастер и одна реплика. В кластере сейчас 
 настроен haproxy, по 5000 порту можно писать и читать ( проксирование на мастер),
 по 5001 только читать (проксирование на реплику).  
 Однако, в приложении пока не сделано разделение потоков записи и чтения, то есть
 куда стучаться при обращении к разным ручкам.  Теоретически, например GET запросы,
 можно отправлять на реплику и не перегружать мастер, когда будет много реплик 
 и много клиентов, такая стратегия принесет плоды, ведь обычно
 клиенты чаще читают, чем пишут.
 
2. ```Как менять путь к базе? Обычно используются переменные окружения для этого… У нас тоже они есть?```
коннекшн стринг меняется параметром окружения. это дотнетик, так что прокидывая CONNECTIONSTRINGS__PGCONNECTION должно работать


3. 
```
Пробую установить в кластере  Ingress Controller  NGINX Ingress Controller
>>>>>>>> helm install ingress-controller mts-ingress-nginx
Получаю вот это 
WARNING: Kubernetes configuration file is group-readable. This is insecure. Location: /home/alex/.kube/config
WARNING: Kubernetes configuration file is world-readable. This is insecure. Location: /home/alex/.kube/config
Error: INSTALLATION FAILED: rendered manifests contain a resource that already exists. Unable to continue with install: could not get information about the resource ClusterRole "ingress-controller-ingress-nginx" in namespace "": clusterroles.rbac.authorization.k8s.io "ingress-controller-ingress-nginx" is forbidden: User "system:serviceaccount:sre-cource-student-107:student107" cannot get resource "clusterroles" in API group "rbac.authorization.k8s.io" at the cluster scope

Вижу: rendered manifests contain a resource that already exists 
```
Важно! Кластер k8s один на всех, ingress так же один, соответственно, и ip адрес внешний будет так же один.
Разделять запросы будем через доменные имена, которые можно указать либо в заголовке Host, либо в файле hosts – как вам удобнее. Не забывайте про ingressClassName: nginx

4.  
``` 
livenessProbe должен быть быстрым и довольно примитивным, ведь проверка лишь
говорит, жив сервис или нет: жив — идём дальше; нет — рестарт Pod'а. Например,
если сервис внутри Pod'а зависит от другого внешнего сервиса (в нашем случае бд),
который недоступен, то рестарт не спасёт — наше приложение стартануло, а обслуживать
клиентов всё равно не может. В общем, у нас все ручки в базу ходят и их для проверки 
дергать такое себе... тогда получается раз нету специлаьной ручки healthz, 
то можно было бы отслеживать swagger, но он судя по всем только живет в 
девелопмент и на проде его не будет...
``` 

liveness отслеживаем по живости порта, а вот readiness - уже должна быть отдельная ручка с проверками в БД 
для liveness сделана tcp проба, для readiness, возможно, появится ручка в будущем.
Лучше не делать для readiness get запрос, например, на прогноз погоды, хотя это и позволит проверить бд, 
так как если она недоступна будет 500. Причина - при масштабировании, в большое число 
инстансов приложения, возрастет нагрузка на БД. 
По этому нужно лезть в код, делать правильный рединесс/ливнесс пробы именно на
уровне кода, которые бы вытаскивали живость коннекта из драйвера.



