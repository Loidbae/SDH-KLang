import logging
import shutil
import os
import getpass
from helpers import get_user
from subprocess import check_output

ENV_PATH = "/etc/environment"

LOG_PATH = f"/home/{get_user()}/homebrew/keyboard/log/"

KB_LAYOUT_FIELD = "XKB_DEFAULT_LAYOUT"
KB_VARIANT_FIELD = "XKB_DEFAULT_VARIANT"

os.makedirs(LOG_PATH, exist_ok=True) # Make log folder before writing to it
logging.basicConfig(filename=LOG_PATH+"keyboard.log",
                    format='[Keyboard] %(asctime)s %(levelname)s %(message)s',
                    filemode='w+',
                    force=True)
logger=logging.getLogger()
logger.setLevel(logging.INFO) # can be changed to logging.DEBUG for debugging issues

def get_user_home() -> str:
    return f"/home/{get_user()}"

def _get_plugin_settings_path() -> str:
    return f"{get_user_home()}/homebrew/"

def _write_to_env(lines):
    try:
        with open(ENV_PATH,"w") as w:
            w.writelines(lines)

    except:
        logger.critical("Couldn't write to environment file!")


def _read_env():
    try:
        with open(ENV_PATH,"r") as env:
            return env.readlines()

    except:
        logger.critical("Could not read environment file!")

def _find_field(field,lines):
    
    for i,line in enumerate(lines):
        found = line.find(field)

        if found != -1:
            return i
        
    return -1


def _get_current_kb_value(field):
    
    env = _read_env()
    fi = _find_field(field, env)

    if fi != -1:
        
        value = env[fi].split(field + "=")
        value = list(filter(lambda c: c != "", value)) # remove "" values from list
        value = value[0].replace("\n",'')
        value = value.replace("#",'none')

        return  value # return only the string value
    else:
        return "none" # returning the default value


def _set_current_kb_value(field, val):

    env = _read_env()
    fi = _find_field(field, env)
    nline = ""

    if val != "none":
        nline = field + "=" + val + "\n"


    if fi != -1:
        env[fi] = nline
    else:
        env.append(nline)
       
    _write_to_env(env)


def _blank_variable(variable):

    # Read environment file and set the variable to blank
    # This needs to be done to avoid invalid combinations which will result in a boot loop
    # We obviously want to avoid that...

    env = _read_env()
    fi = _find_field(variable,env)

    if fi != -1:
        env[fi] = ""
        
    _write_to_env(env)

def _get_kb_layouts_():

    # Get all available keyboard layouts
    layouts = check_output(["localectl","list-x11-keymap-layouts"])

    # Decode bytes to string so they can be manipulated
    string_lays = layouts.decode()
    lay_data = str.split(string_lays,'\n')

    # Insert default option into the array
    dropdownOptions = [{
        'label':"Default",
        'data':"none"
    }]

    for d in lay_data:
        if d == "nec_vndr/jp" or d == "" or d == "custom": continue
        dropdownOptions.append({'label':d,'data':d})

    return dropdownOptions


def _get_kb_variants_():

    # Get the current layout to generate a variant list
    layout = _get_current_kb_value(KB_LAYOUT_FIELD)

    # Insert default option
    dropdownOptions = [{
        'label':"Default",
        'data':"none"
    }]

    if layout != "none":

        # Get all available keyboard variants with the selected language
        variants = check_output(["localectl","list-x11-keymap-variants",layout])

        # Decode bytes to string so they can be manipulated
        string_var = variants.decode()
        var_data = str.split(string_var,'\n')
        var_data = list(filter(lambda c: c != "", var_data))

        for d in var_data:
            dropdownOptions.append({'label':d,'data':d})
    
    return dropdownOptions
        
class Plugin:

    async def dummy_function(self) -> bool:
        return True

    # A normal method. It can be called from JavaScript using call_plugin_function("method_1", argument1, argument2)
    async def get_kb_layouts(self):
        return _get_kb_layouts_()

    async def get_kb_variants(self):
        return _get_kb_variants_()

    async def get_current_kb_layout(self):
        return _get_current_kb_value(KB_LAYOUT_FIELD)

    async def get_current_kb_variant(self):
        return _get_current_kb_value(KB_VARIANT_FIELD)

    async def set_kb_layout(self,layout):
        _set_current_kb_value(KB_LAYOUT_FIELD, layout)

    async def set_kb_variant(self,variant):
        _set_current_kb_value(KB_VARIANT_FIELD, variant)

    async def unset_variant(self):
        _blank_variable(KB_VARIANT_FIELD)

    # Asyncio-compatible long-running code, executed in a task when the plugin is loaded
    async def _main(self):
        logger.info("Initializing...")

        p_settings_path = _get_plugin_settings_path()
        plugin_options_path = p_settings_path + "keyboard/"
        backup_path = plugin_options_path + "backup/"
        backup_env = backup_path + "environment"

        os.makedirs(plugin_options_path, exist_ok=True)
        os.makedirs(backup_path, exist_ok=True)

        # Backing up the environment file, just in case. On linux shit can go down fast...
        if not os.path.isfile(backup_env):
            logger.info("Backing up environment file..")
            shutil.copy2(ENV_PATH, backup_env)


    # Function called first during the unload process, utilize this to handle your plugin being removed
    async def _unload(self):
        logger.info("Unloading Plugin!")
        pass
