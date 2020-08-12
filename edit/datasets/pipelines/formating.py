from ..registry import PIPELINES
from edit.utils import is_list_of, is_tuple_of
import numpy as np


@PIPELINES.register_module()
class ImageToTensor(object):
    """
    [HWC] -> [CHW]

    Args:
        keys (Sequence[str]): Required keys to be converted.
        to_float32 (bool): Whether convert numpy image array to np.float32
            before converted to tensor. Default: True.
    """
    def __init__(self, keys, to_float32=True):
        self.keys = keys
        self.to_float32 = to_float32

    def __call__(self, results):
        """Call function.

        Args:
            results (dict): A dict containing the necessary information and data for augmentation.

        Returns:
            dict: A dict containing the processed data and information.
        """
        for key in self.keys:
            # deal with gray scale img: expand a color channel
            if len(results[key].shape) == 2:
                results[key] = results[key][..., None]
            if self.to_float32 and not isinstance(results[key], np.float32):
                results[key] = results[key].astype(np.float32)
            results[key] = results[key].transpose(2, 0, 1)  # [HWC] -> [CHW]
        return results

    def __repr__(self):
        return self.__class__.__name__ + (
            f'(keys={self.keys}, to_float32={self.to_float32})')


@PIPELINES.register_module()
class Collect(object):
    """Collect data from the loader relevant to the specific task.

    This is usually the last stage of the data loader pipeline. Typically keys
    is set to some subset of "img", "gt_labels".

    Args:
        keys (Sequence[str]): Required keys to be collected.
    """

    def __init__(self, keys):
        self.keys = keys

    def __call__(self, results):
        """Call function.

        Args:
            results (dict): A dict containing the necessary information and
                data for augmentation.

        Returns:
            dict: A dict containing the processed data and information.
        """
        data = []
        for key in self.keys:
            data.append(results[key])
        return data

    def __repr__(self):
        return self.__class__.__name__ + (
            f'(keys={self.keys})')
