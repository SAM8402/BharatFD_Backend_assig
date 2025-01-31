# Backend

---

# FAQ Management System

This is a Django-based FAQ Management System that supports multilingual content, WYSIWYG editor integration, and a REST API for managing FAQs. It also includes caching for improved performance and automated translations using the Google Translate API.

---

## **Table of Contents**
1. [Installation](#installation)
2. [API Usage](#api-usage)
3. [Contribution Guidelines](#contribution-guidelines)

---

## **Installation**

Follow these steps to set up the project locally:

### **Prerequisites**
- Python 3.9 or higher
- Redis (for caching)
- Docker (optional, for containerized deployment)

### **Steps**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/faq-management-system.git
   cd faq-management-system
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

7. **Start Redis**:
   - On Linux/macOS:
     ```bash
     sudo apt install redis-server
     redis-server
     ```
   - On Windows:
     Use Docker or a precompiled Redis binary (see [Redis Installation Guide](#redis-installation-guide)).

8. **Access the Application**:
   - Admin Panel: `http://127.0.0.1:8000/admin`
   - API Endpoint: `http://127.0.0.1:8000/api/faqs/`

---

## **API Usage**

The REST API supports the following operations:

### **List All FAQs**
- **Endpoint**: `GET /api/faqs/`
- **Example**:
  ```bash
  curl -X GET "http://127.0.0.1:8000/api/faqs/"
  ```

### **Filter FAQs by Language**
- **Endpoint**: `GET /api/faqs/?lang=<language_code>`
- **Supported Languages**: `en` (English), `hi` (Hindi), `bn` (Bengali)
- **Example**:
  ```bash
  curl -X GET "http://127.0.0.1:8000/api/faqs/?lang=hi"
  ```

### **Create a New FAQ**
- **Endpoint**: `POST /api/faqs/`
- **Example**:
  ```bash
  curl -X POST "http://127.0.0.1:8000/api/faqs/" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Django?", "answer": "Django is a web framework."}'
  ```

### **Update an FAQ**
- **Endpoint**: `PUT /api/faqs/<id>/`
- **Example**:
  ```bash
  curl -X PUT "http://127.0.0.1:8000/api/faqs/1/" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Django?", "answer": "Django is a Python web framework."}'
  ```

### **Delete an FAQ**
- **Endpoint**: `DELETE /api/faqs/<id>/`
- **Example**:
  ```bash
  curl -X DELETE "http://127.0.0.1:8000/api/faqs/1/"
  ```

---

## **Contribution Guidelines**

We welcome contributions! Please follow these guidelines to contribute to the project:

### **1. Fork the Repository**
- Fork the repository to your GitHub account.

### **2. Clone the Forked Repository**
```bash
git clone https://github.com/your-username/faq-management-system.git
cd faq-management-system
```

### **3. Create a New Branch**
```bash
git checkout -b feature/your-feature-name
```

### **4. Make Your Changes**
- Follow PEP8 guidelines for Python code.
- Write unit tests for new features or bug fixes.

### **5. Commit Your Changes**
- Use clear and descriptive commit messages.
- Follow the [Conventional Commits](https://www.conventionalcommits.org/) format:
  ```bash
  git commit -m "feat: Add multilingual FAQ model"
  git commit -m "fix: Improve translation caching"
  git commit -m "docs: Update README with API examples"
  ```

### **6. Push Your Changes**
```bash
git push origin feature/your-feature-name
```

### **7. Create a Pull Request**
- Go to the original repository and create a pull request.
- Provide a detailed description of your changes.

### **8. Code Review**
- Your pull request will be reviewed by the maintainers.
- Address any feedback or requested changes.

---

## **Redis Installation Guide**

### **Linux/macOS**
1. Install Redis:
   ```bash
   sudo apt install redis-server
   ```
2. Start Redis:
   ```bash
   redis-server
   ```

### **Windows**
1. **Using WSL**:
   - Install WSL and a Linux distribution (e.g., Ubuntu).
   - Follow the Linux instructions above.

2. **Using Docker**:
   - Install Docker Desktop.
   - Run Redis in a container:
     ```bash
     docker run -d --name redis -p 6379:6379 redis
     ```

3. **Using Memurai**:
   - Download and install [Memurai](https://www.memurai.com/).
   - Start the Memurai server.

---

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Acknowledgments**
- [Django](https://www.djangoproject.com/) for the web framework.
- [django-ckeditor](https://github.com/django-ckeditor/django-ckeditor) for WYSIWYG editor support.
- [googletrans](https://pypi.org/project/googletrans/) for automated translations.

---
