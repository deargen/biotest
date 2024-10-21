# flake8: noqa: D100 D101 D102 D105 T201
from dataclasses import dataclass


@dataclass
class BaseConfig:
    @property
    def envvar_prefix(self) -> str:
        return "MLCONFIG_"

    def __post_init__(self):
        self.verify_unknown_env_vars()
        self.update_based_on_env_vars()
        self.confirm_validity()

    def update_based_on_env_vars(self):
        import os
        from dataclasses import fields
        from types import NoneType, UnionType
        from typing import get_args, get_origin

        from rich.console import Console

        # NOTE: without soft wrapping, it will line break depending on the width of the terminal.
        # Which may cause the failure of the doctest.
        console = Console(soft_wrap=True)

        # for key, value in asdict(self).items():
        for class_field in fields(self):
            key = class_field.name
            vartype = class_field.type

            env_var = os.getenv(f"{self.envvar_prefix}{key}")
            if env_var:
                if get_origin(vartype) is UnionType:
                    # If the type is Union, we use the first type
                    # unless the value is None.
                    if NoneType in get_args(vartype) and env_var == "None":
                        setattr(self, key, None)

                        console.print(
                            f"{type(self).__name__}: Updating {key} from env var "
                            f"{self.envvar_prefix}{key}=None as NoneType"
                        )
                    else:
                        self._set_value_as_type(key, env_var, get_args(vartype)[0])
                else:
                    self._set_value_as_type(key, env_var, vartype)

    def _set_value_as_type(self, key, value: str, vartype):
        """Set the string value as the given type."""
        import ast
        from typing import get_origin

        from rich.console import Console

        if get_origin(vartype) is list:
            setattr(self, key, ast.literal_eval(value))
            assert isinstance(
                getattr(self, key), vartype
            ), f"{type(self).__name__}.{key} has to be {vartype} but got {type(getattr(self, key))}"
        elif vartype is bool:
            if value == "True":
                setattr(self, key, True)
            elif value == "False":
                setattr(self, key, False)
            else:
                raise ValueError(
                    f"{type(self).__name__}: Unknown boolean value for {key}={value} trying to update from env var"
                )
        else:
            setattr(self, key, vartype(value))

        console = Console(soft_wrap=True)
        console.print(
            f"{type(self).__name__}: Updating {key} from env var "
            f"{self.envvar_prefix}{key}={value} as type {vartype}"
        )

    def print_fields(self):
        from dataclasses import fields

        from rich.console import Console

        console = Console(soft_wrap=True)

        console.print(f"{type(self).__name__}: Fields:")
        for fld in fields(self):
            console.print(f"{fld.name}: {fld.type} = {fld.default!r}")

    def verify_unknown_env_vars(self):
        import os
        from dataclasses import asdict

        # os.environ.keys() is always uppercase
        for name, value in os.environ.items():
            keys_lower = [k.lower() for k in asdict(self)]
            if (
                name.startswith(self.envvar_prefix)
                and name[len(self.envvar_prefix) :].lower() not in keys_lower
            ):
                print(f"ERROR while updating from env var {name}")
                print("Possible values are:")
                print()
                self.print_fields()
                raise ValueError(f"Unknown environment variable {name}={value}")

    def confirm_validity(self):
        pass


@dataclass
class ExampleConfig(BaseConfig):
    """
    BaseConfig 사용법 예: BaseConfig를 inherit해서 변수, 타입, default값을 적으면 됩니다.

    `envvar_prefix` 함수를 override해서 환경변수 prefix를 정의하고,
    환경변수를 이용해 모든 값을 수정할 수 있습니다.

    Examples:
        >>> cfg = ExampleConfig()
        >>> cfg
        ExampleConfig(train_batch_size=1, alpha=None)

        >>> import os
        >>> os.environ['MLCONFIG_train_batch_size'] = '2'
        >>> ExampleConfig()
        ExampleConfig: Updating train_batch_size from env var MLCONFIG_train_batch_size=2 as type <class 'int'>
        ExampleConfig(train_batch_size=2, alpha=None)

        >>> os.environ['MLCONFIG_alpha'] = '0.5'
        >>> ExampleConfig()
        ExampleConfig: Updating train_batch_size from env var MLCONFIG_train_batch_size=2 as type <class 'int'>
        ExampleConfig: Updating alpha from env var MLCONFIG_alpha=0.5 as type <class 'float'>
        ExampleConfig(train_batch_size=2, alpha=0.5)

        >>> # Setting alpha to None with the string "None"
        >>> os.environ['MLCONFIG_alpha'] = 'None'
        >>> ExampleConfig()
        ExampleConfig: Updating train_batch_size from env var MLCONFIG_train_batch_size=2 as type <class 'int'>
        ExampleConfig: Updating alpha from env var MLCONFIG_alpha=None as NoneType
        ExampleConfig(train_batch_size=2, alpha=None)

        >>> # Undefined name in environment variable. Maybe a typo?
        >>> os.environ['MLCONFIG_unknown'] = '1'
        >>> ExampleConfig()
        Traceback (most recent call last):
         ...
        ValueError: Unknown environment variable MLCONFIG_unknown=1
    """

    train_batch_size: int = 1
    alpha: float | None = None

    @property
    def envvar_prefix(self) -> str:
        return "MLCONFIG_"


def example():
    import rich

    cfg = ExampleConfig()
    rich.print(cfg)


if __name__ == "__main__":
    example()
