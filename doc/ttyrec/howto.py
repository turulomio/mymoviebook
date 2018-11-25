#!/usr/bin/python3
import argparse
import time
import colorama
import os
import subprocess
import gettext
from ttyrecgenerator import RecSession

import pkg_resources
gettext.install('mymoviebook', pkg_resources.resource_filename('mymoviebook', 'locale'))

r=RecSession()
r.comment("# " + _("This is a video to show how to use 'mymoviebook' command"))
r.comment("# ")