# Introduction

The GNU Make Toolkit is a library of utility functions for [GNU Make][gmake]
**4.0** or newer. It provides useful functions for:

- String manipulation
- List manipulation

Most functions are implemented using GNU Make's Guile [integration][guile].

The GNU Make Toolkit implements many of the functions found in the excellent
[GNU Make Standard Library][gmsl]. The GMSL is well tested and runs on all
versions of GNU Make since 3.80.

!!! warning
    The GNU Make Toolkit and this documentation are still a work in progress.

# Usage

Download [toolkit.mk] and include it in your makefile:

```makefile
include toolkit.mk

# Example:
$(call string-join,;,a b c)
=> a;b;c
```

See the [Reference](ref.md) page for a list of functions and helper targets.

[gmake]: https://www.gnu.org/software/make/
[gmsl]:  http://gmsl.sourceforge.net/
[guile]: https://www.gnu.org/software/make/manual/html_node/Guile-Integration.html
[toolkit.mk]:  https://raw.githubusercontent.com/gvalkov/gnu-make-toolkit/master/toolkit.mk
