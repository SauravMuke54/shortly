from pydantic import BaseModel, HttpUrl, field_validator


class LongUrl(BaseModel):
    url: HttpUrl

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: HttpUrl):
        if value.scheme not in {"http", "https"}:
            raise ValueError("URL must start with http:// or https://")

        return value
