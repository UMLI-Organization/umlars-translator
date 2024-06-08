class EaXmiDataSource:
    def __init__(self, data: Any):
        self.data = data

    def get_data(self) -> Any:
        return self.data