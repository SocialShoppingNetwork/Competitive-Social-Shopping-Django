

var msg_day = 'день';
var msg_days = 'днів';
var msg_daysy = 'дні';
var msg_hour = 'година';
var msg_hours = 'годин';
var msg_hoursy = 'години';
var msg_finished = 'Закінчений';
var msg_robots = 'Автомати';
var msg_soon = 'Незабаром';
var src_buy_button = '//static1.wellbid.com/images/buttons/ua/buy_active.png';
var msg_price = 'Ціна: old';
var msg_pricex = 'old';
var src_finished_button = '//static1.wellbid.com/images/buttons/ua/finished.png';
var msg_short_days = 'д.';
var msg_short_hours = 'год.';
var msg_short_minutes = 'хв.';
var msg_short_seconds = 'с.';
var msg_remaining_characters = 'Кількість знаків, котрі можеш ще вписати: ';
var msg_congratulations = 'Вітання';
var msg_congratulationsTo = 'Вітання для ';
var msg_chat_sent = 'Повідомлення відіслано';
var msg_chat_choose = 'Вибери повідомлення, котре хочеш вислати';
var msg_bonus_winner = 'Влучив';

var LOGIN_PAGE = 'https://wellbid.com/login.html';
var UPDATE_PAGE = '/auctionsUpdate.txt';
var CHECK_PRICE_PAGE = '/checkPrice.txt';
var CHECK_PRICE_ACTION_PAGE = '/check.action';
var BUY_PAGE = '/buy.action';
var BEFORE_BUY_PAGE = '/beforeBuy.action';
var BID_PAGE = '/bid.action';
var HOME_PAGE = 'http://wellbid.com/index.html';
var BONUS_IMAGE_1 = '//static1.wellbid.com/images/masks/target_red_1.png';
var BONUS_IMAGE_2 = '//static1.wellbid.com/images/masks/target_red_2.png';
var BONUS_WINNER_IMAGE = '//static1.wellbid.com/images/masks/target_grey.png';
var CHECK_LOGIN_PAGE = '/checkLogin.txt';
var CHECK_LOGIN_ACTION = '/checkLogin.action';
var CHAT_PAGE = '/chat.action';

var advPage = false;
var timerAlert = 10.00000000;
var timerInverse = 3.00000000;
var updateMilis = 1000;
var updateMinSeconds = -2;

var pricePattern = '#,##0.00 ¤';
var pricePattern3 = '#,##0.000 ¤';
var pds = ',';
var pts = ' ';
var pcs = '€';

// This piece of code responsible for disconnecting user, if he did not bid for a while
var activityTimeoutMillis = 900000.00000000;
var activityTimeoutId = setTimeout(wakeUp, activityTimeoutMillis);
function stillWake() {
	if (activityTimeoutId != undefined) {
		clearTimeout(activityTimeoutId);
	}
	activityTimeoutId = setTimeout(wakeUp, activityTimeoutMillis);
}

function wakeUp() {
	var currentPath = window.location.pathname + window.location.search;
	window.location.href = 'http://wellbid.com/wakeUp.html?wakeUpURL=' + currentPath;
}

function setWakes() {
	var b = document.getElementsByTagName('body')[0];
	if (b != undefined) {

		b.setAttribute("onfocus", "stillWake()");
		b.setAttribute("onblur", "stillWake()");
		b.setAttribute("onmouseup", "stillWake()");
		b.setAttribute("onkeyup", "stillWake()");

		b.onfocus = stillWake;
		b.onblur = stillWake;
		b.onmouseup = stillWake;
		b.onkeyup = stillWake;
	}
}
setTimeout(setWakes, 1000);
// end


// This code is responsible for sending
String.prototype.trim = function() {
   return this.replace(/^\s+|\s+$/g, '');
};

String.prototype.endsWith = function(s) {
	return this.match( s + '$');
};

var count = 1;
var receivedCount = 0;
var DAY = 86400;
var HOUR = 3600;
var MINUTE = 60;
var CLASS_NAME_ATTR = "className";
var CLASS_ATTR = "class";
var SEP = ";";

var auctionChangesTimeout = 0;
var updateTimerId = null;
var updateAuctionsId = null;
var auctionsCount = 0;
var auctions = new Object();
var auctionsNR = new Object();
var auctionsB = new Object();
var auctionsSV = new Object();
var auctionsRV = new Object();
var auctionsPC = new Object();
var auctionsBV = new Object();
var auctionsBC = new Object();
var auctionsBCC = new Object();
var auctionsBCM = new Object();
var noIds = false;
var bidsId = undefined;
var chatTS = 0;
var bidsCounter = 0;
var robot = undefined;
var robotSet = undefined;
var bidsWinner = undefined;
var imgId = undefined;
var imgSrc = new Object();
var imgText = new Object();

// buttons
function setButton(b, src) {
	b.src = b.src.replace(/\/[^\/]*.png$/, "/" + src);
}
function setButtonText(b, className, text1, text2) {
	b.className = className;
	var child;
	while ((child = b.firstChild) != null) {
		b.removeChild(child);
	}
	child = document.createElement("b");
	child.appendChild(document.createTextNode(text1));
	b.appendChild(child);
	if (text2 != "") {
		child = document.createElement("span");
		child.appendChild(document.createTextNode(text2));
		b.appendChild(child);
	}
}
function cleanImageSrc(src) {
   return src.replace('_hover', '').replace('_active', '');
}
function hover_img(i) {
	i.src = cleanImageSrc(i.src).replace(/.png$/, "_hover.png");
}
function out_img(i) {
	i.src = cleanImageSrc(i.src);
}
function active_img(i) {
	i.src = cleanImageSrc(i.src).replace(/.png$/, "_active.png");
}
function hover_e(n) {
	hover_img(document.getElementById(n));
}
function out_e(n) {
	out_img(document.getElementById(n));
}
function active_e(n) {
	active_img(document.getElementById(n));
}

