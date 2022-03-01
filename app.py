#! python3
# -*- coding: utf-8 -*-

"""
main.py.

This file starts the flask application.
"""

import json
import ipaddress
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    """Return the site index."""
    return render_template("base.html")


@app.route("/ipcalc", methods=["GET", "POST"])
def ipcalc():
    """Calculate the submitted ip address information."""
    if (request.method == "POST") and (request.form["newmask"] == ""):
        ipaddr = request.form["ipaddr"]
        netmask = request.form["netmask"]
        subnet = ipaddress.IPv4Network(f"{ipaddr}/{netmask}", strict=False)
        subnetinfo = ('{'
                      f'"address": "{ipaddr}",'
                      f'"netmask": "{netmask}",'
                      f'"wildcard": "{subnet.hostmask}",'
                      f'"network": "{subnet.with_prefixlen}",'
                      f'"broadcast": "{subnet.broadcast_address}",'
                      f'"hostmin": "{list(subnet.hosts())[0]}",'
                      f'"hostmax": "{list(subnet.hosts())[-1]}",'
                      f'"hostnet": "{len(list(subnet.hosts()))}"'
                      '}')
        return render_template("ipcalc.html", subnet=json.loads(subnetinfo))

    elif (request.method == "POST") and (request.form != ""):
        ipaddr = request.form["ipaddr"]
        netmask = request.form["netmask"]
        subnet = ipaddress.IPv4Network(f"{ipaddr}/{netmask}", strict=False)
        subnetinfo = ('{'
                      f'"address": "{ipaddr}",'
                      f'"netmask": "{netmask}",'
                      f'"wildcard": "{subnet.hostmask}",'
                      f'"network": "{subnet.with_prefixlen}",'
                      f'"broadcast": "{subnet.broadcast_address}",'
                      f'"hostmin": "{list(subnet.hosts())[0]}",'
                      f'"hostmax": "{list(subnet.hosts())[-1]}",'
                      f'"hostnet": "{len(list(subnet.hosts()))}"'
                      '}')

        newmask = request.form['newmask']
        newmasks = []
        if int(newmask) > int(netmask):  # Subnet
            for newnet in subnet.subnets(new_prefix=int(newmask)):
                newmasks.append({
                                "network": f"{newnet.with_prefixlen}",
                                "broadcast": f"{newnet.broadcast_address}",
                                "hostmin": f"{list(newnet.hosts())[0]}",
                                "hostmax": f"{list(newnet.hosts())[-1]}",
                                "hostnet": f"{len(list(newnet.hosts()))}"
                                })
        else:  # Supernet
            newnet = subnet.supernet(new_prefix=int(newmask))
            newmasks.append({
                            "network": f"{newnet.with_prefixlen}",
                            "broadcast": f"{newnet.broadcast_address}",
                            "hostmin": f"{list(newnet.hosts())[0]}",
                            "hostmax": f"{list(newnet.hosts())[-1]}",
                            "hostnet": f"{len(list(newnet.hosts()))}"
                            })
        print(newmasks)

        return render_template("subnets.html", subnet=json.loads(subnetinfo),
                               newmasks=json.loads(json.dumps(newmasks)))

    else:
        return render_template("base.html")


if __name__ == "__main__":
    app.run()
