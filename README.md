# Project 2, Temperature Sensor System Simulator, 2nd Phase

## Team
* Roberto Baquerizo
* Zach Turner


## Project Summary
* Fill in project summary and goals here.

## Language and Environment Description
* Python 3.8.5
* node v14.15.4 (npm v6.14.10)
* MySQL ver 14.14 distrib 5.7.32

### Node packages
These are the packages used by our project and specified by the `package.json` file in the Node project.
* mysql
* @types/mysql
* nodemon

### Installing Node.js

1. On a new terminal, execute:
```
curl https://raw.githubusercontent.com/creationix/nvm/v0.37.2/install.sh | bash
```
2. Close and open the terminal
3. In new terminal, execute:
```
NODE_VERSION=14.15.4
nvm install $NODE_VERSION && nvm alias default $NODE_VERSION && nvm use default
```

#### Example versions

```
zturner@DESKTOP-07LOS04:/mnt/c/grad-school/eid/eid-project-2$ node -v
v14.15.4
zturner@DESKTOP-07LOS04:/mnt/c/grad-school/eid/eid-project-2$ npm -v
6.14.10
zturner@DESKTOP-07LOS04:/mnt/c/grad-school/eid/eid-project-2$ nvm -v
0.37.2
```

### Installing MySQL

Link for reference: [Install MySQL Tutorial](https://medium.com/@alef.duarte/cant-connect-to-local-mysql-server-through-socket-var-run-mysqld-mysqld-sock-155d580f3a06)

The latest version of MySQL is in the APT repository, which makes installing it easy.

```
sudo apt update
sudo apt install mysql-server
```

To start the local server, run this command:
```
sudo /etc/init.d/mysql start
```

#### Example Version
```
mysql  Ver 14.14 Distrib 5.7.32, for Linux (x86_64) using  EditLine wrapper
```

#### Setting up Sensor User
:information_source: Replace `sensor` below with username.
```
$ sudo mysql
mysql> CREATE USER 'sensor'@'localhost' IDENTIFIED BY 'balderdash';
mysql> GRANT ALL PRIVILEGES ON * . * TO 'sensor'@'localhost';
mysql> FLUSH PRIVILEGES;
mysql> quit;
```

#### Configuring Database

### Running Server Code
:information_source: if executing for the first time, ensure that the required node modules are installed:
```
npm install
```
To start the sensor simulation server, execute:
```
npm start <NUMBER OF SENSORS>
```

## Program Design
* Discuss design approach, solutions, rationale.


## Resources Referenced
* https://www.freecodecamp.org/news/node-js-child-processes-everything-you-need-to-know-e69498fe970a/
* https://www.digitalocean.com/community/tutorials/how-to-create-a-new-user-and-grant-permissions-in-mysql
* https://www.sitepoint.com/using-node-mysql-javascript-client/