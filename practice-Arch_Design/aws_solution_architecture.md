# AWS Solution Architecture - SAP Infrastructure Migration

## Executive Summary

This document presents a comprehensive AWS solution architecture for migrating SAP infrastructure from on-premises to AWS cloud. The solution is designed to host a multi-tier SAP environment across Development, Quality, and Production landscapes while ensuring cost optimization, high availability, and security.

## SAP Infrastructure Context Guide

### What is SAP?

**SAP** = Systems, Applications, and Products in Data Processing
- German enterprise software company that builds software for managing business operations (finance, HR, supply chain, sales, manufacturing, etc.)
- Flagship product: SAP ERP (Enterprise Resource Planning)

### SAP Infrastructure Components

#### In IT Infrastructure Context
When we say SAP server or SAP system, we mean:

1. **SAP Application Server (App Layer)**
   - Runs the business logic (e.g., finance transaction, HR payroll process)
   - Users connect here via SAP GUI or web

2. **SAP Database Server (DB Layer)**
   - Stores all the business data (e.g., customer records, invoices)
   - In our sheet, the DB is SAP HANA (an in-memory DB)

3. **SAP Presentation Layer**
   - User interface (SAP GUI, Fiori, or browser)

### Server Type Breakdown

#### Server Type Column Meaning

**Primary APP** → This EC2 instance is used to host only the application layer (SAP application servers).

**Database** → Dedicated EC2 instance for DB only (HANA in our sheet).

**APP + DB** → 2-Tier setup → one EC2 instance runs both SAP Application + HANA DB together.

**Quality / Production / Development** → Environment labels, telling whether the instance is for Dev, QA, or Prod.

#### Mapping to AWS EC2

**Primary APP:**
- EC2 instance with SUSE OS, no HANA DB installed
- Acts as SAP Application server
- Usually connects to a separate DB EC2 instance

**Database:**
- EC2 instance sized for DB workload (RAM/SSD heavy)
- HANA DB installed
- No app server

**APP + DB:**
- EC2 instance where both layers run together
- Common in smaller / dev / test landscapes
- Not recommended for large Production systems (scaling issues)

**Backup:**
- EC2 instance or EBS snapshot / S3 bucket for backup purposes
- Depends on architecture (can be external backup server)

#### Tier Clarification

**2-Tier:**
- App + DB in one EC2 instance
- Used for small deployments, non-Prod

**3-Tier:**
- Separate App Server EC2 + DB EC2 (and sometimes Web Dispatcher/Firewall as 3rd)
- Used for large Production setups

### BOM Interpretation

**In your sheet:**
- Rows with Primary APP = SAP App servers (EC2)
- Rows with Database = Dedicated DB servers (EC2 with HANA)
- Rows with APP+DB = 2-Tier combined instances

**Project Structure:**
Each row = one server instance (on cloud = one EC2 VM)
All rows together = the complete SAP landscape for that project

**Why so many servers for 1 project?**
Because an SAP project is big and needs different environments:
- **Development (DEV)** → where developers build
- **Quality/Testing (QA)** → for testing
- **Production (PRD)** → live environment for business users
- **Backup/DR** → safety copy

### Currency Conversion Reference

**USD to INR Conversion** (as of current exchange rates):
- 1 USD ≈ ₹88.01 (mid-market rate)
- USD 2,577 ≈ ₹226,772 (rounded to nearest rupee)

*Note: This is the mid-market rate—actual rates from banks or money transfer services may include markup or fees.*

## 1. Requirement Analysis

### 1.1 BOM Analysis

The provided Bill of Materials (BOM) includes:

| Component | Environment | Server Type | vCPU | RAM (GB) | SSD (GB) | Storage (GB) | OS | DB | QTY |
|-----------|-------------|-------------|------|----------|----------|--------------|----|----|-----|
| Firewall | - | - | - | - | - | - | - | - | 1 |
| Development | Primary APP | 4 | 31 | 59 | - | SUSE 12 SP4 | - | 1 |
| Development | Database | 6 | 94 | 450 | - | SUSE 12 SP4 | HANA | 1 |
| Development | APP+DB | 4 | 23 | 59 | - | SUSE 12 SP4 | HANA | 2 |
| Production | Primary APP | 6 | 47 | 59 | - | SUSE 12 SP4 | - | 1 |
| Production | Database | 8 | 125 | 450 | - | SUSE 12 SP4 | HANA | 1 |
| Production | APP+DB | 4 | 31 | 59 | - | SUSE 12 SP4 | HANA | 2 |
| Quality | Primary APP | 4 | 31 | 58 | - | SUSE 12 SP4 | - | 1 |
| Quality | Database | 6 | 94 | 350 | - | SUSE 12 SP4 | HANA | 1 |
| Backup | - | - | - | - | - | 2000 | - | - | 1 |

