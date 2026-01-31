---
title: "RHEL7 Provisioning"
date: 2014-08-02T19:01:00.004+05:30
author: "Ganesh Pagade"
tags: ["linux", "devops"]
draft: false
---

Recently I had been working on adding support for Red Hat Enterprise Linux 7 (RHEL7 / RHEL 7) baremetal provisioning into our product. There are few changes in the process from RHEL6. Unfortunately, since RHEL7 has GAed recently, there is not much information on the internet regarding a workable kickstart file. This blog describes the challenges that I faced and how I resolved them.

# The Setup

Most likely you would be using virtual environment for doing your research. If you are using VMware vSphere, note the you would need ESX 5.5 for this. Because that's the version which supports RHEL7. Also you would need to use vSphere web client (and not the desktop client) to get the RHEL7 option while VM creation.

This VM, PXE server, TFTP server and DHCP server should be in same network. Mostly you would create a private network as you do not want these servers to interfere with your usual servers (like DHCP server). This can be easily done in vSphere.

With this setup in place, I started my first RHEL7 provisioning job using the existing RHEL6 configurations and kickstart file. Kickstart file contained all the packages that were supported in RHEL6.

# Network Device Error

I provided the kickstart network device (as eth0) and dynamic IP address.

First failure I got was with this warning:

```
dracut-initqueue[679]: Warning: Could not boot.
dracut-initqueue[679]: Warning: /dev/root does not exist
```

And I got the dracut prompt.

![]({{ site.url }}/images/posts/2014-08-02-rhel7-provisioning/dev_root_error.png)

After some investigation, I found that the issue was with the eth0 that I had provided as kickstart network device. RHEL7 renames the device in different format. For ex in above screenshot you would find the name as eno16780032. Providing this name instead of eth0 solved the error. 

You could also use the MAC address but somehow for me it did not work in hyphen format (-). MAC address in colon (:) format worked fine. Ex: XX:XX:XX:XX:XX:XX

# Kickstart File Syntax

Next error was due to the 'key --skip' entry in my kickstart file. Latest Anaconda refuses to recognize this option. I just removed this entry to proceed with my investigation.

Further the setup cribbed about no matching %end for %package in kickstart file. This was allowed earlier but now the format needs you to close the %package, %pre, %post etc with matching %end tag.

Refer [Troubleshooting Kickstart files in RHEL 7](https://access.redhat.com/articles/635573) for more information.

# Web Server Error

When it looked like that I got the kickstart file syntax correct, the installation started giving me following error:
error populating transaction after 10 retries: failure: Packages/libstdc++-4.8.2-16.e17.x86_64.rpm from anaconda: [Errno 256] No more mirrors to try.

![]({{ site.url }}/images/posts/2014-08-02-rhel7-provisioning/error_populating_transaction.png)

Not much help from the error message. This one was tricky to resolve.

The hint was in 'c++'. Why are we getting error for this particular package and not for any other package? Whats so special about c++? The special thing is two consecutive special characters.

My datastore, where the ISO content were located, was accessed through http protocol. For this I was using IIS server. I quickly tried to access above rpm from my browser and there I got the error. The error was only for this rpm and not for any other rpm. Little more investigation and found the root cause.

By default IIS does not allow double escaping of special characters. There is a setting in IIS to enable 'Allow double escaping'. After doing this, my installation proceeded further.

# New RHEL7 Packages

Lastly the setup went into interactive mode for few package groups which were no longer present in RHEL7. Since I was reusing RHEL6 kickstart, I had to make changes in the selected packages to make it run for RHEL7. Complete list of packages that had to be modified from RHEL6 to RHEL7 is as follows:
```
@virtualization  -  @virtualization-hypervisor
@cifs-file-server  -  @file-server
@nfs-file-server  -  @file-server
@mysql    -  @mariadb

@mysql-client  -  @mariadb-client
@server-platform  -  removed
@storage-server  -  removed
@turbogears   -  removed
@basic-desktop   -  removed
@desktop-platform  -  removed
@general-desktop  -  removed
@tex    -  @texlive
```

There are many other packages and there could be other changes in the packages. However we support only few selected packages and hence I had to keep my research limited to the same.

# Automation of Post Install Tasks

You may be interested in executing onetime tasks after the system boots for the first time (similar to run once in Windows). We achieve this by creating a script using echo commands in %post, which is executed after reboot by adding the entry into /etc/rc.d/rc.local.

Somehow this didn't work for RHEL7. The reason was that the /etc/rc.d/rc.local didn't have execute permissions by default. Workaround was to add chmod command in the %post section to give it execution permissions:

`chmod +x /etc/rc.d/rc.local`

Additionally if you intend to execute any 32-bit binary file you would need the correct glibc installed on the system. Following commands in %post did the trick for me:

```
wget http://location_to_iso_extract/Packages/glibc-2.17-55.el7.i686.rpm
rpm -ivh glibc-2.17-55.el7.i686.rpm --nodeps
```

# Sample RHEL7 Kickstart file

Finally here is the sample kickstart file that worked for me. Notes that I focus was on automating the provisioning process and not on providing the best values in the kickstart file. For ex below kickstart has ext3 as the fstype which may not be the preferred choice in real world scenario. Similarly for enablemd5.

```
install
text
timezone --utc Africa/Abidjan
lang en_US
keyboard us
network --bootproto dhcp --device ??NET_DEVICE?? --hostname ??HOST_NAME??
url --url http://??DATA_STORE_IP??/??DATA_STORE.VIRTUAL_DIR??/rhel-server-7.0-x86_64-dvd
firewall --disabled
zerombr 
clearpart --all
bootloader --location=mbr
part / --size 1 --grow --fstype ext3
rootpw --iscrypted ??ROOT_PASSWORD??
auth --useshadow --enablemd5
reboot
%packages
@base
@x11
@web-servlet
@emacs
@network-file-system-client
@legacy-x
@virtualization-hypervisor
@virtualization-platform
@system-admin-tools
@php
@system-management
@security-tools
@graphics
@input-methods
@web-server
@backup-server
@print-client
@console-internet
@file-server
@virtualization-tools
@development
@mail-server
@smart-card
@desktop-debugging
@fonts
@postgresql-client
@core
@performance
@postgresql
@compat-libraries
@directory-server
@dial-up
@mariadb-client
@mainframe-access
@scientific
@graphical-admin-tools
@network-server
@print-server
@directory-client
@remote-desktop-clients
@ftp-server
@network-tools
@debugging
@kde-desktop
@backup-client
@mariadb
@virtualization-client
@perl-runtime
@java-platform
%end
%post
# You can enter commands to perform post install operations here.
%end
```
