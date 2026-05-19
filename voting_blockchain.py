# voting_blockchain.py
# Simple Blockchain-Based Voting Management System

import hashlib
import json
from time import time


# -----------------------------
# Candidate Class
# -----------------------------
class Candidate:
    def __init__(self, candidate_id, name):
        self.candidate_id = candidate_id
        self.name = name

    def to_dict(self):
        return {
            "candidate_id": self.candidate_id,
            "name": self.name
        }


# -----------------------------
# Voter Class
# -----------------------------
class Voter:
    def __init__(self, voter_id, name):
        self.voter_id = voter_id
        self.name = name
        self.has_voted = False

    def to_dict(self):
        return {
            "voter_id": self.voter_id,
            "name": self.name,
            "has_voted": self.has_voted
        }


# -----------------------------
# Block Class
# -----------------------------
class Block:
    def __init__(self, index, timestamp, transactions, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }


# -----------------------------
# Blockchain Class
# -----------------------------
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(
            0,
            time(),
            ["Genesis Block"],
            "0"
        )
        self.chain.append(genesis_block)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, transactions):
        previous_block = self.get_latest_block()

        new_block = Block(
            index=previous_block.index + 1,
            timestamp=time(),
            transactions=transactions,
            previous_hash=previous_block.hash
        )

        self.chain.append(new_block)

    def print_chain(self):
        print("\n========== BLOCKCHAIN ==========")

        for block in self.chain:
            print(f"\nBlock Index      : {block.index}")
            print(f"Timestamp        : {block.timestamp}")
            print(f"Transactions     : {block.transactions}")
            print(f"Previous Hash    : {block.previous_hash}")
            print(f"Current Hash     : {block.hash}")
            print("-" * 50)

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Check current hash
            if current.hash != current.calculate_hash():
                return False

            # Check previous hash linkage
            if current.previous_hash != previous.hash:
                return False

        return True


# -----------------------------
# Voting System Class
# -----------------------------
class VotingSystem:
    def __init__(self):
        self.voters = {}
        self.candidates = {}
        self.blockchain = Blockchain()

    # -------------------------
    # Add Candidate
    # -------------------------
    def add_candidate(self):
        candidate_id = input("Enter Candidate ID: ")

        if candidate_id in self.candidates:
            print("Candidate ID already exists!")
            return

        name = input("Enter Candidate Name: ")

        candidate = Candidate(candidate_id, name)
        self.candidates[candidate_id] = candidate

        print("Candidate added successfully!")

    # -------------------------
    # Add Voter
    # -------------------------
    def add_voter(self):
        voter_id = input("Enter Voter ID: ")

        if voter_id in self.voters:
            print("Voter ID already exists!")
            return

        name = input("Enter Voter Name: ")

        voter = Voter(voter_id, name)
        self.voters[voter_id] = voter

        print("Voter added successfully!")

    # -------------------------
    # Cast Vote
    # -------------------------
    def cast_vote(self):
        voter_id = input("Enter Voter ID: ")

        if voter_id not in self.voters:
            print("Voter not found!")
            return

        voter = self.voters[voter_id]

        if voter.has_voted:
            print("This voter has already voted!")
            return

        candidate_id = input("Enter Candidate ID to vote for: ")

        if candidate_id not in self.candidates:
            print("Candidate not found!")
            return

        candidate = self.candidates[candidate_id]

        transaction = {
            "voter_id": voter.voter_id,
            "voter_name": voter.name,
            "candidate_id": candidate.candidate_id,
            "candidate_name": candidate.name
        }

        # Add vote to blockchain
        self.blockchain.add_block(transaction)

        # Mark voter as voted
        voter.has_voted = True

        print("Vote cast successfully!")

    # -------------------------
    # Validate Blockchain
    # -------------------------
    def validate_blockchain(self):
        if self.blockchain.validate_chain():
            print("Blockchain is VALID.")
        else:
            print("Blockchain is INVALID!")

    # -------------------------
    # Menu
    # -------------------------
    def menu(self):
        while True:
            print("\n========= Voting Management System =========")
            print("1. Add Candidate")
            print("2. Add Voter")
            print("3. Cast Vote")
            print("4. Print Blockchain")
            print("5. Validate Chain")
            print("6. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.add_candidate()

            elif choice == '2':
                self.add_voter()

            elif choice == '3':
                self.cast_vote()

            elif choice == '4':
                self.blockchain.print_chain()

            elif choice == '5':
                self.validate_blockchain()

            elif choice == '6':
                print("Exiting system...")
                break

            else:
                print("Invalid choice! Please try again.")


# -----------------------------
# Main Function
# -----------------------------
if __name__ == "__main__":
    voting_system = VotingSystem()
    voting_system.menu()