from collections import namedtuple


class CommonDataForTests:
    CAP_DESCRIPTION = 'A cappuccino is the perfect balance of espresso,' \
                      ' steamed milk and foam. This coffee is all about the' \
                      ' structure and the even splitting of all elements ' \
                      'into equal thirds. An expertly made cappuccino should ' \
                      'be rich, but not acidic and have a mildly sweet ' \
                      'flavouring from the milk. And, because the milk is ' \
                      'not actually mixed in it gives the espresso a ' \
                      'stronger flavour.'

    LATTE_DESCRIPTION = "A latte or caffè latte is a milk coffee that is a " \
                        "made up of one or two shots of espresso, steamed " \
                        "milk and a final, thin layer of frothed milk on top." \
                        " If you don't drink dairy milk, you can easily swap " \
                        "it for a plant-based alternative like soy, oat or " \
                        "coconut milk."

    COFFEE = namedtuple(
        typename='Coffee', field_names=[
            'title', 'description', 'price', 'list_of_images'
        ]
    )

    LATTE = COFFEE(
        title='latte',
        description=LATTE_DESCRIPTION,
        price=2.4,
        list_of_images=['coffee/tests/1.jpg', 'coffee/tests/2.jpg']
    )
    CAPPUCCINO = COFFEE(
        title='cappuccino',
        description=CAP_DESCRIPTION,
        price=2.6,
        list_of_images=['coffee/tests/3.jpg']
    )
    ESPRESSO = COFFEE(
        title='espresso',
        description=None,
        price=1.4,
        list_of_images=None
    )
    IDS = []
    IMAGES_ID = []

    def first_id(self):
        return self.IDS[0]

    def seconds_id(self):
        return self.IDS[1]

    def third_id(self):
        return self.IDS[2]

    wrong_coffee_id = '62d290090b8c6f4ebcae141e'

    def get_wrong_coffee_id(self):
        return self.wrong_coffee_id

    first_coffe_update = COFFEE(
        title='updated_title1',
        description='updated_desc1',
        price=None,
        list_of_images=None
    )
    third_coffee_update = COFFEE(
        title='updated_title2',
        description='updated_desc2',
        price=None,
        list_of_images=['coffee/tests/3.jpg']
    )

    RATINGS_ID = []
    RATING = namedtuple('RATING', field_names=['rating'])
    first_rating = RATING(rating=3)
    third_rating = RATING(rating=1)

    def first_rating_id(self):
        return self.RATINGS_ID[0]

    def third_rating_id(self):
        return self.RATINGS_ID[1]
