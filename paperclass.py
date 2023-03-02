
class PaperSize:
    paper = {'a4': (21.0, 29.7),
         'a5': (14.8, 21.0),
         'a6': (10.5, 14.8)}

    def get_size(self, name):
        return self.paper[name]

    def __str__(self):
        s = ''
        d = self.paper
        lst = []
        for k in d:
            v1, v2 = d[k]
            lst.append(f"'{k}':({v1:.1f},{v2:.1f})")
        s += ', '.join(lst)
        return(f'PaperSize({s})')


obj = PaperSize()
print(obj.get_size('a4'))
print(obj)
