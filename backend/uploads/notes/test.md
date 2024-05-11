---
Document: 世界技能大赛网络系统管理项目精英班训练日志
Author: 黄道金
Role: 教练
Date: 2024.03.12
Subject: Linux
Task: SSH远程登录
---

# SSH远程登录

SSH (Secure Shell) 是一种网络协议，用于加密方式远程登录和操作网络设备，保障数据传输的安全性。通过SSH，用户可以安全地从一个位置访问另一个位置的计算机。

## Training Objectives (训练目标)

### Skill Objectives (能力目标)

- 能够使用SSH客户端远程登录到远程主机。
- 能够生成和使用SSH密钥对。
- 能够配置SSH服务以提高安全性。
- 能够使用SCP和SFTP进行文件传输。 

### Knowledge Objectives (知识目标)

- 理解SSH的工作原理。
- 掌握SSH客户端和服务器的基本使用。
- 掌握SSH密钥对的生成和使用。
- 掌握SSH服务的配置和优化的常见方法。
- 了解SSH的高级功能和配置。

## Training Process and Methods (训练过程与方法)

1. **概念讲解 (Conceptualization)**：介绍SSH的基本概念，包括其工作原理和为何要使用SSH。
2. **案例演示 (Case Demonstration)**: 演示如何使用SSH客户端和服务器进行安全的远程登录。
3. **实际操作 (Hands-on Practice)**: 学员将实践使用SSH进行远程登录，包括生成SSH密钥对。
4. **综合实践 (Integrated Task)**: 配置SSH服务，实施安全策略。
5. **知识延伸 (Knowledge Extension)**: 探讨SSH的高级功能和配置，如端口转发、SSH隧道等。

## Key points (重点)

### Commands (相关命令)

- `ssh`: 远程登录命令。
- `ssh-keygen`: 生成SSH密钥对的命令。
- `ssh-copy-id`: 将本地的SSH公钥复制到远程主机的命令。
- `scp`: 安全的文件传输命令。
- `sftp`: 安全的文件传输协议。

### Files (相关文件)

- `~/.ssh/config`: SSH用户客户端配置文件。
- `/etc/ssh/ssh_config`: SSH全局客户端配置文件。
- `/etc/ssh/sshd_config`: SSH服务配置文件。
- `~/.ssh/id_rsa`, `~/.ssh/id_rsa.pub`: 默认的SSH私钥和公钥文件位置。

## Concepts (基本概念)

- **SSH协议**: 一种加密的网络协议，用于在不安全的网络上进行安全的远程登录和其他安全网络服务。
- **SSH密钥对**: 使用公钥加密技术的一对密钥，包括一个公钥和一个私钥。公钥可安全分享，而私钥必须保密。
- **SSH安全加固**: 通过配置SSH服务，实施安全策略，如禁用密码登录、限制登录用户等。

## Examples (实践案例)

### SSH远程登录与客户端配置

1. Linux客户端使用SSH远程登录
    
    ```bash
    ssh user@remotehost
    ```

> 注意：如果客户端没有安装SSH客户端，可以使用`apt install openssh-client`安装。如果 SSH 服务端没有安装，可以使用`apt install openssh-server`安装 SSH 服务端。

> 注意：`user`是远程主机上的用户名，`remotehost`是远程主机的IP地址或域名。

> 注意：首次登录时，会提示是否接受远程主机的公钥，输入`yes`确认即可。

> 注意：如果远程主机的SSH服务使用非标准22端口，可以使用`-p`参数指定端口号。

> Windows用户可以使用PuTTY, Tabby, MobaXterm, Xshell等SSH客户端工具。

1. SSH客户端配置
    
    ```bash
    vi ~/.ssh/config
    ```
    
    > 如果针对所有用户，可以修改全局配置文件 `/etc/ssh/ssh_config`。

    ```conf
    # web server config
    Host web
        HostName www.example.com
        User demo
        Port 22

    # database server config
    Host db
        HostName 12.34.56.78
        User admin
        Port 2209
        IdentityFile ~/.ssh/id_ed25519
    ```

### SSH客户端使用密钥对登录

1. 客户端生成SSH密钥对
    
    ```bash
    ssh-keygen
    ```

2. 将SSH公钥复制到远程主机
    
    ```bash
    ssh-copy-id user@remotehost
    ```

3. 客户端使用SSH密钥对登录
    
    ```bash
    ssh user@remotehost
    ```
    无需输入密码即可登录。

> 注意：如果使用非默认的密钥文件，可以使用`-i`参数指定密钥文件。


### 使用SSH远程执行命令

```bash
ssh user@remotehost 'cat /etc/issue'
```

### 使用SCP和SFTP进行文件传输

从客户端上传文件到远程主机：

```bash
scp localfile user@remotehost:/path/to/remote
```

从远程主机下载文件到客户端：

```bash
scp user@remotehost:/path/to/remote localfile
```

使用SFTP进行交互式文件传输：

```bash
sftp user@remotehost
sftp> pwd
sfpt> cd /path/to/remote
sfpt> put localfile
sfpt> ls -l
sfpt> get remotefile
sfpt> exit
```

> Windows用户可以使用WinSCP, FileZilla等图形化工具。
    
