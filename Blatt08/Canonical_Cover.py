# -*- coding: utf-8 -*-


class R:
    def __init__(self, fds, attrs):
        self.fds = fds
        self.attrs = attrs

    def canonical_cover(self):
        # Führe für jede FD α → β ∈ F die Linksreduktion durch
        for fd in self.fds:
            red_left(self, fd)

        # Führe für jede (verbliebene) FD die Rechtsreduktion durch, also:
        for fd in self.fds:
            red_right(self, fd)

        # Entferne die FDs der Form α → ∅, die im 2. Schritt möglicherweise entstanden sind.
        self.remove_empty_fd()
        # Fasse mittels der Vereinigungsregel FDs der Form α → β1, ...,α → βn zusammen, so dass α → (β1 ∪ ... ∪ βn)
        # verbleibt.
        self.union_dfs()

    def remove_empty_fd(self):
        temp = self.fds.copy()
        for fd in temp:
            if len(fd.beta) is 0:
                self.fds.remove(fd)

    def union_dfs(self):
        temp = dict()
        for fd in self.fds:
            temp[frozenset().union(fd.alpha)] = temp.setdefault(frozenset().union(fd.alpha), set()) | fd.beta
        new_fds = []
        for alpha, beta in temp.items():
            new_fds += [FD(set(alpha), set(beta))]
        self.fds = new_fds

    def minimal_candidate_keys(self):
        k = [self.minimize(self.attrs)]
        n = 1
        i = 0

        while i < n:
            for fd in self.fds:
                s = fd.alpha | (k[i] - fd.beta)
                found = False
                for j in range(n):
                    if k[j] <= s:
                        found = True
                if not found:
                    k.append(self.minimize(s))
                    n += 1
            i += 1
        return k

    def minimize(self, a):
        copy = a.copy()
        for e in a:
            temp = copy - {e}
            c = attr_closure(self.fds, temp)
            if len(self.attrs ^ c) == 0:
                copy = temp
        return copy


class FD:
    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta


def print_fds(fds):
    for fd in fds:
        print ",".join(fd.alpha) + " → " + ",".join(fd.beta)


def red_left(r, fd):
    # Überprüfe für alle A ∈ α, ob A überflüssig ist, d.h., ob
    for a in fd.alpha:
        temp = fd.alpha.copy()
        temp.remove(a)
        closure = attr_closure(r.fds, temp)
        # β ⊆ AttrHülle(F, α - A) gilt.
        if fd.beta <= closure:
            # Falls dies der Fall ist, ersetze α → β durch (α - A) → β.
            fd.alpha = temp


def red_right(r, fd):
    # Überprüfe für alle B ∈ β, ob
    for b in fd.beta:
        temp = r.fds.copy()
        temp_beta = fd.beta.copy()
        temp_beta.remove(b)
        temp_fd = FD(fd.alpha, temp_beta)
        temp.remove(fd)
        temp.add(temp_fd)
        closure = attr_closure(temp, fd.alpha)
        # B ∈ AttrHülle(F – (α → β) ∪ (α → (β − Β)), α ) gilt.
        if b in closure:
            # Falls dies der Fall ist, ist B auf der rechten Seite überflüssig und kann eliminiert werden,
            # d.h. ersetze α → β durch α → (β–B).
            r.fds = temp
            fd = temp_fd


# AttrHülle(F,α)
def attr_closure(fds, attrs):
    change = True
    # Erg := α
    erg = attrs
    # While (Änderungen an Erg) do
    while change:
        change = False
        # Foreach FD β → γ in F do
        for fd in fds:
            # If β ⊆ Erg then Erg := Erg ∪ γ
            if fd.alpha <= erg:
                temp = erg | fd.beta
                # Test change
                if len(erg ^ temp) != 0:
                    erg = temp
                    change = True
    # Ausgabe α+ = Erg
    return erg

if __name__ == "__main__":
    test = R(set(), {"TN", "N", "A", "DTN", "DN", "MID", "MN", "Y", "L"})
    test.fds.add(FD({"TN", "N", "A", "DTN", "DN"}, {"MID", "MN", "Y", "L"}))
    test.fds.add(FD({"TN"}, {"N", "A"}))
    test.fds.add(FD({"MID"}, {"MN", "Y", "L"}))
    test.fds.add(FD({"DTN"}, {"DN"}))

    test2 = R(set(), {"MID", "MN", "Y", "L"})
    test2.fds.add(FD({"MID"}, {"MN", "Y", "L"}))

    test3 = R(set(), {"DTN", "DN"})
    test3.fds.add(FD({"DTN"}, {"DN"}))

    test.canonical_cover()
    test2.canonical_cover()
    test3.canonical_cover()

    print "\nCanonical Cover:"
    print_fds(test.fds)
    print("\nCandidate Keys")
    for e in test.minimal_candidate_keys():
		print(",".join(e))

