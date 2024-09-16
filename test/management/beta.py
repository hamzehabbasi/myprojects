programs_list_key=Program.objects.all()
programs_list_key=[pro.key for pro in programs_list_key]
try:
    # Check if the user's metadata value is 'waiting'
    metadata = Metadata.objects.get(key='beta-program-enrollment', value='waiting')
    if metadata:
        print(f'programs_list_key: {list(programs_list_key)},')
        # Assuming the beta programs exist in the database
        program_key= input('enter program_key:')
        beta_programs = Program.k(program_key)
        if beta_programs:
            assign = Assign(customer=metadata.customer, program=beta_programs)
            assign.save()
            # Change the metadata value to 'accept'
            metadata.value = 'accepted'
            metadata.save()
        print(f"Beta programs activated for user {metadata.customer}")
    else:
        print("No 'waiting' metadata found for user")
except Metadata.DoesNotExist:
    print("User not found")




metadata.customer.save_synchronize_flag("profiles", True)
