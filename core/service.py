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
            return 'UNKNOWN_NOTIFICATION'

    def process_deposit(self, data):
        currency_id = database.get_currency_id(data['currency'])
        wallet_id, address_id = database.get_info_by_address(data['to'])
        database.insert_deposit(
            data, currency_id, wallet_id, address_id
        )

    def process_withdrawal(self, data):
        currency_id = database.get_currency_id(data['currency'])
        database.insert_withdrawal(data, currency_id)


service = Service()
