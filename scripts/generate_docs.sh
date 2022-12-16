#!usr/bin/bash 

while true; do
    read -p "Which format you want to generate (html/pdf/all)?" choice
    case $choice in 
        [html,h]* ) echo "Generating HTML docs ..." &&
                  echo "You'll find the generated HTML at docs/build/html/index.html" &&
                  cd docs && make html;;
                  
        [pdf,p]* )  echo "Generating PDF docs ..." &&
                  sphinx-build -b pdf docs/source docs/build/pdf &&
                  echo "You'll find the generated PDF at docs/build/pdf";;

        * ) echo "Generating HTML/PDF docs ..." &&
                  cd docs &&
                  make html && 
                  sphinx-build -b pdf ./source ./build/pdf && 
                  echo "You'll find the generated HTML at docs/build/html/index.html" &&
                  echo "You'll find the generated PDF at docs/build/pdf";;
    esac
    break
done
