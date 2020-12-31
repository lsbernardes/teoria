#!/bin/zsh

[[ -z $1 ]] && echo "Escreva alguma coisa pro commit, idiota!" && exit 1
commit="$@"
git add .
git commit -m "$commit"
git push -u origin main
