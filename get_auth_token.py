# For ArgumentParser
import argparse

# For get_auth_token
from ura import eservice

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--access-key', help="Access Key for URA's e-service API")
    return parser.parse_args()

def main():
    args = parse_arguments()

    auth_token = eservice.get_auth_token(args.access_key)

    if auth_token == None:
        print("Could not get any authentication token. Check Access Key and try again.")
        return -1
    else:
        print("Received authentication token: " + auth_token)

if __name__ == '__main__':
    main()
