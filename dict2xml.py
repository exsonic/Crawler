#!/usr/bin/env python
# coding: utf-8
# Original Author: https://github.com/quandyfactory/dict2xml
# Modified by: Bobi Pu
# Feb-14-2013

"""
Converts a native Python dictionary into an XML string. Supports int, float, str, unicode, list, dict and arbitrary nesting.
"""
debug = False

def debug_notify(*args):
    """Prints debug information"""
    if debug == False: 
        return
    for arg in args:
        print '%s; ' % (arg)
    print '\n'

#Those symbols can't show up in xml element's content, otherwise it will disrupt the format of XML file
def xml_escape(s):
    if type(s) == str:
        s = s.replace('"',  ' ')
        s = s.replace('\'', ' ')
        s = s.replace('<',  ' ')
        s = s.replace('>',  ' ')
        s = s.replace('&',  ' ')
    elif type(s) == unicode:
        s = s.replace(u'"',  u' ')
        s = s.replace(u'\'', u' ')
        s = s.replace(u'<',  u' ')
        s = s.replace(u'>',  u' ')
        s = s.replace(u'&',  u' ')
    return s

def convert(obj, elementName = 'item'):
    """Routes the elements of an object to the right function to convert them based on their data type"""
    debug_notify('Inside convert(): obj=%s' % (obj))
    if type(obj) in (int, float, str, unicode):
        return convert_kv('item', obj)
    if hasattr(obj, 'isoformat'):
        return convert_kv('item', obj.isoformat())
    if type(obj) == bool:
        return convert_bool('item', obj)
    if type(obj) == dict:
        return convert_dict(obj)
    if type(obj) == list:
        return convert_list(obj, elementName)
    if type(obj) == set:
        return convert_list([s for s in obj], elementName)
    raise TypeError, 'Unsupported data type: %s (%s)' % (obj, type(obj).__name__)

def convert_dict(obj):
    """Converts a dict into an XML string."""
    debug_notify('Inside convert_dict(): obj=%s' % (obj))
    output = []
    addline = output.append
    for k, v in obj.items():
        debug_notify('Looping inside convert_dict(): k=%s, v=%s, type(v)=%s' % (k, v, type(v)))
        try:
            if k.isdigit():
                k = 'n%s' % (k)

            elementName = k
            #if the key is like 'Experts', 'Posts'. Then element Name is 'Expert' 'Post'
            if elementName[-1] == 's':
                elementName = elementName[:-1]
        except:
            if type(k) in (int, float):
                k = 'n%s' % (k)
        if type(v) in (int, float, str, unicode):
            addline(convert_kv(k, v))
        elif hasattr(v, 'isoformat'): # datetime
            addline(convert_kv(k, v.isoformat()))
        elif type(v) == bool:
            addline(convert_bool(k, v))
        elif type(v) == dict:
            addline('<%s>%s</%s>' % (k, convert_dict(v), k))
        #*****add Post tag name, not Item*******
        elif type(v) == list:  
            addline('<%s>%s</%s>' % (k, convert_list(v, elementName), k))
        elif type(v) == set: # convert a set into a list
            addline('<%s>%s</%s>' % (k, convert_list([s for s in v], elementName), k))
        elif v is None:
            addline('<%s></%s>' % (k, k))
        else:
            raise TypeError, 'Unsupported data type: %s (%s)' % (v, type(v).__name__)
    return ''.join(output)

#Modify: add elementName parameter to repalce 'item'
def convert_list(items, elementName = 'item'):
    """Converts a list into an XML string."""
    debug_notify('Inside convert_list(): %s=%s' % (elementName, items))
    output = []
    addline = output.append
    for item in items:
        debug_notify('Looping inside convert_list(): %s=%s, type(%s)=%s' % (elementName, item, elementName, type(item)))
        #replace 'item' with 'post'
        subelementName = 'Post' if (elementName == 'Thread') else 'item'
        if type(item) in (int, float, str, unicode):
            addline(convert_kv(elementName, item))
        elif type(item) == bool:
            addline(convert_bool(elementName, item))
        elif type(item) == dict:
            addline('<%s>%s</%s>' % (elementName, convert_dict(item), elementName))
        elif type(item) == list:
            addline('<%s>%s</%s>' % (elementName, convert_list(item, subelementName), elementName))
        elif type(item) == set: # convert a set into a list
            addline('<%s>%s</%s>' % (convert_list([s for s in item], elementName)))
        else:
            raise TypeError, 'Unsupported data type: %s (%s)' % (item, type(item).__name__)
    return ''.join(output)

#Modify: remove the type attribue
def convert_kv(k, v):
    """Converts an int, float or string into an XML element"""
    debug_notify('Inside convert_kv(): k=%s, v=%s' % (k, v))
    return '<%s>%s</%s>' % (k, xml_escape(v), k)

#Modify: remove the type attribue
def convert_bool(k, v):
    """Converts a boolean into an XML element"""
    debug_notify('Inside convert_bool(): k=%s, v=%s' % (k, v))
    return '<%s>%s</%s>' % (k, str(v).lower(), k)

def dict2xml(obj, elementName = 'item', root=True):
    """Converts a python object into XML"""
    debug_notify('Inside dict2xml(): obj=%s' % (obj))
    output = []
    addline = output.append
    if root == True:
        addline('<?xml version="1.0" encoding="UTF-8" ?>')
        addline('<root>%s</root>' % (convert(obj, elementName)))
    else:
        addline(convert(obj))
    return ''.join(output)
