EGGS_DIR=../eggs/
if [ -d eggs ];then
    EGGS_DIR=./eggs/
fi

for x in `ls $EGGS_DIR`; 
do  
    A=${x%%-*};B=${x%%-py*};C=${B##*-}; 
    echo "    '$A=$C',"; 
done
