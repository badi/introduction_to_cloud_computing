from fabric.api import task, local
import sys
import os

browser = "firefox"

if sys.platform == 'darwin':
    browser = "open"

@task
def notebook():
    local("bin/convert")
    
@task
def view():
    """view the documentation in a browser"""
    local("{browser} docs/build/html/index.html".format(browser=browser))

@task
def html():
    # disable Flask RSTPAGES due to sphins incompatibility
    os.environ['RSTPAGES'] = 'FALSE'
    # api()
    # man()
    """build the doc locally and view"""
    local("rm -f docs/build/html/notebook/*")
    notebook()
    local("cd docs; make html")


@task
def gh():
    """deploy the documentation on gh-pages"""
    local("rm -f docs/source/modules/*")
    local("git checkout gh-pages")
    local("make pages")

@task
def man():
    """deploy the documentation on gh-pages"""
    #TODO: match on "Commands"
    local("cm man | grep -A10000 \"Commands\"  | sed \$d  > docs/source/man/man.rst")

@task
def api():
    for modulename in ["cloudmesh", "cloudmesh_common", "cloudmesh_install", "cmd3local", "cloudmesh_web"]:
        print 70 * "="
        print "Building API Doc:", modulename 
        print 70 * "="        
        local("sphinx-apidoc -f -o docs/source/api/{0} {0}".format(modulename))



