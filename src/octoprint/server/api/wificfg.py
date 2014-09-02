# coding=utf-8

__author__ = "Philipp Engel <philipp@mr-beam.org>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'

from flask import request, jsonify, make_response, url_for
import octoprint.util as util
from octoprint.server.api import api
import subprocess
import re
import logging
import wifi
import platform


@api.route("/wifi/scan", methods=["GET"])
def scanWifis():
	"""
	Scans for wifi networks and returns a list of SSIDs
	"""
	logger = logging.getLogger(__name__)
	logger.info("blabber")
	ssidlist = []

	# only scan on linux for now
	if platform.system() == 'Linux':
		ssidlist = doWifiScan()
	else:
		ssidlist = ['dinPort', 'UTD']

	return jsonify(ssids=ssidlist)

@api.route("/wifi/join", methods=["POST"])
def selectWifi():
	error = None
	if request.method == 'POST':
		if request.form['joinwifi'] == True:
			join_wifi(request.form['ssid'], request.form['password'])
	# nothing to to - we'll keep the wifi in ap mode

	return jsonify(result='{success: true}')

def doWifiScan():
	ssidlist = []
	try:
		iw_scan = subprocess.check_output(['/sbin/iw', 'wlan1', 'scan', 'ap-force'],
										  stderr=subprocess.STDOUT)
		ssidlist = re.findall(r'SSID: (.*)$', iw_scan, re.MULTILINE)
	except subprocess.CalledProcessError as e:
		print e
	else:
		iw_scan = iw_scan.decode('utf-8')
	return ssidlist

def joinWifi(ssid, password):
	# to do: create wifi config for new wifi, stop & disable hostapd & dhcp, activate wifi in client mode

	interfaces_template = '''
auto lo

iface lo inet loopback
iface eth0 inet dhcp

allow-hotplug wlan0
auto wlan0
iface wlan0 inet dhcp
  wpa-ssid "dinPort"
  wpa-psk "@cHt3rdeCk"

iface default inet dhcp

allow-hotplug wlan1
iface wlan1 inet dhcp
  wpa-ssid "{ssid_placeholder}"
  wpa-psk "{password_placeholder}"
	'''

	interfaces_text = interfaces_template.format(ssid_placeholder=ssid, password_placeholder=password)

	with open("/tmp/interfaces", "w") as text_file:
		text_file.write(interfaces_text)

	subprocess.check_call(["sudo", "cp", "/tmp/interfaces", "/etc/network/interfaces"])

	# subprocess.check_call(['sudo', 'update-rc.d', '-f', 'remove', 'hostapd'])
	# subprocess.check_call(['sudo', 'update-rc.d', '-f', 'remove', 'isc-dhcp-server'])

	subprocess.check_call(['sudo', 'service', 'hostapd', 'stop'])
	subprocess.check_call(['sudo', 'service', 'isc-dhcp-server', 'stop'])
	subprocess.check_call(['sudo', 'service', 'networking', 'restart'])

	return ""
