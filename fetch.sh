spath1=20190404-VB/01_本部/01_VB／Excel
spath2=20190404-VB/02_店舗/01_VB／Excel
dpath=copy
for i in $(cat source2.txt)
do 
	j=$(echo $i | sed 's/#/\//g' |sed 's/\\/\//g')
	if [ -f $spath2/$j ]
	then
		mkdir -p $dpath/$spath2/$(dirname $j)
		cp $spath2/$j $dpath/$spath2/$(dirname $j)
	#fpath=$(find $spath2 |grep -i "$j") 
	#if [ -f $fpath ]
	#then
	#	mkdir -p $dpath/$(dirname $fpath)
	#	cp $fpath $dpath/$fpath
	elif [ -f $spath1/$j ]
	then
		mkdir -p $dpath/$spath1/$(dirname $j)
		cp $spath1/$j $dpath/$spath1/$(dirname $j)
	else
		echo $j 'Not found'
		find $spath2 |grep -i "$j"
	fi
done
