import pm
import argparse

parser = argparse.ArgumentParser(description='Run the password management software')

parser.add_argument('operation', type=str, help='Which operation should the application perform')

args = parser.parse_args()

pm.perform_operation(args.operation)

