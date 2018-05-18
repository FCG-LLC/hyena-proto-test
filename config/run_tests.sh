#!/bin/bash

. ~/.profile
export LANG=C.UTF-8

echo -e "${HYENA_PRIVATE_KEY}" > ~/.ssh/id_rsa; chmod 0600 ~/.ssh/id_rsa
eval $(ssh-agent -s)
ssh-add

make
