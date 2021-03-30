for F in $(ls scss)
do
    F=$(basename $F .scss)
    sass --watch scss/${F}.scss:css/${F}.css &
done
