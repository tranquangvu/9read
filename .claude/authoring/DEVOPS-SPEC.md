# DEVOPS-SPEC.md — DevOps Engineer Career Track module contract

The third program on the site (`devops/`). Pages use the same markup vocabulary as AIFDE and the
internship, so everything in `PATTERNS.md` applies. The page shape is the internship shape from
`INTERN-SPEC.md` (4 Parts, Claude Code section, no labs), with the differences below. Where the
documents disagree, this one wins for `devops/`.

## Audience and voice
- The program takes someone who has **never done DevOps** (a developer, a QA, a fresh graduate) to a
  **senior DevOps engineer on AWS**. Every module carries a `level` in the registry:
  L0 Foundation · L1 Junior · L2 Mid-level · L3 Senior. Write for the reader *entering* that level:
  an L0 page defines every term; an L3 page assumes L0–L2 and argues trade-offs.
- Company stack is fixed. Never present an alternative as the default:
  **AWS** (region `ap-southeast-1`), **Terraform** for IaC, **GitHub Actions** for CI/CD,
  **ECS on Fargate and EKS** for containers, **CloudWatch + Prometheus/Grafana/Loki + Datadog** for
  observability (OpenTelemetry as the instrumentation layer that feeds them), **Argo CD** for GitOps,
  **Helm** for packaging. Mention alternatives (CDK, GitLab, Flux, Pulumi…) in one line at most.
- Teach operational judgement: *what* it is, *why* it exists, *how it fails in production*, *how to
  verify it*. Every topic should leave the reader able to review a Terraform plan / manifest / pipeline
  an agent wrote and spot what is wrong.
- Code blocks are real and runnable (HCL, YAML, bash, kubectl, aws CLI, PromQL, Python). Keep each to
  about 30 lines or fewer, annotate the load-bearing line with a `.cm` comment, and show expected
  output with `<span class="out">` where a command prints something.
- Plain English, second person, opinionated. No marketing register ("leverage", "seamless", "robust").

## The running example (use it everywhere)
**Clinic booking platform**, a Golden Owl-style client system:
- Services: `booking-api` (TypeScript on Node.js 22, distroless image, HTTP :8080, health `/healthz`), `booking-web` (Next.js frontend),
  `booking-worker` (queue consumer). Postgres (RDS), Valkey 8 (ElastiCache; say "Valkey", not Redis, for new caches), S3 uploads bucket, SQS queue.
- AWS Organization with accounts `gol-shared` (CI, ECR, DNS), `gol-dev`, `gol-staging`, `gol-prod`,
  plus `gol-security` / `gol-log-archive` once AR1/SE1 introduce them.
- Domain `clinic.example.com` (`api.clinic.example.com`, `app.clinic.example.com`).
- VPC `10.20.0.0/16` in prod (dev `10.10.0.0/16`, staging `10.15.0.0/16`), 3 AZs.
- ECS cluster `clinic-prod`; EKS cluster `clinic-prod-eks`, namespace `booking`.
- GitHub org `golden-owl`, repos `clinic-app` (app code), `clinic-infra` (Terraform),
  `clinic-gitops` (Argo CD manifests).

### Shared identifiers (already used by written modules — reuse exactly)
- Accounts: `gol-management` 999988887777 (Organizations/payer), `gol-shared` 111122223333 (CI, ECR, DNS),
  `gol-dev` 222233334444, `gol-staging` 333344445555, `gol-prod` 444455556666,
  `gol-security` 555566667777, `gol-log-archive` 666677778888, `gol-sandbox` 888899990000 (training + AI agents,
  role `agent-readonly`). Org ID `o-a1b2c3d4e5`. Identity Center start URL `goldenowl.awsapps.com/start`.
- ECR repos `clinic/<service>` in gol-shared, e.g. `111122223333.dkr.ecr.ap-southeast-1.amazonaws.com/clinic/booking-api:1.8.2`.
- GitHub OIDC roles `gha-clinic-app-ecr-push`, `gha-clinic-app-deploy`, `gha-clinic-infra-plan`,
  `gha-clinic-infra-apply`; shared workflows repo `golden-owl/gha-platform`; modules repo `golden-owl/terraform-modules`.
