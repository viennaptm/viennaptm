@ECHO OFF
set SPHINXBUILD=sphinx-build
set SOURCEDIR=source
set BUILDDIR=build

%SPHINXBUILD% -b html %SOURCEDIR% %BUILDDIR%/html
