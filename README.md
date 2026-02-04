# 🌱 Adaptive Nutrition Site

**AdaptiveNutritionSite** is a web platform designed to automate school meal selection for primary school students. It reduces teachers' administrative workload and provides the school cafeteria with accurate production data, helping minimize food waste and errors.

---

## 🎯 Project Goal

The platform aims to:

- Automate meal selection and reporting for primary school students.
- Reduce administrative tasks for teachers and staff.
- Ensure accurate, real-time meal data for cafeteria planning.

---

## 📝 Key Features

- **Student/Parent Interface:** Simple weekly meal selection with a single click per day. Designed for young students.
- **Teacher/Admin Dashboard:** Displays student responses, generates weekly class summaries automatically.
- **Cafeteria Reporting:** One-click export to Excel with detailed and aggregated reports.
- **Roles & Permissions:** Supports Student/Parent, Teacher, Administrator, and Cafeteria staff roles.
- **Automated Data Handling:** Eliminates manual collection and consolidation. Manages dietary restrictions and allergies.

---

## 💻 Technology Stack

- **Backend:** Python / Django (MVC architecture)
- **Frontend:** Django Templates (HTML, CSS, JavaScript)
- **Database:** PostgreSQL
- **Excel Reporting:** openpyxl library
- **Security:** Role-based authentication, compliant with GDPR/FZ-152

---

## ⚡ User Stories

- **Parent:** Quickly select meals for my child in one place and be sure the teacher receives it automatically.
- **Teacher:** Automatically generate weekly class meal summaries without manual consolidation.
- **Cafeteria Manager:** Access accurate school-wide meal data to plan preparation efficiently.

---

## 🏗 System Design

- **Database:** Relational PostgreSQL with normalized tables for Classes, Students, Dishes, DailyMenus, and WeeklyBreakfasts.
- **One-to-One Mapping:** Each student has one active weekly selection to avoid duplicates.
- **User Interface (UX/UI):** Minimalist, intuitive, and role-specific. Parents/students see a simple weekly menu; teachers/admins see dashboards with summaries.
- **Automated Modules:**
  - **Pooling:** Collects and validates student meal choices.
  - **Export to Excel:** Generates detailed class and school-wide reports with highlights for easy reading.

---

## 📊 Benefits

- Saves teachers up to 3 hours per week.
- Provides accurate, standardized reports for classrooms and the school.
- Ensures dietary restrictions and allergies are respected.
- Reduces food waste by 15–25%.
- Scalable and extendable for multiple schools.

---

## 🔒 Security & Compliance

- Role-based authentication and permissions.
- Compliant with GDPR and Russian FZ-152 for student data.
- Reliable authorization system.

---

