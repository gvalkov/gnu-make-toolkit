# Function reference

## List manipulation


### `rest(list)`

**Returns:** List with the first element removed.

```makefile
$(call rest,1 2 3 4)
=> 2 3 4
```

### `chop(list)`

**Returns:** List with the last element removed.

```makefile
$(call chop,1 2 3 4)
=> 1 2 3
```

### `leq(list1,list2)`

**Returns:** `#t` if the two lists are identical, empty string otherwise

```makefile
$(call leq,1 2 a,1 2 a)
=> #t
```

### `lne(list1,list2)`

**Returns:** empty string if the two lists are identical, `#t` if they differ

```makefile
$(call lne,1 2 a,1 2 b)
=> #t
```

### `reverse(list)`

**Returns:** reverse the order of elements in list

```makefile
$(call reverse,1 2 a)
=> a 2 1
```

### `uniq(list)`

**Returns:** list with all duplicate elements removed

```makefile
$(call uniq,1 1 1 2 3 2 a)
=> 1 2 3 a
```

### `seq(string1,string2)`

**Returns:** `#t` if the two strings are identical

```makefile
$(call seq,123,123)
=> #t
```

### `sne(string1,string2)`

**Returns:** `#t` if the two strings are not identical

```makefile
$(call sne,123,456)
=> #t
```

## String manipulation


### `strlen(string)`

**Returns:** the length of the supplied string

```makefile
$(call strlen,aaabbb)
=> 6
```

### `substr(string)`

**Returns:** a substring

```makefile
$(call strlen,aaabbb)
=> 6
```

### `string-join(string,list)`

**Returns:** A string which is the concatenation of the elements in the list. The
separator between elements is configurable.

```makefile
$(call string-join,!,a b c)
=> a!b!c
$(call string-join,$$,a b c)
=> $a$b$c
```

### `string-upcase(string)`

**Returns:** Returns the text in upper case

```makefile
$(call string-upcase,the1 quick2 brown3 fox4)
=> THE1 QUICK2 BROWN3 FOX4
```

### `string-downcase(string)`

**Returns:** Returns the text in lower case

```makefile
$(call string-upcase,THE1 QUICK2 BROWN3 FOX4)
=> the1 quick2 brown3 fox4
```


[gmake]: https://www.gnu.org/software/make/
[gmsl]:  http://gmsl.sourceforge.net/
[guile]: https://www.gnu.org/software/make/manual/html_node/Guile-Integration.html
[toolkit.mk]:  https://raw.githubusercontent.com/gvalkov/gnu-make-toolkit/master/toolkit.mk
