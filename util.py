'''
This file contains basic utility function that you can use.
'''

MAX_NUM_CLIENTS = 10


def make_message(msg_type, msg_format, message=None):
    '''
    This function can be used to format your message according
    to any one of the formats described in the documentation.
    msg_type defines type like join, disconnect etc.
    msg_format is either 1,2,3 or 4
    msg is remaining. 
    '''
    if msg_format == 2:
        return "%s" % (msg_type)
    if msg_format in [1, 3, 4]:
        return "%s %s" % (msg_type, message)
    return ""
