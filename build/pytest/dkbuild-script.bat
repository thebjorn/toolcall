@echo off
@echo ^<testpackage^>
@echo ^<testpackage:start-time^>
@python -c "import time;print(time.time())"
@echo ^</testpackage:start-time^>
@echo cd c:\srv\work\toolcall
cd c:\srv\work\toolcall
@echo touch c:\srv\work\toolcall\build\this-file-left-on-errors
touch c:\srv\work\toolcall\build\this-file-left-on-errors
@echo ^<testpackage:activate^>
@echo toolcall311
pushd \srv\venv\toolcall311
@call Scripts\activate.bat
if errorlevel 1 (
@echo.
@echo.
@echo.
@echo.
@echo.
@echo ERROR Couldn't activate virtualenv: toolcall311
@echo.
@echo.
exit 1
)
popd
@echo ^</testpackage:activate^>
@echo ^<testpackage:update-pip^>
@echo python -m pip install -U pip --no-compile --no-index --find-links file:///srv/wheelhouse
python -m pip install -U pip --no-compile --no-index --find-links file:///srv/wheelhouse
@echo ^</testpackage:update-pip^>
@echo ^<testpackage:pwd^>
@pwd
@echo ^</testpackage:pwd^>
@echo ^<testpackage:package-requirements^>
@echo python -m pip install -r requirements.txt --no-compile --no-index --find-links file:///srv/wheelhouse
python -m pip install -r requirements.txt --no-compile --no-index --find-links file:///srv/wheelhouse
if errorlevel 1 (
@echo.
@echo.
@echo.
@echo.
@echo.
@echo ERROR pip exited with an error code
@echo.
@echo.
exit 1
)
@echo ^</testpackage:package-requirements^>
@echo ^<testpackage:test-requirements^>
@echo python -m pip install pytest-cov --no-compile --no-index --find-links file:///srv/wheelhouse
python -m pip install pytest-cov --no-compile --no-index --find-links file:///srv/wheelhouse
@echo python -m pip install -e .
python -m pip install -e .
@echo ^</testpackage:test-requirements^>
@echo ^<testpackage:python-version^>
@python --version
@echo ^</testpackage:python-version^>
@echo ^<testpackage:pip-version^>
@pip --version
call which pip
@echo ^</testpackage:pip-version^>
@echo ^<testpackage:pytest-version^>
@pytest --version
call which pytest
@echo ^</testpackage:pytest-version^>
@echo ^<testpackage:coverage-version^>
@coverage --version
call which coverage
@echo ^</testpackage:coverage-version^>
@echo ^<testpackage:pipfrozen^>
@echo pip list
pip list
@echo ^</testpackage:pipfrozen^>
@echo ^<testpackage:pytest^>
set "DJANGO_SETTINGS_MODULE="
set "TESTING=1"
set "DKTESTDATA=c:\srv\data\testdata"
@echo rm -f c:\srv\work\toolcall\build\pytest\pytest-collectonly.txt
rm -f c:\srv\work\toolcall\build\pytest\pytest-collectonly.txt
@echo ^<testpackage:pytest-collectonly^>
@echo pytest --collectonly c:\srv\work\toolcall\tests ^> c:\srv\work\toolcall\build\pytest\pytest-collectonly.txt
pytest --collectonly c:\srv\work\toolcall\tests > c:\srv\work\toolcall\build\pytest\pytest-collectonly.txt
@echo ^</testpackage:pytest-collectonly^>
if errorlevel 1 (
@echo.
@echo.
@echo.
@echo.
@echo.
@echo ERROR pytest --collectonly failed
@echo.
@echo.
type c:\srv\work\toolcall\build\pytest\pytest-collectonly.txt
exit 1
)
@echo rm -f build\pytest\pytest-junit.xml
rm -f build\pytest\pytest-junit.xml
@echo rm -f c:\srv\work\toolcall\build\coverage\coverage-report.txt
rm -f c:\srv\work\toolcall\build\coverage\coverage-report.txt
@echo rm -f .coverage
rm -f .coverage
@echo pytest --color=no --verbose --ignore=toolcall\migrations --junit-xml=build\pytest\pytest-junit.xml  --cov=toolcall --cov-config=.coveragerc tests
pytest --color=no --verbose --ignore=toolcall\migrations --junit-xml=build\pytest\pytest-junit.xml  --cov=toolcall --cov-config=.coveragerc tests
@echo %ERRORLEVEL% > pytest.exit
@echo coverage combine
coverage combine
@echo coverage report ^> c:\srv\work\toolcall\build\coverage\coverage-report.txt
coverage report > c:\srv\work\toolcall\build\coverage\coverage-report.txt
@echo ^</testpackage:pytest^>
@echo ^<testpackage:end-time^>
@python -c "import time;print(time.time())"
@echo ^</testpackage:end-time^>
@echo ^</testpackage^>
@echo rm -f c:\srv\work\toolcall\build\this-file-left-on-errors
rm -f c:\srv\work\toolcall\build\this-file-left-on-errors
