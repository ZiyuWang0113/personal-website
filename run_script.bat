@echo off
"C:\Users\ziyuw\anaconda3\python.exe" "D:\Github\personal-website\opus_scraper.py"

REM Pull the latest changes from GitHub to avoid conflicts
git pull --rebase origin main

REM Add all changes to Git
git add .

REM Commit only if there are changes
git diff --cached --quiet || git commit -m "Auto update on %date%"

REM Push changes to GitHub
git push origin main

REM Pause to keep the window open for debugging
echo.
echo Script execution completed. Press any key to exit.
pause