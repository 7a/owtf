"""
ACTIVE Plugin for Testing for Web Application Fingerprint (OWASP-IG-004)
"""

from framework.dependency_management.dependency_resolver import ServiceLocator

DESCRIPTION = "Active Probing for fingerprint analysis"


def run(PluginInfo):
    Content = ServiceLocator.get_component("plugin_helper").CommandDump(
        'Test Command',
        'Output',
        ServiceLocator.get_component("resource").GetResources('ActiveInfrastructureConfigurationManagement'),
        PluginInfo, [])  # No previous output
    return Content
