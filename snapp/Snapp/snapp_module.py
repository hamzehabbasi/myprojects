# two function fo list kardan
def list_kardan(sel):
    result=''
    for number, kala in enumerate(sel):
        for key ,value in kala.items():
            result += f'{number +1}:{key}:{value} \n'
    return result

def make_list(sel):
    result=''
    for num , kar in enumerate(sel):
        result +=f'{num + 1}:{kar} \n'
    return result

def list_making(sel):
    result=''
    for key ,value in sel.items():
            result += f'{key}:{value} \n'
    return result

# UPDATE
def update_dictionary_value(dictionary, key, new_value):
    for value in dictionary:
        # if number in str(num +1):
            if key in value:
                value[key] = new_value
            else:
                print(f"The key '{key}' does not exist in the dictionary.")
            return dictionary