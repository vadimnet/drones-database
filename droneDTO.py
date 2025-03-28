from pydantic import BaseModel

class DroneDTO(BaseModel):
    id: int
    name: str
    pictures: list[str]
    description: str
    type: int
    characteristics_values: list[str]