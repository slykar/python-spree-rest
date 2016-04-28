from spree.rest import APIEndpoint, APIEntity, APICollection


class OrderEntity(APIEntity):

    def retrieve(self, request):
        pass


class OrderList(APICollection):

    endpoints = [
        (r'[0-9]+', OrderEntity)
    ]

    def retrieve(self, request):
        pass

    def create(self, request):
        pass


class CustomerOrderList(OrderList):

    def retrieve(self, request):
        super(CustomerOrderList, self).retrieve(request)

    def create(self, request):
        pass


class CustomerEntity(APIEntity):
    endpoints = [
        (r'orders', CustomerOrderList)
    ]

    def update(self, request):
        pass

    def retrieve(self, request):
        pass


class CustomerList(APICollection):

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
