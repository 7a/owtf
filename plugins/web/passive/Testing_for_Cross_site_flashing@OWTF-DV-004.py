"""
PASSIVE Plugin for Testing for Cross site flashing (OWASP-DV-004)
"""

from framework.dependency_management.dependency_resolver import ServiceLocator

DESCRIPTION = "Google Hacking for Cross Site Flashing"


def run(PluginInfo):
    Content = ServiceLocator.get_component("plugin_helper").ResourceLinkList(
        'Online Resources',
        ServiceLocator.get_component("resource").GetResources('PassiveCrossSiteFlashingLnk'))
    return Content
