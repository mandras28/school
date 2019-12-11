#! /bin/bash
error_file=$1
name=$2
script=$3
requested_result=$4
outfile=$requested_result.ERROR

# echo test case ${name@Q} started.
# echo run $script
./$script >$outfile
# echo check $requested_result
if ( cmp -s $requested_result $outfile )
then
	rm $outfile
	echo test case ${name@Q} '[OK]'
else
	echo $name >>$error_file
	echo test case ${name@Q} '[ERROR]'
	echo requested: $requested_result '<>' output: $outfile
	diff $requested_result $outfile
fi
# echo test case ${name@Q} done.
# echo
