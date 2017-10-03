view
====
Web UI atop services (gtfs / trasnit web service)
@see http://opentransittools.com/services

build:
  1. install python 2.7, along easy_install, zc.buildout ("zc.buildout==1.5.2") and git
  1. install and pserve http://opentransittools.com/services
  1. git clone https://github.com/OpenTransitTools/view.git
  1. cd view
  1. buildout
  1. git update-index --assume-unchanged .pydevproject

run:
  1. rm nohup.out; nohup bin/pserve config/development.ini --reload VIEW=1 &
  1. http://localhost:33333/stop.html?stop_id=2

test:
  1. bin/test
  1. Selenium Test: ott/view/test/pages.html
  1. Selenium Test: ott/view/test/services.html
     @see Selenium IDE (Firefox Mac/Win) at http://docs.seleniumhq.org/projects/ide/

update localizations:
  1. bin/py setup.py extract_messages        # (re)generates the .pot template file...run anytime you add a new $_ to your code/templates
  1. #bin/python setup.py init_catalog -l en # NOTE: only run once ... adds English as a language
  1. #bin/python setup.py init_catalog -l es # NOTE: only run once ... adds Spanish as a language
  1. bin/python setup.py update_catalog # updates your localized .po files (those originally created by init_catalog)
  1. make changes to .pot files
  1. bin/python setup.py compile_catalog # generates the .mo files

api:
  1. https://trimet.org/ride/header.html?header=__BLAH___%20~~BLAH~~~%20_*BLAH*_%20_**BLA**_&second_header=This%20is%20%5BTriMet%5D(https://en.wikipedia.org/wiki/TriMet)%27s%20Wiki%20Entry&sub_header=N%C3%BAmero%20uno%20buenos%20d%C3%ADas&title=N%C3%BAmero%20uno%20buenos%20d%C3%ADas&emergency_content=This%20Is%20not%20an%20emergency&icon_cls=fa-ss-outline&icon_url=https://twitter.com/trimet


