def arithmetic_arranger(problems, show_answers=False):

    #we define the lines as empty lists to fill later
    first_line = []
    second_line = []
    third_line = []
    fourth_line = []

    #the limit of problems is five
    if len(problems)>5:
        return 'Error: Too many problems.'

    for problem in problems:

        #we define operands and operator
        first_term = problem[:problem.index(' ')]
        operator = problem[problem.index(' ')+1]
        second_term = problem[problem.index(' ')+3:]

        #the operator can only be + or -
        if not (operator == '+' or operator == '-'):
            return "Error: Operator must be '+' or '-'."

        #the operands can only be digits
        if not (first_term.isdigit() and second_term.isdigit()):
            return 'Error: Numbers must only contain digits.'
        
        #the operands can't have more than four digits
        if (len(first_term)>4 or len(second_term)>4):
            return 'Error: Numbers cannot be more than four digits.'

        #we define the max length
        max_len = max(len(first_term), len(second_term))+2

        #we calculate the result of the problem
        if operator == '+':
            result = int(first_term)+int(second_term)
        else:
            result = int(first_term)-int(second_term)
        
        #we buid our lines
        first_line.append(' ' * (max_len - len(first_term)) + first_term)
        second_line.append(operator + ' ' * (max_len - len(second_term) - 1) + second_term)
        third_line.append('-' * max_len)
        fourth_line.append(' ' * (max_len - len(str(result))) + str(result))

    #we put the problems together
    final_output = '\n'.join(['    '.join(first_line),'    '.join(second_line),'    '.join(third_line)])

    #we only show the answers if the user wants
    if show_answers:
        final_output += '\n' + '    '.join(fourth_line)

    return final_output


print(f'{arithmetic_arranger(["3 * 855", "3801 - 2", "45 + 43", "123 + 49"])}')
