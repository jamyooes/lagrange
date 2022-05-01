import random
class Lagrange:
    def __init__(self):
        self.coefficents = [] # this list will hold the coefficents to the function
        self.keys = []        # this list will hold the actual key pairs from the resulting functions
        self.secret = 0       # this will hold the secret in numeric values
        self.generatePrimes()   #this function will be called during instaniation which will create a list of primes for the RSA function
        self.generateLowPrimes()    #this function will be called during instantiation which will create a list of small primes for the RSA function
        self.givenShares = []          # a temp state to handle actual shares from an input
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
        # generate new random coefficents for the largange inerpolation function, which will be stored in a list in self.coefficents 
        self.generate_random_coefficents(int(minimum_shares))
        # assign new shares, the shares will be stored in a list in self.keys
        self.lagrange_interpolation(int(number_of_new_shares))
        return (self.keys)

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
        # I was not sure how to encode strings and decrypt them effectively, so I just assumed the message is going to be an number and will be the y-intercept
        #I tried to encode the number with RSA, but I was unsuccessful
        # I put a check in case a user decides to enter some string
        if message.isdigit() == False:
            print("please input a number")
            return None
        self.secret = self.encode(int(message))
        print(self.secret)
        self.generate_random_coefficents(int(minimum_shares))
        self.lagrange_interpolation(int(share_number))
        self.givenShares = []
        return self.keys

    def decrypt(self, minimum_shares, shares):
        """
        30 points
        # Parameters
        minimum_shares: the minimum number of shares (coordinate pairs) required to unlcok a secret
        shares: the actual secret shares

        # Function
        this function takes the minimum number of shares to unlock a secret, and the shares you are providing and outputs the decoded secret (if you devise a system for converting messages to a coordinate in the encrypt step, to receive the full extra credit, you need to convert those messages to plaintext at this step
        """
        secretMessage = 0
        # print(self.givenShares)
        # perform the math in shamir's secret sharing mechanism
        for current_index_share in range (int(minimum_shares)):

            numerator = 1 # numerator for shamir's secret sharing
            denomimator = 1 # denominator for shamir's secret sharing

            for not_current_share in range (int(minimum_shares)):
                if not_current_share != current_index_share:
                    numerator *= (0-(self.givenShares[not_current_share][0])) # in the numerator 0 is being subtracted from the x values of the shares and then multiplied to each other
                    denomimator *= (self.givenShares[current_index_share][0] - self.givenShares[not_current_share][0]) # the denominator subtracts the current share with the other x value of the shares and multiplies each other
            
            fraction_shamir = numerator/ denomimator # the fractional portion of shamir
            secretMessage += self.givenShares[current_index_share][1] * fraction_shamir # multiply the y value of the current share with the fractional portion of shamir
            # print("shamir: ",fraction_shamir)
            # print("x", self.givenShares[current_index_share][1])
            # print(secretMessage)
        return round(secretMessage, 0)

    # this function will asign new shares using the lagrange_interpolation
    def lagrange_interpolation(self, num_shares):
        # reset the pre-existing keys
        self.keys = []
        for i in range (num_shares):
            share_x = random.randint(-100, 100)   #randomly generate the x value of the share. I am also assuming that it is very trivial to have duplicate keys
            share_y = 0 # y value of the share

            # lagrange interpolation function
            for key, function_coefficients in enumerate (self.coefficents):
                share_y += function_coefficients * (share_x) ** key
            
            # append a tuple for the share. Can access the shares through self.keys 
            self.keys.append((share_x , share_y))

    # function to generate random coefficents to make/remake the equation. The coefficents will be store in self.coefficents, which is a list of coefficents
    def generate_random_coefficents(self, min_shares):
        self.coefficents = []   # empty the pre-existing coefficents to create the new equation
        self.coefficents.append(self.secret) # add our secret as the first coefficents as the y-intercept
        #randomly generate the coefficients
        for i in range (int(min_shares) - 1):
            self.coefficents.append(random.randint(-100, 100))

    #helper function to generate a list of primes for RSA encoding
    def generatePrimes(self):
        self.primes = []
        for numbers in range (2, 1000):
            flag = 0
            for i in range (2, numbers):
                if numbers % i == 0:
                    flag = 1
                    break
            if flag == 0:
                self.primes.append(numbers)
    
    #helper function to generate a list of primes for RSA encoding
    def generateLowPrimes(self):
        self.lowPrimes = []
        for numbers in range (2, 20):
            flag = 0
            for i in range (2, numbers):
                if numbers % i == 0:
                    flag = 1
                    break
            if flag == 0:
                self.lowPrimes.append(numbers)
    
    #help function to handle user input for shares
    def handleShares(self, xShare, yShare):
        self.givenShares.append((xShare, yShare))
    
    #I gave up trying to figure out encoding
    # #use rsa to encode a message
    def encode(self, secret):
        p = random.choice(self.primes)	
        q = random.choice(self.primes)	
        e = random.choice(self.lowPrimes)	
        while p == q:
            q = random.choice(self.primes)	
        self.n = p * q #this is needed to later decode the message for RSA
        poweredMessage = secret ** e 
        encodedMessage = poweredMessage % self.n 
        return encodedMessage

    # no clue how to decode
    def decode(self, encodedMessage):
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
        shares = print("What shares do you have?")
        for i in range(int(minimum_shares)):
            shareX = int(input("What is the x-value of the share: "))
            shareY = int(input("What is the y-value of the share: "))
            interpolation.handleShares(shareX, shareY)
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
    
    continuing = input("Do you want to continue, y for yes and n for no? ")
    while continuing == "y":
            choice = input("Do you want to encrypt or decrypt a secret or generate new shares (e/d/g)?")

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
                shares = print("What shares do you have?")
                for i in range(int(minimum_shares)):
                    shareX = int(input("What is the x-value of the share: "))
                    shareY = int(input("What is the y-value of the share: "))
                    interpolation.handleShares(shareX, shareY)
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
            continuing = input("Do you want to continue, y for yes and n for no? ")


if __name__ == "__main__":
    main()
