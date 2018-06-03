#!/bin/bash
heroku logs -r heroku_prod -d web --tail | grep -w -e vyatsu
