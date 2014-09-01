# coding=utf-8

__author__ = "Philipp Engel <philipp@mr-beam.org>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'

from flask import request, jsonify, make_response, url_for
import octoprint.util as util
from octoprint.server.api import api
import subprocess


@api.route("/wificfg", methods=["GET"])
def scanWifis():
	"""
	Scans for wifi networks and returns a list of SSIDs
	"""
	# try:
	    # iw_scan = subprocess.check_output(['/sbin/iw', 'wlan1', 'scan', 'ap-force'],
	                                          # stderr=subprocess.STDOUT)
	# except subprocess.CalledProcessError as e:
	    # raise InterfaceError(e.output.strip())
	# else:
	    # iw_scan = iw_scan.decode('utf-8')
		
	iw_scan = ['dinPort', 'UTD']
	return jsonify(ssids=iw_scan)
