# risc64Specs
Spec files to build rpm packages for container support feodora33
some of them are the same from fedora x86_64 
but there are some other that has some modification to provide support for riscv64

# some config
To avoid warnings 
```
cat /etc/containerd/config.toml 
#root = "/var/lib/containerd"
#state = "/run/containerd"
#subreaper = true
#oom_score = 0

#[grpc]
#  address = "/run/containerd/containerd.sock"
#  uid = 0
#  gid = 0

#[debug]
#  address = "/run/containerd/debug.sock"
#  uid = 0
#  gid = 0
#  level = "info"

disabled_plugins = ["cri", "zfs", "aufs"]
```
If you have network issues 
```
[root@fedora-riscv ~]# cat /etc/docker/daemon.json 
{
   "userland-proxy": false
}
```
or
```
[root@fedora-riscv ~]# cat /etc/sysconfig/docker 
# /etc/sysconfig/docker

# Modify these options if you want to change the way the docker daemon runs
OPTIONS=" --log-driver=journald \
  --live-restore \
  --default-ulimit nofile=1024:1024 \
  --init-path /usr/libexec/docker/docker-init 
"
```



# some images to test 
- https://hub.docker.com/repository/docker/mmarcrr/fedora33-riscv64
- https://hub.docker.com/repository/docker/mmarcrr/ubuntu-focal-riscv64


## todo
The container support is tested and run over riscv64 but I need to add some modifications to avoid manual configuration 
 
