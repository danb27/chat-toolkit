from abc import ABC, abstractmethod
from typing import Optional


class CostEstimatorBase(ABC):
    """
    Used to add cost estimation functionality to a class.
    """

    def __init__(self, pricing_rate: float, **kwargs):
        """
        Instantiates a cost estimator. Note: Even if a default value is
        set for pricing_rate, the costs and estimations produced by this
        package are the responsibility of the user. You are free to
        ignore, overwrite, or even extend our cost estimation logic.

        :param pricing_rate: Pricing rate for the process.
        """
        self._pricing_rate = pricing_rate

    @property
    @abstractmethod
    def _cost_estimate_data(self) -> tuple[float, dict]:
        """
        Abstract property that returns the estimated cost in of an object's
        usage so far and any relevant metadata available.

        :return: Estimated cost, any applicable metadata.
        """
        pass

    @property
    def cost_estimate_data(self) -> tuple[float, dict]:
        """
        Takes private method and adds any standardized data to the metadata
        before returning
        """
        cost_estimate, metadata = self._cost_estimate_data
        metadata["pricing_rate"] = self._pricing_rate
        return cost_estimate, metadata


class ComponentBase(CostEstimatorBase, ABC):
    """
    Used to create components in a standardized manner.
    """

    def __init__(self, model: Optional[str], **kwargs):
        """
        Instantiates component.

        :param model: Model to specify for ML component.
        :param kwargs: Keyword arguments to pass to parent class.
        """
        super().__init__(**kwargs)
        self._model = model