function getPXYZ() {
	var params = "";
	auctionsCount = 0;
	for (var id in auctions) {
		if (noIds == false) {
			if (id != undefined) {
				params = params + id + SEP;
			}
		}
		auctionsCount++;
	}
	if (params != "") {
		params = "ids=" + params + "&";
	}
	if (bidsId != undefined) {
		if (params == "") {
			params = "ids=" + bidsId + "&";
		}
		params = params + "bidsId=" + bidsId + "&bc=" + bidsCounter + "&";
		if (robot != undefined) {
			params = params + "robot=true&";
		}
	}
	params = params + "c=" + count + "&";
	count++;
	if (iid != undefined && iid != '') {
		params = params + "iid=" + iid + "&";
	}
	if (cid != undefined && cid != '') {
		params = params + "cid=" + cid + "&";
	}
	return params;
}
function getAuctionChanges() {
	var params = getPXYZ();
	//log("getAuctionChanges |" + loggedUser + "|, " + auctionsCount);
	if ((params != "") && ((loggedUser != '') || (auctionsCount > 0))) {
		sendRequest(updateAuctions, UPDATE_PAGE + "?js=true&" + params, null);
	}
}
///////////////////////////////////////////////////////////////////////////////////
//aktualizacja htmla
function setInnerHtml(id, html) {
	setInnerHtmlAndStyle(id, html, null);
}

function setInnerHtmlAndStyle(id, html, style) {
	setRealInnerHtmlAndStyle(id, html, style);
	for (var i = 0; i < 3; i++) {
		setRealInnerHtmlAndStyle(id + "_" + i, html, style);
	}
}
function setRealInnerHtmlAndStyle(id, html, style) {
	var e = document.getElementById(id);
	if (e != undefined) {
		//log("update pola: " + id + " = " + html);

		if (style != null) {
			e.className = style;
		}
		var oldHtml = e.innerHTML;
		e.innerHTML = html;
		if (id.indexOf("p") > -1) {//blink
			var oldPrice = oldHtml.replace(/\D+/g, '');
			var newPrice = html.replace(/\D+/g, '');
			//log("blink: " + oldPrice[1] + " ? " + newPrice[1]);
			if (oldPrice != newPrice) {
				blink(id);
			}
		}
	}
}

function enableButton(id) {
	for (var i = 0; i < 3; i++) {
		var tmp = "s" + id + "_" + i;
		var e = document.getElementById(tmp);
		if (e != undefined) {
			e.disabled = false;
			if (auctionsB[tmp] != undefined) {
				e.src = auctionsB[tmp];
			}
		}
	}
}
function disableButton(id) {
	realDisableButton("s" + id);
	for (var i = 0; i < 3; i++) {
		realDisableButton("s" + id + "_" + i);
	}
}
function realDisableButton(id) {
	var e = document.getElementById(id);
	if (e != undefined) {
		e.disabled = true;
		auctionsB[id] = e.src;
		e.src = src_finished_button;
	}
}
///////////////////////////////////////////////////////////////////////////
// parsowanie odpowiedzi z serwera
function updateAuctions(request) {
	if (request.readyState == 4) {
		//log("got answer: " + request.status);
		if (request.status == 200) {
			var errors = new Array();
			var messages = new Array();
			var infoAlert = false;
			var lines = request.responseText.trim().split("\n");
			var updatedAuctions = new Object();
			var bonus = false;
			var newMail = false;
			for (var i = 0; i < lines.length; i++) {
				var properties = lines[i].trim().split(SEP);
				//log(lines[i] + ", splited: " + properties.length + ", " + properties[0]);
				if (properties.length > 0) {
					switch (properties[0]) {
					case "#CN":
						var c = parseInt(properties[1]);
						if (c <= receivedCount) {
							i = lines.length;
						} else {
							receivedCount = c;
						}
						break;
					case "#AC":
						if (auctions[properties[1]] != undefined) {
							updatedAuctions[properties[1]] = "x";
							if (properties[1] == bidsId) {
								bidsWinner = properties[4];
							}
							setNewTime(properties[1], checkMinimumTime(properties[2]), properties[5] == "true");
							if (properties[1] == bidsId) {
								bidsWinner = properties[4];
							}
							setNewDelta(properties[1], parseInt(properties[6]));
							var cv = auctionCurrentValue(properties[1], properties[3]);
							var cvf = format3(cv);
							var rv = auctionRealValue(properties[1], properties[3]);
							var rvf = format(rv);
							setInnerHtmlAndStyle("p" + properties[1], cvf, "price");
							setInnerHtml("px" + properties[1], cvf);
							setInnerHtml("x" + properties[1], format(rv - cv));
							setInnerHtml("w" + properties[1], properties[4]);
							if (! advPage) {
								// bonus
								if (properties[8] != "_0") {
									bonus = true;
									showBonus(properties[1], properties[8], properties[9]);
								}
								// avatar
								showAvatar(properties[1], properties[10]);
								// przyrost
								if (auctionsBV[properties[1]] != undefined) {
									var bv = auctionBidsCount(properties[1], properties[3]);
									setInnerHtml("bib" + properties[1], bv);
									setInnerHtml("ib" + properties[1], bv);
								}
								setInnerHtml("rv" + properties[1], rvf);
							}
						}
						break;
					case "#BD":
						//wyczysci liste bidderow
						bidsCounter = properties[1];
						var table = document.getElementById("biddersHead");
						var div = document.getElementById("biddersTable");
						if (div != undefined) {
							if (table != undefined) {
								table.style.visibility = 'visible';
							}
							div.innerHTML = properties[2];
						}
						break;
					case "#ER":
						errors.push(properties[2]);
						//log("have error");
						break;
					case "#MS":
						messages.push(properties[2]);
						//log("have message");
						break;
					case "#BC":
						updateBidsCount(properties[1], properties[2]);
						break;
					case "#RT":
						setInnerHtml("robot", properties[1]);
						setInnerHtml("robot2", properties[1]);
						break;
					case "#PT":
						setInnerHtml("profit", properties[1]);
						break;
					case "#PR":
						showPrice(properties[1], properties[2], format(properties[3]), true);
						setInnerHtml("px" + properties[1], format(properties[3]));
						setInnerHtml("x" + properties[1], format(properties[4]));
						break;
					case "#PD":
						showPriceDone(properties[1], format(properties[2]));
						break;
					case "#RE":
						getPrice(properties[1]);
						break;
					case "#RD":
						window.location.href = properties[1];
						break;
					case "#ST":
						setInnerHtml("lrc", properties[1]);
						setInnerHtml("lbc", properties[2]);
						break;
					case "#NT":
						showElementInline('infoAlert');
						infoAlert = true;
						break;
					case "#NM":
						newMail = true;
						break;
					case "#CT":
						chatTS = parseInt(properties[1]);
						break;
					}
				}
			}
			if (loggedUser != '') {
				showNewMail(newMail);
			}
			if (!bonus && !advPage) {
				hideBonus();
			}
			if (advPage) {
				checkReload(updatedAuctions);
			}
			if (messages.length > 0) {
				show("messages", messages);
			}
			if (errors.length > 0) {
				show("errors", errors);
			}
			if (!infoAlert && !advPage) {
				hideElement(null, "infoAlert");
			}
			//log("finished answer");
		} else if ((request.status != 404) && (request.status != 500) && (request.status != 503)) { //if ((request.status == 301) || (request.status == 302)) {
			//redirect do strony logowania
			var newLocation = request.getResponseHeader("Location");
			if ((newLocation != null) && (newLocation != "")) {
				window.location.href = newLocation;
			} else if (advPage) {
				document.location.reload();
			}
		} else {
			//odswiez cala strone
			window.location.reload();
		}
		releaseRequestObject(request);
	}
}

