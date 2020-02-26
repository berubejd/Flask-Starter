#!/usr/bin/env python3.8

from application import create_app

application = create_app()

if __name__ == "__main__":
    application.run(ssl_context="adhoc")
