import Lexer
import Parser


test_programs = [
    """
    {
    dim x integer
    x as 10
    if x LT 20 then
        writeln x
    end
    }
    """,
    """
    {
    dim y real
    y as 3.14
    while (y GT 0) do
        y as y min 1
    end
    }
    """,
    """
    {
     dim x boolean, f, sd, re integer
     a as -10
     b as 20AH
     c as a plus b
     write (c)
     if x then
     [ c as b mult a ]
     } end
    """
]

for i, program in enumerate(test_programs):
    print(f"Тест {i+1}:")
    lexer = Lexer
    tokens = Lexer.search_token(program)
    if tokens:
        parser = Parser(tokens)
        try:
            parser.parse_program()
            print("Программа успешно распознана")
        except SyntaxError as e:
            print(f"Синтаксическая ошибка: {e}")
    print()