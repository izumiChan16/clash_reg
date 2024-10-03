#!/bin/bash

# Download and extract the program
wget https://github.com/DustinWin/clash_singbox-tools/releases/download/sing-box/sing-box-dev-linux-amd64v3.tar.gz
tar -xzf sing-box-dev-linux-amd64v3.tar.gz

# Rename the extracted directory
mv CrashCore sing-box

# Remove the downloaded tar.gz file
rm sing-box-dev-linux-amd64v3.tar.gz

# Create the output directory if it doesn't exist
mkdir -p srs

# Compile each JSON file in the temp_rules directory into the srs directory
for file in temp_rules/*.json; do
    filename=$(basename "$file" .json)
    ./sing-box rule-set compile --output "./srs/${filename}.srs" "$file"
done

# Remove the extracted program directory
rm -rf sing-box

