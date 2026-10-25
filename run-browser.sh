#!/bin/sh
cd "$(dirname "$0")" || exit 1
if command -v node >/dev/null 2>&1; then
  echo 'Open http://127.0.0.1:4173 in your browser.'
  node tools/serve.mjs
else
  echo 'Install Node.js for a localhost preview, or open web/index.html directly.'
fi