### SSH服务器端配置

1. 修改SSH服务配置文件
    
    ```bash
    vi /etc/ssh/sshd_config
    ```

SSH服务提供了用户远程登录Linux系统的途径，用户可以通过SSH客户端连接到SSH服务，然后在远程主机上执行命令。所以，SSH服务的安全性非常重要。通过修改SSH服务的配置文件，可以实施一些安全策略，如禁用密码登录、限制登录用户等。常见的SSH服务相关的安全注意事项有：

- 确保SSH客户端软件的安全性。建议使用系统自带的SSH客户端。如果使用第三方SSH客户端，需要确保软件的来源可靠，尽量选择开源软件，且一定要从官方网站下载最新版本。
- 升级SSH服务器软件到最新版本。新版本的SSH协议修复了旧版本的安全漏洞。
- 使用普通用户登录，并且禁用root用户远程登录。需要root权限时，可以通过sudo或su命令临时提升权限。
- 使用密钥登录，禁用密码登录。密钥登录更加安全，因为密钥比密码更难破解。而且，密钥登录不需要输入密码，没有密码被偷窥泄露的风险。
- SSH服务端口号修改。默认的SSH服务端口号是22，这是黑客最先尝试的端口之一。可以修改SSH服务的端口号（使用大于1024的随机端口），增加黑客的攻击难度。
- 限制SSH服务监听的IP地址。只允许特定网络的主机连接到SSH服务。
- 限制登录重试次数。
- 使用防火墙。使用防火墙保护SSH服务的访问。
- 使用应用防火墙(如fail2ban)。应用防火墙可以监控SSH服务的登录失败次数，当登录失败次数达到一定值时，自动封锁攻击者的IP地址。防止暴力破解。

2. 常见的SSH服务配置选项

    ```conf
    # 禁用root用户远程登录
    PermitRootLogin no

    # 禁用密码登录
    PasswordAuthentication no

    # 修改SSH服务端口号
    Port 2209

    # 限制登录用户
    AllowUsers user1 user2

    # 限制SSH服务监听的IP地址
    ListenAddress 192.168.1.101

    # 只监听IPv4
    AddressFamily inet

    # 使用最新的SSH协议
    Protocol 2

    # 使用密钥登录
    RSAAuthentication yes

    # 设置最大登录时长
    LoginGraceTime 1m

    # 限制登录重试次数
    MaxAuthTries 3

    # 设置最大空闲时长
    ClientAliveInterval 300

    # 设置最大空闲次数
    ClientAliveCountMax 0
    
    # 设置最大连接数
    MaxStartups 10:30:60

    # 设置最大并发连接数
    MaxSessions 10

    # 不使用DNS解析
    UseDNS no
    ```

> 注意：如果修改了SSH服务监听的IP地址或端口号，在重启生效之前，一定要确保网络防火墙允许新的端口通过。否则，可能会因为网络防火墙的限制，导致SSH服务无法访问，无法远程登录服务器。
> 
> 同样，如果修改了SSH服务的配置文件，只允许特定用户登录，一定要确保至少有一个用户可以登录。
>
> 一定要确保配置文件的正确性，否则可能会导致SSH服务无法启动，无法远程登录服务器。

3. 重启SSH服务
    
    ```bash
    systemctl restart sshd
    ```

### 查看SSH服务状态

```bash
systemctl status sshd
```

### 查看SSH服务监听的端口

```bash
ss -tunlp | grep ssh
```

### 查看SSH服务的连接数

```bash
ss -ntp | grep sshd
```

### 查看SSH服务的日志

```bash
journalctl -u sshd
```

### 查看用户登录日志

1. 查看用户近期登录记录

    ```bash
    last
    ```

2. 查看用户近期登录失败记录

    ```bash
    lastb
    ```

3. 查看系统内用户近期登录情况

    ```bash
    lastlog
    ```

## Summary (小结)

SSH是一种安全的远程登录协议，可以保障数据传输的安全性。使用SSH远程登录到Linux系统是非常常见的操作，也是系统管理员的基本技能之一。利用SSH服务，可以远程执行命令、传输文件，管理远程主机。学习SSH服务最重要的是要培养信息网络安全意识，掌握SSH服务安全加固的常用方法和配置技巧。


## Exercises (巩固练习)

对SSH服务进行安全加固，实施安全策略：

- 修改SSH服务端口号为8089；
- 只监听内网IP地址；
- 禁止root用户远程登录；
- 禁止密码登录，只允许密钥登录；
- 只允许用户`skills`远程登录； 
- 禁止TCP流量和X11转发。

对SSH客户端进行配置：

- 配置SSH客户端，使得可以通过`ssh web`快速登录到上述远程主机。

## Practices (综合实践)

配置SSH客户端和服务端使用密钥对登录：

- 1个客户端通过SSH密钥对登录到多个远程主机； 
- 多个客户端通过SSH密钥对登录到1个远程主机。

## Expansions (延伸拓展)

- 探索SSH的高级使用，如X11转发、端口转发等。
- rsync命令和服务。

## References (参考资料)

- ssh --help 
- man ssh_config
- man sshd_config
- 《Linux操作系统应用教程(Debian 11)》