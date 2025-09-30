from itertools import *
from utilities import *


#Credit: ChatGPT for some parts the implementation in this file (for rail fence, caesar box, scytale solvers)

def rail_fence_decrypt(ciphertext, height):
    rail = [['' for _ in range(len(ciphertext))] for _ in range(height)]
    dir_down = None
    row, col = 0, 0

    for char in ciphertext:
        if row == 0:
            dir_down = True
        if row == height - 1:
            dir_down = False
        
        rail[row][col] = '*'
        col += 1
        
        if dir_down:
            row += 1
        else:
            row -= 1

    index = 0
    for r in range(height):
        for c in range(len(ciphertext)):
            if rail[r][c] == '*' and index < len(ciphertext):
                rail[r][c] = ciphertext[index]
                index += 1

    result = []
    row, col = 0, 0
    for _ in range(len(ciphertext)):
        if row == 0:
            dir_down = True
        if row == height - 1:
            dir_down = False
        
        result.append(rail[row][col])
        col += 1
        
        if dir_down:
            row += 1
        else:
            row -= 1

    return ''.join(result)

def caesar_box_decrypt(ciphertext, rows, cols):
    # Corrected implementation
    if len(ciphertext) > rows * cols:
        return None  # Invalid input
        
    matrix = [['' for _ in range(cols)] for _ in range(rows)]
    index = 0
    
    # Fill column by column
    for col in range(cols):
        for row in range(rows):
            if index < len(ciphertext):
                matrix[row][col] = ciphertext[index]
                index += 1
    
    # Read row by row
    plaintext = ''
    for row in range(rows):
        for col in range(cols):
            if matrix[row][col]:  # Only add non-empty cells
                plaintext += matrix[row][col]
    
    return plaintext


def scytale_decrypt(ciphertext, rows, cols):
    # Corrected implementation
    if len(ciphertext) > rows * cols:
        return None  # Invalid input
        
    matrix = [['' for _ in range(cols)] for _ in range(rows)]
    index = 0
    
    # Fill column by column
    for row in range(rows):
        for col in range(cols): 
            if index < len(ciphertext):
                matrix[row][col] = ciphertext[index]
                index += 1
    
    # Read cols
    plaintext = ''
    for col in range(cols):
        for row in range(rows):
            if matrix[row][col]:  # Only add non-empty cells
                plaintext += matrix[row][col]
    
    return plaintext

def RRTS(ciphertext, max_length = 6):
    for length in range(2,max_length+1):
        if len(ciphertext)%length!=0:
            continue
        for p in permutations(list(range(length))):
            fixed_text = []
            for j in range(len(ciphertext)):
                fixed_text.append(ciphertext[j//length*length+p[j%length]])
            answer = ''.join(fixed_text)
            #print(answer)
            if fitness(answer)>FITNESS_CUTOFF:
                return answer
    return None

def solve_transposition(ciphertext, max_size=100):
    fitness_cutoff = FITNESS_CUTOFF
    
    # Rail Fence
    print('Trying rail fence')
    for height in range(2, max_size + 1):
        decrypted = rail_fence_decrypt(ciphertext, height)
        if fitness(decrypted) > fitness_cutoff:
            print(f'Rail Fence (height={height}):')
            return decrypted
    # Scytale - Brute-force both dimensions
    print('Trying Scytale 1')
    for rows in range(2, max_size + 1):
        cols = (len(ciphertext)+rows-1)//rows
        if rows * cols >= len(ciphertext):  # Ensure dimensions fit
            decrypted = scytale_decrypt(ciphertext, rows, cols)
            #print(rows,cols,fitness(decrypted))
            if fitness(decrypted) > fitness_cutoff:
                print(f'Scytale (rows={rows}, cols={cols}):')
                return decrypted
    print('Trying Scytale 2')
    for cols in range(2, max_size + 1):
        rows = (len(ciphertext)+cols-1)//cols
        if rows * cols >= len(ciphertext):  # Ensure dimensions fit
            decrypted = scytale_decrypt(ciphertext, rows, cols)
            #print(rows,cols,fitness(decrypted))
            if fitness(decrypted) > fitness_cutoff:
                print(f'Scytale (rows={rows}, cols={cols}):')
                return decrypted
    # Caesar Box - Brute-force both dimensions
    print('Trying Caesar Box 1')
    for rows in range(2, max_size + 1):
        cols = (len(ciphertext)+rows-1)//rows
        if rows * cols >= len(ciphertext):  # Ensure dimensions fit
            decrypted = caesar_box_decrypt(ciphertext, rows, cols)
            #print(rows,cols,fitness(decrypted))
            if fitness(decrypted) > fitness_cutoff:
                print(f'Caesar Box (rows={rows}, cols={cols}):')
                return decrypted
    print('Trying Caesar Box 2')
    for cols in range(2, max_size + 1):
        rows = (len(ciphertext)+cols-1)//cols
        if rows * cols >= len(ciphertext):  # Ensure dimensions fit
            decrypted = caesar_box_decrypt(ciphertext, rows, cols)
            #print(rows,cols,fitness(decrypted))
            if fitness(decrypted) > fitness_cutoff:
                print(f'Caesar Box (rows={rows}, cols={cols}):')
                return decrypted
    print('Trying standard row-row transposition')
    answer_2 = RRTS(ciphertext)
    if answer_2!=None:
        return answer_2
    return None
