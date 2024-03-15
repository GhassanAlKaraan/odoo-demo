first_name = 'Ghassan'
last_name = 'AlKaraan'


# compute
my_full_name = first_name + ' '+ last_name

# inverse
# my_last_name = my_full_name - first_name
my_last_name = my_full_name[len(first_name)+1 : ]



print(my_last_name)