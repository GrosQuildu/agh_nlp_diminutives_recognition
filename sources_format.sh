#!/bin/bash

targets=(
'./rozpoznawaczek'
'./tests'
)

for target in "${targets[@]}"; do
  echo "Do magic stuff in $target"

  echo 'isort fix imports'
  isort --recursive --atomic "$target"
  echo '-----------------------'

  echo 'pyflakes errors'
  pyflakes "$target"
  echo '-----------------------'

  echo 'mypy checks'
  mypy "$target"
  echo '-----------------------'

  echo 'autopep8 formatting'
  for file in "$target"/*.py; do
      start_line=$(grep '# fmt: on' "$file" -n | head -n1 | cut -d':' -f1)
      if [ -z "$start_line" ]; then
          start_line=1
      fi
      autopep8 -r -i --range $start_line 9999999 "$file"
  done
  echo '*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~'
  echo ''
done