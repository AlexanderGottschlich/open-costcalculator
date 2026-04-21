# Test-Pläne für Plan-Vergleiche

Die Test-Pläne dienen zum Vergleichen verschiedener AWS-Setups mit dem `--compare` Flag.

## Verwendung

```bash
# Einzelner Plan
python src/main.py --plan plan/<plan-name>.plan.json

# Vergleich zweier Pläne
python src/main.py --plan plan/<plan1>.plan.json --compare plan/<plan2>.plan.json
```

---

## 📦 Compute

### EKS Fargate vs EKS EC2
```bash
python src/main.py --plan plan/eks-fargate.plan.json --compare plan/eks-ec2.plan.json
```
| Datei | Beschreibung |
|-------|-------------|
| `eks-fargate.plan.json` | EKS mit Fargate (serverless) |
| `eks-ec2.plan.json` | EKS mit eigenen EC2 Nodes |

### ECS Fargate vs EC2 Single
```bash
python src/main.py --plan plan/ecs-fargate.plan.json --compare plan/ec2-single.plan.json
```
| Datei | Beschreibung |
|-------|-------------|
| `ecs-fargate.plan.json` | ECS Fargate Container |
| `ec2-single.plan.json` | Einzelne EC2 Instanz |

---

## 💾 Datenbank

### RDS Single-AZ vs Multi-AZ
```bash
python src/main.py --plan plan/rds-single-az.plan.json --compare plan/rds-multi-az.plan.json
```
| Datei | Beschreibung |
|-------|-------------|
| `rds-single-az.plan.json` | RDS Single-AZ |
| `rds-multi-az.plan.json` | RDS Multi-AZ |

---

## 🌐 Networking

### ALB Only
```bash
python src/main.py --plan plan/alb.plan.json
```
| Datei | Beschreibung |
|-------|-------------|
| `alb.plan.json` | Application Load Balancer |

### NAT Gateway
```bash
python src/main.py --plan plan/nat-gateway.plan.json
```
| Datei | Beschreibung |
|-------|-------------|
| `nat-gateway.plan.json` | NAT Gateway |

---

## 🗄️ Storage

### S3 Standard
```bash
python src/main.py --plan plan/s3-standard.plan.json
```
| Datei | Beschreibung |
|-------|-------------|
| `s3-standard.plan.json` | S3 Bucket (Standard) |

---

## 🔄 Kombinations-Vergleiche

### EKS Fargate + RDS vs EKS EC2 + RDS
```bash
# Kombiniere first, dann vergleiche
python src/main.py --plan plan/eks-fargate.plan.json
# Mit RDS
```

### Full Stack Vergleich
```bash
# EKS Fargate + RDS
python src/main.py --plan plan/eks-fargate-rds.plan.json --compare plan/eks-ec2-rds.plan.json
```

---

## ✅ Bestehende Pläne

| Datei | Beschreibung |
|-------|-------------|
| `terraform-ecs.plan.json` | ECS Fargate (Original) |
| `terraform-eks.plan.json` | EKS mit Node Group |
| `terraform-fargate.plan.json` | EKS Fargate |
| `terraform-lb.plan.json` | ALB only |
| `terraform-loadbalancer.plan.json` | ALB only (neu) |
| `terraform-spot.plan.json` | EKS Spot Nodes |
| `terraform-sf2l.plan.json` | Vollständige App |

---

## Getestete Vergleiche

1. **EKS Fargate vs Terraform-Fargate**: ✅ Funktioniert
2. **ECS Fargate vs EKS Fargate**: ✅ Funktioniert  
3. **ALB only**: ✅ Funktioniert
4. **EKS vs ECS**: ✅ Funktioniert