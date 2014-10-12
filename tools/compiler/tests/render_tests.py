from ast import *
from linearise import Label, Jump, Branch, Instruction
from render import Render
from errors import Errors
import unittest

class RenderTests(unittest.TestCase):

    def assertSuccess(self, input_lines):
        errors = Errors()
        render = Render(input_lines, errors, indent=False)
        self.assertEquals(errors.num_errors, 0)
        self.assertEquals(errors.num_warnings, 0)
        return render
    
    def testEmpty(self):
        lines = []
        render = self.assertSuccess(lines)
        self.assertEquals(render.lines, [])
    
    def testEmptyFunction(self):
        lines = [Label('f', public=True), Label('f$exit', public=True)]
        render = self.assertSuccess(lines)
        self.assertEquals(render.lines, ['f::', 'f$exit::'])
    
    def testJump(self):
        lines = [Label('f', public=True), Jump('f')]
        render = self.assertSuccess(lines)
        self.assertEquals(render.lines, ['f::', 'jmp f'])
    
    def testNumeralAssignment(self):
        n1 = Name('$r1')
        n1.declaration = Register('$r1')
        lines = [Instruction(AssignStatement(n1, Numeral(7)))]
        render = self.assertSuccess(lines)
        self.assertEquals(render.lines, ['mov 7, $r1'])
    
    def testOut(self):
        n1 = Name('$r1')
        n1.declaration = Register('$r1')
        n2 = Name('$r2')
        n2.declaration = Register('$r2')
        fc = FunctionCall(Name('__out__'), [n1, n2])
        fc.name.declaration = out_builtin
        lines = [Instruction(fc)]
        render = self.assertSuccess(lines)
        self.assertEquals(render.lines, ['out $r1, $r2'])


if __name__ == '__main__':
    unittest.main()
