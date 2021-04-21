import globals
globalsInstance = globals.newGlobalsInstance(__file__
    , settingStatus = True
    , successStatus = True
    , errorStatus = True
    , debugStatus = True
    , failureStatus = True

    , warningStatus = True
    , wrapperStatus = True
    , logStatus = True
    # , testStatus = True
)

from python_framework import initialize
import IdealizarWhatsAppPoolerApi
app = IdealizarWhatsAppPoolerApi.app
api = IdealizarWhatsAppPoolerApi.api
jwt = IdealizarWhatsAppPoolerApi.jwt

@initialize(api, defaultUrl = '/swagger', openInBrowser=False)
def runFlaskApplication(app):
    app.run(debug=False, use_reloader=False)

if __name__ == '__main__' :
    runFlaskApplication(app)
