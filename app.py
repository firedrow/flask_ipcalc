#! python3
# -*- coding: utf-8 -*-

"""
main.py.

This file starts the flask application.
"""

import ipaddress
import re
from flask import Flask, render_template, request

app = Flask(__name__)

def calcSubnet(cidr):
    pass


@app.route("/")
def index():
    """Return the site index."""
    return render_template("base.html")


@app.route("/ipcalc", methods=["GET", "POST"])
def ipcalc():
    """Calculate the submitted ip address information."""
    if request.method == "POST":
        ipaddr = request.form["ipaddr"]
        netmask = request.form["netmask"]
        subnet = ipaddress.IPv4Network(f"{ipaddr}/{netmask}", strict=False)

        return render_template("ipcalc.html",
                               ipaddr=ipaddr,
                               netmask=netmask,
                               wildcard=subnet.hostmask,
                               network=subnet,
                               bcast=subnet.broadcast_address,
                               hostmin=list(subnet.hosts())[0],
                               hostmax=list(subnet.hosts())[-1],
                               hostnet=subnet.num_addresses)
    else:
        return render_template("base.html")


if __name__ == "__main__":
    app.run(debug=True)
