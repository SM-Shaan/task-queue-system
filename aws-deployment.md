# Deploying and Testing the Task Queue System on AWS EC2

This guide provides step-by-step instructions to deploy the Task Queue System (a Celery-based application with Flask, RabbitMQ, Redis, and Flower) on a signle AWS EC2 instance and test its functionality. The deployment uses Docker and Docker Compose for containerization.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Launching an EC2 Instance](#launching-an-ec2-instance)
- [Installing Docker and Docker Compose](#installing-docker-and-docker-compose)
- [Transferring Project Files](#transferring-project-files)
- [Configuring the Environment](#configuring-the-environment)
- [Initializing RabbitMQ Queues](#initializing-rabbitmq-queues)
- [Starting the Application](#starting-the-application)
- [Testing the Deployment](#testing-the-deployment)
- [Troubleshooting](#troubleshooting)
- [Production Considerations](#production-considerations)
- [License](#license)

---

## Prerequisites

* An AWS account with access to the EC2 service.
* A key pair (e.g., `my-keyPair.pem`) for SSH access, downloaded to your local machine (e.g., `E:\my-keyPair.pem` on Windows).
* Basic knowledge of AWS, SSH, and Docker.

---

## Step-by-Step Deployment

### 1. Launch an EC2 Instance

* Log in to the AWS Management Console and navigate to the EC2 dashboard.
* Click **Launch Instance**.
* **Name**: Enter a name (e.g., `TaskQueueInstance`).
* **AMI**: Select **Ubuntu 24.04 LTS** (recommended).
* **Instance Type**: Choose `t3.medium` or higher.
* **Key Pair**: Select your key pair (e.g., `my-keyPair`) or create a new one, and download the `.pem` file.

**Network Settings:**

* Create or select a VPC and subnet.

* Configure a security group with inbound rules:

  * SSH (port 22) from your IP or `0.0.0.0/0` (restrict in production).
  * HTTP (port 5000) for Flask.
  * AMQP (port 5672) for RabbitMQ.
  * Redis (port 6379).
  * Flower (port 5555).
  * RabbitMQ Management UI (port 15672) *(optional, remove in production)*.

* **Storage**: Allocate 20-30 GB.

* Click **Launch Instance** and note the **public IP** (e.g., `18.138.255.244`).

### 2. Connect to the EC2 Instance

Navigate to the directory containing your key:

```bash
icacls "D:\key_pair.pem" /inheritance:r
icacls "D:\key_pair.pem" /remove "NT AUTHORITY\Authenticated Users" "BUILTIN\Users" "BUILTIN\Administrators" "NT AUTHORITY\SYSTEM"
icacls "D:\key_pair.pem" /grant:r "%username%:F"
```

> `%USERNAME%` automatically uses your current Windows username.

**Verify the Permissions:**

```bash
icacls key_pair.pem
```

**Attempt SSH Connection:**

```bash
ssh -i "key_pair.pem" ubuntu@13.229.231.177
```

Fix key permissions if prompted (see Troubleshooting).

---

### 3. Install Docker and Docker Compose

**Update the instance:**

```bash
sudo apt update && sudo apt upgrade -y
```

**Install Docker:**

```bash
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu
```

**Log out and back in:**

```bash
exit
ssh -i E:\my-keyPair.pem ubuntu@18.138.255.244
```

**Install Docker Compose:**

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

---

### 4. Transfer Project Files (from CMD)

From your local machine:

```bash
scp -i "D:\key_pair.pem" -r "D:\task-queue-system\Projectfiles" ubuntu@18.138.255.244:/home/ubuntu/Task_queue_system
```

**Verify Transfer:**

```bash
ssh -i "D:\key_pair.pem" ubuntu@52.77.244.13
ls -l /home/ubuntu/Task_queue_system
```

**Adjust the Directory:**

```bash
cd /home/ubuntu/Task_queue_system
mv Projectfiles/* .
rmdir Projectfiles
ls -l
```

---

### 5. Configure the Environment

**Edit the `.env` file:**

```bash
nano .env
```

Add:

```env
RABBITMQ_USER=admin
RABBITMQ_PASS=your_secure_password
```

> Replace `your_secure_password` with a strong password.

---

### 6. Initialize RabbitMQ Queues

Run the initialization script:

```bash
docker-compose -f docker-compose.yml build web
docker-compose -f docker-compose.yml run --rm web python3 init_queues.py
```

Expected output:

```
Created queue: default
Created queue: high_priority
...
Successfully initialized all queues
```

---

### 7. Start the Application

```bash
docker-compose -f docker-compose.yml up -d
docker ps
```

You should see containers for: `rabbitmq`, `redis`, `web`, `worker`, `data_worker`, `email_worker`, `file_worker`, and `flower`.

---

### 8. Reboot the Instance

```bash
sudo reboot
```

**Reconnect and restart containers:**

```bash
ssh -i E:\my-keyPair.pem ubuntu@18.138.255.244
cd /home/ubuntu/My_web
docker-compose -f docker-compose.aws.yml up -d
```

---

## Testing the Deployment

### 1. Verify Services

**Flask API:**

* From EC2 instance:

```bash
curl http://localhost:5000/
```

* From local machine:

```bash
curl http://18.138.255.244:5000/
```

Expected output:

```json
{"status": "ok", "message": "Task Processing System API", ...}
```

**Flower:**

* Open [http://18.138.255.244:5555/](http://18.138.255.244:5555/) in browser.

**RabbitMQ Management UI:**

* Open [http://18.138.255.244:15672/](http://18.138.255.244:15672/) (username: `admin`, password: from `.env`).

### 2. Test Task Submission

```bash
curl -X POST http://18.138.255.244:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"task_type": "data_processing", "priority": "high", "parameters": {"data": "test"}, "delay": 0}'
```

> Note the returned `task_id` (e.g., `{"task_id": "1234-5678", ...}`).

### 3. Check Task Status

```bash
curl http://18.138.255.244:5000/api/tasks/<task_id>
```

Expected output:

```json
{"status": "completed", "result": ...}
```

---

## Troubleshooting

**SSH Permission Denied:**
Fix key permissions:

```bash
icacls E:\my-keyPair.pem /inheritance:r
icacls E:\my-keyPair.pem /remove "NT AUTHORITY\Authenticated Users" "BUILTIN\Users" "BUILTIN\Administrators" "NT AUTHORITY\SYSTEM"
icacls E:\my-keyPair.pem /grant:r "DESKTOP-RN29TTL\Shaan:F"
```

**Install `python3-venv`:**

```bash
sudo apt update
sudo apt install python3.12-venv
```

**Create & Activate Virtual Environment:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Install dependencies:**

```bash
pip install requests
```

**ModuleNotFoundError:**
Avoid host installation; use Docker container method as shown.

**Container Failures:**

```bash
docker logs <container-id>
```

> While testing the web address, ensure VPN is turned **off**.

**Reconnect After Network Loss:**

```bash
ssh -i "D:\key_pair.pem" ubuntu@52.77.244.13
cd /home/ubuntu/Task_queue_system
python3 -m venv venv
source venv/bin/activate
```

**Port Issues:**
Ensure EC2 security group allows inbound access to:

* Port 5000 (Flask)
* Port 5555 (Flower)
* Port 15672 (RabbitMQ UI)
* Port 5672 (AMQP)
* Port 6379 (Redis)

---

## Production Considerations

* Restrict security group ports (e.g., 5672, 6379, 5555) to the VPC or specific IPs.
* Use EBS for persistent storage of `rabbitmq_data` and `redis_data`.
* Store credentials in AWS Secrets Manager.
* Set up CloudWatch for monitoring.
* Consider Auto Scaling or AWS ECS for scalability.

---

## License

\[Add your license here, e.g., MIT License]