function checkReload(updatedAuctions) {
	for (a in auctions) {
		//brak aktualizacji dla aukcji, wymuś refresh
		if (updatedAuctions[a] == null) {
			document.location.reload();
		}
	}
}

function checkMinimumTime(currentTime) {
	var seconds = updateMinSeconds;
	if (isNaN(currentTime)) {
		return currentTime;
	} else {
		var currentSeconds = parseInt(currentTime);
		if (currentSeconds > seconds) {
			seconds = currentSeconds;
		}
	}
	return seconds;
}

function finishAuction(id) {
	//log("finishAuction " + id);
	setInnerHtmlAndStyle("t" + id, msg_finished, "timer_finished");
	delete auctions[id];
	disableButton(id);
	if (id == bidsId) {
		// ten jest tylko jeden na stronie!
		e = document.getElementById("c" + id);
		if (e != undefined) {
			if (bidsWinner == loggedUser) {
				e.innerHTML = msg_congratulations;
			} else {
				e.innerHTML = msg_congratulationsTo + bidsWinner;
			}
		}
		e = document.getElementById("bidParams");
		//log("mam bidParams");
		if (e != undefined) {
			//log("parent: " + e.parentNode);
			e.parentNode.removeChild(e);
		}
		bidsId = undefined;
	}
}

function formatRemainingTime(seconds) {
	var ss = 0;
	var mm = 0;
	var hh = 0;
	var dd = 0;
	var result = msg_robots;
	if (seconds > 0) {
		result = "";
		dd = Math.floor(seconds / DAY);
		if (dd >= 5) {
			result = dd + " " + msg_daysy;
		} else if (dd >= 2) {
			result = dd + " " + msg_days;
		} else {
			hh = Math.floor(seconds / HOUR);
			mm = Math.floor((seconds - hh * HOUR) / MINUTE);
			ss = seconds - hh * HOUR - mm * MINUTE;
			if (hh < 10) {
				result = "0";
			}
			result = result + hh + ":";
			if (mm < 10) {
				result = result + "0";
			}
			result = result + mm + ":";
			if (ss < 10) {
				result = result + "0";
			}
			result = result + ss;
		}
	}
	return result;
}

function setNewTime(id, newSeconds, finish) {
	var oldSeconds = auctions[id];
	auctions[id] = newSeconds;
	if (auctions[id] != undefined) {
		if (finish) {
			finishAuction(id);
		} else {
			enableButton(id);
			if (auctions[id] == 'soon') {
				setInnerHtmlAndStyle("t" + id, msg_soon, "timer");
			} else {
				var seconds = parseInt(auctions[id]);
				if (!isNaN(oldSeconds) && ((parseInt(oldSeconds) - seconds) != -1)) {
					var time = formatRemainingTime(seconds);
					if (seconds < timerInverse) {
						if (seconds <= 0) {
							if (auctionsNR[id] != undefined) {
								time = "00:00:00";
							} else if (bidsId == id) {
								showAvatar(bidsId, "waiting.jpg");
							}
						}
						setInnerHtmlAndStyle("t" + id, time, "timer_inverse");
					} else if (seconds < timerAlert) {
						setInnerHtmlAndStyle("t" + id, time, "timer_alert");
					} else {
						setInnerHtmlAndStyle("t" + id, time, "timer");
					}
				}
			}
		}
	}
}

function setNewDelta(id, delta) {
	var e = document.getElementById("d" + id);
	if (e != null) {
		var newDelta = null;
		if (delta > DAY) {
			newDelta = Math.floor(delta/DAY) + " " + msg_short_days;
		} else if (delta > HOUR) {
			newDelta = Math.floor(delta/HOUR) + " " + msg_short_hours;
		} else if (delta > MINUTE) {
			newDelta = Math.floor(delta/MINUTE) + " " + msg_short_minutes;
		} else {
			newDelta = delta + " " + msg_short_seconds;
		}
		//e.className = "as_blue" + delta;
		e.innerHTML = newDelta;
	}
}

