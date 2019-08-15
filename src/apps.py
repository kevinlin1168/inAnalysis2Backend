import os
from flask import Flask
from flask_restful import Api
from service.userService.controller.signin import Singin
from service.userService.controller.signup import Singup
import logging
import sys
sys.dont_write_bytecode = True #disable __pycache__
from params import params

par=params()
app = Flask(__name__)
api = Api(app)

# bind api
api.add_resource(Singin, "/user/signin")
api.add_resource(Singup, "/user/signup")


if __name__ == "__main__":
    if '--debug' in sys.argv:
        logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')
    else:
        logging.basicConfig(level=logging.INFO , format='[%(levelname)s] %(message)s')
    logging.info(f'Inanalysis running at port {par.port}')
    app.run(debug='--debug' in sys.argv,port=par.port,host='0.0.0.0')