## Generating SSL certificates
### With Open SSL (slow)
[Stack Overflow Post](https://stackoverflow.com/questions/29458548/can-you-add-https-functionality-to-a-python-flask-web-server)
```console
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```
### With certbot (fast)
[Tutorial](https://pimylifeup.com/raspberry-pi-ssl-lets-encrypt/)
```console
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install certbot
certbot certonly --standalone -d example.com -d www.subdomain.example.com
sudo ls /etc/letsencrypt/live/example.com/
```
