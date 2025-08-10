# NSED742 - Software Engineering & Design
## Course Submission Documentation

**Course:** NSED742 - Software Engineering & Design  
**Supervisor:** Dr. Silas Verkijika  
**Institution:** University of the Sol Plaatje  
**Academic Year:** 2025  
**Submission Date:** To be confirmed...

---

## 📋 Project Summary

**Project Name:** Tender Insight Hub  
**Project Type:** Semester-long Group Project  
**Team Size:** 5 students  
**Development Duration:** 9 sprints (18 weeks)

### Project Description

Tender Insight Hub is a cloud-native SaaS platform designed to assist South African SMEs in navigating public procurement opportunities. The system leverages AI technology to simplify complex tender documents, provide intelligent analysis, and help businesses assess their readiness to compete for government contracts.

The platform addresses critical challenges faced by SMEs in the public procurement space:
- Complex tender documentation that requires specialized expertise to interpret
- Lack of tools to assess company readiness against tender requirements
- Difficulty in tracking and managing multiple tender opportunities
- Limited collaboration capabilities for teams working on tender applications

## 🎯 Learning Objectives Alignment

### Primary Learning Outcomes

1. **Software Engineering Principles**
   - Applied modern software engineering practices throughout development
   - Implemented clean architecture with separation of concerns
   - Used design patterns (Repository, Factory, Strategy) for scalable solutions
   - Maintained high code quality through peer reviews and testing

2. **Full-Stack Development**
   - Backend development using FastAPI with Python 3.11
   - RESTful API design following OpenAPI specifications
   - Multi-database integration (PostgreSQL + MongoDB)
   - Authentication and authorization implementation

3. **AI/ML Integration**
   - Integrated HuggingFace transformers for document summarization
   - Implemented automated readiness scoring algorithms
   - Document processing and text extraction pipelines
   - AI model evaluation and optimization

4. **Project Management & Collaboration**
   - Agile development methodology with sprint planning
   - Version control using Git with feature branch workflow
   - Team leadership rotation ensuring all members gain management experience
   - Continuous integration and deployment practices

## 📊 Technical Requirements Compliance

### ✅ Mandatory Technology Stack

| Requirement | Implementation | Status |
|-------------|----------------|---------|
| **Backend Framework** | FastAPI 0.100+ | ✅ Implemented |
| **SQL Database** | PostgreSQL 15 | ✅ Implemented |
| **NoSQL Database** | MongoDB 6.0 | ✅ Implemented |
| **Authentication** | JWT with bcrypt | ✅ Implemented |
| **CI/CD** | GitHub Actions | ✅ Implemented |
| **AI Integration** | HuggingFace Models | ✅ Implemented |
| **API Documentation** | Swagger/OpenAPI | ✅ Implemented |

### 🔧 Software Engineering Practices

- **Version Control:** Git with feature branches and pull request workflow
- **Code Quality:** ESLint, Prettier, Black formatter, type hints
- **Testing:** Unit tests (80%+ coverage), integration tests, E2E testing
- **Documentation:** Comprehensive API docs, inline code documentation
- **Security:** Input validation, CORS, error handling, JWT security

## 🏢 Multi-Tenant SaaS Architecture

### Subscription Tiers Implementation

The system implements a sophisticated multi-tenant architecture with three distinct pricing tiers:

#### Free Tier (Proof of Concept)
- 1 user per organization
- 3 tender searches per week (rate limiting implemented)
- Basic search and filtering functionality
- No AI features or advanced analytics

#### Basic Tier (SME Focus)
- Up to 3 users per team
- Unlimited tender searches
- Full AI summarization and readiness scoring
- Collaborative workspace features

#### Pro Tier (Enterprise Ready)
- Unlimited team members
- Complete feature access including report exports
- Advanced analytics and insights
- Priority support and custom integrations

### Multi-Tenancy Implementation
- Database-level tenant isolation
- Programmatic feature restrictions based on subscription tier
- Resource usage tracking and billing preparation
- Scalable architecture supporting thousands of organizations

## 🤖 AI Integration Pipeline

### Document Processing Workflow

1. **Document Ingestion**
   - PDF and DOCX file upload handling
   - Text extraction using pdfplumber and python-docx
   - Content validation and preprocessing

2. **AI Summarization**
   - HuggingFace BART model for extractive summarization
   - Fallback to T5-small for resource-constrained environments
   - 120-word summary limit with key information extraction

3. **Readiness Scoring Algorithm**
   - Company profile to tender requirement matching
   - Weighted scoring system (0-100 scale)
   - Automated checklist generation
   - Actionable recommendations engine

### Model Selection Rationale

- **Primary Model:** `facebook/bart-large-cnn`
  - Optimized for news summarization with excellent coherence
  - Balances quality with computational efficiency
  
- **Fallback Model:** `t5-small`
  - Smaller footprint for resource-constrained deployments
  - Maintained acceptable quality for academic demonstration

## 📈 API Design & Public Access

### Internal API (SaaS Platform)
- Authentication-protected endpoints for platform users
- Multi-tenant data isolation and access control
- Real-time tender search and filtering
- Workspace management and collaboration features

### Public API (Civic Tech Integration)
- Open endpoints for third-party developers
- Government spending analytics for transparency
- Document summarization as-a-service
- Rate-limited access with API key management

### API Documentation Standards
- Complete OpenAPI 3.0 specification
- Interactive Swagger UI for testing
- Code examples in multiple programming languages
- Comprehensive error response documentation

## 🔄 Development Methodology

### Agile Sprint Structure

**Sprint Duration:** 2 weeks  
**Total Sprints:** 9 sprints  
**Sprint Goals:** Feature-focused with clear deliverables

#### Sprint Breakdown

