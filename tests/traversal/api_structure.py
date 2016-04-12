from spree.rest import APIEndpoint, APIEntityEndpoint, APICollectionEndpoint


class OrderEntity(APIEntityEndpoint):

    def retrieve(self, request):
        pass


class OrderList(APICollectionEndpoint):

    endpoints = [
        (r'[0-9]+', OrderEntity)
    ]

    def retrieve(self, request):
        pass

    def create(self, request):
        pass


class CustomerOrderList(OrderList):

    def retrieve(self, request):
        pass

    def create(self, request):
        pass


class CustomerEntity(APIEntityEndpoint):

    endpoints = [
        (r'orders', CustomerOrderList)
    ]

    def retrieve(self, request):
        pass


class CustomerList(APICollectionEndpoint):

    endpoints = [
        (r'[0-9]+', CustomerEntity)
    ]

    def retrieve(self, request):
        pass

    def create(self, request):
        pass


class APIRoot(APIEndpoint):

    def retrieve(self, request):
        return None

    endpoints = [
        ('customers', CustomerList),
        ('orders', OrderList),
    ]
