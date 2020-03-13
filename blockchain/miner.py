import random
from timeit import default_timer as timer
from uuid import uuid4
import sys
import requests
import hashlib


# Import OS and set up paths to make finding my.text easier
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
    - Note:  We are adding the hash of the last proof to a number/nonce for the new proof
    """

    start = timer()

    print("\nSearching for next proof")
    proof = str(0)

    # Stringify last proof, new proof is already stringified
    # Keep looping until a match is found
    while valid_proof(str(last_proof), proof) is False:
        # Generate a new random str/int using getrandbits
        proof = str(random.getrandbits(32))

    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof


def valid_proof(last_proof, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the proof?

    IE:  last_hash: ...AE9123456, new hash 123456888...
    """
    # Refactor for my brain to understand...pass in last proof and hash it inside this function rather 
    # than else where
    last_proof_hashed = hashlib.sha256(last_proof.encode()).hexdigest()
    new_proof_hashed = hashlib.sha256(proof.encode()).hexdigest()

    return last_proof_hashed[-6:] == new_proof_hashed[:6]

if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

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
        print(data.get('proof'))
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
