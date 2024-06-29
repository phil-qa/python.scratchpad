import math
from abc import ABC, abstractmethod
import uuid


class ModelItemInterface(ABC):
    @abstractmethod
    def total_value(self):
        pass


class ValueType:
    RETAIL = 1
    SUBSCRIPTION = 2


class Transaction:
    def __init__(self, name, base_value, value_type, frequency):
        self.id = uuid.uuid4()
        self.name = name
        self.base_value = base_value
        self.value_type = value_type
        self.frequency = frequency


# Revenue Analysis
class ValueItem(ModelItemInterface, Transaction):
    def __init__(self, name, base_value=0, value_type=ValueType.RETAIL,
                 frequency=[0, 0]):# thing per term
        super().__init__(name, base_value,value_type,frequency)

    def total_value(self, term_range=1):
        if self.value_type == ValueType.RETAIL:
            return self.base_value
        else:
            return self.base_value * (self.frequency[0] * round(( term_range / self.frequency[1] )))


class CostItem(ModelItemInterface, Transaction):
    def __init__(self, name, base_value=0, value_type=ValueType.RETAIL,
                 frequency=[0, 0]):# thing per term
        super().__init__(name, base_value,value_type,frequency)

    def total_value(self, term_range=1):
        if self.value_type == ValueType.RETAIL:
            return self.base_value  * -1
        else:
            return self.base_value * (self.frequency[0] * round( term_range / self.frequency[1]))* -1


# Class that houses the model items for processing
class RevenueStream:
    def __init__(self, stream_term = 1):
        self.revenue_items = []
        self.positive_value = None
        self.negative_value = None
        self.stream_term = stream_term

    def add_or_update_model_item(self, item_to_add: ModelItemInterface) -> None:
        existing_item = next((item for item in self.revenue_items if item.id == item_to_add.id), None)

        if existing_item is None:
            self.revenue_items.append(item_to_add)
        else:
            index = self.revenue_items.index(existing_item)
            self.revenue_items[index] = item_to_add
        existing_item = next((item for item in self.revenue_items if item.id == item_to_add.id), None)
        self.calculate_term_value(existing_item.id)

    def calculate_term_value(self, item_id):
        revenue_item = [ri for ri in self.revenue_items if ri.id == item_id]
        term_value = (revenue_item.base_value * revenue_item.frequency[0] * (revenue_item.frequency[1]/math.floor(revenue_item.stream_term))) if revenue_item.value_type == ValueType.SUBSCRIPTION else revenue_item.total_value()
        if term_value > 0 :
            self.positive_value+=term_value
        else:
            self.negative_value+=term_value
    def stream_value(self):
        return self.positive_value - self.negative_value