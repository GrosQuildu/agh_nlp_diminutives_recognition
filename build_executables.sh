#!/bin/bash

# 0a. use setup.py to install [DEV] requirements
# pip install -e '.[DEV]'

# 0b. install UPX for ELF compression
# sudo apt install upx-ucl

# BUILD_WINE=yes
# 0c. build docker with wine, python3 and pyinstaller
# git clone https://github.com/webcomics/pywine && cd pywine && docker build -t pywine .

# 1. create ELF with PyInstaller
ELF=./dist/rozpoznawaczek

if [ ! -f "$ELF" ]; then
    echo 'Building ELF'
    pyinstaller --strip --log-level INFO --onefile ./rozpoznawaczek/rozpoznawaczek.py
else
    echo 'Skipping ELF build'
fi

if [ ! -f "$ELF" ]; then
    echo 'ELF file not generated.'
    exit 1
elif [ -z "$(file $ELF | grep ELF)" ]; then
    echo 'Generated file is not ELF'
    exit 1
fi

# 2. create EXE/PE32 with PyInstaller inside docker
if [ ! -z "$BUILD_WINE" ]; then
    PE32=./dist/rozpoznawaczek.exe

    if [ ! -f "$PE32" ]; then
        echo 'Building EXE/PE32'
        docker run -w="/nlp" --mount type=bind,source="$(pwd)",target=/nlp pywine \
            wine pyinstaller --log-level INFO --onefile ./rozpoznawaczek/rozpoznawaczek.py
    else
        echo 'Skipping EXE/PE32 build'
    fi

    if [ ! -f "$PE32" ]; then
        echo 'EXE/PE32 file not generated.'
        exit 1
    elif [ -z "$(file $PE32 | grep PE32)" ]; then
        echo 'Generated file is not EXE/PE32'
        exit 1
    fi

    # 3. create polyglot script with ELF and EXE/PE32 inside
    # Bash and Batch polyglot from https://gist.github.com/prail/24acc95908e581722c0e9df5795180f6
    # NOT IMPLEMENTED
fi

# 3. create EXE/PE32 in virtual machine or smthing

# 4. cleanup
rm -rf build *.spec