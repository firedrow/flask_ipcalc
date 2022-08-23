#! python3
# -*- coding: utf-8 -*-

"""run.py.

This file is the application launcher.  Run this file to start the Flask
server.
"""

from app.views import app

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8100")
