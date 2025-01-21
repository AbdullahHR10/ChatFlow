![ChatFlow](https://github.com/user-attachments/assets/e8946bd6-1f2a-4e3c-a777-c3e2d49fdcf1)

# ChatFlow

ChatFlow is a real-time messaging application designed to help users connect seamlessly through individual and group chats. It features a sleek dark interface for sending messages, sharing files, and staying updated with real-time notifications, making communication efficient and engaging.

---

# 📑 Table of Contents

- [🎯 Project Inspiration](#-project-inspiration)
- [🧠 Why ChatFlow Matters](#-why-chatflow-matters)
- [🧩 Challenges](#-challenges)
- [✨ Features](#-features)
- [🔍 Additional Highlights](#-additional-highlights)
- [⚙️ Installation](#️-installation)
- [🎥 Usage](#-usage)
- [💻 Technologies Used](#-technologies-used)
- [👨‍💻 Developer](#-developer)
- [📄 License](#-license)

---

# 🎯 Project Inspiration
ChatFlow began as an idea to create a messaging platform that bridges the gap between simplicity and functionality. As someone inspired by modern messaging apps like WhatsApp, I wanted to design an application that integrates real-time messaging, group chats, and notifications while maintaining a sleek and intuitive user interface. The goal was to create a platform that feels natural and efficient for users.

# 🧠 Why ChatFlow Matters
ChatFlow is built to provide a seamless messaging experience that prioritizes speed, reliability, and user engagement. Unlike generic messaging platforms, ChatFlow focuses on offering features like real-time notifications, customizable user profiles, and group chat capabilities in one cohesive app. It’s more than just a messaging app—it’s designed to make communication effortless and enjoyable.

# 🧩 Challenges
Real-Time Features
Implementing real-time messaging with Socket.IO posed significant challenges, especially when managing connections for multiple users and handling room-based interactions for both individual and group chats. Ensuring messages sync instantly across devices while maintaining server performance required careful optimization.

Group Chat Functionality
Managing group dynamics—such as creating groups, adding/removing members, and handling group notifications—introduced complexities in both the database schema and user interface. Designing an efficient backend that supports these features while keeping the UI intuitive was a key focus.

UI Design
Building a dark-themed interface that is both functional and visually appealing required constant iterations. Balancing aesthetic elements like tooltips, shadows, and a minimalistic layout with user experience (UX) standards was crucial to ensure ChatFlow feels modern and user-friendly.

# ✨ Features  

- #### **💬 Private Chats:** Start one-on-one conversations with friends, complete with real-time messaging and delivery indicators.  

- #### **👥 Group Chats:** Create and manage group chats, add or remove members, and engage in group conversations effortlessly.  

- #### **🤝 Friends List:** Browse and manage your friends list to quickly start a conversation or create group chats.  

- #### **🖼️ Profile Customization:** Personalize your profile with a custom picture, username, bio, and social media links.  

---

# 🔍 Additional Highlights  

- #### **🌗 Themes (Dark & Light):** Choose between a sleek, modern dark theme or a clean, minimal light theme to suit your preference.  

- #### **📂 Sidebar Navigation:** Intuitive navigation through the app, with a dynamic sidebar that loads different views seamlessly.  

---

# ⚙️ Installation
To get started with ChatFlow, follow these steps:

### Prerequisites

- Ensure you have **Python 3.8** or higher installed on your system.  
- Install and set up **MySQL** for database management:  
  - Create a database named `chatflow_db`.  
  - Ensure you have a MySQL user with access to this database.  

---

### Setup

#### Clone the Repository  

```bash
git clone https://github.com/yourusername/ChatFlow.git
```

Navigate to the Project Directory

```bash
cd ChatFlow
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Configure the Database
Open the config.py file.

Update the database connection settings with your MySQL credentials:

```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://<username>:<password>@localhost/chatflow_db'
```

Initialize the Database

```bash
flask db upgrade
```

This script will create all necessary tables in the chatflow_db database.

Run the Application

```bash
python3 app.py
```

The application will be available at http://localhost:5000 by default.

---


---

# 🎥 Usage
For a quick overview of how to use ChatFlow, watch the demo video below:

[https://youtu.be/_54sPXuVyeo?si=nX9P09atjKgvECjJ](https://youtu.be/04C-2YXay2c )

---

# 💻 Technologies Used

### Languages

- #### **Python:** The primary language used for backend development. (PEP8)
  Style: PEP 8 or pycodestyle.
- #### **HTML:** For structuring the web pages.
- #### **CSS:** For styling the web pages.
- #### **JavaScript:** For adding interactivity to the web application.
  Style: semi-standard.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

### Technologies
- #### **Flask:** Web framework for building the web application.
- #### **MYSQL:** Database used for storing application data.
- #### **Jinja2:** Templating engine used for rendering HTML.

![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)
![Jinja](https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black)

---
# 👨‍💻 Developer
### **Abdullah Hussein**

Hi, I'm Abdullah Hussein, a passionate coding enthusiast and graduate student at ALX. Coding has been a central part of my journey, and I take pride in the projects I've worked on, including ChatFlow. This project showcases my ability to build functional and impactful applications, reflecting my skills and dedication to the craft.

- Email: [AbdullahH.Ragab10@gmail.com](mailto:AbdullahH.Ragab10@gmail.com)
- LinkedIn: [Abdullah Hussein](https://www.linkedin.com/in/abdullah-hussein-061039280/)
- Twitter: [Abdullah Hussein](https://x.com/AbdullahHR20)

---

# 📄 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
