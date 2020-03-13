import random
from timeit import default_timer as timer
from uuid import uuid4
import sys
import requests
import hashlib

import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    """

    start = timer()

    print("Searching for next proof")
    proof = 0

    # Hash last_proof
    last_proof_hashed = hashlib.sha256(last_proof).encode().hexdigest()
    # Starting with zero, pass the new proof into valid_proof function.

    # If the function returns false (likely), do something to create a new proof.

    # Continue passing in random numbers until we hit a return value of true and then return said value
    while valid_proof(last_proof_hashed, proof) is False:
        # Random int? Random bits? Random bigint?
        # This needs to be a more random operation:
        proof = random.random() * 100000

    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof


def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the hash
    of the new proof?

    IE:  last_hash: ...AE9123456, new hash 123456E88...
    """

    # Either pass in last proof and hash here, or hash outside and pass it in / Done above
    # Hash current proof (second arg)
    new_proof = hashlib.sha256(proof).encode().hexdigest()

    # Compare the first six digits of last_hash with the first six digits of new hash
    # If a match, return true, otherwise return false
    return last_hash[:6] == new_proof[-6:]


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        # node = "https://lambda-coin.herokuapp.com/api"
        node = "https://lambda-coin-test-1.herokuapp.com/api"

    coins_mined = 0

    # Load or create ID
    my_file = os.path.join(THIS_FOLDER, 'my_id.txt')
    f = open(my_file, "r")
    id = f.read()
    print("ID is", id)
    f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
