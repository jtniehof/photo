#!/usr/bin/env python

import numpy

def skip_whitespace(f):
    while True:
        d = f.read(1)
        if d is None:
            raise RuntimeError('end of file')
        if not d in (b' ', b'\n', b'\t'):
            break
    f.seek(-1, 1)

def read_to_whitespace(f):
    data = bytearray(b'')
    while True:
        d = f.read(1)
        if d is None:
            raise RuntimeError('end of file')
        if d in (b' ', b'\n', b'\t'):
            break
        data.append(d)
    f.seek(-1, 1)
    return bytes(data)

def read_pgm(fspec):
    with open(fspec, 'rb') as f:
        magic = f.read(2)
        if magic != b'P5':
            raise RuntimeError('not a pgm file')
        skip_whitespace(f)
        w = read_to_whitespace(f)
        if w == '#':
            skip_whitespace(f)
            w = read_to_whitespace(f)
        width = int(w)
        skip_whitespace(f)
        height = int(read_to_whitespace(f))
        skip_whitespace(f)
        maxval = int(read_to_whitespace(f))
        d = f.read(1)
        if not d in (b' ', b'\n', b'\t'):
            raise RuntimeError('bad pgm format after maxval')
        return numpy.fromfile(f, dtype='>u1' if maxval < 256 else '>u2'
                ).reshape(height, -1)

def ws_delimited(s, start):
    while s[start] in (b' ', b'\n', b'\t'):
        start += 1
    end = start
    while s[end] not in (b' ', b'\n', b'\t'):
        end += 1
    return start, end

def pgm_from_string(s):
    if s[0:2] != b'P5':
        raise RuntimeError('not a pgm file')
    start = 2
    start, end = ws_delimited(s, start)
    if s[start:end] == '#':
        start = end
        start, end = ws_delimited(s, start)
    width = int(s[start:end])
    start = end
    start, end = ws_delimited(s, end)
    height = int(s[start:end])
    start = end
    start, end = ws_delimited(s, end)
    maxval = int(s[start:end])
    if not s[end] in (b' ', b'\n', b'\t'):
        raise RuntimeError('bad pgm format after maxval')
    return numpy.frombuffer(s, offset=end + 1, dtype='>u1'
                            if maxval < 256 else '>u2').reshape(height, -1)
