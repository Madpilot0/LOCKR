from flask import Blueprint, render_template, abort, session, redirect, url_for, request
from functools import wraps
from lib.Functions import Functions
from lib.Database import Database
import json
import datetime
import threading
import time

def requires_auth(f):
	@wraps(f)
	def decorated_auth(*args, **kwargs):
		#print("Will be called",functions.lastUpdate,functions.isRefreshing)
		#if threading.activeCount() <= 2 and not functions.isRefreshing and int(time.time() - functions.lastUpdate) > 600:
		#	t = threading.Thread(target=functions.updateAllData)
		#	t.start()
			#functions.updateAllData()
		if not functions.isLoggedIn():
			return redirect(url_for('page_routes.login', secure_uri=functions.getAuthURI()))
		return f(*args, **kwargs)
	return decorated_auth

def requires_admin(f):
	@wraps(f)
	def decorated_admin(*args, **kwargs):
		if not functions.isAdmin():
			return json.dumps({"error": "Unauthorized"}),401
		return f(*args, **kwargs)
	return decorated_admin

def requires_member(f):
	@wraps(f)
	def decorated_member(*args, **kwargs):
		if not functions.isMember():
			return json.dumps({"error": "Unauthorized"}),401
		return f(*args, **kwargs)
	return decorated_member

internal_routes = Blueprint('internal_routes', __name__, template_folder='templates')
functions = Functions()
db = Database()

@internal_routes.route("/internal/character/getWalletInfo")
@requires_auth
def getWalletInfo():
	return json.dumps(functions.getWalletInfo())

@internal_routes.route("/internal/character/getMarketInfo")
@requires_auth
def getMarketInfo():
	return json.dumps(functions.getMarketInfo())

@internal_routes.route("/internal/character/getSysID")
@requires_auth
def getSysID():
	return json.dumps(functions.getCharSysLocID())

@internal_routes.route("/internal/character/getCharacters")
@requires_auth
@requires_admin
def getCharactes():
	return json.dumps(functions.getCharacters())

@internal_routes.route("/internal/character/editCharacter", methods=["POST"])
@requires_auth
@requires_admin
def editCharacter():
	print(request.form)
	res = functions.editCharacter(request.form)
	return redirect(url_for("page_routes.admin"))
	#return json.dumps()

@internal_routes.route("/internal/industry/getAllJobs")
@requires_auth
@requires_member
def getIndustryJobs():
	return json.dumps(functions.getIndustryJobs())

@internal_routes.route("/internal/industry/getCorpAssets")
@requires_auth
@requires_admin
def getCorpAssets():
	return json.dumps(functions.getCorpAssets())

@internal_routes.route("/internal/market/getMarketItems")
@requires_auth
def getMarketItems():
	return json.dumps(functions.getMarketItems())

@internal_routes.route("/internal/market/getPricingInfo")
@requires_auth
@requires_member
def getPricingInfo():
	return json.dumps(functions.getPricingInfo())

@internal_routes.route("/internal/market/postMarketItems",methods=["POST"])
@requires_auth
@requires_admin
def postMarketItems():
	return json.dumps(functions.postMarketItems())

@internal_routes.route("/internal/market/delMarketItem/<itemID>")
@requires_auth
@requires_admin
def delMarketItem(itemID):
	return json.dumps(functions.delMarketItem(itemID))

@internal_routes.route("/internal/market/updatePrice")
@requires_auth
@requires_admin
def updatePrice():
	return
	#return json.dumps(functions.updatePrice())

@internal_routes.route("/internal/mining/getMoonMining")
@requires_auth
@requires_member
def getMoonMining():
	return json.dumps(functions.getMoonMining())

@internal_routes.route("/internal/production/getProduction")
@requires_auth
@requires_member
def getProduction():
	return json.dumps(functions.getProduction())

@internal_routes.route("/interal/production/setTarget/<selID>/<val>")
@requires_auth
@requires_admin
def setTarget(selID, val):
	return json.dumps(functions.setTarget(selID, val))

@internal_routes.route("/internal/structures/getStructures")
@requires_auth
@requires_member
def getStructures():
	return json.dumps(functions.getStructures())

@internal_routes.route("/internal/contracts/getContracts")
@requires_auth
@requires_admin
def getContracts():
	return json.dumps(functions.getContracts())

@internal_routes.route("/internal/users/getRefreshingStatus")
@requires_auth
def getRefreshingStatus():
	return json.dumps(functions.getRefreshingStatus())