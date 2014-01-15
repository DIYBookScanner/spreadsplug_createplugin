# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os

from string import Template
from spreads.plugin import SpreadsPlugin, DevicePlugin, DeviceFeatures, HookPlugin

logger = logging.getLogger('spreadsplug.createplugin')

plugin_types = [SpreadsPlugin]
plugin_types.extend(list(SpreadsPlugin.__subclasses__()))

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
        createplugin_parser = rootparser.add_parser(
            'createplugin', help="Create a new Spreads plugin")
        createplugin_parser.add_argument(
            "plugin_type", type=unicode, help="Plugin type",
            metavar='<{0}>'.format(','.join(
                map(lambda cls: cls.__name__, plugin_types))
              ))
        createplugin_parser.add_argument(
            "plugin_name", type=unicode, help="Plugin name")
        createplugin_parser.set_defaults(subcommand=cls.createplugin)

    def createplugin(config):
        new_plugin_name = config['plugin_name'].get()
        new_plugin_type = config['plugin_type'].get()
        # http://www.mtu.edu/umc/services/web/cms/characters-avoid/
        # TODO: more vigorous list/method
        bad_chars = '#<$+%>!`&*|{?"=}/:@ \'\t\n\\'
        sub_char = '-' # '_' not liked by python eggs
        new_plugin_name = ''.join(c if c not in bad_chars else sub_char for c in new_plugin_name)
        if new_plugin_type not in map(lambda cls: cls.__name__, plugin_types):
            logger.error('Plugin type "{type}" not known! Please choose '
                         'one of {types}.'.format(
                             type=new_plugin_type,
                             types='<{0}>'.format(','.join(
                                 map(lambda cls: cls.__name__, plugin_types)
                               ))
                           ))
        else:
            create_new_plugin(new_plugin_name, new_plugin_type)

    def create_new_plugin(plugin_name, plugin_type):
        """ Creates a blank project for developing a spreads plugin
        Inspiration from the django project's startapp, startproject command
        https://github.com/django/django/blob/master/django/core/management/templates.py

        :param plugin_name:  name of the new plugin
        :type plugin_name:   unicode
        :param plugin_type:  the type of plugin
        :type plugin_type:   unicode
        """

        def copy_directories_files(basedir, destdir, exclude_dirs, exclude_files):
            """ Copies and templates files ending in '.in' from basedir
            to destdir.

            :param basedir:       directory containing templates (.in suffix)
            :type basedir:        unicode
            :param destdir:       directory to copy templates to
            :type destdir:        unicode
            :param exclude_dirs:  list-ish of directories to ignore
            :type exclude_dirs:   [unicode]
            :param exclude_files: list-ish of filenames to ignore
            :type exclude_files:  [unicode]
            """
            for root, dirs, files in os.walk(basedir):
                for dirname in dirs:
                    template_dir = os.sep.join((root, dirname))
                    if dirname in exclude_dirs:
                        logger.info('Skipping "{0}"...'.format(template_dir))
                        continue
                    _dir = os.sep.join((destdir, dirname))
                    os.makedirs(_dir)
                    logger.info('Directory "{0}" created.'.format(_dir))
                    copy_directories_files(template_dir, exclude_dirs, _dir)
                for filename in files:
                    template_path = os.sep.join((root, filename))
                    if not filename.endswith('.in') \
                      or filename in exclude_files \
                      or root.endswith(tuple(exclude_dirs)):
                        logger.info('Skipping "{0}"...'.format(template_path))
                        continue
                    path = os.sep.join((destdir, filename[0:-3]))
                    logger.info('Copying "{0}" to "{1}"...'.format(template_path, path))
                    with open(template_path, 'rb') as template_file:
                        content = template_file.read()
                        content = content.decode('utf-8')
                        template = Template(content)
                        content = template.substitute(constants)
                        content = content.encode('utf-8')
                        with open(path, 'wb') as new_file:
                            new_file.write(content)

        # The following five variables need well-written tests; they are
        # constants pointing to assumed-existing locations in the filesystem.
        template_dirname = 'template'
        template_module_dirname = 'module'
        template_dir = os.sep.join(
            (os.path.dirname(__file__), template_dirname))
        template_module_dir = os.sep.join((template_dir, template_module_dirname))
        
        exclude_filenames = ['PluginTemplate.py.in',
                             'DevicePluginTemplate.py.in',
                             'HookPluginTemplate.py.in']

        logger.info('Using template directory "{0}"...'.format(template_dir))

        # set all of our paths and filenames
        constants = {
            'name': plugin_name,
            'path': plugin_name.lower(),
            'package': 'spreadsplug_{0}'.format(plugin_name.lower()),
            'classname': '{0}{1}Plugin'.format(plugin_name[0].upper(), plugin_name[1:]),
            'superclass': plugin_type}
        constants['packagepath'] = os.sep.join(
            (constants['path'], constants['package']))

        #TODO: we managed to avoid unicode strings up until now... fix!
        # order is important, PluginTemplate is a header file
        template_files = ['PluginTemplate.py.in']
        entry_points = {}
        if plugin_type == 'DevicePlugin' or plugin_type == 'SpreadsPlugin':
            template_files.append('DevicePluginTemplate.py.in')
            entry_points['spreadsplug.devices'] = [
                '{name} = {package}.{classname}:{classname}'.format(**constants)]
        if plugin_type == 'HookPlugin' or plugin_type == 'SpreadsPlugin':
            template_files.append('HookPluginTemplate.py.in')
            entry_points['spreadsplug.hooks'] = [
                '{name} = {package}.{classname}:{classname}'.format(**constants)]
        
        constants['entry_points'] = unicode(repr(entry_points))
        
        if os.path.exists(constants['path']):
            logger.error('Directory "{path}" already exists! Please '
                         'remove "{path}" or choose a different name.'.format(
                             **constants))
            return

        # Create a folder for the project, create a python module inside
        os.makedirs(constants['path'])
        logger.info('Directory "{path}" created.'.format(**constants))
        os.makedirs(constants['packagepath'])
        open('{packagepath}/__init__.py'.format(**constants), 'a').close()
        logger.info('Directory "{packagepath}" created.'.format(**constants))

        # Copy from 'template' (template_dir), ignoring 'module'
        copy_directories_files(template_dir, constants['path'],
                               [template_module_dirname], [])
        # ...now copy from 'module' (template_module_dirname)
        copy_directories_files(template_module_dir, constants['packagepath'],
                               [], exclude_filenames)

        # Create the entry point by appending many templates together
        path = '{packagepath}/{classname}.py'.format(**constants)
        with open(path, 'wb') as f:
            for filename in template_files:
                template_path = os.sep.join((template_module_dir, filename))
                logger.info('Copying "{0}" to "{1}"...'.format(template_path, path))
                with open(template_path, 'rb') as template_file:
                    content = template_file.read()
                    content = content.decode('utf-8')
                    template = Template(content)
                    content = template.substitute(constants)
                    content = content.encode('utf-8')
                    f.write(content)
