##############################################################
# Tools for simulating the result of a cgi.FieldStorage() 
# call; useful for testing CGI scripts outside the web
##############################################################

import types

class FieldMockup:                                   # mocked-up input object
    def __init__(self, str): 
        self.value = str

def formMockup(**kwargs):                            # pass field=value args
    mockup = {}                                      # multi-choice: [value,...]
    for (key, value) in kwargs.items():
        if type(value) is not types.ListType:        # simple fields have .value
            mockup[key] = FieldMockup(str(value))
        else:                                        # multi-choice have list
            mockup[key] = []                         # to do: file upload fields
            for pick in value:
                mockup[key].append(FieldMockup(pick))
    return mockup

def selftest():
    # use this form if fields can be hard-coded
    form = formMockup(name='Bob', job='hacker', food=['Spam', 'eggs', 'ham'])
    print form['name'].value
    print form['job'].value
    for item in form['food']:
        print item.value,
    # use real dict if keys are in variables or computed
    print
    form = {'name':FieldMockup('Brian'), 'age':FieldMockup(38)}
    for key in form.keys():
        print form[key].value

if __name__ == '__main__': selftest()