| Sprint | Lead | Focus Area | Key Deliverables |
|--------|------|------------|------------------|
| 1-2 | Sinethemba | Foundation | Project setup, database design, basic API structure |
| 3-4 | Ashwill | Core Features | Tender search, filtering, company profiles |
| 5-6 | Koketso | Infrastructure | CI/CD, deployment, testing framework |
| 7-8 | Onthatile | AI Integration | Document summarization, readiness scoring |
| 9 | Khethiwe | Finalization | Polish, documentation, final testing |

### Leadership Development

Each team member assumes the Team Lead role for specific sprints, ensuring:
- **Distributed Leadership Experience:** All members gain project management skills
- **Knowledge Transfer:** Comprehensive handover between lead transitions
- **Skill Development:** Technical and soft skills across all team members
- **Academic Reflection:** Individual leadership reports documenting experiences

## 📊 Quality Metrics & Standards

### Code Quality Standards
- **Test Coverage:** Minimum 80% unit test coverage
- **Code Style:** PEP 8 compliance with automated formatting
- **Documentation:** Docstring coverage >90% for public methods
- **Type Safety:** Type hints for all function signatures
- **Security:** OWASP compliance with automated vulnerability scanning

### Performance Benchmarks
- **API Response Time:** <2 seconds (95th percentile)
- **Database Query Performance:** <100ms average
- **AI Processing Time:** <30 seconds for document summarization
- **System Availability:** 99.5% uptime target
- **Concurrent User Support:** 1,000+ simultaneous users

## 🌍 Real-World Impact & Validation

### Problem Statement Validation
The project addresses documented challenges in South African public procurement:
- SME participation rates in government tenders remain low
- Complex documentation creates barriers to entry
- Lack of tools for tender readiness assessment
- Limited collaboration platforms for small businesses

### Market Research Integration
- Analysis of existing tender platforms and their limitations
- Stakeholder interviews with SME representatives
- Competitive analysis of international procurement platforms
- Identification of unique value propositions for South African market

### Scalability Considerations
- Cloud-native architecture supporting horizontal scaling
- Database optimization for large-scale tender data processing
- Caching strategies for improved performance
- API rate limiting and resource management

## 📝 Academic Deliverables

### Individual Submissions
1. **Team Lead Reports** (All members)
   - Leadership experience documentation
   - Decision-making rationale
   - Challenge resolution approaches
   - Teamwork and collaboration reflections

2. **Technical Documentation** (Role-specific)
   - System architecture documentation
   - Database design specifications
   - API endpoint documentation
   - Testing strategy and results

### Team Deliverables
1. **Complete Source Code**
   - GitHub repository with comprehensive commit history
   - Feature branch workflow demonstration
   - Code review evidence through pull requests

2. **Deployment Evidence**
   - Live application deployment
   - CI/CD pipeline configuration
   - Performance monitoring setup

3. **Project Documentation**
   - Comprehensive README and setup guides
   - Architecture diagrams and design decisions
   - User manuals and API documentation

## 🎓 Course Requirement Fulfillment

### NSED742 Core Requirements

#### ✅ Technical Implementation
- [x] FastAPI backend development
- [x] Multi-database integration (SQL + NoSQL)
- [x] AI/ML integration with open-source models
- [x] RESTful API design and documentation
- [x] Authentication and authorization
- [x] Multi-tenant SaaS architecture

#### ✅ Software Engineering Practices
- [x] Version control with Git and GitHub
- [x] Continuous integration and deployment
- [x] Comprehensive testing strategy
- [x] Code quality standards and reviews
- [x] Documentation and technical writing

#### ✅ Project Management
- [x] Team-based development with role rotation
- [x] Agile methodology with sprint planning
- [x] Leadership experience for all members
- [x] Collaborative development practices

#### ✅ Innovation & Creativity
- [x] AI-powered document processing
- [x] Automated readiness scoring
- [x] Public API for civic tech integration
- [x] Multi-tenant SaaS business model

## 📈 Expected Learning Outcomes

### Technical Skills Development
- **Backend Development:** Proficiency in Python, FastAPI, and API design
- **Database Management:** SQL and NoSQL database design and optimization
- **AI Integration:** Practical experience with ML models and document processing
- **DevOps Practices:** CI/CD, containerization, and deployment automation

### Professional Skills Development
- **Project Management:** Agile methodology and team leadership
- **Collaboration:** Git workflow, code reviews, and team communication
- **Documentation:** Technical writing and API documentation
- **Problem Solving:** Real-world business problem analysis and solution design

### Academic Achievement Indicators
- Successful implementation of all core features
- Demonstration of software engineering best practices
- Evidence of effective team collaboration and leadership
- Quality of technical documentation and code
- Innovation in AI integration and user experience design

## 🔍 Evaluation Criteria Alignment

This project is designed to meet and exceed the evaluation criteria for NSED742:

1. **Technical Complexity:** Multi-database, AI-integrated, multi-tenant SaaS platform
2. **Software Engineering Quality:** Clean architecture, comprehensive testing, CI/CD
3. **Innovation:** AI-powered tender analysis and automated readiness assessment
4. **Team Collaboration:** Distributed leadership with documented handovers
5. **Real-World Relevance:** Addresses actual challenges in South African procurement

## 📚 References & Resources

### Academic Sources
- Software Engineering best practices and methodologies
- SaaS architecture and multi-tenancy patterns
- AI/ML integration in web applications
- South African public procurement regulations

### Technical Documentation
- FastAPI official documentation and best practices
- PostgreSQL and MongoDB administration guides
- HuggingFace transformers library documentation
- Docker and containerization best practices

### External APIs & Data Sources
- OCDS eTenders API for South African government tenders
- Public procurement data standards and formats
- Open Government Data initiatives

---
