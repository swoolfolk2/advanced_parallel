from threading import Thread
from random import randint

INPUT_PATH = 'inputs/'
DICTIONARY_PATH = 'dictionary.txt'

WASHER_STATE  = 0
MOM_STATE = 0
CHILD_STATE = 0
STOVE_STATE = 0

mom_finishing_cycle = 0
child_finishing_cycle = 0
stove_finishing_cycle = 0

store_time = randint(3, 5)
cooking_time = 0


def wash_clothes(cycle, cycle_count):
    global WASHER_STATE
    
    if(cycle < cycle_count):
        print("Washer: Washing... ")

    else:
        print("Washer: Finished!")
        WASHER_STATE = 1

def mom_activities(cycle):
    global MOM_STATE
    global mom_finishing_cycle
    global stove_finishing_cycle
    if MOM_STATE == 0:
        print("Mom: Waiting on washer...")

    elif MOM_STATE == 1:
        if cycle == mom_finishing_cycle:
            MOM_STATE = 2
            mom_finishing_cycle += + 1
        print("Mom: Telling child to go to store")

    elif MOM_STATE ==2 :
        if cycle == mom_finishing_cycle:
            mom_finishing_cycle += 10 + store_time
            MOM_STATE = 3
        print("Mom: Giving child money")

    elif MOM_STATE == 3:
        if cycle == mom_finishing_cycle:
            mom_finishing_cycle += 1
            MOM_STATE = 4
        print("Mom: Waiting on child...")
    
    elif MOM_STATE == 4:
        if cycle == mom_finishing_cycle:
            mom_finishing_cycle += 1
            MOM_STATE = 5
            stove_finishing_cycle = cycle + 1
        print("Mom: Receiving change from child")

def child_activities(cycle):

    global CHILD_STATE
    global child_finishing_cycle

    if CHILD_STATE == 0:
        if child_finishing_cycle == cycle:
            child_finishing_cycle += 1
            CHILD_STATE = 1
        print("Child: Waiting on mom...")

    elif CHILD_STATE == 1:
        if cycle == child_finishing_cycle:
            CHILD_STATE = 2
            child_finishing_cycle += 5
        print("Child: Receiving money from mom")

    elif CHILD_STATE == 2 :
        if cycle == child_finishing_cycle:
            CHILD_STATE = 3
            child_finishing_cycle += store_time
        print("Child: Going to the store")

    elif CHILD_STATE == 3:
        if cycle == child_finishing_cycle:
            child_finishing_cycle += 5
            CHILD_STATE = 4
        print("Child: in store...")

    elif CHILD_STATE == 4:
        if cycle == child_finishing_cycle:
            child_finishing_cycle += 1
            CHILD_STATE = 5
        print("Child: Returning from store")
    
    elif CHILD_STATE == 5:
        if cycle == child_finishing_cycle:
            child_finishing_cycle += 1
            CHILD_STATE = 6
        print("Child: Giving change to mom")
    
    elif CHILD_STATE == 6:
        if cycle == child_finishing_cycle:
            child_finishing_cycle += 1
            CHILD_STATE = 6
        print("Child: Waiting on food...")

def stove_activities(cycle, ):
    global STOVE_STATE
    global stove_finishing_cycle

    if STOVE_STATE == 0:
        if cycle == stove_finishing_cycle:
            STOVE_STATE = 1
            stove_finishing_cycle += cooking_time
        print("Stove: Waiting to start cooking...")

    elif STOVE_STATE == 1:
        if cycle == stove_finishing_cycle:
            STOVE_STATE = 2
            print("Stove: Finished cooking!")
        else:
            print("Stove: Cooking...")

def main():
    
    caseFile = open(INPUT_PATH+"case1.txt", 'r')
    

    case_lines = caseFile.readlines()
    
    dictionaries = getDictionary()

    title = case_lines[0].strip('\n')
    w_cycle, w_load = case_lines[1].split()
    stove_insensity = case_lines[2][0]

    print(f'Loading: {title}')
    print('Settings:')
    print(f'\tWashing cycle: {dictionaries[0][w_cycle]}')
    print(f'\tWashing load: {dictionaries[1][w_load]}')
    print(f'\tStove Intesity: {dictionaries[5][stove_insensity]}')

    w_load = int(w_load)
    w_cycle = int(w_cycle) 

    cycle_count = 0
    if w_cycle == 0:
        cycle_count += 75
    else :
        cycle_count += 100

    if w_load == 0: 
        cycle_count *= 0.75
    elif w_load == 2:
        cycle_count *= 1.25

    cycle_count = int(cycle_count)

    cycle_to_tell_child = randint(2, 30)

    global mom_finishing_cycle
    mom_finishing_cycle = cycle_count

    global cooking_time
    if stove_insensity == 0:
        cooking_time = 25
    else:
        cooking_time = 10

    print(f'\nRunning for: {cycle_count} cycles')
    for cycle in range(1, cycle_count + 1):
        print(f'\n=== Cycle {cycle} ===')
        washing_thread = Thread(target = wash_clothes, args = (cycle, cycle_count, ))
        washing_thread.start()
        stove_thread = Thread(target = stove_activities, args = (cycle, ))
        stove_thread.start()
        washing_thread.join()
        if WASHER_STATE == 1 or STOVE_STATE == 2:
            break

        else:

            if cycle_to_tell_child == cycle:
                global MOM_STATE
                global child_finishing_cycle
                MOM_STATE = 1
                mom_finishing_cycle = cycle
                child_finishing_cycle = cycle

            child_thread = Thread(target = child_activities, args = (cycle, ))
            child_thread.start()

            mom_thread = Thread(target = mom_activities, args = (cycle, ))
            mom_thread.start()
        
    print(f'\n=== End of {title} ===')
def getDictionary():
    dictionaryFile = open(DICTIONARY_PATH, 'r')
    dict_lines = dictionaryFile.readlines()

    dictionaries = []
    for line in dict_lines:
        if len(line) == 1:
            continue
        if line.count('-') >= 1 :
            dictionaries.append({})
            
            continue
        line = line.replace(' ', '', line.count(' ')).strip('\n')
        line = line.split('=')
        dictionaries[len(dictionaries) - 1][f'{line[1]}'] = line[0]

    return dictionaries
    


if __name__ == '__main__':
    main()