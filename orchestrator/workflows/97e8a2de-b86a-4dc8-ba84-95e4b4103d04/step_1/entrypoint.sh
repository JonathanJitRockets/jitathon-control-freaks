#!/bin/sh

# Fetch the rules
/app/clj-holmes fetch-rules -o /tmp/clj-holmes-rules/

# Run the scan
/app/clj-holmes scan -p /code -t json -o /tmp/output.json