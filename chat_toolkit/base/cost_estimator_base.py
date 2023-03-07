from abc import ABC, abstractmethod


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
    def cost_estimate_data(self) -> tuple[float, dict]:
        """
        Abstract property that returns the estimated cost in of an object's
        usage so far and any relevant metadata available.

        :return: Estimated cost, any applicable metadata.
        """
        pass