function updateTime() {
	var next = 20;
//	log("update time");
	for (var id in auctions) {
		// nie zamykaj aukcji bez potwierdzenia z serwera, zatrzymaj sie na 00:00:00
		if ((auctions[id] != undefined) && (auctions[id] != 'soon')) {
			var seconds = parseInt(auctions[id]);
			//nie zamknieta
			if (seconds > 0) {
				seconds--;
				setNewTime(id, seconds, false);
				if (next > seconds) {
					next = seconds;
				}
			} else {
				// czas minal ale jeszcze nie zamknieta
				next = 0;
			}
		}
	}
	if (updateAuctionsId == null) {
		if (next > 1) {
			next = next / 2;
		}
		if (auctionChangesTimeout > next) {
			auctionChangesTimeout = next;
		}
		if (auctionChangesTimeout <= 0) {
			getAuctionChanges();
			auctionChangesTimeout = next;
		} else {
			auctionChangesTimeout--;
		}
	}
//	log("updated time " + auctionChangesTimeout);
}
updateTimerId = setInterval(updateTime, 1000);
if (advPage) {
	updateAuctionsId = setInterval(getAuctionChanges, updateMillis);
}
/////////////////////////////////////////////////////////////////
// miganie
var colors = new Array('#22bb22', '#2cb122', '#3aa220', '#49911f', '#58831e', '#67721e', '#77621d', '#85531b', '#95431b', '#a5321a', '#b22418', '#be1818');
var bgColors = new Array('#68a30a', '#79b41c', '#8bc331', '#9bd046', '#a9da5b', '#b8e375', '#c9ec92', '#daf4b0', '#e9fbcd', '#f5fde8', '#f1fbf1', 'transparent');
function blink(id) {
	var e = document.getElementById(id);
	//log("blinking " + id + ", " + e);
	if (e != undefined) {
		e.style.backgroundColor = bgColors[0];
		setTimeout("fade('" + id + "', 1, true)", 20);
		//e.style.color = colors[0];
		//setTimeout("fade('" + id + "', 1, false)", 40);
	}
}
function fade(id, colorId, bg) {
	var e = document.getElementById(id);
	if (e != undefined) {
		if (bg) {
			e.style.backgroundColor = bgColors[colorId];
		} else {
			e.style.color = colors[colorId];
		}
		colorId++;
		//log("fade: " + colorId);
		if (colorId < bgColors.length) {
			setTimeout("fade('" + id + "', " + colorId + ", " + bg + ")", 20);
		}
	}
}
////////////////////////////////////////////////////////////////
//
function auctionCurrentValue(id, no) {
	return auctionsSV[id] + auctionsPC[id] * no;
}
function auctionRealValue(id, no) {
	if (auctionsBV[id] != undefined) {
		return auctionsBV[id] * auctionBidsCount(id, no);
	}
	return auctionsRV[id];
}
function auctionBidsCount(id, no) {
	if (auctionsBC[id] == undefined || auctionsBCC[id] == undefined || auctionsBCM[id] == undefined) {
		return 0;
	}
	if (auctionsBCM[id] == 0) {
		return auctionsBC[id] + auctionsBCC[id] * no;
	}
	return Math.min(auctionsBC[id] + auctionsBCC[id] * no, auctionsBCM[id]);
}
////////////////////////////////////////////////////////////////
//
function formatPrice(v, p) {
	var r = "" + Math.round(v);
	var scale = p.lastIndexOf('.');
	if (scale > -1) {
		scale = p.lastIndexOf('0') - scale;
		if (scale > 0) {
			var m = Math.pow(10, scale);
			r = "" + Math.round(v * m);
		}
	}
	var pos = r.length - 1;
	var f = new Array();
	for (var i = p.length - 1; i > -1; i--) {
		if (p.charAt(i) == '¤') {
			f.unshift(pcs);
		} else if (p.charAt(i) == '0') {
			if (pos > -1) {
				f.unshift(r.charAt(pos--));
			} else {
				f.unshift('0');
			}
		} else if (p.charAt(i) == '.') {
			f.unshift(pds);
		} else if (p.charAt(i) == '#') {
			var x = i;
			while (pos > -1) {
				if (i < 0) {
					i = x;
				}
				if (p.charAt(i) == '#') {
					f.unshift(r.charAt(pos--));
					i--;
				} else if (p.charAt(i) == ',') {
					f.unshift(pts);
					i--;
				} else {
					i = x;
				}
			}
			i = x;
		} else if (p.charAt(i) == ',') {
			if (pos > -1) {
				f.unshift(pts);
			}
		} else {
			f.unshift(p.charAt(i));
		}
	}
	return f.join('');
}
function format(v) {
	return formatPrice(v, pricePattern);
}

function format3(v) {
	var f = formatPrice(v, pricePattern3);
	if (pricePattern != pricePattern3) {
		return f.replace(/(\d)(\D+)?$/, "<span>$1</span>$2");
	}
	return f;
}

/////////////////////////////////////////////////////////////////
//karta aukcji
function getRequestParam(param) {
	var query = document.location.search.substring(1);
	var params = query.split('&');
	for (var i = 0; i < params.length; i++) {
		if (params[i].indexOf(param) > -1) {
			var pos = params[i].indexOf('=');
			if (pos > 0) {
				return params[i].substring(pos + 1);
			}
		}
	}
	return "";
}


// This code is



var CLEAR_TIMEOUT = 15000;
var clearTimeoutId = setTimeout(clearAll, CLEAR_TIMEOUT);

/////////////////////////////////////////////////////////////////
// test
if (window.self !== window.top) {
	if (!/.*facebook.*/.test(location.href)) {
		window.top.location = window.self.location;
	}
}
/////////////////////////////////////////////////////////////////
// flash
function showMovie(name, src, vars, width, height, color, secure, allowScriptAccess) {
	allowScriptAccess = typeof(allowScriptAccess) != 'undefined' ? allowScriptAccess : 'sameDomain';
	document.write(prepShowMovie(name, src, vars, width, height, color, secure, allowScriptAccess));
}
function prepShowMovie(name, src, vars, width, height, color, secure, allowScriptAccess) {
	var m = '';
	m = m + '<object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" codebase="';
	if (secure) {
		m = m + 'https';
	} else {
		m = m + 'http';
	}
	m = m + '://fpdownload.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,79,0" width="' + width + '" height="' + height + '" id="' + name + '" align="top">\n';
	m = m + '<param name="FlashVars" value="' + vars + '" />\n';
	m = m + '<param name="allowScriptAccess" value="' + allowScriptAccess +'" />\n';
	m = m + '<param name="movie" value="' + src + '" />\n';
	m = m + '<param name="quality" value="high" />\n';
	if (color == 'null') {
		m = m + '<param name="wmode" value="transparent" />\n';
	} else {
		m = m + '<param name="bgcolor" value="' + color + '" />\n';
	}
	if (!isIE) {
		m = m + '<embed src="' + src + '" FlashVars="' + vars + '" quality="high" ';
		if (color == 'null') {
			m = m + 'wmode="transparent" ';
		} else {
			m = m + 'bgcolor="' + color + '" ';
		}
		m = m + 'width="' + width + '" height="' + height + '" name="' + name + '" align="top" allowScriptAccess="' + allowScriptAccess + '" type="application/x-shockwave-flash" pluginspage="';
		if (secure) {
			m = m + 'https';
		} else {
			m = m + 'http';
	}
		m = m + '://www.macromedia.com/go/getflashplayer" />\n';
	}
	m = m + '</object>\n';
	return m;
}

