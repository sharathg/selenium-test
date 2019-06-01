echo "*** Python Version (Should be 3.4+)***"
python3 -V
echo ""
echo ""
echo "*** Run Tests ***"
declare -a browserlist=("chrome" "firefox")
for browser in "${browserlist[@]}"
do
    export BROWSER=${browser}
    echo ""
    echo "Performing Tests on ${browser}"
    echo ""
    python3 testRunner.py ${browser}
done