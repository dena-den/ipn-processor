from core.db.base import database


class Service:
    def process_new_notification(self, data):
        if data['type'] == 'in' and data['confirmation'] == 1:
            self.process_deposit(data)
            return 'SUCCESSFUL_DEPOSIT'

        elif data['type'] == 'out' and data['confirmation'] in [0, 1]:
            self.process_withdrawal(data)
            return 'SUCCESSFUL_WITHDRAWAL'

        else:
            return 'UNKNOWN_TYPE'

    def process_deposit(self, data):
        currency_id = database.get_currency_id(data['currency'])
        wallet_id = database.get_wallet_id(data['to'])
        database.insert_deposit(data, currency_id, wallet_id)

    def process_withdrawal(self, data):
        currency_id = database.get_currency_id(data['currency'])
        wallet_id = database.get_wallet_id(data['from'])
        database.insert_withdrawal(data, currency_id, wallet_id)


service = Service()
