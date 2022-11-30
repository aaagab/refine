# REFINE

## Table of Contents
1. [About](#about)
1. [Software Function and Exceptions](#software-function-and-exceptions)
    1. [refine function](#refine-function)
    1. [RefineError Exception](#refineerror-exception)
    1. [RefinePatternError Exception](#refinepatternerror-exception)
1. [GITIGNORE Patterns Specifications](#gitignore-patterns-specifications)
1. [GITIGNORE Patterns added info](#gitignore-patterns-added-info)
1. [Tests](#tests)

## About
Refine software allows to select files in a source directory according to patterns. Patterns can't be put in a text file or provided as a list of strings. Patterns specifications follow `.gitignore` specifications from git software. Refine returns a list of filtered paths that have not been excluded by patterns. Returned paths can be absolute or relative to the provided source directory. Empty directories can be ignored too. Finally a destination directory can be provided in order to copy filtered paths on the fly from source directory to destination directory. This software has been implemented from scratch by Gabriel Auger and it has MIT license.

## Software Function and Exceptions
Module function and exceptions are available through the `__init__.py` file. All classes and functions that start with an underscore are for internal testing purposes only. Internal functions and classes are not documented. Tests directory is available with the refine software sources.

### refine function

```python
def refine(
	direpa_src, 
	patterns=None, 
	get_abs_paths=True,
	filenpa_patterns=None,
	direpa_dst=None,
	keep_empty_dir=True,
):
```
- **direpa_src**: Mandatory string. Accept a directory path. This is the source directory.
- **patterns**: Optional strings list. Accept a patterns list. Patterns must follow gitignore patterns specifications.
- **get_abs_paths**: Optional boolean. refine always returns source directory filtered paths. If get_abs_paths is set to True then returned paths are absolutes. If get_abs_paths is set to False then returned paths are relatives.
- **filenpa_patterns**: Optional strings list. Accept a list of file paths. Each file may contain patterns list to filter source directory. filenpa_patterns option patterns have precedence over patterns option patterns.
- **direpa_dst**: Optional string. Accept a directory path, and create it if unknown. If that path is provided then filtered paths are copied from source directory to destination directory.
- **keep_empty_dir**: Optional boolean. If keep_empty_dir is set to True, returned empty directory paths are included. Included directories are copied to destination when direpa_dst has been provided. If keep_empty_dir is set to False, returned empty directory paths are omitted. Omitted directories are not copied to destination when direpa_dst has been provided.

### RefineError Exception
RefineError exceptions are triggered when refine function options are invalid.

### RefinePatternError Exception
RefinePatternError exceptions are triggered when provided patterns from filenpa_patterns and patterns have invalid syntax.

## GITIGNORE Patterns Specifications 
(copied from https://git-scm.com/docs/gitignore on November 2022)  
- A blank line matches no files, so it can serve as a separator for readability.
- A line starting with `#` serves as a comment. Put a backslash `("\")` in front of the first hash for patterns that begin with a hash.
- Trailing spaces are ignored unless they are quoted with backslash `("\")`.
- An optional prefix `"!"` which negates the pattern; any matching file excluded by a previous pattern will become included again. 
    - It is not possible to re-include a file if a parent directory of that file is excluded. 
    - Git doesn’t list excluded directories for performance reasons, so any patterns on contained files have no effect, no matter where they are defined. Put a backslash `("\")` in front of the first `"!"` for patterns that begin with a literal `"!"`, for example, `"\!important!.txt"`.
- The slash `/` is used as the directory separator. Separators may occur at the beginning, middle or end of the `.gitignore` search pattern.
- If there is a separator at the beginning or middle (or both) of the pattern, then the pattern is relative to the directory level of the particular `.gitignore` file itself. Otherwise the pattern may also match at any level below the `.gitignore` level.
- If there is a separator at the end of the pattern then the pattern will only match directories, otherwise the pattern can match both files and directories.
- For example, a pattern `doc/frotz/` matches `doc/frotz` directory, but not `a/doc/frotz` directory; however `frotz/` matches `frotz` and `a/frotz` that is a directory (all paths are relative from the `.gitignore` file).
- An asterisk `"*"` matches anything except a slash. The character `"?"` matches any one character except `"/"`. The range notation, e.g. `[a-zA-Z]`, can be used to match one of the characters in a range. See fnmatch(3) and the FNM_PATHNAME flag for a more detailed description.
    - FNM_PATHNAME: If this flag is set, match a slash in string only with a slash in pattern and not by an asterisk `(*)` or a question mark `(?)` metacharacter, nor by a bracket expression `([])` containing a slash.

Two consecutive asterisks (`"**"`) in patterns matched against full pathname may have special meaning:  
- A leading `"**"` followed by a slash means match in all directories. For example, `"**/foo"` matches file or directory `"foo"` anywhere, the same as pattern `"foo"`. `"**/foo/bar"` matches file or directory `"bar"` anywhere that is directly under directory `"foo"`.
- A trailing `"/**"` matches everything inside. For example, `"abc/**"` matches all files inside directory `"abc"`, relative to the location of the `.gitignore` file, with infinite depth.
- A slash followed by two consecutive asterisks then a slash matches zero or more directories. For example, `"a/**/b"` matches `"a/b"`, `"a/x/b"`, `"a/x/y/b"` and so on.
- Other consecutive asterisks are considered regular asterisks and will match according to the previous rules.

## GITIGNORE Patterns added info
- Difference between patterns `/*`, `/`, `*`, `/**`, `**/`, and `**`. These patterns apply the same regex on the root directory. The difference is that patterns with double stars continue processing recursively the source directory. It allows applying negated patterns on nested paths.
- Each time a `**` pattern is provided then any matching directory is going to be discarded but still path is going to be processed recursively and only negated patterns starting with `!` are going to be matched against the discarded path. In order to recover the content of a discarded directory, the directory must be restored with a negated pattern i.e. `!logs/`. When a directory is recovered with a negated pattern all nested files and directories are recovered too.
- Difference between `/` and `/logs/`. For the former pattern and because it is the root directory then any files or directory can still be recovered with a negated pattern. However for the latter pattern it is not possible to recover nested files or directories because the discarded directory is not processed recursively. In order to recover nested files and directories from logs directory then any of the following patterns may be used `/logs/*` and `/logs/**` before a negate pattern.
- A pitfall from the negate patterns behavior can be illustrated with the following patterns to recover the `foo` directory.  
```shell
# behavior tested on git 2.20.1 and refine software
# that works
/*
!/foo

# that doesn't work
/*
!/foo/*
```
- For range pattern all characters from `a-zA-Z0-9-` are authorized. A first char `!` is allowed and it negates any of the characters range i.e. `[!a-z]`.

## Tests
- All parts of the refine software have been tested using automated tests that are available in the sources format of the software. All tests from the following url pass successfully https://gist.github.com/jstnlvns/ebaa046fae16543cc9efc7f24bcd0e31.
