from abc import ABC

from chat_toolkit.base.cost_estimator_base import CostEstimatorBase


class ComponentBase(CostEstimatorBase, ABC):
    """
    Used to create components in a standardized manner.
    """

    def __init__(self, model: str, **kwargs):
        """
        Instantiates component.

        :param model: Model to specify for ML component.
        :param kwargs: Keyword arguments to pass to parent class.
        """
        super().__init__(**kwargs)
        self._model = model
