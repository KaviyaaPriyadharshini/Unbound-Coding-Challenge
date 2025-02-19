# Unbound Chat Routing System  
*A lightweight chat UI integrated with a secure Django backend for routing prompts to simulated language models.*

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Demo](#demo)
- [Contributors](#contributors)

---

## Overview
This project is part of the **Unbound Coding Challenge**, where the goal is to develop a modular chat application with regex-based routing logic. The system allows users to interact with a **simulated language model provider**, dynamically routing requests based on predefined policies.

---

## Features
Fetch and display available **LLM models** from the database.  
Process user **chat prompts** and generate responses.  
**Regex-based routing** to redirect requests to alternative models.  
**Admin Portal** to manage routing policies.  
**File Upload Support** for special routing cases.  
Modular Django backend with PostgreSQL integration.  

---

## Tech Stack
### **Backend**
- **Django** (Python Web Framework)
- **Django REST Framework (DRF)** (For API development)
- **sqlite3** (Database for storing models & regex rules)

### **Frontend**
- **HTML, CSS, JavaScript** (Minimal chat UI)
- **Bootstrap / Tailwind CSS** (For styling)

