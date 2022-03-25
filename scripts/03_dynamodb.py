# interact with SynamoDB

import boto3
ddbClient = boto3.client('dynamodb', region_name='eu-west-1')
dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
ddbTable = dynamodb.Table('StockData')

# query table

# put
# add item to table
def write_ddb(TICKER,DATE,CHANGE,CLOSE,PRICE,RSI,SUGGESTION):
    print(TICKER)
    print(DATE)
    print(CHANGE)
    print(CLOSE)
    print(PRICE)
    print(RSI)
    print(SUGGESTION)
    ddbClient.put_item(
        TableName='StockData',
        Item={
            'TICKER': {'S': TICKER },
            'DATE': {'N': DATE },
            'CHANGE': {'N': CHANGE },
            'CLOSE': {'N': CLOSE },
            'PRICE': {'N': PRICE },
            'RSI': {'N': RSI },
            'SUGGESTION': {'S': SUGGESTION }
        }
    )

TICKV = 'AAPL'
DATEV = '20220118'
CHANGEV = str(round(15.98765432,2))
CLOSEV = '234.50'
PRICEV = '150.678'
RSIV = '63.6'
SUGV = 'HOLD'
write_ddb(TICKV,DATEV,CHANGEV,CLOSEV,PRICEV,RSIV,SUGV)

exit()

def get_ddb(ticker,date):
    response = ddbTable.get_item(
        Key={
            'TICKER': ticker,
            'DATE': date
        }
    )
    item = response['Item']
    print(item)

#get_ddb('AAPL',DATEV)

exit()


def write_ddb(TICKER,DATE,CHANGE,CLOSE,PRICE,RSI,SUGGESTION):
    print(TICKER)
    print(DATE)
    print(CHANGE)
    print(CLOSE)
    print(PRICE)
    print(RSI)
    print(SUGGESTION)
    ddbTable.put_item(
        Item={
            'TICKER': TICKER,   # String
            'DATE': DATE,       # Number
            'CHANGE': {
                "N": CHANGE
            },   # Number
            'CLOSE': CLOSE,     # Number
            'PRICE': PRICE,     # Number
            'RSI': RSI,         # Number
            'SUGGESTION': SUGGESTION    # String
        }
    )

TICKV = 'AAPL'
DATEV = 20220114
CHANGEV = round(15.98765432,2)
CLOSEV = '234.50'
PRICEV = '150.678'
RSIV = '63.6'
SUGV = 'HOLD'
write_ddb(TICKV,DATEV,CHANGEV,CLOSEV,PRICEV,RSIV,SUGV)


#
#getItemResponse = ddbClient.get_item(
#    Key = {
#        "TICKER" : {
#            "S" : "AAPL"
#        },
#        "DATE" : {
#            "S" : "20220321"
#        }
#    },
#    TableName = 'SD-20220322-01'
#)
#print(getItemResponse)

#
#response = ddbTable.get_item(
#    Key={
#        'TICKER': 'AAPL'
#    }
#)
#item = response['Item']
#print(item)
#
#putResponse['ResponseMetadata']['HTTPStatuscode']



#
#def query_db(TICKER, dynamodb=None):
#  if not dynamodb:
#    dynamodb = boto3.resource("arn:aws:dynamodb:eu-west-1:830667908377:table/SD-20220322-01")
#
#  table = dynamodb.Table('SD-20220322-01')
#  response = table.query(
#    KeyConditionExpression=Key('TICKER').eq(TICKER)
#  )
#  return response['Items']
#
#if __name__ == '__main__':
#    query_year = 'AAPL'
#    print(f"Movies from {query_year}")
#    movies = query_db(query_year)
#    for movie in movies:
#        print(movie['year'])
#
#
