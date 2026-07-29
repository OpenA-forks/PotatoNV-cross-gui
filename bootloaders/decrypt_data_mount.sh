#!/bin/bash

# patterns for search encryption params
re_pat_1=',fileencryption=aes-256-xts:aes-256-cts'
re_pat_2=',encryptable=footer'

# list of fstab files specified for target kirin cpu
ven_stat=`cat /proc/mounts | grep /vendor`
fstab_hi=`echo /vendor/etc/fstab.hi*`

case $1 in
--help | -h)
	echo ""
	echo " Usage: decrypt_data_mount.sh [hiXXX|fstabXXXX|/path/to/fstab]"
	echo ""
	exit
	;;
*/*   ) fstab_hi="$1" ;;
fstab*) fstab_hi="/vendor/etc/$1" ;;
hi*   ) fstab_hi="/vendor/etc/fstab.$1" ;;
*)
	echo ""
	echo "wrong argument [$1]"
	echo ""
	exit
	;;
esac

if [[ "$ven_stat" = *' ro,'* ]]; then
	echo "Remount /vendor with read/write permissions"
	mount -o remount,rw '/vendor'
fi

decrypt_data() {
	local fstab_file="$1"
	if [ ! -f "$fstab_file" ]; then
		echo "file '$fstab_file' - not exist!"
	else
		local dat=`cat "$fstab_file" | grep ' /data '`
		if [[
			! -z `echo "$dat" | grep "$re_pat_1"` ||
			! -z `echo "$dat" | grep "$re_pat_2"`
		]]; then
			echo "Remove encryption for userdata from '$fstab_file'"
			sed -i -e "s/$re_pat_1//" -e "s/$re_pat_2//" "$fstab_file"
			chmod 0644 "$fstab_file"
		else
			echo "Non encrypted userdata in '$fstab_file'"
		fi
	fi
}

decrypt_data "$fstab_hi"
