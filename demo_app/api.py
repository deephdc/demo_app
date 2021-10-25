"""
Integrate a model with the DEEP API
"""

import argparse
from functools import wraps
import json
import pkg_resources

from aiohttp.web import HTTPBadRequest
from webargs import fields

# import demo_app.config as cfg

print('#' * 100)


def _catch_error(f):
    """Decorate function to return an error as HTTPBadRequest, in case
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            raise HTTPBadRequest(reason=e)
    return wrap


# def _fields_to_dict(fields_in):
#     """
#     Example function to convert mashmallow fields to dict()
#     """
#     dict_out = {}
    
#     for key, val in fields_in.items():
#         param = {}
#         param['default'] = val.missing
#         param['type'] = type(val.missing)
#         if key == 'files' or key == 'urls':
#             param['type'] = str

#         val_help = val.metadata['description']
#         if 'enum' in val.metadata.keys():
#             val_help = "{}. Choices: {}".format(val_help, 
#                                                 val.metadata['enum'])
#         param['help'] = val_help

#         try:
#             val_req = val.required
#         except:
#             val_req = False
#         param['required'] = val_req

#         dict_out[key] = param
#     return dict_out


# def get_metadata():
#     """
#     Function to read metadata
#     https://docs.deep-hybrid-datacloud.eu/projects/deepaas/en/latest/user/v2-api.html#deepaas.model.v2.base.BaseModel.get_metadata
#     :return:
#     """

#     module = __name__.split('.', 1)

#     try:
#         pkg = pkg_resources.get_distribution(module[0])
#     except pkg_resources.RequirementParseError:
#         # if called from CLI, try to get pkg from the path
#         distros = list(pkg_resources.find_distributions(cfg.BASE_DIR, 
#                                                         only=True))
#         if len(distros) == 1:
#             pkg = distros[0]
#     except Exception as e:
#         raise HTTPBadRequest(reason=e)

#     predict_args = get_predict_args()
    
#     for key, val in predict_args.items():
#         predict_args[key]['type'] = str(val['type'])  # make 'type' JSON serializable

#     meta = {
#         'name': None,
#         'version': None,
#         'summary': None,
#         'home-page': None,
#         'author': None,
#         'author-email': None,
#         'license': None,
#         'help-train' : train_args,
#         'help-predict' : predict_args
#     }

#     for line in pkg.get_metadata_lines("PKG-INFO"):
#         line_low = line.lower() # to avoid inconsistency due to letter cases
#         for par in meta:
#             if line_low.startswith(par.lower() + ":"):
#                 _, value = line.split(": ", 1)
#                 meta[par] = value

#     return meta


def get_metadata():
    print('+' * 100)
    metadata = {
        "author": "Author name",
        "description": "Model description",
        "license": "Model's license",
        "url": "URL for the model (e.g. GitHub repository)",
        "version": "Model version",
    }
    return metadata



def get_predict_args():
    
    arg_dict = {
        "arg1": fields.Str(
            required=False,
            missing=None,
            enum=["choice1", "choice2"],  # list of choices
        ),
    }
    
    return arg_dict


@_catch_error
def predict(**kwargs):
    """
    Function to execute prediction
    https://docs.deep-hybrid-datacloud.eu/projects/deepaas/en/latest/user/v2-api.html#deepaas.model.v2.base.BaseModel.predict
    :param kwargs:
    :return:
    """

    return kwargs['arg1']



# def main():
#     """
#     Runs above-described methods from CLI
#     (see below an example)
#     """

#     if args.method == 'get_metadata':
#         meta = get_metadata()
#         print(json.dumps(meta))
#         return meta
#     elif args.method == 'predict':
#         # [!] you may need to take special care in the case of args.files [!]
#         results = predict(**vars(args))
#         print(json.dumps(results))
#         return results


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Model parameters', 
#                                      add_help=False)

#     cmd_parser = argparse.ArgumentParser()
#     subparsers = cmd_parser.add_subparsers(
#                             help='methods. Use \"deep_api.py method --help\" to get more info', 
#                             dest='method')

#     ## configure parser to call get_metadata()
#     get_metadata_parser = subparsers.add_parser('get_metadata', 
#                                          help='get_metadata method',
#                                          parents=[parser])
#     # normally there are no arguments to configure for get_metadata()

#     ## configure arguments for predict()
#     predict_parser = subparsers.add_parser('predict', 
#                                            help='commands for prediction',
#                                            parents=[parser]) 
#     # one should convert get_predict_args() to add them in predict_parser
#     # For example:
#     predict_args = _fields_to_dict(get_predict_args())
#     for key, val in predict_args.items():
#         predict_parser.add_argument('--%s' % key,
#                                default=val['default'],
#                                type=val['type'],
#                                help=val['help'],
#                                required=val['required'])

#     ## configure arguments for train()
#     train_parser = subparsers.add_parser('train', 
#                                          help='commands for training',
#                                          parents=[parser]) 
#     # one should convert get_train_args() to add them in train_parser
#     # For example:
#     train_args = _fields_to_dict(get_train_args())
#     for key, val in train_args.items():
#         train_parser.add_argument('--%s' % key,
#                                default=val['default'],
#                                type=val['type'],
#                                help=val['help'],
#                                required=val['required'])

#     args = cmd_parser.parse_args()
    
#     main()
