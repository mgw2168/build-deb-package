# Building binary deb packages

## Build steps:

```shell
1. mkdir hello_1.0-1_amd64
2. mkdir -p hello_1.0-1_amd64/usr/local/bin
3. cp ~/YourProjects/Hello/hello hello_1.0-1_amd64/usr/local/bin
4. mkdir helloworld_1.0-1_amd64/DEBIAN
5. touch helloworld_1.0-1_amd64/DEBIAN/control
6. dpkg-deb --build --root-owner-group <helloworld_1.0-1_amd64>
```

## Test:
```shell
# install
sudo dpkg -i <package>
# uninstall
sudo dpkg -r <appname>
```

