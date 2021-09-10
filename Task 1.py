def is_float(entry:str) -> bool:
    """ Checks if the string can be converted into float """
    
    try:
        float(entry)
        return True
    except:
        return False

def int_or_none(entry:str):
    """Converts string into integer if possible
    Else returnss None"""

    try:
        return int(entry)
    except:
        return None

def main():
    """ Main function of the program """
    
    greeting = """
_______________________________________________________________________
Доброго дня!
Ця програма рахує кількість унікальних значень у вхідній послідовності
Серед n перших значень
Зокрема, для вхідної послідовності [3.14, -4.5, 3.3, 3.3, 3.14, 4, ...]
при n = 5 така кількість дорівнюватиме 3
_______________________________________________________________________
"""

    list_input_instructions = """
Введіть масив дійсних значень через пробіл           
Приклад: 3.14 4 -3.777 4.4 4.4 3.14 -128             
Зауважимо, що числа некоректного формату ігноруються!
______________________________________________________

"""

    n_input_instructions = """
Введіть кількість перших членів послідовності          
Серед яких необхідно знайти кількість унікальних членів
Введіть all (або довільний некоректний формат)
щоб проаналізувати всі числа
________________________________________________________

"""
    
    print(greeting)

    # input values storage (list(str)) and int
    input_flow = input(list_input_instructions).split()
    n = input(n_input_instructions)

    # read n as integer or None
    count = int_or_none(n)

    # filtered list and set of input
    filtered_flow = []
    unique_entries = set()
    
    # checks if at least one entry is incorrect
    warning_triggered = False

    
    # loop filtering float from anything else
    for entry in input_flow:
        if not is_float(entry):
            warning_triggered = True
            continue
        else:
            if count is 0:
                break
            
            num = float(entry)
            filtered_flow.append(num)
            unique_entries.add(num)

            if count:
                count -= 1

    # print warning about incorrect input
    if warning_triggered:
        print("Попередження: у вхідному масиві наявні некоректні значення",
              "Їх автоматично буде видалено")
        
    if count is None:
        print("Кількість унікальних елементів у масиві", len(unique_entries))
    else:
        print("Кількість унікальних елементів у масиві серед перших", int(n) - count, ":", len(unique_entries))
        
if __name__ == "__main__":
    main()
