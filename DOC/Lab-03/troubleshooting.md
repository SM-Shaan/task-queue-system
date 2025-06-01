## Troubleshooting

### 1. Chocolatey Not Recognized (Windows)

**Error**: `choco : The term 'choco' is not recognized...`

**Solution**:
- Install Chocolatey in PowerShell (Run as Administrator):

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; `
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; `
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

- Verify installation:

```powershell
choco --version
```

- Add Chocolatey to PATH (if needed):

```powershell
$env:Path += ";C:\ProgramData\chocolatey\bin"
```

- Install Pulumi:

```powershell
choco install pulumi -y
```

### 2. Pulumi Access Token Error

**Error**: `error: invalid access token`

**Solution**:
- Log in using browser-based authentication:

```bash
pulumi login
```

- Press `Enter` to open the browser and authenticate.
- Alternatively, use a token from [Pulumi Tokens](https://app.pulumi.com/account/tokens).

### 3. SSH Key Pair Issues

Ensure the `app-key-pair.pub` public key is correctly added to `__main__.py`. Restrict SSH access (port 22) to your IP in production for security.

The resulting system is:
- **Containerized**: Packaged in Docker containers.
- **Cloud-hosted**: Deployed on AWS for high availability.
- **Automated**: Managed with Pulumi's Infrastructure-as-Code.
### 3.  How To access private_ip ?

### 4. ModuleNotFoundError: No module named 'awscli'
This means the Python AWS CLI wrapper isn't installed properly in your system.

If you really want to use Python pip inside a virtual environment:
```bash
pip install awscli
```
Then confirm:

```bash
aws --version
```
But note: this can create conflicts on Windows if you have a global AWS CLI installed separately.

### 5. No instances in aws console:
 Check AWS Region: Make sure you are viewing the correct region (ap-southeast-1) in the AWS Console. Instances created in a different region will not show up.

### 6. Ip address is not working:
```bash
 ssh -i "D:\asynchronous_task_processing_system_using_Flask_Celery_RabbitMQ\pulumi\app-key-pair" ubuntu@13.215.46.60
 ```

You should now see your containers running.
 If You Still Don’t See Containers Running
Check the cloud-init log for errors:
```bash
cat /var/log/cloud-init-output.log
```
This will show if any step in your user_data failed (e.g., git clone, docker-compose).

The resulting system is:
- **Containerized**: Packaged in Docker containers.
- **Cloud-hosted**: Deployed on AWS for high availability.
- **Automated**: Managed with Pulumi's Infrastructure-as-Code.


