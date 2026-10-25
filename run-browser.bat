@echo off
cd /d "%~dp0"
where node >nul 2>nul
if errorlevel 1 (
  echo Node.js is not installed. Opening the static browser preview instead.
  start "" "%~dp0web\index.html"
) else (
  start "" "http://127.0.0.1:4173"
  node tools\serve.mjs
)
