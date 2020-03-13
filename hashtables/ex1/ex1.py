#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(16)

    # Check length isn't 1, if so return None ( as per test spec)
    # Loop through the weights list (using length), insert each one into the hash table.
    # Key is the weight, the value is the index in the list

    # Loop through list again, passing in the limit - the current weight into the retrieve function
    # Assign each return value to a temporary variable.
    # Check if the the variable exists (aka, true). If it's false, continue
    # If it's true, we have a match to the limit.
    # Create a new tuple using the returned value (the index of the matching item), and the current
    # number we are on in the loop (the index of the matching item)

    return None


def print_answer(answer):
    if answer is not None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")
