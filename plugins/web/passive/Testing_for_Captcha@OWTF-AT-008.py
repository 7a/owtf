"""
PASSIVE Plugin for Testing for Captcha (OWASP-AT-008)
"""

from framework.dependency_management.dependency_resolver import ServiceLocator

DESCRIPTION = "Google Hacking for CAPTCHA"


def run(PluginInfo):
    Content = ServiceLocator.get_component("plugin_helper").ResourceLinkList(
        'Online Resources',
        ServiceLocator.get_component("resource").GetResources('PassiveCAPTCHALnk'))
    return Content
