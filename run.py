
from tigopesa.tigoPesa import TigoCharges, generated_transactiion_id


def main():
    first_name = input('Enter your firt name :')
    last_name = input('Enter your Last name :')
    phoneNumber = input('Enter phone number: ')
    amount = input('Enter the amount pay:')
    tigo_charge = TigoCharges(

        subscriber_phone_number=phoneNumber,
        f_name=first_name,
        l_name=last_name,
        local_amount=int(amount),
        origin_amount=int(amount)
    )
    result = tigo_charge.charge()
    print(result)
    print(generated_transactiion_id)


if __name__ == '__main__':
    main()
