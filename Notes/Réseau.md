
## Rasperrybpi

> Nom d'hote: Raspi1
> Ip: 192.168.0.2

Fait tourner un serveur DHCP et sert aussi de routeur.
Config `/etc/dhcp/dhcpd.conf`
`sudo systemctl status isc-dhcp-server`
`cat /var/lib/dhcp/dhcpd.leases`

Possibilité de se connecter en ssh. Sert de passerelle pour le réseau.

Fait tourner un serveur nginx avec page web simple d'état.
Config: ``
Interface simple php: 

## D-link acces point

Configuration par le web: http://192.168.0.50
user: piadmin
mdp: wWdLBcRZV'd2y.5

## réseau:
ssid: raspinet
mdp: 12345678

# DHCP

Configuration :

```
sudo nano /etc/dhcp/dhcpd.conf
```

Actuellement :

```
subnet 192.168.0.0 netmask 255.255.255.0 {
    range 192.168.0.100 192.168.0.199;
    option routers 192.168.0.2;
    option domain-name-servers 1.1.1.1, 8.8.8.8;}
```

Redémarrer :

```
sudo systemctl restart isc-dhcp-server
```

État :

```
sudo systemctl status isc-dhcp-server
```

Voir les baux :

```
cat /var/lib/dhcp/dhcpd.leases
```

# Routage

Vérifier :

```
cat /proc/sys/net/ipv4/ip_forward
```

Doit afficher :

```
1
```

Configuration permanente :

```
cat /etc/sysctl.d/99-router.conf
```

```
net.ipv4.ip_forward=1
```

Recharger :

```
sudo sysctl --system
```

# NAT

Voir les règles :

```
sudo iptables -t nat -L -n -v
```

Voir le forwarding :

```
sudo iptables -L FORWARD -n -v
```

Ajouter les règles :

```
sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADEsudo iptables -A FORWARD -i eth0 -o wlan0 -j ACCEPTsudo iptables -A FORWARD -i wlan0 -o eth0 \    -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
```


## Changer l'adresse IP de `eth0`

Édite le fichier :

```
sudo nano /etc/network/interfaces
```

Tu devrais avoir quelque chose comme :

```
auto eth0iface eth0 inet static
    address 192.168.0.2
    netmask 255.255.255.0
```

Par exemple, pour passer sur `10.0.0.2/24` :

```
auto eth0iface eth0 inet static
    address 10.0.0.2
    netmask 255.255.255.0
```


## Réappliquer la configuration réseau

Le plus simple est de redémarrer le Raspberry :

```
sudo reboot
```

Si tu ne veux pas redémarrer :

```
sudo ifdown eth0sudo ifup eth0
```

(si `ifupdown` est bien installé et utilisé).


# Switch
premiere connection grace à telnet

hostname: switch-RG
vlan 2: admin-switch
mdp config: 2950