- Prod subnets: public `10.20.0.0/24`–`10.20.2.0/24`, private `10.20.32.0/19`, `10.20.64.0/19`, `10.20.96.0/19`,
  isolated `10.20.200.0/24`–`10.20.202.0/24`. gol-shared VPC `10.0.0.0/16`.
- Buckets `gol-<env>-clinic-uploads`, `gol-prod-clinic-web-assets`. Service Connect namespace `clinic.internal`.
- Terraform owns infra; the deploy pipeline owns the running image (Terraform ignores `task_definition`
  / `desired_count` on ECS services). Share values between states via SSM parameters, not `terraform_remote_state`.

## Version baseline (do not contradict)
Terraform ≥ 1.10 with S3-native state locking (`use_lockfile = true`, no DynamoDB table needed);
AWS provider `~> 6.0`; `terraform-aws-modules/vpc` and `/eks` from the registry; Kubernetes / EKS
`1.33`; EKS **access entries** (not `aws-auth` ConfigMap) and **EKS Pod Identity** (IRSA as the older
alternative); Karpenter `v1` APIs (`karpenter.sh/v1` NodePool, `karpenter.k8s.aws/v1` EC2NodeClass);
Gateway API `v1`; Argo CD 3.x; Helm 3; GitHub Actions authenticating to AWS via **OIDC**
(`aws-actions/configure-aws-credentials`), never long-lived access keys.

## Source layout
- Write fragments in `.claude/authoring/devops_src/<code>.html`. Build with
  `python3 .claude/authoring/devops_build.py <code>`. The build writes `devops/modules/<code>.html`
  and supplies head, sidebar, badges (Core/Elective, target score, level, "~N days"), page-nav and
  footer from the `DEVOPS_MODULES` registry in `assets/site.js`. **Never edit a built page by hand.**
- Fragment format is the same as the internship (`<!-- meta: days=N -->`, hero, `<!-- @@BODY@@ -->`,
  body through the Resources `<ul>`).
- Write in chunks of 400 lines or fewer (create the file, then append with further edits).
- Parallel authors **do not edit `assets/site.js`** (the coordinator removes `soon` flags) and run QA
  with `--pages-only`:
  `python3 .claude/authoring/qa.py --program devops --pages-only devops/modules/<code>.html`

## Page structure (in this order)
1. Hero: `h1` (the registry name), lead paragraph, `callout-why` starting
   **"Why it matters in production:"**.
2. **Exactly 4 Parts** with the Part I–IV kicker classes (PATTERNS §1). Each Part ≥ 3 `h3`s
   (QA enforces ≥ 2).
3. `<h2>Working with Claude Code</h2>`: 2–4 prompts in `<pre class="code">`, the two-up grid
   **"Let the agent do"** / **"You must check"**, and a `callout-warn` of red flags in AI-written
   infra for this topic.
4. `Skill ladder: what each score looks like` (labels 0 No exposure · 1 Awareness · 2 Works with
   support · 3 Works independently · 4 Leads &amp; coaches; `.target` on 3 for Core, 2 for Elective),
   then `callout-tip` "Self-check before claiming 3:" (or 2).
5. `Pitfalls &amp; pro tips`: 4–6 cards, ✗ first then ✓.
6. `Evidence checklist`: 4–6 `evidence-box` items with stable lowercase `data-key`s. The **last** item
   is `font-semibold`, ends with `(mentor evidence ✓)` and is a practice task of a few hours that
   produces a showable artifact (PR, `terraform plan`, Grafana screenshot, runbook, URL).
7. `Resources`: 5–8 links, official docs only (`docs.aws.amazon.com`, `aws.amazon.com/blogs`,
   `developer.hashicorp.com`, `registry.terraform.io`, `kubernetes.io`, `docs.github.com`,
   `argo-cd.readthedocs.io`, `docs.docker.com`, `boto3.amazonaws.com`, `docs.ansible.com`, `backstage.io`, `docs.claude.com`, `karpenter.sh`, `helm.sh`, `prometheus.io`, `grafana.com/docs`,
   `docs.datadoghq.com`, `opentelemetry.io`, `sre.google`, `dora.dev`, `github.com/<org>` READMEs).

