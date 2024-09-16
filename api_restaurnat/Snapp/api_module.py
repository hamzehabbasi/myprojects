from django.http import HttpResponse

# def delete_reserve(foods,dele):
#     if dele in foods:
#         dele.delete()
#         return f'your request ({dele}) is deleted'

# def more_food(list_foods,plus,reserved):
#     for i in list_foods:
#         if plus == i['name_food']:
#             if not plus in reserved:
#                 plus=reserved.append(i)
#                 plus.save()
#                 return f'your request ({plus}) reserved'
#             else:
#                 i=input('you reserved this food before. do you want more(yes=1)?')
#                 if i== '1':
#                     plus.save()
#                     return f'your request ({plus}) reserved'
#                 else:
#                     return  'ok thanks for your waiting'

# def reserve_food(list_foods,plus):
#     for i in list_foods:
#         if plus == i['name_food']:
#             # if not plus in reserved:
#             #     plus=reserved.append(i)
#             i.save()
#             return f'your request ({plus}) reserved'
#         else:
#                 i=input('you reserved this food before. do you want more(yes=1)?')
#                 if i== '1':
#                     plus.save()
#                     return f'your request ({plus}) reserved'
#                 else:
#                     return  'ok thanks for your waiting'

# def edit_reserve(reserved,edit,new_food):
#     if edit in reserved:
#         reserved.edit=new_food
#         reserved.save()

def list_kardan(sel):
    result=''
    for number, kala in enumerate(sel):
        for key ,value in kala.items():
            result += f'{number +1}:{key}:{value} \n'
    return result
#
def make_list(sel):
    result=''
    for num , kar in enumerate(sel):
        result +=f'{num + 1}:{kar} \n'
    return result
