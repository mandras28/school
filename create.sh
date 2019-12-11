if ( [[ $# -lt 3 ]] || [[ $1 != class && $1 != pupil ]] || [[ $1 == class && $# -ne 3 ]] || [[ $1 == pupil && $# -ne 7 ]] )
then
	echo usage: 
	echo "	" $0 class '<class_name>' '<class_master_name>'
	echo or
	echo "	" $0 pupil '<new_id>|next' '<class_name>' '<family_name>' '<first_name>' '<birth_date>' '<birth_place>'
	exit 1
fi

type=$1
id=$2

if [[ $type == class ]]
then
	master=$3
	curl --insecure -w "%{http_code}\n" --request POST --url https://127.0.0.1:5000/${type}/${id}\?master=${master}
elif [[ $type == pupil ]]
then
	class_name=$3
	family_name=$4
	first_name=$5
	birth_date=$6
	birth_place=$7
	curl --insecure -w "%{http_code}\n" --request POST --url https://127.0.0.1:5000/${type}/${id}\?class_name=${class_name}\&family_name=${family_name}\&first_name=${first_name}\&birth_date=${birth_date}\&birth_place=${birth_place}
fi
