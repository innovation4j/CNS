echo "df -h"
sudo df -h /dev/nvme*
echo "ls -alh"
sudo ls -alh /var/log/sys*
echo ""
echo "delete syslog"
sudo sh -c 'cat /dev/null > /var/log/syslog'
echo "remove syslog.*"
sudo rm -rf /var/log/syslog.*
echo ""
echo "df -h"
sudo df -h /dev/nvme*
echo "ls -alh"
sudo ls -alh /var/log/sys*
