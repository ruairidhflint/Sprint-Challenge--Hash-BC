#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


class Ticket:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination


def reconstruct_trip(tickets, length):
    hashtable = HashTable(length)
    route = [None] * length

    # Insert all tickets into the hash table with starting point as the key and destination
    # as the value
    for item in tickets:
        hash_table_insert(hashtable, item.source, item.destination)

    # set initial values of iterations and destination
    iterations = 0
    current_value = "NONE"

    # Loop through tickets (?) for the correct length, retrieving values and storing them in the route array until 'None" is reached
    # Correct length will have to ignore the initial None value and be one short to ignore the final None value, as per the spec
    while iterations < length - 1:
        current_value = hash_table_retrieve(hashtable, current_value)
        route[iterations] = current_value
        iterations += 1

    return route
