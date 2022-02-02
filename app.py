#!/usr/bin/env python3

from flask import Flask, send_from_directory, request
from functools import wraps
from werkzeug import secure_filename
from tempfile import mkdtemp
import os, psutil, json, shutil, zipfile

HOME = os.path.expanduser('~')
DOWNLOAD_FOLDER = HOME + "/download"
VERSION_FILE = DOWNLOAD_FOLDER + "/latest-version.json"
USER_TOKEN = "qzuxmrLGwDs3KPKX5V5KyA=="
ADMIN_TOKEN = "o4S9qPk284HLuC8mx8qz2rtJNJFAX2Mnqg=="

FILE_EXCEPTIONS = ["testfolder"]

app = Flask(__name__)

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		givenToken = None
		if 'x-access-token' in request.headers:
			givenToken = request.headers['x-access-token']
		if not givenToken == USER_TOKEN:
			return 'Unauthorized Access!', 401
		if not givenToken:
			return 'Unauthorized Access!', 401
		return f(*args, **kwargs)

	return decorated

def admin_token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		givenToken = None
		if 'x-access-token' in request.headers:
			givenToken = request.headers['x-access-token']
		if not givenToken == ADMIN_TOKEN:
			return 'Unauthorized Access!', 401
		if not givenToken:
			return 'Unauthorized Access!', 401
		return f(*args, **kwargs)

	return decorated

@app.route("/version/<path:path>", methods=['GET'])
@token_required
def versionGet(path):
	if path == "latest":
		loc = VERSION_FILE
	else:
		loc = DOWNLOAD_FOLDER + f"/{path}/content.json"

	try:
		with open(loc) as version:
			return json.loads(version.read())['version'], 200
	except FileNotFoundError:
		return "File with the version number was not found", 404

@app.route("/content/<path:path>", methods=['GET'])
@token_required
def contentGet(path):
	if path == "latest":
		loc = VERSION_FILE
	else:
		loc = DOWNLOAD_FOLDER + f"/{path}/content.json"

	try:
		with open(loc) as version:
			return str(json.loads(version.read())['content']), 200
	except FileNotFoundError:
		return "File with the version number was not found", 404

@app.route("/count/<path:path>", methods=['GET'])
@token_required
def countGet(path):
	if path == "latest":
		loc = VERSION_FILE
	else:
		loc = DOWNLOAD_FOLDER + f"/{path}/content.json"

	try:
		with open(loc) as version:
			return str(json.loads(version.read())['count']), 200
	except FileNotFoundError:
		return "File with the version number was not found", 404

@app.route("/versionFile", methods=['GET'])
@token_required
def versionFileGet():
	try:
		with open(VERSION_FILE) as version:
			return str(version.read()), 200
	except FileNotFoundError:
		return "File with the version number was not found", 404

@app.route("/packages/<path:path>", methods=['GET'])
@token_required
def packagesGet(path):
	for exception in FILE_EXCEPTIONS:
		if exception in path:
			return "Access denied", 403
	return send_from_directory(DOWNLOAD_FOLDER, path, as_attachment=True)

@app.route("/status", methods=['GET'])
def statusGet():
    for proc in psutil.process_iter():
        try:
            if "java" in proc.name().lower():
                return "online", 200
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return "offline", 418

# @app.route("/pushVersion", methods=['PUT'])
# @admin_token_required
# def pushVersionFile():
# 	try:
# 		message = request.form['version']
# 		with open(VERSION_FILE, "rw", encoding="UTF-8") as version:
# 			original = json.loads(version.read())
# 			original['version'] = message
# 			version.write(json.dumps(original))
# 		return {"success":200}, 200
# 	except:
# 		return {"error":304}, 304

@app.route('/pushUpdate', methods = ['POST'])
@admin_token_required
def pushUpdate():
	if request.method == 'POST':
		try:
			f = request.files['file']
			if not ".zip" in f.filename:
				return {"Error: Content isn't a zip file":422}, 422
			fileName=secure_filename(f.filename)
			tmp = mkdtemp()
			
			f.save(fileName)

			with zipfile.ZipFile(fileName, 'r') as zip_ref:
				zip_ref.extractall(tmp)
			if os.path.isfile(tmp+"/latest-version.json"):
				shutil.copyfile(tmp+"/latest-version.json", DOWNLOAD_FOLDER)
				with open(tmp+"/latest-version.json", "r", encoding="UTF-8") as version:
					original = json.loads(version.read())
					latestVersion = DOWNLOAD_FOLDER+f"""/{original["version"]}"""
					os.makedirs(latestVersion)
				shutil.rmtree(tmp+"/latest-version.json")
			else:
				return {"Error: Zip didn't contain any version file":422}, 422
			shutil.copytree(tmp,latestVersion)
			shutil.rmtree(fileName)
			shutil.rmtree(tmp)
			return {"success":200}, 200
		except:
			return {"error":400}, 400

@app.route("/teapot", methods=["GET"])
def teapot():
	return {"I'm a teapot",418}, 418

if __name__ == '__main__':
    app.run(port=25566)