#!/usr/bin/env python

#####################################################################################
#
# Copyright (c) 2012-2013, Alexander Todorov <atodorov@nospam.dif.io>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#####################################################################################

import sys
import json
import urllib
import httplib
from exceptions import BaseException
from pip.util import get_installed_distributions


def difio_register(data, useragent, excluded_names = []):
    """
        Register to Difio

        @data = {
            'user_id'    : int,
            'app_name'   : '',
            'app_uuid'   : '',
            'app_type'   : '',
            'app_url'    : '',
            'app_vendor' : int,
            'pkg_type'   : int,
            'installed'  : [{'n: 'name', 'v' : 'version' : 't' : int (optional)}],
        }

    """

    if not data.has_key('pkg_type'):
        data['pkg_type'] = 0 # Python

    if not data.has_key('app_type'):
        data['app_type'] = 'python-%d.%d.%d' % (sys.version_info[0], sys.version_info[1], sys.version_info[2])

    # make a list of package names
    for dist in get_installed_distributions(local_only=True):
        # skip some packages if told to
        if dist.project_name.lower() not in excluded_names:
            data['installed'].append({'n' : dist.project_name, 'v' : dist.version})


    json_data = json.dumps(data)
    params = urllib.urlencode({'json_data' : json_data})
    headers = {"User-agent": "%s" % useragent}

    conn = httplib.HTTPSConnection('difio-otb.rhcloud.com')
    conn.request('POST', '/application/register/', params, headers)
    response = conn.getresponse()

    if (response.status != 200) or (not response.getheader('Content-type').startswith('application/json')):
        raise BaseException('Communication failed - %s' % response.read())

    result = json.loads(response.read())
    print result['message']
    sys.exit(result['exit_code'])
