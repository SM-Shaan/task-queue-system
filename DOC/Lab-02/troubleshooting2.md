## Troubleshooting

**SSH Permission Denied:**
Fix key permissions:

```bash
icacls E:\key-pair.pem /inheritance:r
icacls E:\key-pair.pem /remove "NT AUTHORITY\Authenticated Users" "BUILTIN\Users" "BUILTIN\Administrators" "NT AUTHORITY\SYSTEM"
icacls E:\key-pair.pem /grant:r "DESKTOP-RN29TTL\Shaan:F"
icacls E:\key-pair.pem /inheritance:r
icacls E:\key-pair.pem /remove "NT AUTHORITY\Authenticated Users" "BUILTIN\Users" "BUILTIN\Administrators" "NT AUTHORITY\SYSTEM"
icacls E:\key-pair.pem /grant:r "DESKTOP-RN29TTL\Shaan:F"
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
