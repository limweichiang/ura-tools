# For ArgumentParser
import argparse

# For get_private_residential_property_transactions
from ura import eservice

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--out-file', help="Output filename [Default=stdout]")
    parser.add_argument('-k', '--access-key', help="Access Key for URA's e-service API")
    return parser.parse_args()

def main():
    args = parse_arguments()

    transactions = eservice.get_private_residential_property_transactions(args.access_key)

    if transactions == None:
        print("Could not get any data. Check Access Key and try again.")
        return -1
    else:
        # Write out to file
        if args.out_file:
            with open(args.out_file, "w") as f:
                f.write(transactions)
        else:
            print(transactions)

if __name__ == '__main__':
    main()
