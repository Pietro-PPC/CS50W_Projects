# This is a script that iterates through the scss directory
# and watches every file inside it, directing the result css
# codes to the css directory. 

for F in $(ls scss)
do
    F=$(basename $F .scss)
    sass --watch scss/${F}.scss:css/${F}.css &
done
