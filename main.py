import flask
from rapidscan_wrapper import RapidScan
import os
from os import path
import logging

scan_backend = flask.Flask("scan_backend")


def _import_module(module_name):
    try:
        module = __import__(path.join("./modules", module_name, "module"))
    except ImportError:
        return None
    return module


def _install_module_dependencies(module_name):
    logging.info("Installing dependencies for module {}".format(module_name))
    try:
        module = _import_module(module_name)
        if module is not None:
            module.install_dependencies()
    except Exception as e:
        logging.error(
            "Error installing dependencies for module {}: {}".format(module_name, e))
        exit(1)


def _for_all_modules(func):
    for module_name in os.listdir("./modules"):
        func(module_name)


@scan_backend.route("/api/modules/<module_name>/invoke", methods=["POST"])
def invoke_module(module_name):
    module = _import_module(module_name)
    if module is None:
        return flask.jsonify({"error": "Module not found"}), 404
    if not hasattr(module, "Module"):
        return flask.jsonify({"error": "Module not found"}), 404
    if not hasattr(module.Module, "invoke"):
        return flask.jsonify({"error": "Module not found"}), 404
    params = flask.request.json
    if params is None:
        return flask.jsonify({"error": "Invalid parameters"}), 400
    module_instance = module.Module(params)
    return flask.jsonify(module_instance.invoke())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting scan_backend")
    logging.info("Installing dependencies for modules")
    _for_all_modules(_install_module_dependencies)
    logging.info("Starting Server...")
    scan_backend.run(host="127.0.0.1", port=5000)