No lab cards, no `<dialog>`, no "In the field" section.

## Density gates (`qa.py --program devops`)
- 600–1,400 lines once built (aim ~900–1,200)
- ≥ 3 diagrams (SVG `role="img"` in `.diagram-card` and/or Mermaid) — aim for 4
- ≥ 3 tables · ≥ 8 code blocks · ≥ 5 callouts incl. ≥ 1 `callout-warn` · 5–8 resources

## Links
- In-program: `<a href="./ks5.html" class="text-viol underline decoration-viol/40">KS5</a>`. Link to
  the owner instead of re-teaching (see ownership below). Linking to a module still marked `soon` is
  fine — every module in the registry will ship.
- External links: `class="text-coral underline" target="_blank" rel="noopener"`.

## Module scopes and topic ownership
Each module owns the topics listed. A neighbour writes one sentence and a link.

| Code | Owns |
|---|---|
| FN1 | What DevOps is (CALMS, the three ways), SDLC and the deployment pipeline end to end, DORA four keys + reliability, value-stream thinking, toil, the DevOps career ladder and how this program maps to it, blameless culture intro |
| FN2 | Filesystem hierarchy, users/groups/permissions/sudo, processes and signals, systemd units and journald, package management, disk/memory/CPU inspection (`top`, `free`, `df`, `iostat`, `ss`, `lsof`), log reading, SSH and keys, a troubleshooting method for a sick box |
| FN3 | OSI/TCP-IP in practice, IP and CIDR maths, ports, TCP handshake and states, DNS resolution chain and record types, HTTP/1.1–2–3, TLS handshake and certificates, L4 vs L7 load balancing, NAT, proxies, tools (`dig`, `curl -v`, `mtr`, `tcpdump`, `openssl s_client`) |
| FN4 | Git internals for ops, trunk-based vs GitFlow for infra, PR review for infra repos, CODEOWNERS, branch protection and rulesets, conventional commits, semver and tags, monorepo vs polyrepo for infra, signed commits |
| FN5 | Bash safely (`set -euo pipefail`, quoting, traps, exit codes), text tools (`grep/sed/awk/jq/yq`), cron, idempotent scripts, Python with boto3 for AWS automation, CLI argument parsing, when to stop scripting and use Terraform |
| FN6 | Images and layers, Dockerfile best practices, multi-stage builds, distroless/slim, non-root, build cache and BuildKit, multi-arch (arm64/Graviton), compose for local stacks, container networking and volumes, namespaces/cgroups under the hood, image size and CVE basics |
| AW1 | AWS global infrastructure, Organizations and OUs, SCPs, IAM users/roles/policies, policy evaluation logic, permission boundaries, IAM Identity Center (SSO) and permission sets, AWS CLI profiles and `aws sso login`, MFA, root account hygiene, IAM Access Analyzer |
| AW2 | VPC design and CIDR planning, public/private/isolated subnets, route tables, IGW, NAT gateway (and its cost), SG vs NACL, VPC endpoints (gateway/interface), peering vs Transit Gateway, VPC Flow Logs, IPv6 basics, Client VPN / SSM instead of bastions |
| AW3 | EC2 instance families incl. Graviton, AMIs, user data, launch templates, Auto Scaling groups and policies, ALB vs NLB, target groups and health checks, listener rules, SSM Session Manager, Spot basics, EBS-backed instance lifecycle |
| AW4 | S3 (storage classes, lifecycle, versioning, encryption, bucket policies, Block Public Access, presigned URLs, replication), EBS volume types and snapshots, EFS, CloudFront (origins, OAC, cache policies, invalidations) |
| AW5 | RDS and Aurora (Multi-AZ, read replicas, parameter groups, backups/PITR, RDS Proxy, upgrades, Performance Insights), DynamoDB (keys, capacity modes, GSIs), ElastiCache Redis/Valkey, choosing between them |
| AW6 | Lambda (runtime, cold starts, concurrency, layers, packaging), API Gateway HTTP vs REST, SQS (visibility timeout, DLQ, FIFO), SNS fan-out, EventBridge buses/rules/scheduler, Step Functions overview. (Application-side queue patterns stay in intern SD8.) |
| AW7 | Route 53 hosted zones, record types and alias records, routing policies (weighted, latency, failover), health checks, delegating subdomains across accounts, ACM public certs and DNS validation, cert region rules (us-east-1 for CloudFront), domain cutover runbook |
| IA1 | Terraform workflow (init/plan/apply), providers, resources, data sources, variables/outputs/locals, state and remote S3 backend with native locking, `for_each`/`count`, dependencies, `import` blocks, `moved` blocks, reading a plan safely |
| IA2 | Module design and versioning, registry modules, environment layout (directories vs workspaces), Terragrunt mention, state splitting and blast radius, `terraform test`, tflint/validate, policy-as-code (OPA/Conftest, checkov hand-off to SE2), drift detection, Terraform in GitHub Actions with plan-on-PR / apply-on-merge |
| IA3 | Ansible inventory, playbooks, roles, idempotency, Ansible vs Terraform boundaries, SSM Run Command / State Manager / Patch Manager, golden AMIs with Packer + EC2 Image Builder |
| CI1 | GitHub Actions anatomy (workflows, jobs, steps, runners, contexts, expressions), triggers, matrix builds, caching, artifacts, reusable workflows and composite actions, OIDC to AWS, self-hosted vs hosted runners (ARC on EKS mention), concurrency, pinning actions by SHA, pipeline speed |
| CI2 | CD vs continuous deployment, environments and approvals, promotion dev→staging→prod, release strategies (rolling, blue/green, canary, shadow), feature flags as release control, DB migrations in deploys (expand/contract), rollback vs roll-forward, release versioning and changelogs |
| CI3 | Secrets Manager vs SSM Parameter Store, KMS keys, envelope encryption, key policies, rotation, injecting secrets into ECS/EKS/Lambda/GitHub Actions, External Secrets Operator (hand-off to KS7 for the EKS details), `.env` hygiene, secret scanning and leaked-key response |
| CI4 | ECR repositories, lifecycle policies, immutable tags, cross-account pull, image scanning (ECR enhanced/Inspector, Trivy), SBOM (Syft), signing (cosign / AWS Signer), provenance and SLSA levels, dependency pinning and Dependabot/Renovate |
| CN1 | ECS concepts (cluster, task definition, task, service), Fargate vs EC2 launch type, task role vs execution role, networking mode awsvpc, ALB integration, logging with awslogs/FireLens, ECS Exec, Terraform for an ECS service |
| CN2 | ECS deployment types (rolling with circuit breaker, blue/green with CodeDeploy, ECS native blue/green), Service Auto Scaling (target tracking, step, scheduled), capacity providers and Fargate Spot, Service Connect, ECS on EC2 when needed, ECS vs EKS decision table |
| KS1 | Why Kubernetes, the control loop / desired state, control plane components (API server, etcd, scheduler, controller manager) and node components (kubelet, kube-proxy, container runtime), Pods, ReplicaSets, Deployments, Services, Namespaces, labels/selectors, `kubectl` fluency, local clusters (kind) |
| KS2 | Deployments vs StatefulSets vs DaemonSets vs Jobs/CronJobs, rollout strategy fields, ConfigMaps and Secrets (as objects), env vs volume mounts, probes (liveness/readiness/startup), requests/limits, QoS classes, LimitRange/ResourceQuota, PodDisruptionBudgets, affinity/anti-affinity, taints/tolerations, topology spread, graceful shutdown |
| KS3 | Service types (ClusterIP/NodePort/LoadBalancer/headless), CoreDNS, kube-proxy modes, Ingress and ingress controllers, Gateway API (GatewayClass/Gateway/HTTPRoute), NetworkPolicy, CNI concept. (EKS-specific VPC CNI and AWS LB Controller → KS6.) |
| KS4 | Volumes, PV/PVC, StorageClasses and dynamic provisioning, EBS CSI and EFS CSI drivers, access modes, volume snapshots, StatefulSet storage, running databases on K8s vs RDS, backup/restore with Velero |
| KS5 | EKS architecture and shared responsibility, control plane options, managed node groups vs self-managed vs Fargate vs **EKS Auto Mode**, Terraform `terraform-aws-modules/eks`, EKS add-ons (CoreDNS, kube-proxy, VPC CNI, EBS CSI, Pod Identity agent), access entries for cluster access, cluster endpoint access, kubeconfig via `aws eks update-kubeconfig`, bootstrap baseline |
| KS6 | Amazon VPC CNI (ENIs, IP per pod, warm pools, prefix delegation, IP exhaustion, custom networking), security groups for pods, AWS Load Balancer Controller (ALB Ingress, NLB Services, IngressGroups, target type ip), ExternalDNS, cert-manager vs ACM, Gateway API on EKS (AWS Gateway API controller / VPC Lattice mention) |
| KS7 | Authn/authz to the cluster (access entries + access policies, RBAC Roles/ClusterRoles/Bindings), workload identity (EKS Pod Identity, IRSA), Pod Security Standards / admission, Kyverno policies, secrets on EKS (External Secrets Operator, Secrets Store CSI), image provenance admission, envelope encryption of K8s secrets with KMS, GuardDuty EKS protection hand-off to SE1 |
| KS8 | HPA (CPU/memory/custom metrics, behavior), VPA, KEDA (SQS-driven scaling), Cluster Autoscaler vs Karpenter, Karpenter NodePools/EC2NodeClass, consolidation and disruption budgets, Spot with Karpenter, Graviton, bin-packing and right-sizing requests, Kubecost / split cost allocation |
| KS9 | Helm charts (structure, templates, values, helpers, dependencies), chart versioning and OCI registries (ECR), `helm diff`, helmfile mention, Kustomize bases/overlays/patches, when to use which, rendering and validating manifests in CI (kubeconform) |
| KS10 | GitOps principles, Argo CD architecture, Applications, Projects, sync policies and waves/hooks, app-of-apps and ApplicationSets for multi-env/multi-cluster, image updater, repo layout for `clinic-gitops`, Argo Rollouts canary/blue-green with analysis, secrets in GitOps |
| KS11 | EKS version upgrades (control plane, add-ons, nodes, API deprecations, `pluto`/upgrade insights), node rotation, troubleshooting playbook (Pending, CrashLoopBackOff, ImagePullBackOff, OOMKilled, DNS, networking, 5xx at the ALB), `kubectl debug`, events, cluster backups, runbooks |
| KS12 | Kubernetes API extension model, CRDs, controllers and reconcile loops, operators (when to adopt vs build), Kubebuilder/controller-runtime basics, admission webhooks, ACK (AWS Controllers for Kubernetes) and Crossplane for AWS resources |
| KS13 | Service mesh concepts (sidecar vs ambient), Istio on EKS, mTLS, traffic splitting, retries/timeouts at the mesh, observability from the mesh, multi-cluster topologies (per-env, per-region), cross-cluster service discovery, when not to adopt a mesh |
| OB1 | Three pillars and the observability vs monitoring distinction, CloudWatch metrics/dimensions/namespaces, Logs and Logs Insights, metric filters, alarms and composite alarms, dashboards, Container Insights for ECS/EKS, X-Ray / Application Signals, log retention and cost |
| OB2 | Prometheus data model and pull model, exporters, PromQL (rate, histogram_quantile, aggregation), recording and alerting rules, Alertmanager routing, kube-prometheus-stack on EKS, Amazon Managed Prometheus/Grafana, Grafana dashboards-as-code, Loki for logs (LogQL), cardinality control |
| OB3 | Datadog agent on EC2/ECS/EKS, integrations (AWS), infrastructure metrics, APM and service map, log pipelines and indexes, monitors and SLO objects, dashboards, tagging strategy (`env`, `service`, `version`), Datadog cost drivers, when we use Datadog vs the OSS stack |
| OB4 | OpenTelemetry concepts (signals, SDKs, auto-instrumentation, context propagation, semantic conventions), the Collector (receivers/processors/exporters), ADOT on EKS/ECS, sampling (head vs tail), exporting the same telemetry to CloudWatch, Prometheus/Tempo and Datadog, trace-log-metric correlation |
| SR1 | SRE principles, SLI selection per service type, SLO maths and windows, error budgets and policies, burn-rate alerting (multi-window), alert design (symptoms not causes, actionability), golden signals / RED / USE |
| SR2 | Incident lifecycle and severity levels, incident commander and roles, comms templates and status pages, on-call rotations and handoffs, runbooks, PagerDuty/Opsgenie style escalation, blameless postmortems with timeline and action items, toil reduction |
| SR3 | Failure modes on AWS, multi-AZ design, RTO/RPO, DR strategies (backup-restore, pilot light, warm standby, multi-site active-active), AWS Backup, cross-region replication, game days and chaos engineering with AWS FIS, dependency failure handling at the infra level |
| SR4 | Load testing with k6, test types (load, stress, soak, spike), test environments and data, reading results (latency percentiles, throughput, saturation), capacity models, quotas and service limits, cost per request |
| SE1 | Shared responsibility, CloudTrail (org trail), AWS Config and conformance packs, GuardDuty (incl. EKS/RDS/S3 protection), Security Hub and FSBP, Inspector, Macie mention, WAF and Shield on ALB/CloudFront, IAM hygiene audits, incident response for a compromised key or instance |
| SE2 | Shift-left model, SAST (CodeQL/Semgrep), SCA/dependency scanning, secret scanning, IaC scanning (Checkov/Trivy config/tfsec), container scanning gates, DAST (ZAP) in pipelines, security gates and exception process, threat modelling for infra changes |
| SE3 | Compliance frameworks we meet with clients (SOC 2, ISO 27001, PCI DSS, Vietnam PDPD/Decree 13), mapping controls to AWS services, AWS Audit Manager and Artifact, evidence collection automation, audit-ready logging and retention, access reviews |
| AR1 | AWS Well-Architected six pillars and reviews, multi-account strategy, Control Tower and landing zone, OU design, account vending, centralized networking (TGW, shared VPC/RAM), centralized logging, architecture decision records for infra |
| AR2 | FinOps lifecycle (inform/optimise/operate), tagging and cost allocation, Cost Explorer, CUR and Athena, budgets and anomaly detection, rightsizing (Compute Optimizer), Savings Plans vs RIs, Spot strategy, storage and data-transfer costs, NAT gateway trap, unit economics |
| AR3 | Platform engineering and team topologies, the platform as a product, golden paths, Backstage (catalog, software templates), self-service infra via templates/modules, developer experience metrics, platform API design |
| AR4 | The 7 Rs, discovery and assessment (Migration Hub, Application Discovery), lift-and-shift with MGN, database migration with DMS, containerising a legacy app, strangler-fig on AWS, cutover planning and rollback |
| AR5 | What senior means (scope, ambiguity, influence), writing design docs/RFCs, reviewing others' infra, mentoring juniors through this program, estimation of infra work, vendor/tool evaluation, stakeholder communication, interviewing DevOps candidates, running the on-call program |
| AR6 | Claude Code and agents for Terraform/K8s authoring, guardrails (plan-only credentials, read-only roles, hooks, sandboxed accounts), MCP servers for AWS/Kubernetes/observability, AI-assisted incident triage, ChatOps, evaluating agent output, what never to delegate |

## Cross-program links
The internship already has light AWS/Docker pages (`../../intern/modules/op2.html`, `op4.html`,
`op5.html`). Link to them only as "lighter intro" pointers; this program is self-contained and must
not depend on them. Application-level patterns (retries, caching, queues) live in intern SD7–SD10:
link `../../intern/modules/sd10.html` etc. instead of re-teaching them.
