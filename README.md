view
====
Web UI atop services (gtfs / trasnit web service)
@see http://opentransittools.com/services

build:
  0. install python 2.7, along easy_install, zc.buildout ("zc.buildout==1.5.2") and git
  1. install and pserve http://opentransittools.com/services
  2. git clone https://github.com/OpenTransitTools/view.git
  2. cd view
  3. buildout
  4. git update-index --assume-unchanged .pydevproject

run:
  1. rm nohup.out; nohup bin/pserve config/development.ini --reload VIEW=1 &
  2. http://localhost:33333/stop.html?stop_id=2

test:
  1. bin/test
  2. Selenium Test: ott/view/test/pages.html
  3. Selenium Test: ott/view/test/services.html
     @see Selenium IDE (Firefox Mac/Win) at http://docs.seleniumhq.org/projects/ide/
