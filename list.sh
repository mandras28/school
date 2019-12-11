if [ $# -ne 2 ]
then
	echo usage: $0 '<type>' '<id>'
	exit 1
fi

type=$1
id=$2

curl --insecure -w "%{http_code}\n" --request GET --url https://localhost:5000/${type}/${id}
