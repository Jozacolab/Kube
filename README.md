# Fase 3 — API em containers com Kubernetes

Projeto didatico de uma API Flask instrumentada com Prometheus, imagem Docker
nao-root, manifests Kubernetes, pipeline GitHub Actions e painel Grafana.

## Arquivos principais

- `app.py` e `tests/`: API HTTP, probes, metricas Prometheus e testes.
- `Dockerfile`: imagem Python enxuta executada como usuario nao privilegiado.
- `.github/workflows/ci-cd.yml`: testes, publicacao no GHCR e deploy opcional.
- `k8s/app/`: namespace, Deployment com duas replicas e Service ClusterIP.
- `k8s/monitoring/`: valores do kube-prometheus-stack, ServiceMonitor e painel.

## Testes locais

No PowerShell, na raiz do repositorio:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

## Imagem e API

Com Docker Desktop aberto e usando o modo Linux containers:

```powershell
docker build -t api-fase3:local .
docker run --rm -p 8080:8080 api-fase3:local
```

Em outro terminal, valide os endpoints:

```powershell
Invoke-RestMethod http://localhost:8080/
Invoke-RestMethod http://localhost:8080/healthz
Invoke-WebRequest http://localhost:8080/metrics
```

`/` retorna a identificacao da instancia; `/healthz` e `/readyz` atendem as
probes; `/metrics` expoe o contador HTTP. O Docker daemon precisa estar ativo
para construir e executar a imagem.

## Kubernetes local

Inicie um cluster local (por exemplo, Kubernetes do Docker Desktop) e confirme
o contexto antes de aplicar recursos:

```powershell
kubectl config current-context
kubectl cluster-info
kubectl apply -k k8s/app
kubectl set image deployment/api api=api-fase3:local -n fase3
kubectl rollout status deployment/api -n fase3
kubectl get pods,svc -n fase3
```

O cluster do Docker Desktop consegue usar a imagem local. Para outros clusters,
publique uma imagem em um registry acessivel e atualize a imagem do Deployment.
Teste o Service e a escala:

```powershell
kubectl port-forward service/api 8080:80 -n fase3
Invoke-RestMethod http://localhost:8080/
kubectl scale deployment/api --replicas=4 -n fase3
kubectl get pods -n fase3 -o wide
kubectl rollout undo deployment/api -n fase3
```

O campo `instance` permite observar qual replica respondeu. O `Service` distribui
as conexoes entre os Pods prontos; o comando `scale` demonstra escala manual.

## CI/CD com GitHub Actions

Pull requests executam os testes. Pushes para `main` publicam a imagem
`ghcr.io/<proprietario>/<repositorio>:<commit>` no GitHub Container Registry.
Para habilitar deploy automatico, crie o secret de repositorio `KUBECONFIG` com
o conteudo do kubeconfig do cluster (Base64 em uma linha). O runner Ubuntu
precisa alcancar o endpoint do cluster; nao use credenciais de um cluster local
nao acessivel pela internet. Configure o pacote GHCR como publico para que um
cluster sem `imagePullSecret` consiga baixar a imagem, ou adapte o cluster para
autenticacao no registry.

O job de deploy aplica `k8s/app`, define a imagem imutavel do commit e aguarda
`kubectl rollout status`. Sem o secret, o deploy e explicitamente ignorado,
mas testes e publicacao ainda podem ocorrer.

## Monitoramento Prometheus e Grafana

Com `helm` instalado e o cluster ativo:

```powershell
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm upgrade --install monitoring prometheus-community/kube-prometheus-stack `
  --namespace monitoring --create-namespace `
  --values k8s/monitoring/kube-prometheus-stack-values.yaml
kubectl apply -f k8s/monitoring/api-servicemonitor.yaml
kubectl apply -f k8s/monitoring/api-dashboard.yaml
```

O stack instala Prometheus, Grafana, kube-state-metrics e exporters de nos.
O `ServiceMonitor` coleta `/metrics` da API; o dashboard inclui taxa de
requisicoes, CPU e memoria dos containers, alem de Pods prontos. Os dados sao
metricas reais somente depois que os recursos estao ativos no cluster.

Abra o Grafana em outro terminal:

```powershell
kubectl port-forward service/monitoring-grafana 3000:80 -n monitoring
```

Consulte a senha inicial no Secret `monitoring-grafana` do namespace `monitoring`
e acesse `http://localhost:3000`. Os dashboards padrao do stack mostram recursos
do cluster; o painel `API - Fase 3` e carregado a partir do ConfigMap.

## Evidências e Conclusão da Fase 3

Todas as etapas do roteiro prático foram executadas, validadas e documentadas com sucesso:
- **Testes da API**: 3 testes aprovados via `pytest` (cobertura de endpoints, probes e métricas).
- **Conteinerização Docker**: imagem `api-fase3:local` construída com usuário non-root e validada em container local.
- **Kubernetes Local**: cluster `kind-fase3` ativo, deployment com 2 réplicas mínimas escalado para 4 réplicas.
- **Balanceamento de Carga e Resiliência**: distribuição comprovada por identificador de instância via `ClusterIP` e rollback testado sem indisponibilidade (`maxUnavailable: 0`).
- **Observabilidade**: stack `kube-prometheus-stack` instalado via Helm, 4 réplicas da API monitoradas via `ServiceMonitor` (status UP) e dashboard customizado no Grafana exibindo tráfego real.

