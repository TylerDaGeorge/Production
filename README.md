# 🛠️ Hybrid Smart Production Scheduler & Gamified Job Board

A modular, scalable, and mobile-friendly smart production planning system designed for CNC machine shops. Combines an adaptive scheduling engine with gamified workflows to improve job visibility, streamline resource allocation, and boost operator engagement.

---

## 🎯 Project Goal

To build a modern shop floor management tool that:
- Optimizes job scheduling using setup time, machine availability, and due dates
- Engages operators with gamification features like points, badges, and leaderboards
- Tracks inventory and material statuses in real time
- Provides mobile access and local-first syncing to ensure uptime and reliability
- Supports managers with analytics, forecasting, and override capabilities

---

## 🧩 Key Features by Development Phase

### ✅ Phase 1: Core Scheduling + Basic Job Board
- APS engine for optimized job scheduling
- Job board UI with drag-and-drop or click-to-claim interface
- Operator login with job claim/release and status updates
- Manager dashboard for job monitoring

### 🕹️ Phase 2: Gamification Layer
- “Hot Job” tagging and job urgency highlights
- Points system and bonus incentives
- Leaderboards and achievement badges
- Notifications for unclaimed or urgent jobs

### 🧠 Phase 3: AI Scheduling + Manager Tools
- LLM assistant for natural language job prioritization
- Auto-suggestions based on operator skill and availability
- Job reassignment and override tools for leads
- Usage analytics for bottleneck detection

### 📈 Phase 4: Operator Performance & Feedback
- Time tracking, scrap rates, personal records
- Coaching suggestions and feedback forms
- Adaptive point system based on output and improvement

### 🏭 Phase 5: Inventory Integration & Forecasting
- Inventory-based job release control
- Auto-reordering alerts
- Forecasting based on customer-provided demand
- Real-time job blockage based on inventory status

### 📱 Phase 6: Mobile App & UX Enhancements
- Responsive or cross-platform app (React Native / Flutter)
- Offline mode with local-first data sync
- Digital work instructions embedded in job cards
- Push notifications for job and point updates

---

## 🧠 System Design Principles

- **Modular UI** for easy future redesigns
- **Local-first architecture** with cloud sync via CouchDB/PouchDB
- **PostgreSQL backend** with real-time updates and conflict resolution
- **Role-based access control** with JWT authentication
- **CI/CD ready** with scalable monolith or microservices architecture

---

## 🛡️ Security & Compliance
- JWT access & refresh tokens
- Role-based access control (RBAC)
- HTTPS enforced, encrypted local storage
- Audit logs for all job claims, overrides, and point updates

---

## 🧪 Testing Strategy
- Unit Testing: Jest / Pytest
- Integration Testing: Cypress / Playwright
- Manual Testing: Weekly sessions with operators
- Staging Environment: Isolated QA with dummy data

---

## 🗃️ Core Database Tables
- `jobs`: Job metadata, status, due dates, claims
- `users`: Login info, roles, points, badges
- `job_history`: Event log of job progress
- `inventory`: Material status and availability
- `performance_records`: Personal output and efficiency stats

---

## 📦 Tech Stack

| Layer         | Tooling/Tech             |
|---------------|--------------------------|
| Frontend      | React / Vue, Tailwind    |
| Mobile App    | React Native / Flutter   |
| Backend       | FastAPI / Express        |
| Database      | PostgreSQL + SQLAlchemy  |
| Sync Engine   | PouchDB / CouchDB        |
| Auth          | JWT + bcrypt             |
| CI/CD         | GitHub Actions / Docker  |
| Forecasting   | Prophet / ARIMA (optional) |

---

## ⚙️ MVP Scope

**Minimum Launch Features**
- Manual job entry from shipping
- Claim/complete jobs with status updates
- Points for completed jobs (no badges/leaderboards yet)
- Operator and department lead dashboards
- Real-time updates via local sync

---

## 👥 Roles and Permissions

| Role            | Permissions Summary                                     |
|-----------------|----------------------------------------------------------|
| **Operator**    | View/claim jobs, update statuses, view points/history   |
| **Dept Lead**   | Assign jobs, override claims, view all stats            |
| **Shipping**    | Request jobs, update material status, flag urgent jobs  |
| **Admin**       | Manage users, system settings, full visibility          |

---

## 📲 Example Workflows

**Operator Workflow**
1. Open app → View job board
2. Claim a job → Mark as "Running"
3. Complete job → Mark as "Finished"
4. Earn points and move to next

**Shipping Workflow**
1. Submit job request with part # and due date
2. Mark material as ordered/received
3. Promote urgent jobs with "Hot" tag

---

## 📊 Gamification Rules

- 🎯 Base Points: Earned per job completed
- 🔥 Bonuses: For urgent jobs and personal bests
- 🏆 Badges: Earned for achievements (coming soon)
- 🍪 Weekly Team Rewards: Based on team performance

---

## 🛠️ Optional Features (Stretch Goals)

- QR code scanning for bin/job sheet lookup
- Integrated time tracking & efficiency metrics
- Chatbot assistant for onboarding and FAQs

---

## 🧰 Developer Setup

```bash
# Clone this repo
git clone https://github.com/your-org/hybrid-production-app.git
cd hybrid-production-app

# Install dependencies for the backend
cd backend
pip install -r requirements.txt

# Run backend tests
pytest
```

## 📚 Available Endpoints
The FastAPI backend currently provides a few in-memory job management endpoints.

| Method | Path            | Description                     |
|-------|-----------------|---------------------------------|
| GET   | `/jobs/`        | List all jobs                   |
| POST  | `/jobs/`        | Create a job `{part_number}`    |
| POST  | `/jobs/claim`   | Claim job `{job_id, username}`  |
| POST  | `/jobs/unclaim` | Unclaim job `{job_id}`          |
| POST  | `/jobs/complete`| Complete job `{job_id}`         |
| GET   | `/jobs/{job_id}`| Retrieve a job by ID            |
| POST  | `/users/`       | Create a user `{username, password}` |
| GET   | `/users/`       | List all users                     |
| GET   | `/users/{username}` | Retrieve a user by username |

