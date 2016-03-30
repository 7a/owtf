"""
GREP Plugin for Testing for application configuration management (OWASP-CM-004) <- looks for HTML Comments
https://www.owasp.org/index.php/Testing_for_application_configuration_management_%28OWASP-CM-004%29
NOTE: GREP plugins do NOT send traffic to the target and only grep the HTTP Transaction Log
"""

from framework.dependency_management.dependency_resolver import ServiceLocator

DESCRIPTION = "Plugin to assist manual testing"


def run(PluginInfo):
    Content = ServiceLocator.get_component("plugin_helper").ResourceLinkList(
        'Online Resources',
        ServiceLocator.get_component("resource").GetResources('ExternalFileExtHandling'))
    return Content
