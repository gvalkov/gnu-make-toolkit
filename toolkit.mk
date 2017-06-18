# ----------------------------------------------------------------------------
# Refuse to run with versions of GNU Make older than 4.0 or those that
# haven't been compiled with guile support.
# ----------------------------------------------------------------------------

__MIN_MAKE_VERSION := 4.0
__MIN_MAKE_ERROR := gnu-make-toolkit requires gmake $(__MIN_MAKE_VERSION) or greater

ifeq "$(MAKE_VERSION)" ""
    $(error unable to determine gmake version: $(__MIN_MAKE_ERROR))
endif

ifneq "$(__MIN_MAKE_VERSION)" "$(firstword $(sort $(__MIN_MAKE_VERSION) $(MAKE_VERSION)))"
    $(error $(__MIN_MAKE_ERROR))
endif

ifneq "$(filter guile,$(.FEATURES))" "guile"
    $(error gnu-make-toolkit requires a gmake with guile support)
endif

# ----------------------------------------------------------------------------
# Useful variables
# ----------------------------------------------------------------------------

__space :=
__space +=

__tab :=	#


# ----------------------------------------------------------------------------
# Guile setup
# ----------------------------------------------------------------------------

define __gmt_guile_setup
(use-modules (srfi srfi-1))

(define (rest arg)
  (if (pair? arg) (cdr arg)))

(define (chop arg)
  (if (pair? arg)
	(reverse
      (cdr (reverse arg)))))
endef

$(guile $(__gmt_guile_setup))


# ----------------------------------------------------------------------------
# List manipulation
# ----------------------------------------------------------------------------

# --------------------------------------------------------------------------->
# Function: rest(list)
# Returns:  List with the first element removed.
# Example:
#   $(call rest,1 2 3 4)
#   => 2 3 4
# ---------------------------------------------------------------------------<
rest = $(guile (rest (quote ($1))))


# --------------------------------------------------------------------------->
# Function: chop(list)
# Returns:  List with the last element removed.
# Example:
#   $(call chop,1 2 3 4)
#   => 1 2 3
# ---------------------------------------------------------------------------<
chop = $(guile (chop (quote ($1))))


# --------------------------------------------------------------------------->
# Function: leq(list1, list2)
# Returns:  #t if the two lists are identical, empty string otherwise
# Example:
#   $(call leq,1 2 a,1 2 a)
#   => #t
# ---------------------------------------------------------------------------<
leq = $(guile (equal? (quote ($1)) (quote ($2))))


# --------------------------------------------------------------------------->
# Function: lne(list1, list2)
# Returns:  empty string if the two lists are identical, #t if they differ
# Example:
#   $(call lne,1 2 a,1 2 b)
#   => #t
# ---------------------------------------------------------------------------<
lne = $(guile (not (equal? (quote ($1)) (quote ($2)))))


# --------------------------------------------------------------------------->
# Function: reverse(list)
# Returns:  reverse the order of elements in list
# Example:
#   $(call reverse,1 2 a)
#   => a 2 1
# ---------------------------------------------------------------------------<
reverse = $(guile (reverse (quote ($1))))

# --------------------------------------------------------------------------->
# Function: uniq(list)
# Returns:  list with all duplicate elements removed
# Example:
#   $(call uniq,1 1 1 2 3 2 a)
#   => 1 2 3 a
# ---------------------------------------------------------------------------<
uniq = $(guile (delete-duplicates (quote ($1))))


# ----------------------------------------------------------------------------
# String manipulation
# ----------------------------------------------------------------------------


# --------------------------------------------------------------------------->
# Function: seq(string1,string2)
# Returns:  #t if the two strings are identical
# Example:
#   $(call seq,123,123)
#   => #t
# ---------------------------------------------------------------------------<
seq = $(guile (string=? "$1" "$2"))


# --------------------------------------------------------------------------->
# Function: sne(string1,string2)
# Returns:  #t if the two strings are not identical
# Example:
#   $(call sne,123,456)
#   => #t
# ---------------------------------------------------------------------------<
sne = $(guile (not (string=? "$1" "$2")))


# --------------------------------------------------------------------------->
# Function: strlen(string)
# Returns:  the length of the supplied string
# Example:
#   $(call strlen,aaabbb)
#   => 6
# ---------------------------------------------------------------------------<
strlen = $(guile (string-length "$1"))


# --------------------------------------------------------------------------->
# Function: substr(string)
# Returns:  a substring
# Example:
#   $(call strlen,aaabbb)
#   => 6
# ---------------------------------------------------------------------------<
substr = $(guile (substring "$1" $2 $3))


# >-------------------------------------------------------------------------->
# Function:
#   string-join
# Arguments:
#   1: Character to put between fields.
#   2: List to merge into a string.
# Returns:
#   A string which is the concatenation of the elements in the list. The
#   separator between elements is configurable.
# Example:
#   (call string-join,!,a b c)
#   => a!b!c
#   (call string-join,$$,a b c)
#   => $a$b$c
# <--------------------------------------------------------------------------<
string-join = $(guile (string-join (map object->string (quote ($2))) "$1"))


# >-------------------------------------------------------------------------->
# Function:
#   string-upcase uc
# Arguments:
#   1: String to upcase.
# Returns:
#   Returns the text in upper case
# Example:
#   $(call string-upcase,the1 quick2 brown3 fox4)
#   => 'THE1 QUICK2 BROWN3 FOX4'
# <--------------------------------------------------------------------------<
string-upcase = $(guile (string-upcase "$1"))


# >-------------------------------------------------------------------------->
# Function:
#   string-downcase
# Arguments:
#   1: String to downcase.
# Returns:
#   Returns the text in lower case
# Example:
#   $(call string-upcase,the1 quick2 brown3 fox4)
#   => 'THE1 QUICK2 BROWN3 FOX4'
# <--------------------------------------------------------------------------<
string-downcase = $(guile (string-downcase "$1"))


# ----------------------------------------------------------------------------
# Debugging and assertions
# ----------------------------------------------------------------------------

gmt-print-%: ; @echo $* = $($*)


# >-------------------------------------------------------------------------->
# Function:
#   assert-file-exists
# Arguments:
#   1: String to downcase.
# Returns:
#   Returns the text in lower case
# Example:
#   $(call string-upcase,the1 quick2 brown3 fox4)
#   => 'THE1 QUICK2 BROWN3 FOX4'
# <--------------------------------------------------------------------------<
