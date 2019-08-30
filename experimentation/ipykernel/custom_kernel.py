# import ipdb

import json
import atexit

from IPython.core.interactiveshell import InteractiveShell


class MyShell(InteractiveShell):
    def __init__(self, ipython_dir=None, profile_dir=None,
                 user_module=None, user_ns=None,
                 custom_exceptions=((), None), **kwargs):

        # This is where traits with a config_key argument are updated
        # from the values on config.
        super(InteractiveShell, self).__init__(**kwargs)
        # if 'PromptManager' in self.config:
        #     warn('As of IPython 5.0 `PromptManager` config will have no effect'
        #          ' and has been replaced by TerminalInteractiveShell.prompts_class')
        self.configurables = [self]

        # These are relatively independent and stateless
        self.init_ipython_dir(ipython_dir)
        self.init_profile_dir(profile_dir)
        self.init_instance_attrs()
        self.init_environment()

        # Check if we're in a virtualenv, and set up sys.path.
        self.init_virtualenv()

        # Create namespaces (user_ns, user_global_ns, etc.)
        self.init_create_namespaces(user_module, user_ns)
        # This has to be done after init_create_namespaces because it uses
        # something in self.user_ns, but before init_sys_modules, which
        # is the first thing to modify sys.
        # TODO: When we override sys.stdout and sys.stderr before this class
        # is created, we are saving the overridden ones here. Not sure if this
        # is what we want to do.
        self.save_sys_module_state()
        self.init_sys_modules()

        # While we're trying to have each part of the code directly access what
        # it needs without keeping redundant references to objects, we have too
        # much legacy code that expects ip.db to exist.
        # self.db = PickleShareDB(os.path.join(self.profile_dir.location, 'db'))

        self.init_history()
        self.init_encoding()
        self.init_prefilter()

        self.init_syntax_highlighting()
        self.init_hooks()
        self.init_events()
        self.init_pushd_popd_magic()
        self.init_user_ns()
        self.init_logger()
        self.init_builtins()

        # The following was in post_config_initialization
        self.init_inspector()
        self.raw_input_original = input
        self.init_completer()
        # TODO: init_io() needs to happen before init_traceback handlers
        # because the traceback handlers hardcode the stdout/stderr streams.
        # This logic in in debugger.Pdb and should eventually be changed.
        self.init_io()
        self.init_traceback_handlers(custom_exceptions)
        self.init_prompts()
        self.init_display_formatter()
        self.init_display_pub()
        self.init_data_pub()
        self.init_displayhook()
        self.init_magics()
        self.init_alias()
        self.init_logstart()
        self.init_pdb()
        self.init_extension_manager()
        self.init_payload()
        self.init_deprecation_warnings()
        self.hooks.late_startup_hook()
        self.events.trigger('shell_initialized', self)
        atexit.register(self.atexit_operations)


def main():
    # kernel = MyKernel()
    # stream = json.dumps(
    #     {
    #         'code': 'import matplotlib.pyplot as plt; plt.plot([0,1])',
    #         'allow_stdin': False
    #     })

    shell = MyShell()
    shell.run_cell('import matplotlib.pyplot as plt; plt.plot([0,1])')


if __name__ == '__main__':
    main()
