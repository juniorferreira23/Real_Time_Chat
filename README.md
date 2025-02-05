# Real-Time Chat with Python

## 📖 Description and Goal  
This project aims to practice knowledge of client-server architecture using Python's socket library and parallelism with threading.  

---

## 💻 Technologies  
- **Python**: Version 3.12.3  

## Libraries  
- **Socket**  

---

## ✨ Features  
- **Run Server**: Starts the TCP (IPv4) socket server.  
- **Listen and Send Messages**: Both the server and clients communicate through the configured port.  
- **Broadcast**: The server replicates a message sent by a client to other clients in the same room.  
- **Custom Message Sending**: Clients send personalized chat messages.  

---

## 🛠 Installation  

### ✅ Requirements  
1. **Python**: Make sure Python is installed on your system. [Download Python](https://www.python.org/downloads/)  
2. **Git**: Install Git to clone the repository. [Download Git](https://git-scm.com/downloads)  

### 🔄 Clone the Repository  
Open your terminal (Bash, PowerShell, or CMD) and run the following command:  
```bash
git clone https://github.com/juniorferreira23/Real_Time_Chat.git
```

### ▶️ Running the Code  
```bash
python3 server.py
```

Then, run a client or as many as you want:  
```bash
python3 client.py
