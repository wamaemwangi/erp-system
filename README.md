# ERP System - Complete Business Management Platform

A production-ready Enterprise Resource Planning (ERP) system built with Python/Django. Supports 6 business modules with multi-level approval workflows, complete audit trails, and a REST API.

## Live Demo
*Coming soon - Deploying to PythonAnywhere*

## Features

### 🏢 HR Module
- Leave application with 4-tier approval (HOD → HR → Manager → GM)
- Overtime tracking and approval
- Leave balances and history

### 📦 Procurement Module
- Store requisitions with multi-level approval
- Purchase requisitions with itemized requests
- Posting and receiving workflows

### 💰 Finance Module
- Petty cash requests with line items (max 3,000 KES)
- Imprest requests (minimum 3,001 KES)
- Salary advance requests
- Posting and surrender workflows

### 🚚 Fleet Module
- Transport requisitions
- Work tickets
- Fuel requisitions

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Django 6.0, Django REST Framework |
| Frontend | Bootstrap 5, HTML, CSS, JavaScript |
| Database | SQLite / PostgreSQL |
| Authentication | Django Auth |

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/petty-cash/` | Petty cash requests |
| `/api/imprest/` | Imprest requests |
| `/api/leaves/` | Leave applications |
| `/api/store-requisitions/` | Store requisitions |
| `/api/purchase-requisitions/` | Purchase requisitions |
| `/api/salary-advance/` | Salary advances |
| `/api/transport/` | Transport requisitions |
| `/api/work-tickets/` | Work tickets |
| `/api/dashboard/stats/` | Dashboard statistics |

## Installation

```bash
# Clone the repository
git clone https://github.com/wamaemwangi/erp-system.git

# Navigate to project directory
cd erp-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run the server
python manage.py runserver




### Step 6: Paste into README.md

1. Click on `README.md` in VSCode (it will be empty)
2. Paste the content above (Ctrl+V)
3. Save the file (Ctrl+S)

---

### Step 7: Commit and push in GitHub Desktop

1. Go back to **GitHub Desktop**
2. You'll see `README.md` listed as a changed file
3. At the bottom left, type a summary: `Add professional README`
4. Click **"Commit to main"**
5. Click **"Push origin"** (top button)

---

### Step 8: Verify

Go back to: `https://github.com/wamaemwangi/erp-system`

Refresh the page. You should see your README displayed beautifully!

---

**Try these steps. Tell me when you see the README on your GitHub page!** 🚀

---

Author
Eddie Wamae Mwangi

GitHub: @wamaemwangi

Email: eddiewamae163@gmail.com

---
