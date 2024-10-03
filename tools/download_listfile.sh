#!/bin/bash

# 定义目标文件夹
DIR="list_files"

# 检查文件夹是否存在，存在则删除
if [ -d "$DIR" ]; then
  rm -rf "$DIR"
fi

# 创建文件夹
mkdir "$DIR"

# 读取文件中的链接并下载到指定文件夹
for url in $(grep -o 'https://[^,]*' rulesets.txt); do
  wget -q -P "$DIR" "$url"
done

# 输出不包含后缀的文件名列表，用空格分隔
for file in "$DIR"/*.list; do
  basename "$file" .list
done | tr '\n' ' '

# 换行
echo
