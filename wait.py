import boto3
import os
import time

env_var_name = 'MATCH_ROLE'
interval_in_seconds = int(os.environ.get('INTERVAL_IN_SECONDS', 10))
max_attempts = int(os.environ.get('MAX_ATTEMPTS', 100))
attempts_made = 0

if env_var_name not in os.environ:
  print('Expected {} environment variable to be defined'.format(env_var_name))
  quit(1)

match_role = os.environ[env_var_name]

for attempts_made in range(max_attempts):
  client = boto3.client('sts')
  try:
    response = client.get_caller_identity()
  except:
    print('Error getting identity')
  else:
    if match_role in response['Arn']:
      print('Matching role ("{}") found'.format(response['Arn']))
      quit(0)

    print('Matching role not found')
    print('Expected to find {} in {}'.format(match_role, response['Arn']))

  if (attempts_made + 1) >= max_attempts:
    print('Maximum number of attempts reached ({}), giving up'.format(max_attempts))
    quit(2)

  print('Will check again in {} seconds'.format(interval_in_seconds))
  print('----------------------------------------------')
  time.sleep(interval_in_seconds)