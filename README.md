# DevHub PrintSrc v0.0.5

Library for generation printable `.html` file from selected source files in directory.

Meanwhile in Russia printed documents are legally valid only.
Print sources from GitHub, stitch them and sign them if you need to delivery results to your customer or register
your rights for code.

## Using

Just import `printsrc` from `dvhb_printsrc`. Can use as is in `fabfile.py`:

Example **`fabfile.py`**:

    from dvhb_printsrc import printsrc

Then you can run:

    $ fabfile printsrc:'path/to/src',outFile.html,,'.py[oc]+$\\,static'

**Note:** double backslash on regex separation, because of it's not raw string! Of course you also can use regex
`'or'` — `'|'` but then regex hasn't be splited to separate expressions (see function parameters description).

For automatic install add string to your **`pipreq`** file:

    git+https://github.com/dvhb/dvhb_printsrc.git@0.0.5#egg=dvhb_printsrc==0.0.5

## API

Function parameters:

* `in_folder` — folder with sources;
* `out_file` — target filename for print;
* `include` — string with regexes of file paths for inclusion to printing. Separate regex with `r'\,'`;
* `exclude` — string with regexes of file paths for exclusion from printing. Separate regex with `r'\,'`;
* `inc_file` — filenfme of file with regexes of file paths for inclusion to printing. Separate by new line;
* `exc_file` — filenfme of file with regexes of file paths for exclusion from printing. Separate by new line;
* `toc` — print or none table of content. If string — it'll be text of toc header;
* `uparr` — print or not after each source file link to begin of document. If string — it'll be text of link;
* `style` — name css style for highlighting from `pygments`. Example: http://pygments.org/demo/ ;
* `css` — filensme of css file with custom styles;
* `title` — <title> prefix of resulted html file;
* `verbose` — print current actions to standart output;
* `binary_ext` — list of binary filenames extensions (always exluded).

## Algoritm

`.html` extension automatically added to out file.

Regexps of inclusion and exclusion from string and from files concatenated.

Binary extesions exlusion list always added list of binary files extensions.

Custom styles from file added after styles from pygments. To omit pygments styles set `styles` to logical `False`.

In begin all files excluded.

First file check for inclusion. If inclusion regex list empty — all files included. First match make file included.

Then included file check for exclusion. If exclusion regex list empty — already included file stay included.
First match make file excluded and function check next file.

If file included function try search pygments lexer for filename. If lexer found — file content processed with him and append to output .html file. If lexer not found — function try to encode file content to `UTF-8`. If success —
it included as is inside `<div class="highlight"><pre>\n{0}\n</pre></div>` blocks and append to output .html file.