/////////////////////////////////////////////////////////////////
// ukrywanie elementów bo kliknięciu checkboxa
function hide(id, checkbox, count) {
	var e;
	var v = 'visible';
	var p = 'static';
	if (! checkbox.checked) {
		v = 'hidden';
		p = 'absolute';
	}
	for (var i = 0; i < count; i++) {
		e = document.getElementById(id + i);
		if (e != null) {
			e.style.visibility = v;
			e.style.position = p;
		}
	}
}
function toggle(id, count) {
	for (var i = 0; i < count; i++) {
		toggleOne(id + i);
	}
}
function toggleOne(id) {
	var e = document.getElementById(id);
	if (e != null) {
		if (e.style.display == 'none') {
			e.style.display = 'block';
		} else {
			e.style.display = 'none';
		}
	}
}
function setDisabled(id, count, d) {
	var i;
	var e;
	for (i = 0; i < count; i++) {
		e = document.getElementById(id + i);
		if (e != undefined) {
			e.disabled = d;
		}
	}
}
function enableFields(id, count) {
	setDisabled(id, count, false);
}
function disableFields(id, count) {
	setDisabled(id, count, true);
}
/////////////////////////////////////////////////////////////////
//
function updateBidsCount(c, cp) {
	var e = document.getElementById("bidsCount");
	//log("bidsCount: " + e.nodeName);
	if (e != undefined) {
		if (c == "-") {
			//reload, wylogowany
			window.location.reload();
		} else {
			e.innerHTML = c.trim();
			e = document.getElementById("bcn");
			if (e != undefined) {
				e.innerHTML = parseInt(c) - parseInt(cp);
			}
			e = document.getElementById("bcp");
			if (e != undefined) {
				e.innerHTML = parseInt(cp.trim());
			}
		}
	}
}
/////////////////////////////////////////////////////////////////
// errors i messages
function clearAll() {
//	log("clearing all");
	if (clearTimeoutId != null) {
		clearTimeout(clearTimeoutId);
		clearTimeoutId = null;
	}
	clear("errors");
	clear("messages");
	//log("clean");
}
function clear(id) {
	var e = document.getElementById(id);
	if (e != undefined) {
		while (e.childNodes.length > 0) {
   			e.removeChild(e.firstChild);
		}
	}
}
function show(id, texts) {
	var e = document.getElementById(id);
//	log("show: " + id + ", " + e);
	if (e != undefined) {
		while (e.childNodes.length > 0) {
   			e.removeChild(e.firstChild);
		}
		var ul = document.createElement("ul");
		e.appendChild(ul);
		ul.setAttribute(CLASS_NAME_ATTR, id);
		ul.setAttribute(CLASS_ATTR, id);
		var li;
		for (var i = 0; i < texts.length; i++) {
			li= document.createElement("li");
			ul.appendChild(li);
			li.appendChild(document.createTextNode(texts[i]));
		}
		if (clearTimeoutId != null) {
			clearTimeout(clearTimeoutId);
		}
		clearTimeoutId = setTimeout(clearAll, CLEAR_TIMEOUT);
	} else {
		window.alert(texts.join("\n"));
	}
}
/////////////////////////////////////////////////////////////////
// przełączanie obrazków
function showBig(id, path) {
	var e = document.getElementById(id);
	//log(e.src + ", " + path);
	if (e != null) {
		e.style.backgroundImage = "url('" + path + "')";
	}
}
function showBonus(id, type, winner) {
	var e;
	var newImg = '';
	var newWinner = '';
	if (winner.length > 0) {
		newImg = BONUS_WINNER_IMAGE;
		newWinner = '<div class="bonus_winner">' + msg_bonus_winner + '<br />' + winner + '</div>';
	} else {
		newImg = this['BONUS_IMAGE' + type];
	}
	if (newImg != '') {
		newImg = "url('" + newImg + "')";
		if (imgId == undefined || imgSrc[imgId] == undefined) {
			showBonusImage(id, newImg, newWinner);
		} else {
			if (imgId != id) {
				hideBonus()
			}
			showBonusImage(id, newImg, newWinner);
		}
	}
}
function showBonusImage(id, newImg, newWinner) {
	imgId = id;
	var e = document.getElementById("img_" + imgId);
	if (e != undefined && e.style.backgroundImage != newImg) {
		if (imgSrc[imgId] == undefined) {
			imgSrc[imgId] = e.style.backgroundImage;
			imgText[imgId] = e.innerHTML;
		}
		e.style.backgroundImage = newImg;
		e.innerHTML = newWinner + imgText[imgId];
		e = document.getElementById("ib" + imgId);
		if (e != undefined) {
			e.style.position = 'absolute';
			e.style.visibility = 'hidden';
		}
	}
}
function hideBonus() {
	var e = document.getElementById("img_" + imgId);
	if (e != undefined) {
		if (imgSrc[imgId] != undefined) {
			e.style.backgroundImage = imgSrc[imgId];
			delete imgSrc[imgId];
			e.innerHTML = imgText[imgId];
			delete imgText[imgId];
			e = document.getElementById("ib" + imgId);
			if (e != undefined) {
				e.style.position = '';
				e.style.visibility = 'visible';
			}
			imgId = undefined;
		}
	}
}
/////////////////////////////////////////////////////////////////
// bidowanie
function bid(aid) {
	log("bid");
	clearAll();
	var url = BID_PAGE + "?js=true&" + getPXYZ() + "aid=" + aid + "&";
	sendRequest(updateAuctions, url, null);
	setTimeout(getAuctionChanges, 1500);
	return false;
}

/////////////////////////////////////////////////////////////////
//

function showAvatar(id, name) {
	var e = document.getElementById("av" + id);
	if (e != undefined && name != undefined && name != "") {
		var x = parseInt(auctions[id]);
		if (x <= 0) {
			name = "waiting.jpg";
		}
		log("showAvatar " + id + ", " + name + " (" + x + ")");
		e.src = e.src.replace(/\/[^\/]+$/, "/" + name);
	}
}

/////////////////////////////////////////////////////////////////
// ograniczenie długości pól tekstowych
function checkLength(e, t, l) {
	var keycode;
	if (e != null) {
		if (e.keyCode) {
			keycode = e.keyCode;
		} else {
			keycode = e.which;
		}
	}
	if ((keycode > 34) && (keycode < 41) || (keycode == 8) || (keycode == 9) || (keycode == 116)) {
		return true;
	} else if (t.value.length >= l) {
		return false;
	}
	return true;
}
function updateRemainingCharacters(t, l) {
	var c = document.getElementById("counter");
	if (c != undefined) {
		c.innerHTML = msg_remaining_characters + (l - t.value.length);
	}
}
/////////////////////////////////////////////////////////////////
//
function checkSubmit(e) {
	var keycode;
	if (e != null) {
		if (e.keyCode) {
			keycode = e.keyCode;
		} else {
			keycode = e.which;
		}
	}
	return (keycode != 13);
}
/////////////////////////////////////////////////////////////////
// ustawia focus
function focus(id) {
	var e = document.getElementById(id);
	if (e != undefined) {
		e.focus();
	}
}
/////////////////////////////////////////////////////////////////
//sprawdzanie cookie
function cookiesEnabled(path) {
	document.cookie = "test_cookie=cookie_enabled";
	var idx = document.cookie.indexOf("test_cookie=");
	var date = new Date();
	date.setTime(date.getTime() + ((-1)*24*60*60*1000));
	document.cookie = "test_cookie=; expires=" + date.toGMTString();
	if (idx == -1) {
		window.location.replace(path);
	}
}

