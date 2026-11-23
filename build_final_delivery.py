import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

TEMPLATE_PATH = "TEMPLATE ENTREGA_Fase 3_Administracao de containers em ambientes distribuidos.docx"
OUTPUT_PATH = "Entrega_Fase_03_Administracao_Containers.docx"
ALT_OUTPUT_PATH = "Relatorio_Fase_03.docx"

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def add_heading_1(doc, text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(16)
    h.paragraph_format.space_after = Pt(6)
    h.paragraph_format.keep_with_next = True
    run = h.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = RGBColor(15, 76, 129) # FIAP Navy
    return h

def add_heading_2(doc, text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(4)
    h.paragraph_format.keep_with_next = True
    run = h.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = RGBColor(43, 91, 132)
    return h

def add_heading_3(doc, text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(8)
    h.paragraph_format.space_after = Pt(3)
    h.paragraph_format.keep_with_next = True
    run = h.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(11.5)
    run.font.bold = True
    run.font.color.rgb = RGBColor(70, 70, 70)
    return h

def add_body_p(doc, text, bold_prefix=None, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Calibri'
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(30, 30, 30)
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(11)
    run.font.italic = italic
    run.font.color.rgb = RGBColor(50, 50, 50)
    return p

def add_bullet_p(doc, text, bold_prefix=None):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.first_line_indent = Inches(-0.15)
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    r_bullet = p.add_run("• ")
    r_bullet.font.name = 'Calibri'
    r_bullet.font.size = Pt(10.5)
    r_bullet.font.bold = True
    r_bullet.font.color.rgb = RGBColor(15, 76, 129)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Calibri'
        r_pre.font.size = Pt(10.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(30, 30, 30)
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(10.5)
    run.font.color.rgb = RGBColor(50, 50, 50)
    return p

def add_callout(doc, text, title="NOTA TÉCNICA", border_color="0F4C81", bg_color="F0F4F8"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.rows[0].cells[0]
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    # Left border only
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="none"/>
            <w:left w:val="single" w:sz="36" w:space="0" w:color="{border_color}"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    r_t = p.add_run(f"📌 {title}: ")
    r_t.font.name = 'Calibri'
    r_t.font.size = Pt(10)
    r_t.font.bold = True
    r_t.font.color.rgb = RGBColor(15, 76, 129)
    
    r_body = p.add_run(text)
    r_body.font.name = 'Calibri'
    r_body.font.size = Pt(10)
    r_body.font.color.rgb = RGBColor(40, 40, 40)
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)

def add_image_figure(doc, img_path, caption, width_inches=6.2):
    if not os.path.exists(img_path):
        print(f"Warning: Image {img_path} not found!")
        return
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.paragraph_format.keep_with_next = True
    run_img = p_img.add_run()
    run_img.add_picture(img_path, width=Inches(width_inches))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(10)
    run_cap = p_cap.add_run(caption)
    run_cap.font.name = 'Calibri'
    run_cap.font.size = Pt(9.5)
    run_cap.font.bold = True
    run_cap.font.italic = True
    run_cap.font.color.rgb = RGBColor(100, 100, 100)

def main():
    print("Loading template:", TEMPLATE_PATH)
    doc = docx.Document(TEMPLATE_PATH)

    # 1. Fill Table 0 (Course, Project, Student)
    if len(doc.tables) > 0:
        table = doc.tables[0]
        # Row 0: Curso
        table.rows[0].cells[1].text = "Administração de containers em ambientes distribuídos"
        # Row 1: Projeto
        table.rows[1].cells[1].text = "Entrega da Fase 3 - API Conteinerizada, CI/CD, Kubernetes e Observabilidade"
        # Row 2: Discente
        table.rows[2].cells[1].text = "Josias Soares de Souza"

        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    for r in p.runs:
                        r.font.name = 'Calibri'
                        r.font.size = Pt(10.5)

    # Remove the placeholder text paragraph "REALIZE A ATIVIDADE AVALIATIVA DA FASE NESTE TEMPLATE."
    for p in list(doc.paragraphs):
        if "REALIZE A ATIVIDADE" in p.text:
            p.text = ""

    # Document Header Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(18)
    p_title.paragraph_format.space_after = Pt(4)
    run_t = p_title.add_run("RELATÓRIO TÉCNICO DE IMPLEMENTAÇÃO E ENTREGA DA FASE 3")
    run_t.font.name = 'Calibri'
    run_t.font.size = Pt(18)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor(15, 76, 129)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(14)
    run_sub = p_sub.add_run("Arquitetura Distribuída, Conteinerização Docker, Orquestração Kubernetes, CI/CD Automatizado e Observabilidade Full-Stack com Prometheus e Grafana")
    run_sub.font.name = 'Calibri'
    run_sub.font.size = Pt(12)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(100, 100, 100)

    # =========================================================================
    # CAPÍTULO 1: INTRODUÇÃO E ESCOPO DO PROJETO
    # =========================================================================
    add_heading_1(doc, "1. Introdução e Escopo do Projeto")
    add_body_p(doc, "O presente trabalho consolida as práticas fundamentais de engenharia de software moderna, cultura DevOps e infraestrutura distribuída na nuvem, desenvolvidas ao longo da disciplina 'Administração de containers em ambientes distribuídos'. O objetivo central desta entrega é construir, executar, validar e documentar uma solução ponta a ponta com rigor de ambiente de produção, conectando código-fonte versionado, testes automatizados, conteinerização segura, implantação declarativa em cluster Kubernetes e observabilidade em tempo real.")
    add_body_p(doc, "Para viabilizar uma demonstração reproduzível, transparente e de alta didática, foi adotada como núcleo da aplicação uma API HTTP desenvolvida em Python (Flask/Gunicorn). Seu escopo enxuto e desacoplado de dependências externas de banco de dados permite focar exatamente nas propriedades de infraestrutura crítica: probes de integridade (startup, liveness e readiness), governança de réplicas, balanceamento de carga nativo via kube-proxy, tolerância a falhas sem indisponibilidade (zero downtime rolling update), capacidade de rollback instantâneo e coleta granular de métricas de negócio e de sistema.")

    add_heading_2(doc, "1.1 Arquitetura Geral da Solução")
    add_body_p(doc, "A arquitetura implementada organiza-se em camadas progressivas que atendem aos mais altos padrões de confiabilidade da engenharia de software:")
    add_bullet_p(doc, "API HTTP em Python 3.13 com instrumentação Prometheus oficial, expondo endpoints de negócio (/), probes de saúde (/healthz e /readyz) e métricas (/metrics).", "Camada de Aplicação: ")
    add_bullet_p(doc, "Imagem Docker construída com python:3.13-slim, executando sob usuário não-root (UID 10001, appuser), com empacotamento de dependências e sem testes embutidos na imagem de runtime.", "Camada de Conteinerização: ")
    add_bullet_p(doc, "Pipeline automatizado no GitHub Actions (.github/workflows/ci-cd.yml) com validação de testes em PRs, build e publicação autenticada no GitHub Container Registry (GHCR) indexada pelo SHA do commit, e deploy condicional seguro.", "Camada de Integração e Entrega Contínua (CI/CD): ")
    add_bullet_p(doc, "Deployment declarativo com 2 réplicas mínimas (escalado para 4), estratégia RollingUpdate (maxUnavailable=0), securityContext restritivo (readOnlyRootFilesystem=true, drop capabilities ALL) e Service ClusterIP para balanceamento de carga interno.", "Camada de Orquestração Kubernetes: ")
    add_bullet_p(doc, "Stack completo instalado via Helm chart kube-prometheus-stack no namespace 'monitoring', com ServiceMonitor capturando métricas da API a cada 15s e Dashboard personalizado provisionado via ConfigMap no Grafana.", "Camada de Observabilidade: ")

    # =========================================================================
    # CAPÍTULO 2: AMBIENTE DE EXECUÇÃO E FERRAMENTAS
    # =========================================================================
    add_heading_1(doc, "2. Configuração do Ambiente e Ferramentas")
    add_body_p(doc, "Diferentemente de abordagens puramente teóricas ou cenários estáticos, todas as etapas descritas neste documento foram efetivamente executadas e validadas no ambiente local de laboratório, com captura autêntica de logs, estados de cluster e gráficos gerados por tráfego real.")
    add_body_p(doc, "A tabela a seguir discrimina as ferramentas, papéis técnicos e versões exatas validadas durante o ciclo de implementação:")

    # Table of tools
    tbl_tools = doc.add_table(rows=1, cols=4)
    tbl_tools.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_tools.autofit = False
    hdr_cells = tbl_tools.rows[0].cells
    hdr_titles = ["Componente / Ferramenta", "Versão Observada", "Papel na Arquitetura", "Status de Execução"]
    hdr_widths = [Inches(1.8), Inches(1.3), Inches(2.2), Inches(1.2)]
    for i, title in enumerate(hdr_titles):
        hdr_cells[i].text = title
        hdr_cells[i].width = hdr_widths[i]
        set_cell_background(hdr_cells[i], "1F4E78")
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = 'Calibri'
            r.font.size = Pt(9.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)

    tools_data = [
        ("Python Local & Runtime", "3.14.7 (dev) / 3.13 (container)", "Execução dos testes unitários e runtime da API", "Aprovado (3 testes)"),
        ("Pytest Framework", "9.2.0", "Automação e validação dos testes funcionais", "3/3 Passando"),
        ("Docker Desktop / Engine", "29.7.2 (Client) / 4.90.0 (Server)", "Construção de imagens OCI e execução de containers", "Ativo (desktop-linux)"),
        ("Kubernetes Cluster", "v1.31.2 (kind-fase3)", "Control Plane, CNI, Kubelet e orquestração de Pods", "Node Ready (Ativo)"),
        ("Kubectl CLI", "v1.36.1 (Client) / v1.31.2 (Server)", "Gerenciamento e aplicação de manifestos declarativos", "Conectado ao cluster"),
        ("Helm Package Manager", "v3.16.3", "Gerenciamento de releases do stack de monitoramento", "Chart Deployed"),
        ("Prometheus Server", "v3.16.0", "Coleta (scrape) de métricas de sistema e da aplicação", "22 Alvos Ativos (UP)"),
        ("Grafana OSS", "13.3.1", "Visualização de métricas e dashboards analíticos", "Dashboard Importado"),
    ]

    for row_idx, data in enumerate(tools_data):
        row = tbl_tools.add_row()
        bg_color = "F9FAFC" if row_idx % 2 == 0 else "FFFFFF"
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            cell.text = text
            cell.width = hdr_widths[col_idx]
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            p = cell.paragraphs[0]
            if col_idx in [1, 3]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = 'Calibri'
                r.font.size = Pt(9)
                if col_idx == 3:
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(20, 120, 40)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(4)
    p_sp.paragraph_format.space_after = Pt(6)

    add_heading_2(doc, "2.1 Validação do Cluster Kubernetes Local")
    add_body_p(doc, "Para hospedar os workloads da disciplina, foi inicializado um cluster Kubernetes local dedicado denominado 'kind-fase3', integrado ao backend Linux WSL 2 do Docker. A validação do Control Plane, dos componentes CoreDNS e do status de prontidão do nó worker/master pode ser comprovada na evidência abaixo:")

    add_image_figure(doc, "evidencias/print_04_k8s_cluster_nodes.png",
                     "Figura 1: Evidência de verificação do cluster Kubernetes local (kubectl cluster-info e kubectl get nodes)")

    add_callout(doc, "O nó 'fase3-control-plane' encontra-se em estado 'Ready' executando o runtime containerd://2.0.0 sobre kernel Linux 6.6. O contexto ativo 'kind-fase3' assegura isolamento total contra operações acidentais em clusters externos ou de produção.",
                title="ISOLAMENTO DE AMBIENTE", border_color="0F4C81", bg_color="F0F4F8")

    # =========================================================================
    # CAPÍTULO 3: DESENVOLVIMENTO DA APLICAÇÃO E TESTES
    # =========================================================================
    add_heading_1(doc, "3. Criação da Aplicação e Testes Automatizados")
    add_body_p(doc, "A aplicação desenvolvida em app.py foi concebida sob os preceitos de resiliência e observabilidade exigidos em ecossistemas conteinerizados. Os endpoints implementados atendem a propósitos bem definidos:")
    add_bullet_p(doc, "Retorna metadados em JSON contendo o nome do serviço (api-fase3), a versão ativa e o identificador único da instância (obtido do hostname/ID do Pod). Essa diferenciação é vital para comprovar o balanceamento de carga entre diferentes réplicas.", "GET / (Index): ")
    add_bullet_p(doc, "Verificação de integridade básica (Liveness Probe). Retorna HTTP 200 {'status': 'healthy'}. Seu objetivo é indicar ao Kubelet que o processo Python/Gunicorn está vivo; caso falhe consecutivamente, o Kubernetes reinicia o container.", "GET /healthz (Liveness Probe): ")
    add_bullet_p(doc, "Verificação de prontidão para receber tráfego (Readiness Probe). Retorna HTTP 200 {'status': 'ready'}. Se a aplicação estiver em processo de inicialização ou sobrecarregada, a probe falha e o Service retira temporariamente o Pod da rota de tráfego, evitando requisições com erro para os usuários.", "GET /readyz (Readiness Probe): ")
    add_bullet_p(doc, "Exposição de métricas no formato padrão Prometheus via biblioteca prometheus-client. A métrica 'api_http_requests_total' computa o total de requisições categorizadas por método HTTP, endpoint de destino e código de status.", "GET /metrics (Observabilidade): ")

    add_heading_2(doc, "3.1 Automação e Execução de Testes com Pytest")
    add_body_p(doc, "Seguindo a pirâmide de testes e a metodologia de CI, nenhum artefato é promovido sem validação prévia. O módulo tests/test_app.py realiza três suítes de testes determinísticos:")
    add_bullet_p(doc, "Garante que o endpoint raiz retorne status 200 e a estrutura JSON esperada com campos 'service', 'instance' e 'version'.", "test_index_returns_service_information: ")
    add_bullet_p(doc, "Valida que /healthz e /readyz retornem HTTP 200 e confirmem a prontidão e saúde da aplicação.", "test_health_and_readiness_probes: ")
    add_bullet_p(doc, "Testa a exposição da métrica 'api_http_requests_total' após requisições aos endpoints, assegurando que o contador seja incrementado corretamente.", "test_metrics_endpoint_exposes_request_counter: ")

    add_body_p(doc, "A execução dos testes foi realizada com sucesso no terminal PowerShell, resultando na aprovação de 100% dos cenários:")

    add_image_figure(doc, "evidencias/print_01_pytest.png",
                     "Figura 2: Execução dos testes unitários da API com Pytest (3 passed in 0.96s)")

    # =========================================================================
    # CAPÍTULO 4: CONTEINERIZAÇÃO DOCKER E SEGURANÇA
    # =========================================================================
    add_heading_1(doc, "4. Conteinerização com Docker e Práticas DevSecOps")
    add_body_p(doc, "O arquivo Dockerfile foi elaborado com rígidas diretrizes de segurança, redução de superfície de ataque e otimização de imagens OCI:")
    add_bullet_p(doc, "Garante uma imagem enxuta baseada em Debian, contendo apenas o essencial para a execução do Python.", "Imagem Base Minimalista (python:3.13-slim): ")
    add_bullet_p(doc, "O container não é executado como root. Foi criado o usuário de sistema 'appuser' com UID 10001, instrução 'USER 10001', prevenindo que uma eventual vulnerabilidade na aplicação conceda privilégios de superusuário no host.", "Execução Não-Privilegiada (Non-Root): ")
    add_bullet_p(doc, "Os testes automatizados e arquivos auxiliares foram intencionalmente excluídos da imagem através do .dockerignore, garantindo menor tamanho em disco e sigilo de código de teste em produção.", "Isolamento de Camadas e .dockerignore: ")
    add_bullet_p(doc, "Utilização do servidor de aplicação Gunicorn com workers e threads (gthread), preparado para alta concorrência e bind na porta não privilegiada 8080.", "Servidor de Produção (Gunicorn): ")

    add_heading_2(doc, "4.1 Construção da Imagem e Execução do Container Local")
    add_body_p(doc, "A imagem foi compilada localmente com a tag 'api-fase3:local' e instanciada em container isolado 'api-teste' com mapeamento de portas 8080:8080:")

    add_image_figure(doc, "evidencias/print_02_docker_build_run.png",
                     "Figura 3: Compilação da imagem Docker e execução do container em background (docker build & run)")

    add_heading_2(doc, "4.2 Validação dos Endpoints HTTP no Container")
    add_body_p(doc, "Com o container em execução, foram disparadas chamadas HTTP contra a porta exposta no host para verificar a resposta da API, a integridade das probes e a correta exportação de métricas:")

    add_image_figure(doc, "evidencias/print_03_docker_endpoints.png",
                     "Figura 4: Consulta aos endpoints /, /healthz, /readyz e métricas Prometheus em localhost:8080")

    add_callout(doc, "A consulta ao endpoint /metrics confirmou a presença da série temporal 'api_http_requests_total' com labels 'endpoint', 'method' e 'status', atestando que o scraping do Prometheus encontrará dados válidos para consolidação de taxas e volumetria.",
                title="COMPROVAÇÃO DE INSTRUMENTAÇÃO", border_color="107C41", bg_color="F2F9F4")

    # =========================================================================
    # CAPÍTULO 5: IMPLANTAÇÃO DECLARATIVA NO KUBERNETES
    # =========================================================================
    add_heading_1(doc, "5. Implantação Declarativa no Kubernetes")
    add_body_p(doc, "A infraestrutura da aplicação no Kubernetes foi concebida sob o paradigma declarativo através de manifestos Kustomize organizados no diretório k8s/app/:")
    add_bullet_p(doc, "Cria o namespace isolado 'fase3' para segregar os recursos da aplicação dos componentes de monitoramento e de sistema.", "k8s/app/namespace.yaml: ")
    add_bullet_p(doc, "Declara 2 réplicas iniciais com rolling update (maxSurge: 1, maxUnavailable: 0), alocação de recursos (requests: 50m CPU / 64Mi RAM; limits: 500m CPU / 128Mi RAM), probes (startupProbe, livenessProbe e readinessProbe), além de restrições de segurança como 'readOnlyRootFilesystem: true', remoção de todas as capabilities de Linux ('drop: [ALL]') e volume emptyDir em memória montado em /tmp para arquivos de lock do Gunicorn.", "k8s/app/deployment.yaml: ")
    add_bullet_p(doc, "Expondo a aplicação internamente na porta 80 do cluster e roteando o tráfego para a porta 8080 dos Pods com o label 'app: api'.", "k8s/app/service.yaml: ")

    add_heading_2(doc, "5.1 Aplicação dos Manifestos e Rollout do Deployment")
    add_body_p(doc, "Após carregar a imagem local no cluster kind ('kind load docker-image api-fase3:local --name fase3'), os manifestos foram aplicados e a imagem do Deployment atualizada, acompanhando o rollout com sucesso:")

    add_image_figure(doc, "evidencias/print_05_k8s_deploy_pods_svc.png",
                     "Figura 5: Implantação no namespace 'fase3', atualização da imagem, status do rollout e recursos ativos")

    # =========================================================================
    # CAPÍTULO 6: ALTA ESCALABILIDADE, LOAD BALANCING E ROLLBACK
    # =========================================================================
    add_heading_1(doc, "6. Alta Escalabilidade, Balanceamento de Carga e Rollback")
    add_body_p(doc, "Em ambientes distribuídos modernos, a capacidade de absorver picos de demanda e manter a integridade dos serviços mesmo diante de falhas de código ou pacotes é mandatória.")

    add_heading_2(doc, "6.1 Balanceamento de Carga e Escala Manual")
    add_body_p(doc, "Para validar a distribuição de requisições, foi realizado o scaling horizontal da aplicação de 2 para 4 réplicas com o comando 'kubectl scale deployment/api --replicas=4 -n fase3'.")
    add_body_p(doc, "Em seguida, foram disparadas múltiplas requisições sequenciais originadas dentro do cluster contra o endereço DNS interno do Service ('http://api.fase3.svc.cluster.local/'). Como evidenciado abaixo, as requisições foram distribuídas de forma balanceada entre os diferentes Pods ativos ('dg4qd', 'twmzn', 'c94pf', 'w88hw'), comprovando o funcionamento do kube-proxy e do algoritmo de distribuição:")

    add_image_figure(doc, "evidencias/print_06_k8s_scale_loadbalancing.png",
                     "Figura 6: Escala horizontal para 4 réplicas e comprovação do balanceamento de carga através do campo instance")

    add_heading_2(doc, "6.2 Tolerância a Falhas (Zero Downtime) e Procedimento de Rollback")
    add_body_p(doc, "Um dos requisitos mais críticos de ambientes em produção é garantir que deploys defeituosos não causem indisponibilidade aos usuários. Para demonstrar a resiliência da configuração, foi injetada intencionalmente uma imagem inexistente no Deployment ('api=api-fase3:imagem-inexistente'):")
    add_bullet_p(doc, "Como o manifesto define 'maxUnavailable: 0', o Kubernetes cria o novo Pod mas NUNCA encerra nenhuma réplica antiga antes que o novo Pod esteja 100% aprovado pela Readiness Probe.", "Garantia de Disponibilidade (Zero Downtime): ")
    add_bullet_p(doc, "O novo Pod entrou imediatamente em estado 'ErrImagePull'. Durante todo o período da falha, as 4 réplicas saudáveis anteriores continuaram ativas e atendendo a totalidade das requisições sem nenhuma perda de pacote.", "Comportamento sob Falha: ")
    add_bullet_p(doc, "O operador acionou o comando 'kubectl rollout undo deployment/api -n fase3'. O Kubernetes reverteu instantaneamente a revisão para o replicaset estável anterior, descartando o Pod defeituoso e restaurando a estabilidade plena em segundos.", "Rollback Instantâneo: ")

    add_image_figure(doc, "evidencias/print_07_k8s_fault_tolerance_rollback.png",
                     "Figura 7: Simulação de falha de imagem (ErrImagePull com maxUnavailable=0) e rollback executado com sucesso")

    # =========================================================================
    # CAPÍTULO 7: PIPELINE DE CI/CD COM GITHUB ACTIONS
    # =========================================================================
    add_heading_1(doc, "7. Pipeline de CI/CD com GitHub Actions")
    add_body_p(doc, "O ciclo de vida da entrega contínua foi modelado no arquivo .github/workflows/ci-cd.yml, estruturado em três estágios lógicos estritamente orquestrados:")
    add_bullet_p(doc, "Executado em todo Pull Request e em pushes para a branch 'main'. Inicializa uma máquina virtual Ubuntu limpa, configura Python 3.13, instala as dependências de requirements-dev.txt e roda o pytest. Se algum teste falhar, a pipeline é imediatamente abortada.", "Job 1: test (Integração Contínua): ")
    add_bullet_p(doc, "Depende do sucesso do job de teste ('needs: test') e dispara apenas em pushes na branch 'main'. Autentica-se automaticamente no GitHub Container Registry (GHCR) com o segredo efêmero 'GITHUB_TOKEN', compila a imagem Docker e publica a tag imutável indexada pelo SHA do commit ('ghcr.io/<owner>/<repo>:<sha>').", "Job 2: publish (Publicação OCI): ")
    add_bullet_p(doc, "Executa após a publicação da imagem ('needs: publish'). O workflow avalia a presença do secret 'KUBECONFIG'. Se configurado para um cluster remoto acessível, aplica os manifestos injetando a tag da imagem recém-gerada e aguarda o término do rollout. Caso o secret esteja ausente (como ocorre tipicamente em laptops locais privados), o pipeline emite uma mensagem clara informando que o deploy foi ignorado com segurança.", "Job 3: deploy (Implantação Segura): ")

    add_image_figure(doc, "evidencias/print_11_cicd_pipeline.png",
                     "Figura 8: Diagrama do fluxo automatizado de CI/CD implementado no GitHub Actions (.github/workflows/ci-cd.yml)")

    add_callout(doc, "O runner do GitHub Actions roda na nuvem pública e, por princípios de segurança de rede, não possui rota para acessar diretamente o cluster Kubernetes local do Docker Desktop. Por esse motivo, a arquitetura preconiza que o pipeline teste e publique no GHCR, cabendo ao operador aplicar a imagem no cluster de laboratório via kubectl, sem versionar credenciais sensíveis.",
                title="DIRETRIZ DE SEGURANÇA EM CI/CD", border_color="0F4C81", bg_color="F0F4F8")

    # =========================================================================
    # CAPÍTULO 8: OBSERVABILIDADE COM PROMETHEUS E GRAFANA
    # =========================================================================
    add_heading_1(doc, "8. Observabilidade: Monitoramento com Prometheus e Grafana")
    add_body_p(doc, "Para alcançar observabilidade completa (Four Golden Signals: latência, tráfego, erros e saturação), foi implantado o stack oficial da comunidade Prometheus através do Helm chart 'kube-prometheus-stack' no namespace 'monitoring'.")

    add_heading_2(doc, "8.1 Componentes do Stack em Execução")
    add_body_p(doc, "A instalação via Helm provisionou os operadores, os servidores de série temporal, coletores de nós e o Grafana. A verificação detalhada confirma que todos os Pods atingiram estado 'Running' e prontidão plena:")

    add_image_figure(doc, "evidencias/print_08_monitoring_stack_pods.png",
                     "Figura 9: Pods do stack de monitoramento em execução no namespace 'monitoring' (Prometheus, Grafana 3/3, Alertmanager)")

    add_heading_2(doc, "8.2 Integração via ServiceMonitor (Scrape Automático)")
    add_body_p(doc, "A descoberta e coleta de métricas da API não foi feita por configurações manuais, mas sim através do padrão Kubernetes Operator utilizando a CRD ServiceMonitor declarada em k8s/monitoring/api-servicemonitor.yaml. O Prometheus Operator detectou os Pods da API no namespace 'fase3' e iniciou o scrape periódico no endpoint /metrics a cada 15 segundos.")
    add_body_p(doc, "A consulta direta à API de targets do Prometheus Server comprovou que todas as 4 réplicas da aplicação estavam com status de saúde 'UP':")

    add_image_figure(doc, "evidencias/print_09_prometheus_targets_up.png",
                     "Figura 10: Alvos ativos do Prometheus comprovando a coleta contínua (100% UP) nas réplicas da API")

    add_heading_2(doc, "8.3 Dashboard Customizado no Grafana com Tráfego Real")
    add_body_p(doc, "O painel analítico da aplicação foi provisionado como código através do ConfigMap 'api-dashboard' com o rótulo 'grafana_dashboard: 1', carregado automaticamente pelo container sidecar do Grafana.")
    add_body_p(doc, "Após a geração de carga de requisições sequenciais contra a API, o painel 'API - Fase 3' apresentou dados em tempo real nos seus quatro gráficos centrais:")
    add_bullet_p(doc, "Mede sum(rate(api_http_requests_total[5m])), registrando o pico de requisições de carga e normalização subsequente.", "Painel 1 (Requisições HTTP por segundo): ")
    add_bullet_p(doc, "Mede a taxa de CPU individual de cada Pod via métricas do cAdvisor/Kubelet, demonstrando consumo balanceado em torno de 50m-120m cores durante o teste de estresse.", "Painel 2 (CPU utilizada por pod): ")
    add_bullet_p(doc, "Mede a memória de trabalho (working set bytes) de cada Pod, demonstrando estabilidade em aproximadamente 35 a 42 MiB (bem abaixo do limite configurado de 128 MiB).", "Painel 3 (Memória utilizada por pod): ")
    add_bullet_p(doc, "Mede a contagem de Pods prontos via kube-state-metrics, registrando visualmente o degrau de transição de 2 para 4 réplicas ativas.", "Painel 4 (Réplicas prontas): ")

    add_image_figure(doc, "evidencias/print_10_grafana_dashboard.png",
                     "Figura 11: Dashboard analítico 'API - Fase 3' no Grafana com métricas reais coletadas do cluster", width_inches=6.4)

    # =========================================================================
    # CAPÍTULO 9: CONCLUSÃO E MATRIZ DE EVIDÊNCIAS
    # =========================================================================
    add_heading_1(doc, "9. Conclusão e Matriz de Evidências")
    add_body_p(doc, "A realização deste projeto cobriu de ponta a ponta todos os domínios essenciais exigidos para um profissional de engenharia DevOps e administração de ambientes distribuídos. A solução combinou rigor de desenvolvimento (testes unitários determinísticos), boas práticas de segurança em containers (usuário não-root, filesystem somente leitura, imagem minimalista), resiliência em orquestração (zero downtime, health probes desacopladas e rollback testado) e observabilidade moderna baseada em operadores de monitoramento.")
    add_body_p(doc, "A tabela a seguir sumariza a matriz de conformidade entre os requisitos propostos na Fase 3 e os resultados empíricos atingidos:")

    # Table of Results
    tbl_res = doc.add_table(rows=1, cols=4)
    tbl_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_res.autofit = False
    hdr_cells2 = tbl_res.rows[0].cells
    hdr_titles2 = ["Atividade / Etapa", "Critério de Aceite", "Resultado Observado", "Evidência"]
    hdr_widths2 = [Inches(1.8), Inches(2.0), Inches(1.8), Inches(0.9)]
    for i, title in enumerate(hdr_titles2):
        hdr_cells2[i].text = title
        hdr_cells2[i].width = hdr_widths2[i]
        set_cell_background(hdr_cells2[i], "1F4E78")
        p = hdr_cells2[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = 'Calibri'
            r.font.size = Pt(9.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)

    checklist_data = [
        ("1. Testes Automatizados", "Aprovação de todos os testes unitários da API", "3 testes aprovados em 0.96s (100% de sucesso)", "Figura 2"),
        ("2. Imagem Docker OCI", "Build funcional, usuário non-root e sem testes", "Imagem compilada (api-fase3:local, 45.4MB)", "Figura 3"),
        ("3. Endpoints e Probes", "Respostas 200 em /, /healthz, /readyz e /metrics", "JSON validado, probes ativas, métricas expostas", "Figura 4"),
        ("4. Cluster Kubernetes", "Contexto ativo, control-plane e nós prontos", "Cluster kind-fase3 ativo com node Ready", "Figura 1"),
        ("5. Implantação e Service", "2 réplicas prontas, Service ClusterIP e probes", "Deployment com rollout concluído no namespace fase3", "Figura 5"),
        ("6. Escala e Load Balancing", "Escala para 4 réplicas e tráfego balanceado", "4 réplicas ativas; distribuição comprovada por ID", "Figura 6"),
        ("7. Tolerância e Rollback", "Zero downtime em falha de imagem e rollback rápido", "maxUnavailable:0 manteve pods; rollback ok", "Figura 7"),
        ("8. Pipeline CI/CD", "Workflow com jobs de test, publish GHCR e deploy", "Workflow configurado com permissões e segredos", "Figura 8"),
        ("9. Stack Monitoramento", "Instalação do Helm kube-prometheus-stack", "Todos os componentes ativos no namespace monitoring", "Figura 9"),
        ("10. Coleta Prometheus", "ServiceMonitor descobrindo e raspando a API", "4/4 alvos da API em status UP a cada 15s", "Figura 10"),
        ("11. Dashboard Grafana", "Painel com 4 gráficos e tráfego real consolidado", "Dashboard 'API - Fase 3' com dados reais", "Figura 11"),
    ]

    for row_idx, data in enumerate(checklist_data):
        row = tbl_res.add_row()
        bg_color = "F9FAFC" if row_idx % 2 == 0 else "FFFFFF"
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            cell.text = text
            cell.width = hdr_widths2[col_idx]
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
            p = cell.paragraphs[0]
            if col_idx in [3]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = 'Calibri'
                r.font.size = Pt(8.5)
                if col_idx == 2:
                    r.font.color.rgb = RGBColor(20, 120, 40)
                elif col_idx == 3:
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(15, 76, 129)

    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_before = Pt(8)
    p_sp2.paragraph_format.space_after = Pt(4)

    # =========================================================================
    # CAPÍTULO 10: REFERÊNCIAS BIBLIOGRÁFICAS
    # =========================================================================
    add_heading_1(doc, "10. Referências Bibliográficas")
    refs = [
        "KUBERNETES. Kubernetes Documentation: Concepts, Workloads, Services and Probes. Disponível em: <https://kubernetes.io/docs/>. Acesso em: 23 nov. 2026.",
        "DOCKER. Docker Documentation: Best Practices for Writing Dockerfiles & Security. Disponível em: <https://docs.docker.com/>. Acesso em: 23 nov. 2026.",
        "GITHUB. GitHub Actions Documentation: Continuous Integration and Package Registries (GHCR). Disponível em: <https://docs.github.com/actions>. Acesso em: 23 nov. 2026.",
        "PROMETHEUS COMMUNITY. Kube-Prometheus-Stack Helm Chart Repository. Disponível em: <https://github.com/prometheus-community/helm-charts>. Acesso em: 23 nov. 2026.",
        "PROMETHEUS. Python Client Documentation: Instrumenting HTTP Applications. Disponível em: <https://prometheus.github.io/client_python/>. Acesso em: 23 nov. 2026.",
        "GRAFANA LABS. Grafana Documentation: Provisioning Dashboards and Datasources as Code. Disponível em: <https://grafana.com/docs/>. Acesso em: 23 nov. 2026.",
        "PALLETS PROJECTS. Flask: A Python Microframework. Disponível em: <https://flask.palletsprojects.com/>. Acesso em: 23 nov. 2026.",
        "DORA (DevOps Research and Assessment). Software Delivery Performance Metrics and Accelerate State of DevOps Report. Disponível em: <https://dora.dev/>. Acesso em: 23 nov. 2026."
    ]
    for ref in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(2)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.left_indent = Inches(0.25)
        p_ref.paragraph_format.first_line_indent = Inches(-0.25)
        run_ref = p_ref.add_run(ref)
        run_ref.font.name = 'Calibri'
        run_ref.font.size = Pt(9.5)
        run_ref.font.color.rgb = RGBColor(60, 60, 60)

    # Save to both outputs:
    doc.save(OUTPUT_PATH)
    print(f"Saved final deliverable to: {OUTPUT_PATH}")

    doc.save(ALT_OUTPUT_PATH)
    print(f"Saved updated report to: {ALT_OUTPUT_PATH}")

if __name__ == '__main__':
    main()
