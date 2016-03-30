from framework.dependency_management.dependency_resolver import ServiceLocator

DESCRIPTION = "XML Injection Plugin to assist manual testing"


def run(PluginInfo):
    Content = ServiceLocator.get_component("plugin_helper").ResourceLinkList(
        'Online Resources',
        ServiceLocator.get_component("resource").GetResources('ExternalXMLInjection'))
    return Content
