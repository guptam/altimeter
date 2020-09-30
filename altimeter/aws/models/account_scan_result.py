"""pydantic models representing account scan results """
from typing import List, Dict, Union, Any

from altimeter.core.alti_base_model import BaseAltiModel


class AccountScanResult(BaseAltiModel):
    """pydantic model representing account scan results """

    account_id: str
    artifacts: List[str]
    errors: List[str]
    api_call_stats: Dict[str, Union[int, Dict[str, Any]]]
