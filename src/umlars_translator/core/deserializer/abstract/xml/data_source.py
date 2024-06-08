from xml.etree.ElementTree import Element


class XmlDataSource:
    def __init__(self, data: ) -> None:
        self._data = data 

    @property
    def data(self) -> Any:
        return self._data
    
    @data.setter
    def data(self, data: Any) -> None:
        self._data = data