/////////////////////////////////////////////////////////////////
//logowanie
var logs = new Array();
function log(msg) {
	var log = document.getElementById("log");
	if (log != null) {
		var now = new Date();
		logs.push(msg);
		if (logs.length > 50) {
			logs.shift();
		}
		log.innerHTML = logs.join("<br />");
	}
}
/////////////////////////////////////////////////////////////////
//
function _getOffsetTop(e) {
	var offsetTop = e.offsetTop;
	var parent = e.offsetParent;
	while (parent != null) {
		offsetTop = offsetTop + parent.offsetTop;
		parent = parent.offsetParent;
	}
	return offsetTop;
}

function _getOffsetLeft(e) {
	var offsetLeft = e.offsetLeft;
	var parent = e.offsetParent;
	while (parent != null) {
		offsetLeft = offsetLeft + parent.offsetLeft;
		parent = parent.offsetParent;
	}
	return offsetLeft;
}

/////////////////////////////////////////////////////////////////////////////////////////
//check price

var auctionsRE = new Object();
var bc = new Object();

function getPrice(auctionId) {
	setTimeout("getPrice2(" + auctionId + ")", 500);
}
function getPrice2(auctionId) {
	if (auctionId != '') {
		if (auctionsRE[auctionId] != undefined) {
			return true;
		}
		sendRequest(updateAuctions, CHECK_PRICE_PAGE + "?js=true&aid=" + auctionId + "&", null);
	}
	return false;
}

function checkPrice(auctionId) {
	if ((loggedUser != '') && (auctionId != '')) {
		if (auctionsRE[auctionId] != undefined) {
			return true;
		}
		sendRequest(updateAuctions, CHECK_PRICE_ACTION_PAGE + "?js=true&aid=" + auctionId + "&", null);
	}
	return false;
}

function showPrice(auctionId, bidNo, price, show) {
	if (show) {
		showBuy(auctionId, bidNo, price, "");
		for (var i = 1; i < 4; i++) {
			showBuy(auctionId, bidNo, price, "_" + i);
		}
	}
	auctionsRE[auctionId] = price;
	setTimeout("hidePrice(" + auctionId + ")", 15000);
}

function showBuy(auctionId, bidNo, price, suffix) {
	var e = document.getElementById("f" + auctionId + suffix);
	if (e != undefined) {
		e.action = BEFORE_BUY_PAGE;
		e.method = "POST";
		e["bidNo"].value = bidNo;
		e = document.getElementById("s" + auctionId + suffix);
		if (e != undefined) {
			bc[auctionId] = e.src;
			e.src = src_buy_button;
		}
		e = document.getElementById("p" + auctionId + suffix);
		if (e != undefined) {
			e.innerHTML = price;
			blink("p" + auctionId + suffix);
		}
	}
}

function showPriceDone(auctionId, price) {
	showSold(auctionId, price, "");
	for (var i = 1; i < 4; i++) {
		showSold(auctionId, price, "_" + i);
	}
}

function showSold(auctionId, price, suffix) {
	var e = document.getElementById("f" + auctionId + suffix);
	if (e != undefined) {
		e.action = '';
		e.method = "POST";
		e["bidNo"].value = '';
		auctionsRE[auctionId] = price;
		realDisableButton("s" + auctionId + suffix);
		e = document.getElementById("p" + auctionId + suffix);
		if (e != undefined) {
			e.innerHTML = price;
			blink("p" + auctionId + suffix);
		}
	}
}
function hidePrice(auctionId) {
	hideBuy(auctionId, "");
	setInnerHtml("px" + auctionId, msg_pricex);
	setInnerHtml("x" + auctionId, msg_pricex);
	for (var i = 1; i < 4; i++) {
		hideBuy(auctionId, "_" + i);
	}
}

function hideBuy(auctionId, suffix) {
	var e = document.getElementById("f" + auctionId + suffix);
	if (e != undefined) {
		e.action = CHECK_PRICE_ACTION_PAGE;
		e.method = "GET";
		e["bidNo"].value = '';
		delete auctionsRE[auctionId];
		e = document.getElementById("s" + auctionId + suffix);
		if (e != undefined) {
			e.src = bc[auctionId];
		}
		e = document.getElementById("p" + auctionId + suffix);
		if (e != undefined) {
			if (suffix == "") {
				e.innerHTML = msg_pricex;
			} else {
				e.innerHTML = msg_price;
			}
			blink("p" + auctionId + suffix);
		}
	}
}

function nextBlink(auctionId, first) {
	if (auctionsRE[auctionId] == undefined) {
		if (! first) {
			blink("p" + auctionId);
			for (var i = 1; i < 4; i++) {
				blink("p" + auctionId + "_" + i);
			}
		}
		var next = 10 + Math.floor(Math.random() * 100) % 50;
		setTimeout("nextBlink(" + auctionId + ", false)", next * 1000);
	}
}

/////////////////////////////////////////////////////////////////////////////////////////
//ukrywanie kategorii

function showElement(id, p) {
	var e = document.getElementById(id);
	if (e != null) {
		e.style.visibility = 'visible';
		e.style.display = 'block';
		if (p != null) {
			e.style.left = _getOffsetLeft(p) + 'px';
		}
	}
}

function showElementInline(id) {
	var e = document.getElementById(id);
	if (e != null) {
		e.style.visibility = 'visible';
		e.style.display = 'inline-block';
	}
}

function hideElement(e, id1, id2) {
	var el = document.getElementById(id1);
	var elp = document.getElementById(id2);
	if (el != undefined) {
		if (elp == undefined) {
			elp = el;
		}
		e = e || window.event;
		if (e != undefined) {
			var reltg = (e.relatedTarget) ? e.relatedTarget : e.toElement;
			if(reltg != null) {
				while (reltg != el && reltg != elp && reltg.nodeName != 'BODY') {
					reltg = reltg.parentNode
				}
			}
			if (reltg == el || reltg == elp) return;
		}
		el.style.visibility = "hidden";
		el.style.display = "none";
	}
}