**Total Resources:** 50 vCPUs, 514 GB RAM, 1,662 GB SSD, 2,000 GB Storage

### 1.2 Core Components Identification

#### Compute Requirements
- **Total Instances:** 10 cloud servers + 1 firewall
- **vCPU Range:** 4-8 cores per instance
- **Memory Range:** 15-125 GB RAM per instance
- **Operating System:** SUSE 12 SP4 (SAP certified)

#### Storage Requirements
- **Root Storage:** 58-450 GB SSD per instance
- **Backup Storage:** 2,000 GB additional storage
- **Database Storage:** High-performance storage for HANA databases

#### Database Requirements
- **SAP HANA:** 6 instances across environments
- **Memory-optimized:** High RAM requirements (up to 125 GB)

#### Networking & Security
- **Firewall:** Network security appliance
- **Multi-tier:** Separation between app and database layers

## 2. AWS Services Mapping

### 2.1 Compute Services

| BOM Component | AWS Service | Instance Type | Justification |
|---------------|-------------|---------------|---------------|
| Primary APP (Dev) | EC2 | m5.2xlarge | 8 vCPU, 32 GB RAM |
| Database (Dev) | EC2 | r5.2xlarge | 8 vCPU, 64 GB RAM, memory-optimized |
| APP+DB (Dev) | EC2 | m5.xlarge | 4 vCPU, 16 GB RAM |
| Primary APP (Prod) | EC2 | m5.2xlarge | 8 vCPU, 32 GB RAM |
| Database (Prod) | EC2 | r5.4xlarge | 16 vCPU, 128 GB RAM |
| APP+DB (Prod) | EC2 | m5.2xlarge | 8 vCPU, 32 GB RAM |
| Primary APP (Quality) | EC2 | m5.2xlarge | 8 vCPU, 32 GB RAM |
| Database (Quality) | EC2 | r5.2xlarge | 8 vCPU, 64 GB RAM |
| Firewall | EC2 | c5.large | 2 vCPU, 4 GB RAM |

### 2.2 Storage Services

| Requirement | AWS Service | Configuration |
|-------------|-------------|---------------|
| Root Volumes | EBS gp3 | 100-500 GB per instance |
| HANA Data | EBS io2 | High IOPS for database performance |
| Backup Storage | S3 Standard | 2 TB initial capacity |
| Archive Storage | S3 Glacier | Long-term backup retention |

### 2.3 Networking Services

| Component | AWS Service | Purpose |
|-----------|-------------|---------|
| Virtual Network | VPC | Isolated network environment |
| Subnets | Public/Private Subnets | Multi-tier architecture |
| Load Balancing | Application Load Balancer | Traffic distribution |
| Security | Security Groups/NACLs | Network-level security |
| Connectivity | VPN/Direct Connect | Hybrid connectivity |

### 2.4 Security Services

| Requirement | AWS Service | Implementation |
|-------------|-------------|----------------|
| Firewall | AWS WAF + Security Groups | Network security |
| Identity Management | IAM | Access control |
| Encryption | KMS | Data encryption at rest |
| Monitoring | CloudWatch + CloudTrail | Security monitoring |
| Backup | AWS Backup | Automated backup solution |

## 3. Solution Architecture Design

### 3.1 High-Level Architecture

```
[Users] → [Route 53] → [CloudFront] → [Application Load Balancer]
                                              ↓
[Public Subnet: WAF + Firewall (EC2)] → [Private Subnet: SAP App Servers]
                                              ↓
[Database Subnet: SAP HANA Servers] ← [S3 Backup Storage]
```

### 3.2 Environment-Specific Architecture

#### Development Environment
- **APP Server:** 1x m5.2xlarge (Primary APP)
- **Database:** 1x r5.2xlarge (HANA DB)
- **Combined:** 2x m5.xlarge (APP+DB)

#### Quality Environment
- **APP Server:** 1x m5.2xlarge (Primary APP)
- **Database:** 1x r5.2xlarge (HANA DB)

