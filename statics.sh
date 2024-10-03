#!/bin/bash

### environment
TOP=`readlink -f "$0" | xargs dirname`
TIME=$(date +"%Y%m%d-%H%M%S")
SHORTLOG_FILE="shortlog-"$TIME".log"

if [ -x $1 ]; then
    echo "usage: $0 <year>"
    echo ""
    echo "example) $0 2022"
    exit
fi

data1=$1-01-01
date2=$1-12-31


### functions
run_repoinit_sync(){
    repo init -b develop -m default.xml -u https://github.com/harunobukurokawa/agl-all-repo
    repo sync -j`nproc`
}

run_repo_update(){
    repo sync -j`nproc`
}

## repo 取得 対象ディレクトリを取得
if [ -e .repo ]; then
    run_repo_update
else
    run_repoinit_sync
fi

AGL_DIR=`repo list | awk '{print $1}'`

## git shortlog を繰り返し
for dir in $AGL_DIR
do
    pushd $dir > /dev/null
    git shortlog -se --since=$data1 --until=$date2 >> $TOP/$SHORTLOG_FILE
    popd >> /dev/null
done

# 標準出力
cd $TOP
cat $SHORTLOG_FILE |  awk '{arry[$NF] += $1;} END{for(i in arry){print arry[i] " " i}}' | sort -nr
