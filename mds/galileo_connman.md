# Intel Galileo开发版PCI-e无线网卡wifi配置

由于网上很多配置wifi的方式在我的伽利略开发板上都行不通，最后终于找到这个可以用的“冷门”办法：

## 系统配置

开发板： Intel Galileo gen2
无线网卡：PCI-e intel wifi link 5100
开发板系统： EGLIBC based Linux([download](https://software.intel.com/en-us/iot/hardware/galileo/downloads))


## 所用工具

#### 硬件：
usb无线网卡或者pci-e接口的无线网卡。
（注意如果你用的是和我一样的pci-e网卡，注意顺便买来天线接上，不然信号贼弱，这种网卡不接天线是不行的。）

#### 软件：
comman(开发板的完整版linux已经内置)

> 参考:
>
>《connman百度百科》( http://baike.baidu.com/link?url=3C6RQqswxVvGMxNy7XA1-bWUBU6W0G7_Rvvsv2DRyv04nontgZ9oX7MRgeeNvMuRmjRMqf75_tqspSgjhb8Ysa )

## 步骤
1. shell下：`connmanctl`，之后跳出"connmanctl>"提示符，之后的connman操作就在这个提示符后操作
2. `connmanctl> enable wifi`，应该反馈`Enabled wifi`
3. `connmanctl> scan wifi`, 反馈`Scan completed for wifi`
4. `connmanctl> services`,此时会列出已经搜索到的wifi，样子像下边这样：
~~~
rip and run guest network wifi_c8f733840a94_72697020616e642072756e206775657374206e6574776f726b_managed_psk
    ripandrunbaby        wifi_c8f733840a94_726970616e6472756e62616279_managed_psk
    SVPMeterConnectWiFi  wifi_c8f733840a94_5356504d65746572436f6e6e65637457694669_managed_none
                         wifi_c8f733840a94_hidden_managed_psk
    HOME-86DF            wifi_c8f733840a94_484f4d452d38364446_managed_psk
    xfinitywifi          wifi_c8f733840a94_7866696e69747977696669_managed_none
    Tnd home             wifi_c8f733840a94_546e6420686f6d6520_managed_psk
    ALBNETNEW            wifi_c8f733840a94_414c424e45544e4557_managed_psk
    aatblt-guest         wifi_c8f733840a94_616174626c742d6775657374_managed_none
    aatblt               
    。
    。
    。
~~~
5.找到你要链接的wifi之后，复制对应信息，并退出connman(`connmanctl> exit`)
6.编辑wifi.config文件来配置自动链接 `sudo vi /var/lib/connman/wifi.config`,写入类似下边的内容并保存：
（注意名字不能改，就是wifi.config）

~~~bash
[service_wifi_c8f733840a94_726970616e6472756e62616279_managed_psk]
Type = wifi
Security = wpa2
Name = ripandrunbaby
Passphrase = yourpass
~~~

这样，开机时板子就会搜索相应的wifi自动登陆了。

> 参考:
> 
> 《connman: wifi configuration》( https://github.com/IntelOpenDesign/MakerNode/wiki/connman:-wifi-configuration )
> 《Connecting to a Wi-Fi Network》( https://software.intel.com/en-us/node/519955 )