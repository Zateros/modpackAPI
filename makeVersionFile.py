#!/usr/bin/env python3

import os, json, sys

NEW_PACKAGE_LOCATION = os.getcwd() + f"/{sys.argv[1]}"

jarFiles = []
for root, dirs, files in os.walk(NEW_PACKAGE_LOCATION):
	for file in files:
		if file.endswith(".jar"):
			jarFiles.append(file)

with open("latest-version.json", "w", encoding="UTF-8", ) as new:
	new.write(json.dumps({"version":sys.argv[1].replace("/",""),"content": jarFiles, "count":str(len(jarFiles))}))
