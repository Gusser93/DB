class R:
    def __init__(self, fds, attrs):
        self.fds = fds
        self.attrs = attrs

    def canonical_cover(self):
        for fd in self.fds:
            red_left(self, fd)
        for fd in self.fds:
            red_right(self, fd)

        self.remove_empty_fd()
        self.union_dfs()
        print_fds(self.fds)

    def remove_empty_fd(self):
        for fd in self.fds:
            if len(fd.beta) is 0:
                self.fds.remove(fd)

    def union_dfs(self):
        temp = dict()
        for fd in self.fds:
            temp[frozenset().union(fd.alpha)] = temp.setdefault(frozenset().union(fd.alpha), set()) | fd.beta
        new_fds = []
        for alpha, beta in temp.items():
            new_fds += [FD(alpha, beta)]
        self.fds = new_fds


class FD:
    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta


def print_fds(fds):
    for fd in fds:
        print "".join(fd.alpha) + " -> " + "".join(fd.beta)


def red_left(r, fd):
    for a in fd.alpha:
        temp = fd.alpha.copy()
        temp.remove(a)
        closure = attr_closure(r.fds, temp)
        if fd.beta <= closure:
            fd.alpha = temp


def red_right(r, fd):
    for b in fd.beta:
        temp = r.fds.copy()
        temp_beta = fd.beta.copy()
        temp_beta.remove(b)
        temp_fd = FD(fd.alpha, temp_beta)
        if fd not in temp:
            continue
        temp.remove(fd)
        temp.add(temp_fd)
        closure = attr_closure(temp, fd.alpha)
        if b in closure:
            r.fds = temp


def attr_closure(fds, attrs):
    change = True
    erg = attrs
    while change:
        change = False
        for fd in fds:
            if fd.alpha <= erg:
                temp = erg | fd.beta
                if len(erg ^ temp) != 0:
                    erg = temp
                    change = True

    return erg

if __name__ == "__main__":
    test = R(set(), {"A", "B", "C", "D", "E", "F"})
    test.fds.add(FD({"F"}, {"C", "D"}))
    test.fds.add(FD({"A"}, {"E", "B", "D"}))
    test.fds.add(FD({"D", "C"}, {"B", "A", "F"}))
    test.fds.add(FD({"E"}, {"B", "D"}))
    test.fds.add(FD({"D"}, {"C", "E"}))

    test.canonical_cover()
