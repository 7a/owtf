from framework.dependency_management.dependency_resolver import ServiceLocator

DESCRIPTION = "Runs commands on an agent server via SBD -i.e. for IDS testing-"


def run(PluginInfo):
    Core = ServiceLocator.get_component("core")
    Content = "%s Results:<br />" % DESCRIPTION
    plugin_params = ServiceLocator.get_component("plugin_params")
    config = ServiceLocator.get_component("config")
    for Args in plugin_params.GetArgs({
        'Description': DESCRIPTION,
        'Mandatory': {
            'RHOST': config.Get('RHOST_DESCRIP'),
            'SBD_PORT': config.Get('SBD_PORT_DESCRIP'),
            'SBD_PASSWORD': config.Get('SBD_PASSWORD_DESCRIP'),
            'COMMAND_FILE': config.Get('COMMAND_FILE_DESCRIP')
        },
        'Optional': {
            'REPEAT_DELIM': config.Get('REPEAT_DELIM_DESCRIP')}}, PluginInfo):

        plugin_params.SetConfig(Args)  # Sets the auxiliary plugin arguments as config
        Core.RemoteShell.Open({
                              'ConnectVia': config.GetResources('RCE_SBD_Connection'),
                              'InitialCommands': None
                              }, PluginInfo)
        Core.RemoteShell.RunCommandList(Core.GetFileAsList(Args['COMMAND_FILE']))
        Core.RemoteShell.Close(PluginInfo)

    return Content
