def test_rest(make):
    assert make('$(call rest,1 2 3 4)') == '2 3 4'
    assert make('$(call rest,1)') == ''
    assert make('$(call rest,)') == ''

def test_chop(make):
    assert make('$(call chop,1 2 a)') == '1 2'
    assert make('$(call chop,1 2 a 4)') == '1 2 a'
    assert make('$(call chop,1)') == ''
    assert make('$(call chop,)') == ''

def test_leq(make):
    assert make('$(call leq,1 2 a,1 2 a)') == '#t'
    assert make('$(call leq,1 2 3,1 2 3 4)') == ''
    assert make('$(call leq,1 2 3 4,1 2 3)') == ''
    assert make('$(call leq,a,a)') == '#t'
    assert make('$(call leq,,)') == '#t'

def test_lne(make):
    assert make('$(call lne,1 2 a,1 2 a)') == ''
    assert make('$(call lne,1 2 3,1 2 3 4)') == '#t'
    assert make('$(call lne,1 2 3 4,1 2 3)') == '#t'
    assert make('$(call lne,1,1)') == ''
    assert make('$(call lne,,)') == ''

def test_reverse(make):
    assert make('$(call reverse,)') == ''
    assert make('$(call reverse,1)') == '1'
    assert make('$(call reverse,1 2)') == '2 1'
    assert make('$(call reverse,1 a 3)') == '3 a 1'

def test_uniq(make):
    assert make('$(call uniq,)') == ''
    assert make('$(call uniq,a)') == 'a'
    assert make('$(call uniq,a a)') == 'a'
    assert make('$(call uniq,a aa)') == 'a aa'
    assert make('$(call uniq,a aa a)') == 'a aa'
    assert make('$(call uniq,a b ba ab b a a ba a)') == 'a b ba ab'
