from dotenv import load_dotenv
import secrets
import warnings
from typing import Annotated, Any, Literal
from pydantic import (
    AnyUrl,
    BeforeValidator,
    HttpUrl,
    MariaDBDsn,
    computed_field,
    model_validator,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import (
    Self,
)  # Self是一个类型变量，用于表示当前类的类型。在这个案例中，Self用于表示Settings类的类型。
import app.core.path_config as path_config

load_dotenv()


# 这个函数用于解析CORS(跨域资源共享)配置，它检查输入值，如果是字符串且不以[开头，则将其按逗号分隔，并返回列表。如果是列表或字符串，则直接返回。如果不符合这些条件，则抛出错误。
def prase_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    """Global settings for the application."""

    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./src)
        env_file=path_config.BASE_DIR.parent / ".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = (
        60 * 24 * 7
    )  # 60 minutes * 24 hours * 7 days = 1 week
    FRONTEND_HOST: str = "http://localhost:8000"
    ENVIRONMENT: Literal["local", "staging", "production"] = (
        "local"  # Literal(字面意思) is a type that restricts to the given values
    )

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(prase_cors)
    ] = []

    @computed_field  # 计算字段允许在序列化模型或数据类时包含属性和缓存属性。这对于从其他字段计算出来的字段，或计算成本较高且应缓存的字段非常有用。
    @property  # 用于将一个方法定义为属性，调用时不需要加括号
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rsplit("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    # CORS(跨域资源共享)配置，允许访问API的域名列表。
    # Annotated是Python的类型提示系统的一部分，用于提供关于变量的额外信息。在这个例子中，它用来关联额外的验证器到BACKEND_CORS_ORIGINS属性。使用Annotated可以让开发者在类型注释中嵌入更多的元数据或验证逻辑，这不仅可以增强代码的可读性，也可以提升运行时的数据处理能力。
    # BeforeValidator是一个Pydantic的装饰器/验证器，用于在数据赋值给模型属性之前对数据进行处理或验证。在这个案例中，BeforeValidator(prase_cors)应用于BACKEND_CORS_ORIGINS，意味着在赋值前，会先调用prase_cors函数来处理或验证输入值。

    PROJECT_NAME: str
    SENTRY_DSN: HttpUrl | None = None
    MARIADB_SERVER: str
    MARIADB_PORT: int = 3306
    MARIADB_USER: str
    MARIADB_PASSWORD: str = ""
    MARIADB_DB: str = ""

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(
        self,
    ) -> MariaDBDsn:  # MariaDBDsn是一个Pydantic的数据类，用于表示MariaDB的DSN(Data Source Name)。DSN是一个包含了数据库连接信息的字符串，用于连接数据库。在这个案例中，MariaDBDsn用于表示SQLAlchemy的数据库连接URI。
        return MultiHostUrl.build(  # MultiHostUrl是一个Pydantic的数据类，这是一个构造函数或方法，用于创建一个复合URL。这里特别用于数据库连接URI的构建。
            scheme="mariadb+pymysql",
            username=self.MARIADB_USER,
            password=self.MARIADB_PASSWORD,
            host=self.MARIADB_SERVER,
            port=self.MARIADB_PORT,
            path=self.MARIADB_DB,
        )

    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    # TODO: update type to EmailStr when sqlmodel supports it
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None

    @model_validator(
        mode="after"
    )  # model_validator是一个Pydantic的装饰器，用于在模型验证阶段对模型进行验证。在这个案例中，mode="after"表示在模型验证阶段之后执行验证。
    def _set_default_emails_from(self) -> Self:
        if not self.EMAILS_FROM_NAME:
            self.EMAILS_FROM_NAME = self.PROJECT_NAME
        return self

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    @computed_field  # type: ignore[prop-decorator]
    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)

    # TODO: update type to EmailStr when sqlmodel supports it
    FIRST_SUPERUSER: str = "test@example.com"
    # TODO: update type to SecretStr when sqlmodel supports it
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    # 这段代码定义了一个使用装饰器@model_validator的方法_enforce_non_default_secrets，其目的是在模型（如配置类）的验证阶段之后确保某些敏感信息（如密钥或密码）没有保持默认值，从而提高应用的安全性。
    @model_validator(mode="after")
    def _enforce_non_defualt_secrets(self) -> Self:
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_default_secret("MARIADB_PASSWORD", self.MARIADB_PASSWORD)
        self._check_default_secret(
            "FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD
        )

        return self


settings = Settings()  # type: ignore
