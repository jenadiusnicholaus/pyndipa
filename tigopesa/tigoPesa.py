import requests
import random
import string
import simplejson as myjson
from requests.exceptions import HTTPError
import json
api_key = "FDw9cmtBB2GHe7XdfYtwHNBtYlSir3g4"

client_id = "JtFM1DZLTzvUasIAV5jAZpHvXOkdLkmo"
client_secret = "ine4AbDG0cHDsaSy"
account = "25565267890"
pin = "3487"
id = "ElimuTube Company"


class AccessToken:
    """ in this class < get both client_id and secret_id and generates the token for  >
    """

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

        super(AccessToken, self).__init__()

    def get_access_api_token(self):
        """ Token is generated from these method"""
        try:
            api_url = 'https://secure.tigo.com/v1/oauth/generate/accesstoken-test-2018?grant_type=client_credentials'
            data = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
            }
            # header = {
            #     'content_typ': 'application/json',
            # }
            # PARAMS = {'header': header}
            # get_param = PARAMS['header']
            response = requests.post(url=api_url, data=data, )
            if response.status_code in range(200, 299):
                token_dict = json.loads(response.text)
                # print(token_dict)
                access_token = token_dict['accessToken']
                issuedAt = token_dict['issuedAt']
                expiresIn = token_dict['expiresIn']
                # print(f'access_token: {access_token}')
                # print(f'issuedAt: {issuedAt}')
                # print(f'expiresIn: {expiresIn}')
                return access_token
            else:
                print(response.text)
                return response.text
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')


def generated_transactiion_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


class TigoCharges:
    """ This class , creates charges from the customer by passing all necessary information"""

    def __init__(self,

                 subscriber_phone_number,
                 f_name,
                 l_name,
                 local_amount,
                 origin_amount,
                 transactionRefId=generated_transactiion_id(),
                 ):
        self.transactionRefId = transactionRefId
        self.phone_number = subscriber_phone_number
        self.f_name = f_name
        self.l_name = l_name
        self.local_amount = local_amount
        self.origin_amount = origin_amount
        super(TigoCharges, self).__init__()

    def get_token(self):
        """get token from generate token class """
        token_obj = AccessToken(client_id=client_id,
                                client_secret=client_secret)
        # get an access token  from obtained parameter
        token = token_obj.get_access_api_token()
        return token

    def get_params(self):
        """get all necessary parameter from the customer"""

        body_parameter = {
            "transactionRefId": str(self.transactionRefId),
            "MasterMerchant": {
                "account": account,
                "pin": pin,
                "id": id
            },
            "Subscriber": {
                "account": str(self.phone_number),
                "countryCode": "255",
                "country": "TZA",
                "firstName": str(self.f_name),
                "lastName": str(self.l_name)
            },
            "redirectUri": "http://40.113.155.216/payment/callback",
            "callbackUri": "https://40.113.155.216/payment/statuscallback",
            "language": "swa",
            "originPayment": {
                "amount": float(self.origin_amount),
                "currencyCode": "TZS",
                "tax": "0.00",
                "fee": "0.00"
            },
            "LocalPayment": {
                "amount": float(self.origin_amount),
                "currencyCode": "TZS"
            },

        }
        stringify_body = myjson.dumps(body_parameter, separators=(
            ',', ': '), sort_keys=True, indent=4)
        return stringify_body

    def get_url(self):
        api_url = 'https://secure.tigo.com/v1/tigo/payment-auth-test-2018/authorize'
        return api_url

    def get_headers(self):
        headers = {
            'accessToken': str(self.get_token()),
            'Content-type': 'application/json',
            # "Accept": "text/plain"
        }
        return headers

    def charge(self, ):
        """after operation like , gwting token, parameyer, urld hearer have been
        made correctly now is time to go a head and making post request to tigo servers"""

        # data = urllib.parse.urlencode(self.get_params()).encode("utf-8")

        try:
            api_url = self.get_url()
            _data = self.get_params()
            headers = self.get_headers()
            response = requests.post(api_url, data=_data, headers=headers)
            jsonResponse = response
            print(jsonResponse.content)
            return jsonResponse

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            return f'HTTP error occurred: {http_err}'
        except Exception as err:
            print(f'HTTP error occurred: {err}')
            print(jsonResponse.content)
            return f'Other error occurred: {err}'


class PaymentStatusCallback:

    """
    Body
    trans_status   =<transaction status success/fail>&...
    transaction_ref_Id  =<transaction ref ID>&...
    exter nal_ref_id  =<external_ref_id>&...
    mfs_id=<mfs_id>&...
    verification_code=<Access Token>
    """

    # TODO is  it will be done automatically after money submission

    def __init__(self, ):
        pass


#
# class ValidateMFS():
#     def __init__(self, transactionRefId, account, firstName, lastName):
#         self.transactionRefId = transactionRefId
#         self.account = account
#         self.firstName = firstName
#         self.lastName = lastName
#         super(ValidateMFS, self).__init__()
#
#     def get_parameter(self):
#         body_params = {
#             "transactionRefId": str(self.transactionRefId),
#             "ReceivingSubscriber": {
#                 "account": str(self.account),
#                 "countryCallingCode": "255",
#                 "countryCode": "TZA",
#                 "firstName": str(self.firstName) or None,
#                 "lastName": str(self.firstName) or None
#             }
#         }
#         stringfied_body = myjson.dumps(body_params, separators=(',', ': '), sort_keys=True, indent=4)
#         return stringfied_body
#
#     def get_url(self):
#         url = "https://secure.tigo.com/v1/tigo/mfs/validateMFSAccount-test-2018"
#         return url
#
#     def get_token(self):
#         token_obj = AccessToken(client_id=client_id, client_secret=client_secret)
#         # get an access token  from obtained parameter
#         token = token_obj.get_access_api_token()
#         return token
#
#     def get_header(self):
#         """
#         Header
#                 Content-Type:application/json
#                 accessToken:<valid access token>"""
#         header = {
#             'content_type': 'application/json',
#             'accessToken': str(self.get_token())
#         }
#         return header
#
#     def validate(self):
#         url = self.get_url()
#         data = self.get_parameter()
#         header = self.get_header()
#         request = requests.post(url, data=data, headers=header)
#         response = request
#         return response

# def main():
#     client_id = "JtFM1DZLTzvUasIAV5jAZpHvXOkdLkmo"
#     client_secret = "ine4AbDG0cHDsaSy"
#
#     token_obj = AccessToken(client_id=client_id, client_secret=client_secret)
#     # get an access token  from obtained parameter
#     token = token_obj.get_access_api_token()
#
#     tigo_charge = TigoCharges(
#
#         transactionRefId="yerwershg123",
#         subscriber_phone_number="255714694508",
#         f_name="Isaya",
#         l_name="Bendera",
#         local_amount="2929.63",
#         origin_amount="2892.009")
#     # print(tigo_charge.get_params())
#     res = tigo_charge.post_charger()
#     print(res)
#     # get_validate_parameter = json.loads(res.text)
#     # transactionRefId = get_validate_parameter['transactionRefId'],
#
#     # validdateMFS = ValidateMFS(transactionRefId="yershg123", account='255658123964', firstName=None,
#     #                            lastName=None)
#     # print(validdateMFS.validate())
#
#
# if __name__ == '__main__':
#     main()
