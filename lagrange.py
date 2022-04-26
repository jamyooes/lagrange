import random
class Lagrange:
    def __init__(self):
        pass

    def generate_new_shares(self, minimum_shares, shares, number_of_new_shares):
        """
        30 points
        # Parameters
        minimum_shares: the minimum number of shares (coordinate pairs) required to unlcok a secret
        shares: the actual secret shares
        number_of_new_shares: the number of new shares requested (should be consistent with old shares)

        # Function
        this function outputs new keys given the secret shares
        """
        coefficents = []    # this will hold the coefficents to the function
        keys = []           # this will hold the actual key pairs from the resulting functions
        
        # generate random coefficents for the function the range is quite trivial and I couldn't think of the ranges I could use
        for i in range (int(minimum_shares) - 1):
            coefficents.append(random.randint(0, 9999))
        
        # insert values for each share
        for key_generation in range (int(shares)):
            key_val = 0 # reset the key val when in the next share

            # function to generate the secret shares
            for key, function_coefficients in enumerate (coefficents):
                key_val += function_coefficients * (key_generation + 1) ** key
            
            # append a key-val pair where the key is the share number where the val is the secret value for the share
            keys.append((key_generation + 1, key_val))
        return (keys)

    def encrypt(self, message, minimum_shares, share_number):
        """
        30 points
        # Parameters
        message: a message you wish to encrypt, you can choose to simply encode numbers or, for extra credit, you can convert plaintext messages to a number representation and encode that
        minimum_shares: the minimum number of shares required to "unlock" the secret
        share_number: the number of shares generated

        # Function
        this function outputs coordinate pairs (the secret shares) that can be handed out to the end user
        """
        pass

    def decrypt(self, minimum_shares, shares):
        """
        30 points
        # Parameters
        minimum_shares: the minimum number of shares (coordinate pairs) required to unlcok a secret
        shares: the actual secret shares

        # Function
        this function takes the minimum number of shares to unlock a secret, and the shares you are providing and outputs the decoded secret (if you devise a system for converting messages to a coordinate in the encrypt step, to receive the full extra credit, you need to convert those messages to plaintext at this step
        """
        pass


def main():
    interpolation = Lagrange()
    choice = input(
        "Do you want to encrypt or decrypt a secret or generate new shares (e/d/g)?"
    )

    if choice == "e":
        message = input("What is the secret you wish to encrypt?")
        minimum_shares = input(
            "What is the minimum number of shares you wish to deploy?"
        )
        share_number = input(
            "What is the minimum number of shares you wish to generate?"
        )
        encryption = interpolation.encrypt(message, minimum_shares, share_number)
        print(encryption)

    elif choice == "d":
        minimum_shares = input(
            "What is the minimum number of shares you need to decrypt?"
        )
        shares = input("What shares do you have?")
        decryption = interpolation.decrypt(minimum_shares, shares)
        print(decryption)

    elif choice == "g":
        minimum_shares = input(
            "What is the minimum number of shares you need to decrypt?"
        )
        shares = input("What shares do you have?")
        share_number = input("What is the number of new shares you want to generate?")
        new_shares = interpolation.generate_new_shares(
            minimum_shares, shares, share_number
        )
        print(new_shares)


if __name__ == "__main__":
    main()
