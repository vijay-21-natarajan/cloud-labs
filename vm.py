# vm.py 

'''
sudo apt update
sudo apt install apache2 -y
sudo systemctl enable apache2
sudo systemctl status apache2
sudo nano /var/www/html/index.html
sudo apt install net-tools
ifconfig  

//create and configure

sudo apt install haproxy -y
sudo apt install haproxy -y
// store the below 8 lines in this file : sudo nano /etc/haproxy/haproxy.cfg
frontend http_front
bind *:80
default_backend http_back
backend http_back
balance roundrobin
server vm1 <VM1_IP>:80 check
server vm2 <VM2_IP>:80 check
server vm3 <VM3_IP>:80 check

sudo systemctl restart haproxy
sudo systemctl enable haproxy
sudo systemctl status haproxy
http://<load_balancer_IP>
//load balancer 

nano script.sh
echo “hello Raghav”
Ctrl+O  + enter + Ctrl+X
crontab -e 
*/1****./script.sh>>./output.log
Ctrl+O  + enter + Ctrl+X
cat output.log

'''