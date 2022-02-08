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


@app.route("/")
def index():
    """Return the site index."""
    return render_template("base.html")


@app.route("/ipcalc", methods=["GET", "POST"])
def ipcalc():
    """Calculate the submitted ip address information."""
    if request.method == "POST":
        return render_template("ipcalc.html",
                               ipaddr=request.form["ipaddr"],
                               netmask=request.form["netmask"],
                               wildcard="test",
                               network="test",
                               bcast="test",
                               hostmin="test",
                               hostmax="test",
                               hostnet="test")
    else:
        return render_template("base.html")


if __name__ == "__main__":
    app.run(debug=True)
