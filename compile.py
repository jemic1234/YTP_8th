import os
import core.lib

f = [i for i in os.listdir('modules/') if i.endswith('.py')]

pre = ''

for i in f:
    pre = pre + '# ' + i + '\n\n' + '\n'.join(core.lib.read_from_file(f'modules/{i}').split('\n')[7:]) + '\n\n'

template = core.lib.read_from_file('template.py').replace('<code>',pre)
core.lib.write_to_file(template,'app.py')