/////////////////////////////////////////////////////////////////
//check login
var cl = 0;

function checkLogin(login, id) {
	log("checkLogin");
	if (login.length > 2 && login.length < 13) {
		var url = CHECK_LOGIN_PAGE + "?js=true&cl=" + cl + "&login=" + login + "&";
		cl++;
		sendRequest(updateDiv, url, id);
	}
	return false;
}

function proposeLogin(id, login) {
	var e = document.getElementById(id);
	if (e != undefined) {
		e.value = login;
	}
}

function clearInput(i) {
	i.value = '';
	i.onfocus = '';
}

/////////////////////////////////////////////////////////////////
//usuwanie z obserwowanych
function fillIds(form, chName, idsName) {
	var ch = document.getElementsByName(chName);
	var ids = "";
	for (var i = 0; i < ch.length; i++) {
		if (ch.item(i).type == 'checkbox' && ch.item(i).checked == true) {
			ids = ids + ch.item(i).value + ";";
		}
	}
	form.elements[idsName].value = ids;
}

/////////////////////////////////////////////////////////////////
//

var animateEv = "";

function startAnimate(id, p, curr, dest, ev) {
	animateEv = ev;
	animate(id, p, curr, dest, ev);
}
function animate(id, p, curr, dest, ev) {
	if (animateEv == ev) {
		var animateStep = 10;
		var e = document.getElementById(id);
		if (e != null) {
			var n = curr;
			if (e.style[p] != "") {
				n = parseInt(e.style[p]);
			}
			if (n < dest) {
				n = n + animateStep;
				if (n > dest) {
					n = dest;
				}
			} else {
				n = n - animateStep;
				if (n < dest) {
					n = dest;
				}
			}
			e.style[p] = n + "px";
			if (n != dest) {
				setTimeout("animate('" + id + "', '" + p + "', " + n + ", " + dest + ", '" + ev + "')", 10);
			}
		}
	}
}
//
var currentTab = 'rules';
function showTab(id) {
	var e = undefined;
	if (currentTab != '') {
		e = document.getElementById(currentTab);
		if (e != undefined) {
			if (e.className.indexOf("hidden") == -1) {
				e.className = e.className + "hidden";
			}
			e = document.getElementById(currentTab + 'Tab');
			if (e != undefined) {
				e.className = "bottomButtonMenuUnactive";
			}
		}
	}
	if (id != '') {
		currentTab = '';
		e = document.getElementById(id);
		if (e != undefined) {
			currentTab = id;
			if (e.className.indexOf("hidden") > -1) {
				e.className = e.className.substring(0, e.className.indexOf("hidden"));
			}
			e = document.getElementById(currentTab + 'Tab');
			if (e != undefined) {
				e.className = "bottomButtonMenuActive";
			}
		}
	}
}
////////////////////////////////////////////////////////////////
//
function getPageOffsetTop() {
	if (typeof(window.pageYOffset) == 'number') {
		return window.pageYOffset;
	} else if (document.body && document.body.scrollTop) {
		return document.body.scrollTop;
	} else if (document.documentElement && document.documentElement.scrollTop) {
		return document.documentElement.scrollTop;
	}
	return -1;
}
function startScrollPage() {
	setTimeout(scrollPage, 5000);
}
function scrollPage() {
	if (getPageOffsetTop() < 625) {
		window.scrollBy(0, 3);
		setTimeout(scrollPage, 10);
	}
}
////////////////////////////////////////////////////////////////
//countries
var countriesPos = 0;
var countriesPosMoves = 0;
var scrollCountriesId = undefined;
var scrollCountriesDone = false;

function scrollCountries(right) {
	var c = document.getElementById("flags");
	if (c != undefined) {
		var flagWidth = 49;
		var sep = "a>";
		var step = 1;
		var idx = 0;
		var flags = c.innerHTML.split(new RegExp(sep));
		if (flags[flags.length - 1] == "") {
			flags.pop();
		}
		if (right) {
			countriesPos -= step;
			if (countriesPos < -flagWidth) {
				flags.push(flags.shift());
				c.innerHTML = flags.join(sep) + sep;
				countriesPos += (flagWidth + step);
				if (countriesPosMoves > 1 && scrollCountriesDone) {
					stopScrollCountries();
				}
			}
			countriesPosMoves++;
		} else {
			countriesPos += step;
			if (countriesPos > 0) {
				flags.unshift(flags.pop());
				c.innerHTML = flags.join(sep) + sep;
				countriesPos -= (flagWidth + step);
				if (countriesPosMoves > 1 && scrollCountriesDone) {
					stopScrollCountries();
				}
			}
			countriesPosMoves++;
		}
		c.style.marginLeft = countriesPos + "px";
	}
}

function startScrollCountries(right) {
	stopScrollCountries();
	if (scrollCountriesId == undefined) {
		countriesPosMoves = 0;
		scrollCountriesDone = false;
		scrollCountriesId = setInterval("scrollCountries(" + right + ")", 10);
	}
}
function stopScrollCountries() {
	if (scrollCountriesId != undefined) {
		if (scrollCountriesDone) {
			clearInterval(scrollCountriesId);
			scrollCountriesId = undefined;
		} else {
			scrollCountriesDone = true;
		}
	}
}

function showNewMail(show) {
	var e = document.getElementById("envelope");
	if (e != undefined) {
		if (show) {
			e.className = e.className.replace("envelopeLink", "envelopeNewLink");
		} else {
			e.className = e.className.replace("envelopeNewLink", "envelopeLink");
		}
	}
}
var sbted = false;
function submitLock() {
	if (sbted) {
		return false;
	}
	sbted = true;
	return true;
}
////////////////////////////////////////////////////////////////
// slider
var cSlide = -1;
var pSlide;
var slideTimeout;
function switchBanner(e1, e2, o) {
	if (o >= 1) {
		e1.style.opacity = 1;
		e2.style.opacity = 0;
		e2.style.display = 'none';
	} else {
		e1.style.opacity = o;
		setTimeout(function(){switchBanner(e1, e2, o + 0.3);}, 50);
	}
}
function slideBanner(m, n) {
	if (slideTimeout != undefined) {
		clearTimeout(slideTimeout);
	}
	if (cSlide < 0) {
		cSlide = n;
		document.getElementById('b' + n).src.replace('Empty', 'Full');
	} else if (cSlide != n) {
		pSlide = cSlide;
		cSlide = n;
		if (cSlide >= m) {
			cSlide = 0;
		}
		//alert(m + ', ' + pSlide + ', ' + cSlide);
		var e1 = document.getElementById('b' + pSlide);
		e1.src = e1.src.replace('Full', 'Empty');
		var e2 = document.getElementById('b' + cSlide);
		e2.src = e2.src.replace('Empty', 'Full');
		e1 = document.getElementById('bd' + cSlide);
		e1.style.zIndex = 1;
		e1.style.display = 'block';
		e2 = document.getElementById('bd' + pSlide);
		e2.style.zIndex = 0;
		switchBanner(e1, e2, 0.2);
	}
	slideTimeout = setTimeout(function(){slideBanner(m, cSlide + 1);}, 20000);
}

