# -*- coding: utf-8 -*-
import re
import os
from datetime import datetime
from xml.sax import saxutils

from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import HtmlFormatter


binary = [
    r'\.ico$',
    r'\.png$',
    r'\.gif$',
    r'\.jpg$',
    r'\.jpeg$',
    r'\.tif$',
    r'\.tiff$',
    r'\.xap$',
    r'\.swf$',
    r'\.svg$',
    r'\.report$',
    r'\.py[co]+$',
    r'\.zip$',
    r'\.gz$',
    r'\.bz$',
    r'\.bz2$',
    r'\.jar$',
]


def printsrc(in_folder, out_file, include=None, exclude=None, inc_file=None, exc_file=None,
                    toc=True, uparr=True, style='trac', css=None, title='DevHub PrintSrc', verbose=True, binary_ext=[]):
    """
    Print sources to html file with sintax highlighting

    :in_folder: — folder with sources;
    :out_file: — target filename for print;
    :include: — string with regexes of filenames for inclusion to printing. Separate regex with ``r'\,'``;
    :exclude: — string with regexes of filenames for exclusion from printing. Separate regex with ``r'\,'``;
    :inc_file: — filenfme of file with regexes of filenames for inclusion to printing. Separate by new line;
    :exc_file: — filenfme of file with regexes of filenames for exclusion from printing. Separate by new line;
    :toc: — print or none table of content. If string — it'll be text of toc header;
    :uparr: — print or not after each source file link to begin of document. If string — it'll be text of link;
    :style: — name css style fro highlighting from pygments. Example: http://pygments.org/demo/ ;
    :css: — filensme of css file with custom styles;
    :title: — title prefix of resultet html file;
    :verbose: — print current actions to standart output;
    :binary_ext: — list of binary filenames extensions (always exluded).
    """

    style_list = ''

    if style:
        style_list = HtmlFormatter(style=style).get_style_defs() + '\n'

    if css:
        with open(css, 'r') as css_style:
            style_list += css_style.read() + '\n'

    header = u"""<!DOCTYPE html>
<html>
<head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
    <title>{0}: {1}</title>
    <style type="text/css">
        {2}
        * {{word-break: break-all; word-wrap: break-word;}}
        .highlight{{font-size: 12; line-height: 14px; border: 1px solid #bb8844; border-radius: 4px;padding: 10px;}}
    </style>
</head>
<body>\n<a name="printsrc_begin"></a>\n""".format(title.decode('UTF-8'), datetime.now().isoformat(), style_list)
    footer = u'</body>\n</html>'

    def make_patterns(patterns, mode=re.U):
        return [re.compile(pat, mode) for pat in patterns if pat]

    def make_patterns_from_string(patterns, mode=re.U):
        return make_patterns(patterns.split('\,'), mode)

    def pattern_from_file(src_file, mode=re.U):
        with open(src_file, 'r') as inc_src:
            return make_patterns([pat.rstrip('\n') for pat in inc_src if pat], mode)

    if isinstance(include, basestring):
        include = make_patterns_from_string(include.decode('UTF-8'))

    if isinstance(exclude, basestring):
        exclude = make_patterns_from_string(exclude.decode('UTF-8'))

    if isinstance(inc_file, basestring):
        if include is None:
            include = []

        include += pattern_from_file(inc_file.decode('UTF-8'))

    if exclude is None:
        exclude = []

    if isinstance(exc_file, basestring):

        exclude += pattern_from_file(exc_file.decode('UTF-8'))

    exclude += make_patterns(binary + binary_ext, (re.U | re.I))

    if toc:
        if isinstance(toc, basestring):
            toc = toc.decode('UTF-8')
        else:
            toc = u'Table of content'

    toc_text = toc and u'<h4>{0}</h4>\n<ol id="printsrc_toc" class="printsrc__toc">\n'.format(toc) or ''

    if uparr:
        if isinstance(uparr, basestring):
            uparr = uparr.decode('UTF-8')
        else:
            uparr = u'Up &uarr;'

        uparr = u"""<div class="printsrc__to-begin">
    <a class="printsrc__to-begin-link" href="#printsrc_begin">{0}</a>
</div>\n""".format(uparr)
    else:
        uparr = ''

    counter = 0
    out_file = out_file.decode('UTF-8')
    temp_file = out_file + '.tmp'

    with open(temp_file, 'w') as fd:

        for root, dirs, files in os.walk(in_folder):
            if verbose:
                print 'Dir:', root
                print 'Included dirs:', dirs
                print 'Included files:', files

            for name in files:
                current_file = os.path.join(root, name)

                parse_this = False

                if not include:
                    if verbose:
                        print current_file, 'included'

                    parse_this = True
                else:
                    for pattern in include:
                        if re.search(pattern, current_file):
                            if verbose:
                                print current_file, 'for', pattern.pattern, 'included'

                            parse_this = True
                            break

                if parse_this and exclude:
                    for pattern in exclude:
                        if re.search(pattern, current_file):
                            if verbose:
                                print current_file, 'for', pattern.pattern, 'excluded'

                            parse_this = False
                            break

                if not parse_this:
                    continue

                counter += 1
                toc_file = saxutils.escape(current_file.replace(u'{0}/'.format(in_folder), ''))

                try:
                    lexer = get_lexer_for_filename(name)
                except:
                    lexer = None

                if toc_text:
                    toc_text += '<li class="printsrc__toc-element"><a class="printsrc__toc-link" href="#printsrc_{0}">{1}</a></li>\n'.format(counter, toc_file)

                with open(current_file) as fds:
                    try:
                        src = saxutils.escape(fds.read())

                        if lexer:
                            highlighted = highlight(src, lexer, HtmlFormatter())
                        else:
                            highlighted = u'<div class="highlight"><pre>\n{0}\n</pre></div>'.format(src)

                        fd.write(u'<h4 id="printsrc_{0}">{0}: {1}</h4>\n{2}\n{3}\n'.format(counter, toc_file,
                            highlighted, uparr).encode('UTF-8'))
                    except UnicodeDecodeError:
                        print 'ERROR: can\'t write:', current_file

    if toc_text:
        toc_text += '</ol>\n'

    if not out_file.endswith('.html') and not out_file.endswith('.htm'):
        out_file += '.html'

    with open(out_file, 'w') as fd:
        fd.write(header.encode('UTF-8'))
        fd.write(toc_text.encode('UTF-8'))

        with open(temp_file, 'r') as src:
            fd.write(src.read())

        fd.write(footer.encode('UTF-8'))

    os.unlink(temp_file)
