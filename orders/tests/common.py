class CommonDataForTests:
    COFFEE_IDS = []

    ORDER_IDS = []

    COFFEE_ORDER_IDS = []

    @staticmethod
    def remove_duplicate(lst: list):
        s = set()
        for coffee in lst:
            if coffee not in s:
                yield coffee
                s.add(coffee)

    @staticmethod
    def get_first_coffee_id():
        return CommonDataForTests.COFFEE_IDS[0]

    @staticmethod
    def get_second_coffee_id():
        return CommonDataForTests.COFFEE_IDS[1]

    @staticmethod
    def get_third_coffee_id():
        return CommonDataForTests.COFFEE_IDS[2]

    @staticmethod
    def get_order_id():
        return CommonDataForTests.ORDER_IDS[0]

    @staticmethod
    def get_first_coffee_order_id():
        return list(CommonDataForTests.remove_duplicate(
            CommonDataForTests.COFFEE_ORDER_IDS))[0]

    @staticmethod
    def get_second_coffee_order_id():
        return list(CommonDataForTests.remove_duplicate(
            CommonDataForTests.COFFEE_ORDER_IDS))[1]

    @staticmethod
    def get_third_coffee_order_id():
        return list(CommonDataForTests.remove_duplicate(
            CommonDataForTests.COFFEE_ORDER_IDS))[2]

    @staticmethod
    def get_wrong_coffee_order():
        return '62d3f37d28cb8a5fc5dffe42'
