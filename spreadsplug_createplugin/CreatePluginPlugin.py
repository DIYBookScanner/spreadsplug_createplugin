# -*- coding: utf-8 -*-
import logging

from spreads.plugin import DevicePlugin, DeviceFeatures, HookPlugin

class CreatePluginPlugin(HookPlugin):
    """ Plugin for CreatePlugin

    """

    @classmethod
    def configuration_template(cls):
        """ Allows a plugin to define its configuration keys.

        The returned dictionary has to be flat (i.e. no nested dicts)
        and contain a PluginOption object for each key.

        Example::

          {
           'a_setting': PluginOption(value='default_value'),
           'another_setting': PluginOption(value=[1, 2, 3],
                                           docstring="A list of things"),
           # In this case, 'full-fat' would be the default value
           'milk': PluginOption(value=('full-fat', 'skim'),
                                docstring="Type of milk",
                                selectable=True),
          }

        :return: dict with unicode: PluginOption(value, docstring, selection)
        """
        return {}

    @classmethod
    def add_command_parser(cls, rootparser):
        """ Allows a plugin to register a new command with the command-line
            parser. The subparser that is added to :param rootparser: should
            set the class' ``__call__`` method as the ``func`` (via
            ``set_defaults``) that is executed when the subcommand is specified
            on the CLI.

        :param rootparser: The root parser that this plugin should add a
                           subparser to.
        :type rootparser:  argparse.ArgumentParser

        """
        pass

    def prepare_capture(self, devices, path):
        """ Perform some action before capturing begins.

        :param devices:     The devices used for capturing
        :type devices:      list(DevicePlugin)
        :param path:        Project path
        :type path:         pathlib.Path

        """
        pass

    def capture(self, devices, path):
        """ Perform some action after each successful capture.

        :param devices:     The devices used for capturing
        :type devices:      list(DevicePlugin)
        :param path:        Project path
        :type path:         pathlib.Path

        """
        pass

    def finish_capture(self, devices, path):
        """ Perform some action after capturing has finished.

        :param devices:     The devices used for capturing
        :type devices:      list(DevicePlugin)
        :param path:        Project path
        :type path:         pathlib.Path

        """
        pass

    def process(self, path):
        """ Perform one or more actions that either modify the captured images
            or generate a different output.

        .. note:
            This method is intended to operate on the *done* subdfolder of
            the project directory. At the beginning of postprocessing, it
            will contain copies of the images in *raw*. This is to ensure that
            a copy of the original, scanned images will always be available
            for archival purposes.

        :param path:        Project path
        :type path:         pathlib.Path

        """
        pass

    def output(self, path):
        """ Assemble an output file from the postprocessed images.

        .. note:
            This method is intended to take its input files from the *done*
            subfolder of the project path and store its output in the
            *out* subfolder.

        :param path:        Project path
        :type path:         pathlib.Path

        """
        pass
