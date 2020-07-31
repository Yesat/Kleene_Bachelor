class Calculator:
    def __init__ (self):
        self.stack = []

    def push (self, p):
        if p in ['+', '·']:
            op1 = self.stack.pop ()
            op2 = self.stack.pop ()
            self.stack.append ('(%s %s %s)' % (op1, p, op2) )
        elif p == '!':
            op = self.stack.pop ()
            self.stack.append ('%s!' % (op) )
        elif p in ['*']:
            op = self.stack.pop ()
            self.stack.append ('%s%s' % (op, p) )
        else:
            self.stack.append (p)

    def convert (self, l):
        l.reverse ()
        for e in l:
            self.push (e)
        return self.stack.pop ()


