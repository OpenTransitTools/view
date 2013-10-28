from ConfigParser import SafeConfigParser
import glob
import logging
log = logging.getLogger()

INI=['view.ini', 'app.ini']
parser = None

def get_parser(ini=None):
    ''' make the config parser
    '''
    global parser

    try:
        if parser is None:
            candidates = []
            if ini is None: 
                ini = INI
            for i in ini:
                # add the .ini file and ./config/.ini file to our candidate file list
                candidates.append(i)
                candidates.append('./config/' + i)

            parser = SafeConfigParser()
            found = parser.read(candidates)
            logging.config.fileConfig(found)
    except:
        log.info("Couldn't find an acceptable ini file from {0}...".format(candidates))

    return parser


def get(id, def_val=None, section='view'):
    ''' get config value
    '''
    ret_val = def_val
    try:
        if get_parser():
            ret_val = get_parser().get(section, id)
            if ret_val is None:
                ret_val = def_val
    except:
        log.info("Couldn't find '{0}' in config under section '{1}'".format(id, section))

    return ret_val


def get_int(id, def_val=None, section='view'):
    ''' get config value as int (or go with def_val)
    '''
    ret_val = def_val
    try:
        v = get(id, def_val, section)
        if v:
            ret_val = int(v)
    except:
        log.info("Couldn't find int value '{0}' in config under section '{1}'".format(id, section))

    return ret_val
