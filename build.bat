rd /s /q build
xcopy lib build\lib /E /I
xcopy src build /E /EXCLUDE:.gitignore
mkdir build\storage\patches
