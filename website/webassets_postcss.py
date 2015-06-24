from webassets.filter import ExternalTool, option

__all__ = ['PostCSS']


class PostCSS(ExternalTool):
    name = 'postcss'
    max_debug_level = None
    options = {
        'binary': 'POSTCSS_BIN',
        'plugins': option('POSTCSS_PLUGINS', type=list),
        'extra_args': option('POSTCSS_EXTRA_ARGS', type=list)
    }

    def input(self, infile, outfile, **kwargs):
        args = [self.binary or 'postcss']

        for plugin in self.plugins or []:
            args.extend(('--use', plugin))

        if self.extra_args:
            args.extend(self.extra_args)

        args.append(kwargs['source_path'])

        self.subprocess(args, outfile, infile)
