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

### Installing Node.js

* substitute NODE_VERSION for 14.15.4

```
RUN curl https://raw.githubusercontent.com/creationix/nvm/v0.37.2/install.sh | bash
```

Close and open the terminal


```
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

### Sample Output
```
code
```

## Program Design
* Discuss design approach, solutions, rationale.
