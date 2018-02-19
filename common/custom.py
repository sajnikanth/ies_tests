import config
import sys
import glob
import os
import re
import random
import base64
from random import randint
from PIL import Image
from time import localtime, strftime


def catch_exception(self):  # Refer to http://j.mp/1yBy0Wd
    # get file_name
    try:
        filename = sys.exc_info()[2].tb_frame.f_code.co_filename
    except:  # noqa
        filename = 'unable to get filename'
    if '/tests/' in filename:
        filename = filename.split('/tests/')[1]
    # get linenumber
    try:
        linenumber = sys.exc_info()[2].tb_lineno
    except:  # noqa
        linenumber = 'unable to get line number'
    # append ticket number if any
    try:
        # official regex for JIRA
        ticket = re.search('((([A-Za-z]{1,10})-?)[A-Z]+-\d+)', self.error.message.encode('utf-8').strip()).group(1)
    except:  # noqa
        ticket = '***NO JIRA TICKET***'

    # get error message
    try:
        if len(self.error.message) == 0:
            error = 'no error message'
        else:
            error = self.error.message
    except:  # noqa
        error = str(error)
    # append username
    exception_message = 'Exception in ' + filename +\
        ' at Line ' + str(linenumber) + '; ' +\
        error +\
        ' ' + ticket
    # cleanup
    exception_message.replace('  ', ' ')
    assert 1 == 2, exception_message


def tear_down(self):
    if self.error == '':
        try:
            for file_name in glob.glob('./' + self.timestamp + '*.*'):
                os.remove(file_name)
        except:  # noqa
            pass


def generate_random_operations(self):
    random_operations = dict(
        random.sample(
            config.operations_template.items(),
            random.choice(range(1, len(config.operations_template) + 1))
        )
    )
    # edit_get_by_url_encoded_operation requires operatation to be in json (wtf)
    if 'edit_get' in self._testMethodName and 'encoded_operation' not in self._testMethodName:
        random_operations_encoded = ''
        for key in random_operations.keys():
            if key == 'effects':
                random_operations_encoded =\
                    random_operations_encoded +\
                    key.title() + '=' + str(random_operations[key][0]) + '&'
            else:
                for value_key in random_operations[key].keys():
                    random_operations_encoded =\
                        random_operations_encoded +\
                        key.title() + '.' + value_key.title() + '=' + str(random_operations[key][value_key]) + '&'
        return random_operations_encoded[:-1]  # remove the last &
    else:
        return random_operations


def create_test_image(
        image_name=strftime('%Y%m%d%H%M%S', localtime())+'.jpg', resolution=(800, 600), file_type='JPEG', **options):
    image = Image.new('RGBA', size=resolution, color=(randint(0, 255), randint(0, 255), randint(0, 255)))
    image.save(image_name, file_type)
    if len(options) > 0:
        if options['options'] == 'encode':
            with open(image_name, 'rb') as image_file:
                encoded_string = base64.b64encode(image_file.read())
            return {'name': image_name, 'encoded_string': encoded_string}
    else:
        return {'name': image_name}
