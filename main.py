import boto3
import argparse
import pprint

parser = argparse.ArgumentParser()
parser.add_argument('--profile',
                    action="store",
                    required=True)
parser.add_argument('--apiId',
                    action="store",
                    required=True)
parser.add_argument('--authorizerId',
                    action="store",
                    required=False,
                    default=None)
parser.add_argument('--debug',
                    action="store_true",
                    default=False)
parser.add_argument('--region',
                    action="store",
                    required=False,
                    default="us-east-1")
args = parser.parse_args()

session = boto3.Session(profile_name=args.profile, region_name=args.region)
apigateway = session.client('apigateway')

paginator = apigateway.get_paginator('get_resources')
iterator = paginator.paginate(restApiId=args.apiId)

total = 0
for page in iterator:
    for item in page['items']:
        try:
            verbs = list(item['resourceMethods'].keys())
            if 'OPTIONS' in verbs:
                verbs.remove('OPTIONS')
            for verb in verbs:
                method = apigateway.get_method(
                    restApiId = args.apiId,
                    resourceId = item['id'],
                    httpMethod = verb)
                
                if args.authorizerId != None and args.authorizerId == method['authorizerId']:
                    if args.debug:
                        print(item['path'],verb,method['authorizerId'])
                    total+=1
        except KeyError:
            if args.debug:
                print("Error on resource id: %s: KeyError exception found" % item['id'])
    if args.debug:
        print("Running on debug mode")
        break

print("%d resources using authorizer id: %s" % (total, args.authorizerId))