#! /bin/bash

run_server_script=./run_server.sh
error_file=error.lst
test_case_file=test_case.lst
server_start_wait=3  # [sec]

echo testing REST server $prog_file.
echo check wether server is running:
./list.sh class all >/dev/null 2>&1
result=$?
if [[ $result -ne 0 ]]
then 
	echo server is NOT running ':-('
	echo let\'s start it!
	$run_server_script $prog_file >/dev/null 2>&1 &
	echo waiting $server_start_wait sec ...
	sleep $server_start_wait
	echo check again wether server is running:
	./list.sh class all >/dev/null 2>&1
	result=$?
	if [[ $result -ne 0 ]]
	then
		echo cannot start server $result ':-('
		exit 2
	fi
	echo server has been started successfully ':-)'
else
	echo server is up ':-)'
fi

echo run test cases ...
echo
>$error_file
<$test_case_file xargs -L 1 ./test_case.sh $error_file
echo
echo all $(wc -l <$test_case_file) test cases DONE, $(wc -l <$error_file) 'ERROR(S)' found.
echo