#### Production Environment
- **APP Server:** 1x m5.2xlarge (Primary APP)
- **Database:** 1x r5.4xlarge (HANA DB)
- **Combined:** 2x m5.2xlarge (APP+DB)
- **High Availability:** Multi-AZ deployment

### 3.3 Well-Architected Framework Implementation

#### Security
- VPC with private subnets for database tier
- Security groups for network segmentation
- IAM roles for service access
- Encryption at rest and in transit
- AWS WAF for web application firewall

#### Reliability
- Multi-AZ deployment for production
- Automated backups and snapshots
- Health checks and auto-recovery
- Cross-region backup for DR

#### Cost Optimization
- Right-sizing based on actual requirements
- Reserved Instances for predictable workloads
- Automated scheduling for dev/test environments
- S3 lifecycle policies for backup data

#### Performance Efficiency
- Memory-optimized instances for HANA
- High IOPS storage for databases
- CloudFront for content delivery
- Auto Scaling for application tiers

#### Operational Excellence
- CloudWatch monitoring and alerting
- AWS Systems Manager for patch management
- Infrastructure as Code (CloudFormation)
- Automated backup and recovery procedures

#### Sustainability
- Right-sizing to avoid over-provisioning
- Scheduled shutdown of non-production environments
- Use of latest generation instances for better efficiency

## 4. Cost Optimization & Pricing Models

### 4.1 Instance Pricing Comparison (Monthly)

#### On-Demand Pricing
| Instance Type | Qty | Unit Price | Monthly Cost |
|---------------|-----|------------|--------------|
| m5.xlarge | 2 | $140 | $280 |
| m5.2xlarge | 5 | $280 | $1,400 |
| r5.2xlarge | 2 | $365 | $730 |
| r5.4xlarge | 1 | $730 | $730 |
| c5.large | 1 | $53 | $53 |
| **Total** | **11** | | **$3,193** |

#### 1-Year Reserved Instance (No Upfront)
| Instance Type | Qty | Unit Price | Monthly Cost | Annual Savings |
|---------------|-----|------------|--------------|----------------|
| m5.xlarge | 2 | $97 | $194 | 31% |
| m5.2xlarge | 5 | $194 | $970 | 31% |
| r5.2xlarge | 2 | $253 | $506 | 31% |
| r5.4xlarge | 1 | $506 | $506 | 31% |
| c5.large | 1 | $37 | $37 | 30% |
| **Total** | **11** | | **$2,213** | **31%** |

#### 3-Year Reserved Instance (No Upfront)
| Instance Type | Qty | Unit Price | Monthly Cost | Annual Savings |
|---------------|-----|------------|--------------|----------------|
| m5.xlarge | 2 | $66 | $132 | 53% |
| m5.2xlarge | 5 | $132 | $660 | 53% |
| r5.2xlarge | 2 | $172 | $344 | 53% |
| r5.4xlarge | 1 | $344 | $344 | 53% |
| c5.large | 1 | $25 | $25 | 53% |
| **Total** | **11** | | **$1,505** | **53%** |

### 4.2 Storage and Additional Services

| Service | Monthly Cost |
|---------|-------------|
| EBS Storage (2 TB) | $200 |
| S3 Standard (2 TB) | $46 |
| Data Transfer | $100 |
| Load Balancer | $25 |
| **Total Additional** | **$371** |

### 4.3 Total Cost Comparison

| Pricing Model | Compute | Storage & Services | **Total Monthly** | **Annual Cost** |
|---------------|---------|-------------------|-------------------|-----------------|
| On-Demand | $3,193 | $371 | **$3,564** | **$42,768** |
| 1-Year RI | $2,213 | $371 | **$2,584** | **$31,008** |
| 3-Year RI | $1,505 | $371 | **$1,876** | **$22,512** |

## 5. Final Recommendation

### 5.1 Recommended Approach: Hybrid Pricing Strategy

1. **Production Environment:** 3-Year Reserved Instances
   - Predictable workload with continuous operation
   - Maximum cost savings (53%)

2. **Development/Quality:** 1-Year Reserved Instances
   - Moderate usage with scheduled shutdowns
   - Balanced flexibility and savings (31%)

3. **Testing/Spike Capacity:** On-Demand Instances
   - Unpredictable usage patterns
   - Pay only when needed

### 5.2 Projected Annual Savings
- **Total Annual Cost:** $28,500 (hybrid approach)
- **Savings vs On-Demand:** $14,268 (33% reduction)

## 6. Implementation & Migration Plan

### 6.1 Migration Strategy: Lift and Shift with Optimization

