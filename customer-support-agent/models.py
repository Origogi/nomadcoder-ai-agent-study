from pydantic import BaseModel


class UserAccountContext(BaseModel):
    customer_id: int
    name: str
    email : str
    tier: str = "basic"  # premium enterprise

class InputGuardRailOutput(BaseModel):
    is_off_topic : bool
    reason : str