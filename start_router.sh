#!/bin/bash

source routes.sh

waitress-serve --port=8000 --call 'router:create_app'