function prepPass(ibg, ifg) {
	var e = document.getElementById(ibg);
	if (e != undefined) {
		e.parentNode.removeChild(e);
	}
	e = document.getElementById(ifg);
	if (e != undefined) {
		e.style.position = 'static';
		e.focus();
	}
}

function hasClass(ele,cls) {
	return ele.className.match(new RegExp('(\\s|^)'+cls+'(\\s|$)'));
}

function addClass(ele,cls) {
	if (!this.hasClass(ele,cls)) ele.className += " "+cls;
}

function removeClass(ele,cls) {
	if (hasClass(ele,cls)) {
    	var reg = new RegExp('(\\s|^)'+cls+'(\\s|$)');
		ele.className=ele.className.replace(reg,' ');
	}
}




var isIE = false;
var requests = new Array();
var requestTypes = { normal : {key : "Content-type", value : "application/x-www-form-urlencoded"}};

function getRequestObject() {
	if (requests.length < 1) {
		//log("new request " + typeof XMLHttpRequest);
		if (window.XMLHttpRequest && !(window.ActiveXObject)) {
			try {
				return new XMLHttpRequest();
			} catch (e) {log("to nie jest FF");}
		}
		isIE = true;
		//log("IE");
		// Internet Explorer
		try {
			return new ActiveXObject("Msxml2.XMLHTTP.6.0");
		} catch(e) {}
		try {
			return new ActiveXObject("Msxml2.XMLHTTP.3.0");
		} catch(e) {}
		try {
			return new ActiveXObject("Msxml2.XMLHTTP");
		} catch(e) {}
		try {
			return new ActiveXObject("Microsoft.XMLHTTP");
		} catch(e) {}
		//log("This browser does not support XMLHttpRequest." );
		return undefined;
	} else {
		//log("reuse request");
		return requests.pop();
	}
}
function releaseRequestObject(request) {
	//log("releasing request");
	requests.push(request);
}
function sendRequest(callback, url, id) {
	var request = getRequestObject();
	if (request != undefined) {
		var d = new Date();
		url = url + "t=" + d.getTime();
		if (isIE) {
			request.open("GET", url, true);
			if (callback != null) {
				if (id != null) {
					request.onreadystatechange = function() { callback(request, id);};
				} else {
					request.onreadystatechange = function() { callback(request);};
				}
			} else {
				request.onreadystatechange = function() {};
			}
		} else {
			if (callback != null) {
				if (id != null) {
					request.onload = function() { callback(request, id);};
				} else {
					request.onload = function() { callback(request);};
				}
			} else {
				request.onload = function() {};
			}
			request.open("GET", url, true);
		}
		request.send(null);
		//log("request sent " + typeof request + ", " + isIE);
	} else {
		//log("nic nie wysyłamy bo się nie da");
	}
}

function sendPostRequest(callback, url, id, contentType, params) {
	var request = getRequestObject();

	if (request != undefined) {
		if (isIE) {
			request.open("POST", url, true);
			request.setRequestHeader(contentType.key, contentType.value);
			if (callback != null) {
				if (id != null) {
					request.onreadystatechange = function() { callback(request, id);};
				} else {
					request.onreadystatechange = function() { callback(request);};
				}
			} else {
				request.onreadystatechange = function() {};
			}
		} else {
			if (callback != null) {
				if (id != null) {
					request.onload = function() { callback(request, id);};
				} else {
					request.onload = function() { callback(request);};
				}
			} else {
				request.onload = function() {};
			}
			request.open("POST", url, true);
			request.setRequestHeader(contentType.key, contentType.value);
		}
		var d = new Date();
		params = params + "&t=" + d.getTime();
		log("params " + params);
		request.send(params);

	} else {
		log("nic nie wysyłamy bo się nie da");
	}
}

function updateDiv(request, id) {
	if (request.readyState == 4) {
		//log("got answer: " + request.status);
		if (request.status == 200) {
			var e = document.getElementById(id);
			if (e != undefined) {
				e.innerHTML = request.responseText;
			}
		}
	}
}

function say() {
	sendRequest(null, UPDATE_PAGE + "?js=true&c=0&", null);
}



/////////////////////////////////////////////////////////////////////////////////////////
//okienko
function openWindowNamed(url, name, width, height) {
	//checking available window size
	if (window.screen && (width == 0 || height == 0)) {
		width = window.screen.availWidth - 100;
		height = window.screen.availHeight - 100;
	}

	var features = 'menubar=0,scrollbars,resizable,status=0,top=0,left=0,width=' + width + ',height=' + height;
	var w = window.open(url, name, features);
	if ((w == null) && (window.opener != null)) {
		w = window.opener.open(url, name, features);
	}
	if (w != null) {
		w.focus();
	}
}

/////////////////////////////////////////////////////////////////////////////////////////
//popup onclick

function showLayer(width, height, content, id) {
	// checking available window size
	var top = 150;
	var left = 200;
	var maxW = "100%";
	var maxH = "1000px";
	if (window.screen) {
		left = (window.screen.availWidth / 2) + 456 - width;
		//top = (window.screen.availHeight - height - 200) / 2;
		maxW = window.screen.availWidth + "px";
	}
	var parent = document.getElementById(id);
	if (parent != null) {
		parent.innerHTML = '<div onclick="hideLayer(\'' + id + '\');" class="layer" style="cursor:pointer;top:' + top + 'px;left:' + left + 'px;width:' + width + 'px;height:' + height + 'px;">' +
			content + '</div>';
	}
}

function hideLayer(id) {
	var parent = document.getElementById(id);
	if (parent != null) {
		parent.innerHTML = '';
	}
}

