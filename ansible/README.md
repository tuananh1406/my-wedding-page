### ANSIBLE AUTO DEPLOY HỆ THỐNG WEBSITE CÁ NHÂN
## Các tags hiện  có
* install-systemd: Cài đặt website lên server mới
# Ansible-playbook:
```shell
ansible-playbook -i hosts webserver.yml -l <host_name> -t <tag_name>
hoặc
ansible-playbook -i hosts webserver.yml -t <tag_name>
```

        - Trong đó: 
                host_name: tên hoặc ip của server trong file host
                tag_name: tên tag cần chạy
