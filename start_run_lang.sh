#!/bin/bash

waitress-serve --port=9000 --call 'run_lang:create_app'