#### Phase 1: Assessment and Planning (Weeks 1-2)
1. **Current Environment Assessment**
   - Document existing SAP landscape
   - Identify dependencies and integrations
   - Performance baseline establishment
   - Security and compliance requirements

2. **AWS Account Setup**
   - Create AWS Organizations structure
   - Set up billing and cost management
   - Configure IAM policies and roles
   - Establish VPC and networking foundation

#### Phase 2: Infrastructure Provisioning (Weeks 3-4)
1. **Network Configuration**
   ```
   VPC Creation → Subnet Design → Security Groups → Route Tables
   ```

2. **Compute Resources**
   ```
   EC2 Instance Launch → EBS Volume Configuration → OS Installation
   ```

3. **Security Implementation**
   ```
   WAF Configuration → Security Groups → IAM Roles → Encryption Setup
   ```

#### Phase 3: SAP Installation and Configuration (Weeks 5-6)
1. **Development Environment**
   - Install SAP HANA database
   - Configure application servers
   - System connectivity testing
   - Performance optimization

2. **Quality Environment**
   - Replicate development configuration
   - Configure system refresh procedures
   - Testing and validation

#### Phase 4: Production Migration (Weeks 7-8)
1. **Production Setup**
   - Install production SAP systems
   - Configure high availability
   - Implement backup procedures
   - Security hardening

2. **Data Migration**
   - Database export/import
   - Application data transfer
   - Validation and testing
   - Performance tuning

#### Phase 5: Cutover and Go-Live (Week 9)
1. **Pre-Cutover Activities**
   - Final data synchronization
   - DNS updates preparation
   - Rollback procedures verification
   - Communication plan execution

2. **Cutover Execution**
   - Maintenance window start
   - Final data migration
   - System startup and validation
   - User acceptance testing
   - Go-live confirmation

#### Phase 6: Post-Migration Support (Weeks 10-12)
1. **Monitoring and Optimization**
   - Performance monitoring setup
   - Cost optimization review
   - Security assessment
   - Operational procedures documentation

2. **Knowledge Transfer**
   - Team training on AWS services
   - Documentation handover
   - Support procedures establishment
   - Lessons learned documentation

### 6.2 Risk Mitigation

| Risk | Impact | Mitigation Strategy |
|------|--------|-------------------|
| Data Loss | High | Multiple backup copies, validation procedures |
| Extended Downtime | High | Thorough testing, rollback procedures |
| Performance Issues | Medium | Load testing, performance optimization |
| Security Vulnerabilities | High | Security assessment, compliance validation |
| Cost Overrun | Medium | Cost monitoring, reserved instance planning |

### 6.3 Success Criteria

1. **Technical Success**
   - All SAP systems operational in AWS
   - Performance meets or exceeds current baseline
   - Zero data loss during migration
   - Security compliance maintained

2. **Business Success**
   - Minimal business disruption (<8 hours downtime)
   - Cost reduction achieved (minimum 30%)
   - Improved system reliability and availability
   - Enhanced disaster recovery capabilities

## 7. Monitoring and Maintenance

### 7.1 Monitoring Strategy

#### CloudWatch Metrics
- CPU, Memory, Disk utilization
- Network performance
- Application response times
- Database performance metrics

#### Custom Monitoring
- SAP-specific metrics
- Business transaction monitoring
- User experience metrics
- License utilization tracking

### 7.2 Maintenance Procedures

#### Regular Maintenance
- OS patching (monthly)
- SAP system updates (quarterly)
- Security updates (as needed)
- Performance optimization (monthly)

#### Backup and Recovery
- Daily incremental backups
- Weekly full system backups
- Monthly backup testing
- Quarterly disaster recovery testing

## 8. Conclusion

The proposed AWS solution architecture provides a robust, scalable, and cost-effective platform for hosting SAP infrastructure. The hybrid pricing strategy delivers significant cost savings while maintaining the flexibility needed for varying workload demands. The phased migration approach minimizes business risk while ensuring a smooth transition to the cloud.

**Key Benefits:**
- 33% cost reduction compared to on-demand pricing
- Enhanced reliability and availability
- Improved disaster recovery capabilities
- Scalable architecture for future growth
- Comprehensive security implementation

**Next Steps:**
1. Approve the proposed architecture and migration plan
2. Initiate AWS account setup and initial infrastructure provisioning
3. Begin detailed migration planning and scheduling
4. Start team training on AWS services and best practices