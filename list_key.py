#!/usr/bin/env /Users/vkamlesh/.virtualenvs/finpy/bin/python
import sys
sys.path.insert(1, '/Users/vkamlesh/src/finpy/mftool/mftool')
from mftool import Mftool
import json

mf = Mftool()
value = mf.get_open_ended_solution_scheme_performance(True)
mf.get_open_ended_hybrid_scheme_performance
value_dict = json.loads(value)
print(value_dict.keys())