from pydantic import BaseModel, Field


class TrainingConfig(BaseModel):

    model_name: str

    learning_rate: float = Field(
        gt=0,
        le=1
    )

    epochs: int = Field(
        gt=0,
        le=10000
    )

    batch_size: int = Field(
        gt=0
    )