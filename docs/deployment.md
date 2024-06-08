# Deploying to AWS EC2

On **EC2** Dashboard -> Lauch an instance

- Name
- Amazon Machine Image (AMI)
- Instance type
- Create new key pair (Key pair type: RSA, Private key file format:.pem)
- Allow SSH traffic from Anywhere
- Allow HTTPS traffic from the internet
- Allow HTTP traffic from the internet
- User data

        #!/bin/bash
        echo "export VAR_NAME=value" >> /etc/profile

Connect to instance -> SSH client

- Open an SSH client.
- Locate your private key file. The key used to launch this instance is <your_file_name>.pem
- Run this command, if necessary, to ensure your key is not publicly viewable. `chmod 400 "<your_file_name>.pem"`
- Connect to your instance using its Public DNS:

        ssh -i "<your_file_name>.pem" <your_instance_domain>

Update and install dependences

        sudo apt-get update
        sudo apt install -y python3-pip nginx

Create configuration file `sudo vim /etc/nginx/sites-enabled/fastpai_nginx` with these content bellow and save `:wd`

        server {
            listen 80;
            server_name <your_ipv4_public_address>;
            location / {
                    proxy_pass http://127.0.0.1:8000;
                }       
            }

Enable the configuration: `sudo service nginx restart`

Clone and install requirements `pip install -r requirements.txt --break-system-packages`

Run app `python3 -m uvicorn main:app`

Access the application via `http://<your_public_ip_address>/`

Keep server running on EC2 instance after ssh is terminated `nohup bash your_server_script.sh &`
