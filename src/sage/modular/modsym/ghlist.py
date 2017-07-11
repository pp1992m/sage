r"""
List of coset representatives for `\Gamma_H(N)` in `{\rm SL}_2(\ZZ)`
"""
###########################################################################
#       Sage: System for Algebra and Geometry Experimentation
#
#       Copyright (C) 2005 William Stein <wstein@gmail.com>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#    This code is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    General Public License for more details.
#
#  The full text of the GPL is available at:
#
#                  http://www.gnu.org/licenses/
###########################################################################
from __future__ import absolute_import
from sage.structure.richcmp import richcmp_method, richcmp
from sage.structure.sage_object import SageObject
from sage.structure.sage_object import register_unpickle_override

from . import p1list


@richcmp_method
class GHlist(SageObject):
    r"""
    A class representing a list of coset representatives for `\Gamma_H(N)` in
    `{\rm SL}_2(\ZZ)`.

    TESTS::

        sage: L = sage.modular.modsym.ghlist.GHlist(GammaH(18,[13]))
        sage: loads(dumps(L)) == L
        True
    """
    def __init__(self, group):
        """
        EXAMPLES::

            sage: L = sage.modular.modsym.ghlist.GHlist(GammaH(8,[7])); L # indirect doctest
            List of coset representatives for Congruence Subgroup Gamma_H(8) with H generated by [7]
        """
        self.__group = group
        N = group.level()
        v = group._coset_reduction_data()[0]
        N = group.level()
        coset_reps = set([a for a, b, _ in v if b == 1])
        w = [group._reduce_coset(x*u, x*v) for x in coset_reps for u,v in p1list.P1List(N).list()]
        w = sorted(set(w))
        self.__list = w

    def __getitem__(self, i):
        """
        EXAMPLES::

            sage: L = sage.modular.modsym.ghlist.GHlist(GammaH(8, [5])); L[5] # indirect doctest
            (1, 3)
        """
        return self.__list[i]

    def __richcmp__(self, other, op):
        r"""
        Compare ``self`` to ``other``.

        EXAMPLES::

            sage: L1 = sage.modular.modsym.ghlist.GHlist(GammaH(18, [11]))
            sage: L2 = sage.modular.modsym.ghlist.GHlist(GammaH(18, [13]))
            sage: L1 > L2
            True
            sage: L1 == QQ
            False
        """
        if not isinstance(other, GHlist):
            return NotImplemented
        else:
            return richcmp(self.__group, other.__group, op)

    def __len__(self):
        """
        Return the length of the underlying list (the index of the group).

        EXAMPLES::

            sage: L = sage.modular.modsym.ghlist.GHlist(GammaH(24, [5])); len(L) # indirect doctest
            192
        """
        return len(self.__list)

    def __repr__(self):
        """
        String representation of self.

        EXAMPLES::

            sage: L = sage.modular.modsym.ghlist.GHlist(GammaH(11,[4])); L.__repr__()
            'List of coset representatives for Congruence Subgroup Gamma_H(11) with H generated by [4]'
        """
        return "List of coset representatives for %s"%self.__group

    def list(self):
        r"""
        Return a list of vectors representing the cosets. Do not change the
        returned list!

        EXAMPLES::

            sage: L = sage.modular.modsym.ghlist.GHlist(GammaH(4,[])); L.list()
            [(0, 1), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (3, 0), (3, 1), (3, 2), (3, 3)]
        """
        return self.__list

    def normalize(self, u, v):
        r"""
        Given a pair `(u,v)` of integers, return the unique pair `(u', v')`
        such that the pair `(u', v')` appears in ``self.list()`` and `(u, v)`
        is equivalent to `(u', v')`.

        This will only make sense if `{\rm gcd}(u, v, N) = 1`; otherwise the
        output will not be an element of self.

        EXAMPLES::

            sage: sage.modular.modsym.ghlist.GHlist(GammaH(24, [17, 19])).normalize(17, 6)
            (1, 6)
            sage: sage.modular.modsym.ghlist.GHlist(GammaH(24, [7, 13])).normalize(17, 6)
            (5, 6)
            sage: sage.modular.modsym.ghlist.GHlist(GammaH(24, [5, 23])).normalize(17, 6)
            (7, 18)
        """
        return self.__group._reduce_coset(u,v)


class _GHlist_old_pickle(GHlist):
    """
    This class exists only for dealing with old pickles.

    This needs to handle both old-style class pickles, where there is
    no input to the class on the initial ``__init__`` call, and the
    new class pickles, we need to have ``__setstate__`` handle it.
    """
    def __init__(self):
        """
        For unpickling old pickles.

        TESTS::

            sage: from sage.modular.modsym.ghlist import _GHlist_old_pickle
            sage: L = _GHlist_old_pickle()
            sage: type(L) == GHlist
            True
        """
        self.__class__ = GHlist

    def __setstate__(self, state):
        """
        For unpickling new pickles.

        TESTS::

            sage: from sage.modular.modsym.ghlist import GHlist
            sage: L = GHlist(GammaH(4,[]))
            sage: Lp = loads(dumps(L))
            sage: L == Lp
            True
            sage: type(Lp) == GHlist
            True
        """
        # We don't really want this class, but we want to handle new
        #   pickles without creating a new class
        self.__class__ = GHlist
        self.__dict__ = state # Default pickling is ``state = self.__dict__``

register_unpickle_override('sage.modular.modsym.ghlist', 'GHlist',
                           _GHlist_old_pickle)

