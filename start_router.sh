#!/bin/bash
# For "watch" mode, call with FLASK_ENV=development as well.

source routes.sh

FLASK_APP=router flask run --port 8080
