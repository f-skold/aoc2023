#!/bin/sh

cd ~/src/aoc2023
day="$(date +"%d")"

touch "testdata/test_${day}.txt"
touch "testdata/data_${day}.txt"
[ ! -e "code/d${day}_1.py" ] && ( sed "s:12:$day:g" code/template_with_class.py > "code/d${day}_1.py" )

if git status ; then
    git add "testdata/test_${day}.txt" "testdata/data_${day}.txt" "code/d${day}_1.py"
    git commit -m "Empty files added for day $day"
fi
