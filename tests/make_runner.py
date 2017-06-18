'''
Utilities for testing makefiles.
'''

import pytest
import textwrap
import subprocess
import collections


class MakeRunner:
    '''
    A class that executes bits of make scripts in a temporary directory.

    Example usage:
    >>> make = MakeRunner()
    >>> res = make.run('VAR := 1')
    >>> res.returncode
    0
    '''

    def __init__(self, tmpdir, make_exe='gmake', valid_exit_codes={0}):
        self.tmpdir = tmpdir
        self.make_exe = make_exe
        self.script_count = 0
        self.valid_exit_codes = valid_exit_codes

    def write_script(self, script):
        script = textwrap.dedent(script)

        path = self.tmpdir.join('%03d.mk' % self.script_count)
        path.write(script)

        self.script_count += 1
        return path, script

    def format_error(self, script, res) -> str:
        template = '''
        {cmd}

        Script:
        {script}

        Output:
        {stderr}
        '''

        def indent(text, prefix='>  '):
            return textwrap.indent(text.strip(), prefix, lambda line: True)

        template = textwrap.dedent(template).rstrip()
        return template.format(
            cmd=indent(' '.join(res.args)),
            script=indent(script),
            stderr=indent(res.stderr.decode('utf8')),
        )

    def run(self, script, target=None) -> subprocess.CompletedProcess:
        path, script = self.write_script(script)
        cmd = [self.make_exe, '-f', str(path)]

        if target:
            cmd.append(target)

        res = subprocess.run(cmd, cwd=str(self.tmpdir), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        exit_nok = res.returncode not in self.valid_exit_codes
        output_nok = b'Syntax error' in res.stderr or b'ERROR' in res.stderr
        if exit_nok or output_nok:
            pytest.fail(self.format_error(script, res))

        return res


class InspectableMakeRunner(MakeRunner):
    '''
    A class that executes bits of make script and also knows all the
    variables that were set during the execution of that script.

    Example usage:
      >>> make = InspectableMakeRunner()
      >>> res = make.run('VAR := 1')
      >>> res['VAR']
      '1'
    '''

    script_prefix = '''
    _VARIABLES_OLD := $(.VARIABLES)
    '''

    script_suffix = '''
    all:
    	$(foreach v, \\
    	  $(filter-out $(_VARIABLES_OLD) _VARIABLES_OLD,$(.VARIABLES)), \\
    	  $(info !VAR $(v) = $($(v))))
    '''

    class CompletedProcessWithVars(subprocess.CompletedProcess, collections.MutableMapping):
        def __getitem__(self, key):
            return self.vars[key]

    def write_script(self, script) -> str:
        script = (self.script_prefix, script, self.script_suffix)
        script = '\n'.join(map(textwrap.dedent, script))
        return super().write_script(script)

    def parse_output(self, output):
        for line in output.decode('utf8').splitlines():
            if not line.startswith('!VAR '):
                continue
            yield self.parse_var_line(line)

    def parse_var_line(self, line):
        return line.replace('!VAR ', '', 1).split(' = ', 1)

    def run(self, script, target='all') -> CompletedProcessWithVars:
        res = super().run(script, target)
        res.vars = {name: value for name, value in self.parse_output(res.stdout)}
        res.__class__ = InspectableMakeRunner.CompletedProcessWithVars
        return res


class ToolkitTestRunner(InspectableMakeRunner):
    '''
    A class that makes it convenient to test the gnu make toolkit.

    Example usage:
      >>> make = ToolkitTestRunner()
      >>> make('$(firstword one two three)')
      one
    '''

    script_prefix = '''
    include {toolkit_path}
    _VARIABLES_OLD := $(.VARIABLES)
    '''

    def __init__(self, *args, toolkit_path, **kwargs):
        super().__init__(*args, **kwargs)
        self.script_prefix = self.script_prefix.format(toolkit_path=toolkit_path)

    def write_script(self, script):
        script = 'OUT := %s' % script
        return super().write_script(script)

    def run(self, *args, **kwargs):
        res = super().run(*args, **kwargs)
        return res['OUT']

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)
